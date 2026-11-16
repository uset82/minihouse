#!/usr/bin/env python3
"""MiniHouse · Solver independiente de barras 3D (Euler-Bernoulli, 6 GDL/nudo).

Estado: HERRAMIENTA DE VERIFICACION INDEPENDIENTE (nivel 2 del informe).
No sustituye a Robot ni libera nada. Unidades: N, m, Pa (entrada coherente).

Elemento: barra 3D con EA, EIy, EIz, GJ; sin alabeo (perfiles abiertos quedan
fuera de alcance: usar SCI P385 / solver con 7o GDL para eso), sin rigidez
geometrica, sin releases (extremos rigidos). Suficiente para comparar chasis
de RHS conceptual y para reproducir soluciones cerradas de viga.

Uso como biblioteca:
    m = Modelo()
    m.nudo(id, x, y, z); m.barra(id, n1, n2, A, E, Iy, Iz, G, J, vec_y=(...))
    m.apoyo(nudo, (dx,dy,dz,rx,ry,rz))  # 1 = restringido
    m.carga_nodal(nudo, fx=..., mz=...)
    m.carga_distribuida(barra, q, direccion='global_z'|'local_y'...)  # N/m
    res = m.resolver()  # -> desplazamientos, reacciones, fuerzas de extremo

Selftest: python barras3d.py --selftest
  - viga simply supported: delta = 5qL^4/384EI, M_mid = qL^2/8
  - casos del informe: L=6, q=2452.5, EI=1.68e6 -> 24.634 mm (a=0);
    a=1.2 -> delta 1.490 mm, M_A=-1.766 kNm, M_mid=2.207 kNm
  - voladizo puntual: delta = PL^3/3EI
  - torsion: phi = TL/GJ
  - equilibrio global de reacciones en cada caso
"""
import numpy as np

GDL = 6


def _mat_local(E, A, Iy, Iz, G, J, L):
    k = np.zeros((12, 12))
    ea = E * A / L
    gj = G * J / L
    # axial
    for i, j, s in [(0, 0, 1), (0, 6, -1), (6, 0, -1), (6, 6, 1)]:
        k[i, j] = ea * s
    # torsion
    for i, j, s in [(3, 3, 1), (3, 9, -1), (9, 3, -1), (9, 9, 1)]:
        k[i, j] = gj * s
    # bending about local z (forces in local y) -> Iy? convention:
    # local y displacement uses Iz? We define: flexion en plano x-y usa Iy
    # (convencion declarada: Iy = inercia para flexion que desplaza en y local)
    for (I, dofs) in [(Iy, (1, 5, 7, 11)), (Iz, (2, 4, 8, 10))]:
        a = 12 * E * I / L**3
        b = 6 * E * I / L**2
        c = 4 * E * I / L
        d = 2 * E * I / L
        i1, r1, i2, r2 = dofs
        sub = np.array([
            [ a,  b, -a,  b],
            [ b,  c, -b,  d],
            [-a, -b,  a, -b],
            [ b,  d, -b,  c],
        ])
        # for the z-plane the rotation sign flips (right-hand rule)
        if I is Iz:
            sub = sub * np.array([[1, -1, 1, -1]]) * np.array([[1], [-1], [1], [-1]])
        idx = [i1, r1, i2, r2]
        for ii in range(4):
            for jj in range(4):
                k[idx[ii], idx[jj]] += sub[ii, jj]
    return k


def _rot(n1, n2, vec_y):
    x = np.array(n2) - np.array(n1)
    L = np.linalg.norm(x)
    x = x / L
    yref = np.array(vec_y, dtype=float)
    z = np.cross(x, yref)
    if np.linalg.norm(z) < 1e-9:
        raise ValueError("vec_y paralelo al eje de la barra")
    z /= np.linalg.norm(z)
    y = np.cross(z, x)
    R = np.vstack([x, y, z])  # global -> local
    T = np.zeros((12, 12))
    for b in range(4):
        T[3*b:3*b+3, 3*b:3*b+3] = R
    return T, L


class Modelo:
    def __init__(self):
        self.nudos = {}      # id -> np.array xyz
        self.barras = {}     # id -> dict
        self.apoyos = {}     # nudo -> tuple 6 bool
        self.fnod = {}       # nudo -> np.array 6
        self.qdist = []      # (barra_id, q N/m, modo)

    def nudo(self, nid, x, y, z):
        self.nudos[nid] = np.array([x, y, z], dtype=float)

    def barra(self, bid, n1, n2, A, E, Iy, Iz, G, J, vec_y=(0, 0, 1)):
        self.barras[bid] = dict(n1=n1, n2=n2, A=A, E=E, Iy=Iy, Iz=Iz, G=G, J=J, vec_y=vec_y)

    def apoyo(self, nid, restric):
        self.apoyos[nid] = tuple(bool(v) for v in restric)

    def carga_nodal(self, nid, fx=0, fy=0, fz=0, mx=0, my=0, mz=0):
        v = np.array([fx, fy, fz, mx, my, mz], dtype=float)
        self.fnod[nid] = self.fnod.get(nid, np.zeros(6)) + v

    def carga_distribuida(self, bid, q, modo="global_z"):
        # modos: global_z (grav), local_y, local_z ; q en N/m, signo directo
        self.qdist.append((bid, q, modo))

    def resolver(self):
        ids = list(self.nudos)
        idx = {n: i for i, n in enumerate(ids)}
        nd = len(ids) * GDL
        K = np.zeros((nd, nd))
        elems = {}
        for bid, b in self.barras.items():
            T, L = _rot(self.nudos[b["n1"]], self.nudos[b["n2"]], b["vec_y"])
            kl = _mat_local(b["E"], b["A"], b["Iy"], b["Iz"], b["G"], b["J"], L)
            kg = T.T @ kl @ T
            dofs = [idx[b["n1"]] * 6 + i for i in range(6)] + [idx[b["n2"]] * 6 + i for i in range(6)]
            for a in range(12):
                for c in range(12):
                    K[dofs[a], dofs[c]] += kg[a, c]
            elems[bid] = (T, L, kl, dofs)
        F = np.zeros(nd)
        for n, v in self.fnod.items():
            F[idx[n]*6:idx[n]*6+6] += v
        # cargas distribuidas -> vector equivalente de empotramiento perfecto
        feq_local = {}
        for bid, q, modo in self.qdist:
            T, L, kl, dofs = elems[bid]
            fl = np.zeros(12)
            if modo == "local_y":
                fl[[1, 7]] = q * L / 2
                fl[5] = q * L**2 / 12
                fl[11] = -q * L**2 / 12
            elif modo == "local_z":
                fl[[2, 8]] = q * L / 2
                fl[4] = -q * L**2 / 12
                fl[10] = q * L**2 / 12
            elif modo == "global_z":
                fg = np.zeros(12)
                fg[[2, 8]] = q * L / 2
                # proyeccion: se arma en global abajo
                T3 = T[:3, :3]
                qv = T3 @ np.array([0, 0, q])
                fl = np.zeros(12)
                fl[[1, 7]] = qv[1] * L / 2
                fl[[2, 8]] = qv[2] * L / 2
                fl[5] = qv[1] * L**2 / 12
                fl[11] = -qv[1] * L**2 / 12
                fl[4] = -qv[2] * L**2 / 12
                fl[10] = qv[2] * L**2 / 12
                # componente axial
                fl[[0, 6]] = qv[0] * L / 2
            else:
                raise ValueError(modo)
            feq_local[bid] = feq_local.get(bid, np.zeros(12)) + fl
            fg = T.T @ fl
            for a in range(12):
                F[dofs[a]] += fg[a]
        # condiciones de apoyo
        fijos = []
        for n, r in self.apoyos.items():
            for i in range(6):
                if r[i]:
                    fijos.append(idx[n] * 6 + i)
        libres = [i for i in range(nd) if i not in set(fijos)]
        u = np.zeros(nd)
        Kff = K[np.ix_(libres, libres)]
        u[libres] = np.linalg.solve(Kff, F[libres])
        R = K @ u - F
        # fuerzas de extremo locales (incluye correccion de carga distribuida)
        fuerzas = {}
        for bid, (T, L, kl, dofs) in elems.items():
            ue = u[dofs]
            fl = kl @ (T @ ue) - feq_local.get(bid, np.zeros(12))
            fuerzas[bid] = fl
        return dict(u=u, R=R, idx=idx, fuerzas=fuerzas, elems=elems, fijos=fijos)


# ---------------- selftests ----------------

def _viga(a=0.0, L=6.0, q=2452.5, EI=1.68e6, E=210e9):
    """Viga del informe: apoyos simétricos retranqueados a; un solo elemento
    no basta (apoyos interiores), se discretiza en tramos de 0.3 m."""
    I = EI / E
    m = Modelo()
    xs = np.arange(0, L + 1e-9, 0.3)
    for i, x in enumerate(xs):
        m.nudo(i, x, 0, 0)
    for i in range(len(xs) - 1):
        m.barra(i, i, i + 1, A=0.01, E=E, Iy=I, Iz=I, G=81e9, J=1e-6, vec_y=(0, 1, 0))
        m.carga_distribuida(i, -q, "local_z")
    # apoyos en x=a y x=L-a: pin + roller (restringen z; y tambien para estabilidad)
    ia = int(round(a / 0.3)); ib = int(round((L - a) / 0.3))
    m.apoyo(ia, (1, 1, 1, 0, 0, 0))
    m.apoyo(ib, (0, 1, 1, 0, 0, 0))
    # evitar mecanismo axial/torsional: fijar rx en un apoyo
    m.apoyo(ia, (1, 1, 1, 1, 0, 0))
    return m, xs


def selftest():
    tol = 2e-3  # 0.2% relativo (discretizacion 0.3 m, carga consistente: exacto en nodos)
    # --- caso informe a=0 ---
    m, xs = _viga(a=0.0)
    r = m.resolver()
    imid = len(xs) // 2
    delta = -r["u"][r["idx"][imid] * 6 + 2]
    esperado = 5 * 2452.5 * 6**4 / (384 * 1.68e6)  # 0.024634 m
    assert abs(delta - esperado) / esperado < tol, (delta, esperado)
    # momento en el centro desde fuerzas de extremo del elemento adyacente
    fe = r["fuerzas"][imid]  # elemento que empieza en el centro
    Mmid = fe[4]  # momento local y en nudo i (signo: ver abajo)
    assert abs(abs(Mmid) - 11036.25) / 11036.25 < 0.01, Mmid
    # equilibrio vertical
    Rz = sum(r["R"][i * 6 + 2] for i in r["idx"].values())
    assert abs(Rz - 2452.5 * 6) < 1e-6, Rz
    print(f"OK viga a=0: delta={delta*1000:.3f} mm (esperado {esperado*1000:.3f}), |M_mid|={abs(Mmid):.1f} Nm")
    # --- caso informe a=1.2 ---
    m, xs = _viga(a=1.2)
    r = m.resolver()
    delta = -r["u"][r["idx"][imid] * 6 + 2]
    q, L, EI, a = 2452.5, 6.0, 1.68e6, 1.2
    esperado = (q / EI) * (5 * (L - 2*a)**4 / 384 - a**2 * (L - 2*a)**2 / 16)
    assert abs(delta - esperado) / esperado < 0.01, (delta, esperado)
    ia = int(round(a / 0.3))
    MA = r["fuerzas"][ia][4]
    assert abs(abs(MA) - 1765.8) / 1765.8 < 0.01, MA
    Mmid2 = r["fuerzas"][imid][4]
    assert abs(abs(Mmid2) - 2207.25) / 2207.25 < 0.02, Mmid2
    Rz = sum(r["R"][i * 6 + 2] for i in r["idx"].values())
    assert abs(Rz - q * L) < 1e-6
    print(f"OK viga a=1.2: delta={delta*1000:.3f} mm (esperado {esperado*1000:.3f}), |M_A|={abs(MA):.1f}, |M_mid|={abs(Mmid2):.1f} Nm")
    # --- voladizo puntual ---
    m = Modelo()
    P, L, E, I = 1000.0, 2.0, 210e9, 8e-6
    m.nudo(0, 0, 0, 0); m.nudo(1, L, 0, 0)
    m.barra(0, 0, 1, A=0.01, E=E, Iy=I, Iz=I, G=81e9, J=1e-5, vec_y=(0, 1, 0))
    m.apoyo(0, (1, 1, 1, 1, 1, 1))
    m.carga_nodal(1, fz=-P)
    r = m.resolver()
    d = -r["u"][r["idx"][1] * 6 + 2]
    esp = P * L**3 / (3 * E * I)
    assert abs(d - esp) / esp < 1e-9
    print(f"OK voladizo: delta={d*1000:.4f} mm (exacto {esp*1000:.4f})")
    # --- torsion ---
    m = Modelo()
    T0, L, G, J = 500.0, 3.0, 81e9, 2e-6
    m.nudo(0, 0, 0, 0); m.nudo(1, L, 0, 0)
    m.barra(0, 0, 1, A=0.01, E=210e9, Iy=8e-6, Iz=8e-6, G=G, J=J, vec_y=(0, 1, 0))
    m.apoyo(0, (1, 1, 1, 1, 1, 1))
    m.carga_nodal(1, mx=T0)
    r = m.resolver()
    phi = r["u"][r["idx"][1] * 6 + 3]
    esp = T0 * L / (G * J)
    assert abs(phi - esp) / esp < 1e-9
    print(f"OK torsion: phi={phi:.6f} rad (exacto {esp:.6f})")
    print("SELFTEST barras3d OK: informe reproducido + 2 casos exactos + equilibrio.")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    selftest()