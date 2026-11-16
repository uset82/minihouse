#!/usr/bin/env python3
"""Auditoria EXACTA del perfil completo de computeBeamDeflectionMm (TS).
Referencia: doble integracion analitica de EI v''=M con v(a)=0, v'(L/2)=0,
continuidad en el apoyo. Convencion referencia: v positiva hacia ARRIBA;
TS devuelve sag positivo hacia ABAJO -> TS = -v_ref.
"""

def ts_deflection(x_m, a):
    L, q, EI = 6.0, 2452.5, 1.68e6
    a = max(0.0, min(1.8, a))
    l = L - 2 * a
    x = x_m if x_m <= L / 2 else L - x_m
    if x >= a:
        u = x - a
        t1 = (u * (l**3 - 2 * l * u**2 + u**3)) / 24
        t2 = (a**2 * u * (l - u)) / 4
        return (q / EI) * (t1 - t2) * 1000
    z = a - x
    slope = (q / EI) * (l**3 / 24 - (a**2 * l) / 4)
    cant = (q / EI) * ((a**2 * z**2) / 4 - (a * z**3) / 6 + z**4 / 24)
    return (-slope * z + cant) * 1000


def exact_v_up(x_m, a):
    """Solucion analitica exacta, v positiva hacia arriba (m)."""
    L, q, EI = 6.0, 2452.5, 1.68e6
    R = q * L / 2
    l = L - 2 * a
    x = x_m if x_m <= L / 2 else L - x_m
    # EI v' = R(x-a)^2/2 - q x^3/6 + D1 (tramo central); D1 por v'(L/2)=0
    D1 = q * L**3 / 48 - R * (l / 2) ** 2 / 2
    C1 = D1  # continuidad de pendiente en x=a
    C2 = q * a**4 / 24 - C1 * a  # v(a)=0
    D2 = C2
    if x >= a:
        return (R * (x - a) ** 3 / 6 - q * x**4 / 24 + D1 * x + D2) / EI
    return (-q * x**4 / 24 + C1 * x + C2) / EI


ok = True
for a in (0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8):
    maxerr = 0.0
    for i in range(601):
        x = i * 6.0 / 600
        ts = ts_deflection(x, a)
        ref = -exact_v_up(x, a) * 1000
        maxerr = max(maxerr, abs(ts - ref))
    good = maxerr < 1e-6
    ok &= good
    print(f"a={a}: error maximo en 601 puntos = {maxerr:.2e} mm  {'OK' if good else 'DIVERGE'}")

print("\nRESULTADO:", "FORMULA TS EXACTA EN TODO EL PERFIL" if ok else "HAY DIVERGENCIA REAL")
print("Nota: el 'DIVERGE' del audit anterior era error del integrador Euler propio (h=25mm), no de la formula TS.")