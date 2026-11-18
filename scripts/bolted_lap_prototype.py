#!/usr/bin/env python3
"""MiniHouse · a printable test article for the woven, bolted base-frame joint.

CONCEPTUAL — NOT FOR FABRICATION.

The sketches show four numbered members interlaced "like hands over one another",
with bolts at the laps and sandwich walls in the middle. A folded paper model
makes the over/under sequence look easy. Four RIGID bars cannot do it: the
precedence graph is a cycle (4 -> 1 -> 2 -> 3 -> 4), so there is no order in
which all four can simply be lowered into place. One strip must bend and thread.

This script builds a small PETG test article for that single question, plus bolt
access. It emits:

  * four STL bodies (one per numbered ply), each a set of watertight shells;
  * one multi-object 3MF with the four print bodies;
  * one faceted STEP assembly with the four plies and reference M6 bolts;
  * a readable Markdown assembly/measurement sheet and a JSON record.

It is a stdlib-only generator. No CAD library or Fusion connector is assumed.
The print proves assembly sequence, hole alignment, wrench clearance and
disassembly. It proves NOTHING about steel or bolt capacity, preload, corrosion,
thermal bridging or Norwegian code compliance. EN 1993-1-8 and NS-EN 1090-2
checks remain pending; only the responsible engineer may release anything.

Usage:
  python bolted_lap_prototype.py --selftest
  python bolted_lap_prototype.py --out-dir fase1/prototipo \
      --out-md fase1/prototipo-union-atornillada-R0.md \
      --out-json knowledge/comparisons/bolted-lap-prototype.json
"""
import argparse
import datetime
import json
import math
import struct
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict, deque
from pathlib import Path

# --- dimensions, all in mm ---------------------------------------------------
BED = (180.0, 180.0, 180.0)      # Bambu A1 mini, verified bed volume
BAR_W = 50.0                     # 1:2 of a nominal 100 mm flat bar
BAR_L = 150.0                    # joint region only, not the 6 m frame
BAR_T = 2.0                      # thin enough to thread; see docstring
SCALE_LAYOUT = 0.5
CROSS_X = (30.0, 120.0)          # two crossings per ply
CROSS_Y = (30.0, 120.0)
SPLIT_U = 75.0
JOG = 2.0                        # one thickness of dogleg
JOG_HALF = 1.0                   # half-width of the vertical riser web
BOLT_D = 6.0
HOLE_D = 6.4                     # M6 clearance (RepRap FFF guide)
NUT_AF = 10.0
POCKET_AF = 10.2                 # 0.2 mm mating clearance
POCKET_DEPTH = 5.5
BOSS_D = 20.0
BOSS_H = 5.5
WRENCH_D = 24.0
WRENCH_H = 18.0
TAB_T = 3.0
SEGMENTS = 24                    # hole-circle discretisation

# The over/under. First value is the level at u=30, second at u=120.
# 0 = lower, JOG = upper. A ply at JOG passes over the one at 0.
LEVELS = {
    1: (0.0, JOG),   # under 2 at (30,30), over 4 at (120,30)
    2: (JOG, 0.0),   # over 1, under 3
    3: (JOG, 0.0),   # over 2, under 4
    4: (0.0, JOG),   # under 1, over 3  <-- the flexible, threaded strip
}
THREAD_PLY = 4
CROSSINGS = ((30.0, 30.0, 1, 2), (120.0, 30.0, 4, 1),
             (30.0, 120.0, 2, 3), (120.0, 120.0, 3, 4))
PANEL_GAP = (CROSS_X[1] - CROSS_X[0]) - BAR_W        # 40 mm between inner edges
SLOT = PANEL_GAP - 2.0 * TAB_T                       # 34 mm locating gap

STATUS = "CONCEPTUAL — NOT FOR FABRICATION"
SCOPE = "assembly sequence and tool access only"
NO_CLAIM = "no strength claim"
NEEDLES = (STATUS, SCOPE, NO_CLAIM, "EN 1993-1-8", "NS-EN 1090-2", "thermal bridge")


# --- tiny vector helpers ----------------------------------------------------
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross3(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def norm(v):
    return math.sqrt(sum(c * c for c in v))


def unit(v):
    n = norm(v)
    if n == 0:
        return (1.0, 0.0, 0.0)
    return tuple(c / n for c in v)


def cross2(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def signed_area(poly):
    return 0.5 * sum(poly[i][0] * poly[(i + 1) % len(poly)][1]
                     - poly[(i + 1) % len(poly)][0] * poly[i][1]
                     for i in range(len(poly)))


def point_in_tri(p, a, b, c, eps=1e-9):
    d = (cross2(a, b, p), cross2(b, c, p), cross2(c, a, p))
    return (all(x >= -eps for x in d) or all(x <= eps for x in d))


# --- 2D triangulation -------------------------------------------------------
def ear_clip(poly):
    """Triangulate a simple polygon. Returns CCW triangles."""
    pts = list(poly)
    if len(pts) < 3:
        raise ValueError("polygon needs at least three vertices")
    if signed_area(pts) < 0:
        pts.reverse()
    tris = []
    guard = 0
    while len(pts) > 3:
        guard += 1
        if guard > len(poly) ** 2 + 10:
            raise RuntimeError("ear clipping did not converge")
        n = len(pts)
        clipped = False
        for i in range(n):
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
            if cross2(a, b, c) <= 1e-9:
                continue
            skip = {(i - 1) % n, i, (i + 1) % n}
            if any(point_in_tri(p, a, b, c) for j, p in enumerate(pts) if j not in skip):
                continue
            tris.append((a, b, c))
            del pts[i]
            clipped = True
            break
        if not clipped:
            raise RuntimeError("no ear found — polygon may self-intersect")
    tris.append(tuple(pts))
    return tris


def polygon_with_hole(outer, hole):
    """Outer CCW, hole CW. Bridged into one simple polygon for ear clipping."""
    outer = list(outer)
    hole = list(hole)
    if signed_area(outer) < 0:
        outer.reverse()
    if signed_area(hole) > 0:
        hole.reverse()
    o0, o1 = outer[0], outer[1]
    # The bridge position changes the ear-clipping path. A single fixed bridge
    # can dead-end near the hole, so try every split of the ring.
    last = None
    for k in range(len(hole)):
        h = hole[k:] + hole[:k]
        poly = [o0] + h + [o1] + outer[2:]
        bridges = {frozenset((o0, h[0])), frozenset((h[-1], o1))}
        try:
            return ear_clip(poly), bridges
        except RuntimeError as exc:
            last = exc
    raise RuntimeError(f"no bridge produced a triangulation: {last}")


def circle(cx, cy, r, ccw=True):
    step = 2.0 * math.pi / SEGMENTS
    return [(cx + r * math.cos(i * step if ccw else -i * step),
             cy + r * math.sin(i * step if ccw else -i * step))
            for i in range(SEGMENTS)]


# --- watertight shell -------------------------------------------------------
class Shell:
    """One closed triangulated body. Vertices are shared by rounded coordinate."""

    def __init__(self, name):
        self.name = name
        self.verts = []
        self.lookup = {}
        self.tris = []

    def v(self, p):
        key = tuple(round(float(c), 6) for c in p)
        if key not in self.lookup:
            self.lookup[key] = len(self.verts)
            self.verts.append((float(p[0]), float(p[1]), float(p[2])))
        return self.lookup[key]

    def tri(self, p, q, r):
        a, b, c = self.v(p), self.v(q), self.v(r)
        if len({a, b, c}) < 3:
            return
        pa, pb, pc = self.verts[a], self.verts[b], self.verts[c]
        if norm(cross3(sub(pb, pa), sub(pc, pa))) < 1e-9:
            return
        self.tris.append((a, b, c))

    def quad(self, p, q, r, s):
        self.tri(p, q, r)
        self.tri(p, r, s)

    def bbox(self):
        if not self.verts:
            return None
        return tuple((min(v[i] for v in self.verts), max(v[i] for v in self.verts))
                     for i in range(3))

    def watertight(self):
        counts = Counter()
        for a, b, c in self.tris:
            for e in ((a, b), (b, c), (c, a)):
                counts[frozenset(e)] += 1
        return all(n == 2 for n in counts.values())


def ray_rectangle(cx, cy, angle, x0, y0, x1, y1):
    """Intersection of a ray from an interior point with an axis-aligned rectangle."""
    dx, dy = math.cos(angle), math.sin(angle)
    candidates = []
    if abs(dx) > 1e-12:
        candidates.append(((x1 - cx) / dx if dx > 0 else (x0 - cx) / dx))
    if abs(dy) > 1e-12:
        candidates.append(((y1 - cy) / dy if dy > 0 else (y0 - cy) / dy))
    t = min(v for v in candidates if v > 1e-9)
    return (cx + t * dx, cy + t * dy)


def radial_annulus(inner, outer):
    """Triangulate the material between two concentric, equally sampled rings."""
    n = len(inner)
    if len(outer) != n:
        raise ValueError("rings must have the same number of samples")
    tris = []
    for i in range(n):
        j = (i + 1) % n
        tris.append((inner[i], inner[j], outer[j]))
        tris.append((inner[i], outer[j], outer[i]))
    return tris


def extrude_tris(name, tris, z0, z1):
    sh = Shell(name)
    for a, b, c in tris:
        sh.tri((a[0], a[1], z1), (b[0], b[1], z1), (c[0], c[1], z1))
        sh.tri((a[0], a[1], z0), (c[0], c[1], z0), (b[0], b[1], z0))
    ori = defaultdict(int)
    und = Counter()
    for a, b, c in tris:
        for e in ((a, b), (b, c), (c, a)):
            ori[e] += 1
            und[frozenset(e)] += 1
    for (a, b), n in ori.items():
        if n != 1 or und[frozenset((a, b))] != 1:
            continue
        sh.quad((a[0], a[1], z0), (b[0], b[1], z0),
                (b[0], b[1], z1), (a[0], a[1], z1))
    return sh


def extrude_region(name, outer, hole, z0, z1, outer_ring=None):
    """Extrude a rectangle with a circular hole, or any explicit annulus.

    A bridged ear-clip polygon cuts a wedge out of the lap, so holes are built as
    radial annuli: each hole vertex is projected onto the outer boundary and the
    material between the two rings is triangulated directly.
    """
    if hole is None:
        tris = ear_clip(outer)
        return extrude_tris(name, tris, z0, z1)
    ring = list(hole)
    if signed_area(ring) < 0:
        ring.reverse()
    if outer_ring is None:
        xs, ys = [p[0] for p in outer], [p[1] for p in outer]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        cx = sum(p[0] for p in ring) / len(ring)
        cy = sum(p[1] for p in ring) / len(ring)
        r = math.hypot(ring[0][0] - cx, ring[0][1] - cy)
        # A long rectangle seen from an off-centre hole has a very narrow angular
        # window on its far end. Sampling the circle alone misses that window and
        # cuts the end off, so add the four corner rays explicitly.
        angles = [math.atan2(p[1] - cy, p[0] - cx) % (2.0 * math.pi) for p in ring]
        angles += [math.atan2(y - cy, x - cx) % (2.0 * math.pi)
                   for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
        angles = sorted(set(round(a, 10) for a in angles))
        ring = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in angles]
        outer_ring = [ray_rectangle(cx, cy, a, x0, y0, x1, y1) for a in angles]
    return extrude_tris(name, radial_annulus(ring, outer_ring), z0, z1)


# --- the four plies ---------------------------------------------------------
def ply_map(ply):
    """Local (u along bar, v across bar) -> global (x,y), orientation preserving."""
    if ply in (1, 3):
        center = CROSS_Y[0] if ply == 1 else CROSS_Y[1]
        return lambda u, v: (u, center + v)
    center = CROSS_X[0] if ply == 2 else CROSS_X[1]
    return lambda u, v: (center - v, u)


def build_ply(ply):
    mp = ply_map(ply)
    v0, v1 = -BAR_W / 2.0, BAR_W / 2.0
    lo, hi = LEVELS[ply]
    shells = []

    for idx, (u0, u1, lvl) in enumerate(((0.0, SPLIT_U, lo), (SPLIT_U, BAR_L, hi)), 1):
        outer = [mp(u0, v0), mp(u1, v0), mp(u1, v1), mp(u0, v1)]
        u_hole = CROSS_X[0] if idx == 1 else CROSS_X[1]
        hole = [mp(u_hole + r * math.cos(a), r * math.sin(a))
                for (r, a) in []]  # placeholder, rebuilt below
        ring = circle(u_hole, 0.0, HOLE_D / 2.0, ccw=True)
        hole = [mp(u, v) for u, v in ring]
        shells.append(extrude_region(f"ply{ply}_half{idx}", outer, hole, lvl, lvl + BAR_T))

    # Vertical web joining the two levels; overlaps both halves on purpose.
    web_outer = [mp(SPLIT_U - JOG_HALF, v0), mp(SPLIT_U + JOG_HALF, v0),
                 mp(SPLIT_U + JOG_HALF, v1), mp(SPLIT_U - JOG_HALF, v1)]
    shells.append(extrude_region(f"ply{ply}_dogleg", web_outer, None,
                                 min(lo, hi), max(lo, hi) + BAR_T))

    for n, u in enumerate(CROSS_X, 1):
        z0 = (lo if n == 1 else hi) + BAR_T
        cx, cy = mp(u, 0.0)
        outer = [mp(u + px, py) for px, py in circle(0.0, 0.0, BOSS_D / 2.0)]
        inner = [mp(u + px, py) for px, py in circle(0.0, 0.0, POCKET_AF / 2.0, ccw=True)]
        shells.append(extrude_region(f"ply{ply}_boss{n}", outer, inner, z0, z0 + BOSS_H,
                                     outer_ring=outer))
    return shells


def reference_bolts():
    """Four reference M6 assemblies for STEP only — never printed."""
    shells = []
    for x, y, _a, _b in CROSSINGS:
        z_bot, z_top = -6.0, 9.0
        shells.append(extrude_region(
            f"bolt_{x:.0f}_{y:.0f}_shaft",
            circle(x, y, BOLT_D / 2.0), None, z_bot, z_top))
        shells.append(extrude_region(
            f"bolt_{x:.0f}_{y:.0f}_head",
            circle(x, y, 5.0), None, z_top, z_top + 4.0))
        shells.append(extrude_region(
            f"bolt_{x:.0f}_{y:.0f}_nut",
            circle(x, y, NUT_AF / 2.0), None, -10.0, z_bot))
    return shells


# --- assembly graph ---------------------------------------------------------
def precedence():
    """Edge a->b means a must be lower than b, i.e. a placed before b."""
    return {lower: upper for _x, _y, lower, upper in CROSSINGS}


def vertical_order():
    """Kahn's algorithm. Returns None when the weave is a closed cycle."""
    edges = precedence()
    indeg = {i: 0 for i in range(1, 5)}
    succ = defaultdict(list)
    for a, b in edges.items():
        succ[a].append(b)
        indeg[b] += 1
    q = deque(i for i, d in indeg.items() if d == 0)
    out = []
    while q:
        n = q.popleft()
        out.append(n)
        for m in succ[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    return out if len(out) == 4 else None


def cycle_nodes():
    edges = precedence()
    seen = []
    cur = 1
    for _ in range(4):
        seen.append(cur)
        cur = edges.get(cur, cur)
    return seen + [cur] if cur == seen[0] else seen


# --- numeric proofs ---------------------------------------------------------
def clearance():
    """Wrench keep-out vs the two plies not in each lap, plus hole ligaments."""
    axes = []
    for x, y, a, b in CROSSINGS:
        others = [p for p in (1, 2, 3, 4) if p not in (a, b)]
        dmin = float("inf")
        for p in others:
            mp = ply_map(p)
            v0, v1 = -BAR_W / 2.0, BAR_W / 2.0
            c0, c1 = mp(0.0, v0), mp(BAR_L, v1)
            rx0, rx1 = sorted((c0[0], c1[0]))
            ry0, ry1 = sorted((c0[1], c1[1]))
            dx = max(rx0 - x, 0.0, x - rx1)
            dy = max(ry0 - y, 0.0, y - ry1)
            dmin = min(dmin, math.hypot(dx, dy))
        axes.append({"crossing": [x, y], "lap": [a, b],
                     "nearest_other_ply_mm": round(dmin, 2),
                     "spare_mm": round(dmin - WRENCH_D / 2.0, 2)})
    return {
        "hole_clearance_mm": round(HOLE_D - BOLT_D, 3),
        "nut_seat_clearance_mm": round(POCKET_AF - NUT_AF, 3),
        "ligament_mm": round((BAR_W - HOLE_D) / 2.0, 2),
        "edge_margin_mm": round(CROSS_X[0] - BAR_W / 2.0, 2),
        "slot_mm": round(SLOT, 2),
        "wrench": axes,
        "min_wrench_spare_mm": min(a["spare_mm"] for a in axes),
    }


def bounds(shells):
    bs = [s.bbox() for s in shells if s.bbox()]
    return [(min(b[i][0] for b in bs), max(b[i][1] for b in bs)) for i in range(3)]


def geometry():
    plies = {i: build_ply(i) for i in range(1, 5)}
    printed = [s for i in range(1, 5) for s in plies[i]]
    box = bounds(printed)
    return {
        "plies": plies,
        "printed": printed,
        "bolts": reference_bolts(),
        "box": box,
        "size": tuple(round(b[1] - b[0], 3) for b in box),
        "margins": tuple(round(BED[i] - (box[i][1] - box[i][0]), 3) for i in range(3)),
    }


# --- writers ----------------------------------------------------------------
def write_stl(path, shells):
    tris = [t for s in shells for t in s.tris]
    data = bytearray(b"MiniHouse woven lap prototype - conceptual not for fabrication".ljust(80, b" ")[:80])
    data += struct.pack("<I", len(tris))
    for shell in shells:
        for a, b, c in shell.tris:
            pa, pb, pc = shell.verts[a], shell.verts[b], shell.verts[c]
            n = unit(cross3(sub(pb, pa), sub(pc, pa)))
            data += struct.pack("<12fH", *n, *pa, *pb, *pc, 0)
    Path(path).write_bytes(bytes(data))
    return len(tris)


def write_3mf(path, plies):
    """Multi-object 3MF with embedded meshes; object ids come from the mapping keys."""
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")

    ids = sorted(plies)
    objects = []
    for i in ids:
        shells = plies[i]
        vs, ts = [], []
        for sh in shells:
            off = len(vs)
            vs.extend(sh.verts)
            ts.extend((a + off, b + off, c + off) for a, b, c in sh.tris)
        vxml = "".join(f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>'
                       for x, y, z in vs)
        txml = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in ts)
        objects.append(f'<object id="{i}" type="model" name="ply {i}">'
                       f'<mesh><vertices>{vxml}</vertices><triangles>{txml}</triangles>'
                       f'</mesh></object>')
    model = ('<?xml version="1.0" encoding="UTF-8"?>'
             '<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             '<resources>' + "".join(objects) + '</resources><build>'
             + "".join(f'<item objectid="{i}"/>' for i in ids)
             + '</build></model>')
    ct = ('<?xml version="1.0" encoding="UTF-8"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Override PartName="/3D/3dmodel.model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
          '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" '
            'Target="/3D/3dmodel.model"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("3D/3dmodel.model", model)
    return len(objects)


class StepWriter:
    """Minimal faceted STEP assembly writer — enough for import, not a CAD kernel."""

    def __init__(self):
        self.n = 0
        self.lines = []
        self.points = {}
        self.vertices = {}
        self.directions = {}
        self.edges = {}

    def add(self, text):
        self.n += 1
        self.lines.append(f"#{self.n} = {text};")
        return self.n

    def point(self, p):
        key = tuple(round(float(c), 6) for c in p)
        if key not in self.points:
            self.points[key] = self.add(
                "CARTESIAN_POINT('',({:.6f},{:.6f},{:.6f}))".format(*key))
        return self.points[key]

    def vertex(self, p):
        pid = self.point(p)
        key = pid
        if key not in self.vertices:
            self.vertices[key] = self.add(f"VERTEX_POINT('',#{pid})")
        return self.vertices[key]

    def direction(self, d):
        key = tuple(round(float(c), 6) for c in unit(d))
        if key not in self.directions:
            self.directions[key] = self.add(
                "DIRECTION('',({:.6f},{:.6f},{:.6f}))".format(*key))
        return self.directions[key]

    def edge(self, p, q):
        key = (tuple(round(float(c), 6) for c in p), tuple(round(float(c), 6) for c in q))
        if key not in self.edges:
            v1, v2 = self.vertex(p), self.vertex(q)
            line = self.add(f"LINE('',#{self.point(p)},#{self.direction(sub(q, p))})")
            self.edges[key] = self.add(f"EDGE_CURVE('',#{v1},#{v2},#{line},.T.)")
        return self.edges[key]

    def shell(self, sh):
        faces = []
        for a, b, c in sh.tris:
            pa, pb, pc = sh.verts[a], sh.verts[b], sh.verts[c]
            nv = unit(cross3(sub(pb, pa), sub(pc, pa)))
            xv = unit(sub(pb, pa))
            placement = self.add("AXIS2_PLACEMENT_3D('',#{},{},{})".format(
                self.point(pa), "#" + str(self.direction(nv)), "#" + str(self.direction(xv))))
            plane = self.add("PLANE('',#{})".format(placement))
            loop = []
            for p, q in ((pa, pb), (pb, pc), (pc, pa)):
                e = self.edge(p, q)
                loop.append(self.add(f"ORIENTED_EDGE('',*,*,#{e},.T.)"))
            bound = self.add("FACE_BOUND('',#{},.T.)".format(
                self.add("EDGE_LOOP('',({}))".format(",".join(f"#{x}" for x in loop)))))
            faces.append(self.add(f"ADVANCED_FACE('',#{bound},#{plane},.T.)"))
        return self.add("CLOSED_SHELL('',({}))".format(",".join(f"#{f}" for f in faces)))

    def solid(self, sh):
        s = self.shell(sh)
        return self.add(f"MANIFOLD_SOLID_BREP('{sh.name}',#{s})")

    def write(self, path, shells):
        stamp = datetime.datetime.now().replace(microsecond=0).isoformat()
        head = [
            "ISO-10303-21;", "HEADER;",
            "FILE_DESCRIPTION(('MiniHouse conceptual woven lap prototype'),'2;1');",
            f"FILE_NAME('bolted_lap_prototype.step','{stamp}',('Inge'),('MiniHouse'),"
            "'stdlib faceted export','conceptual - not for fabrication','');",
            "FILE_SCHEMA(('AUTOMOTIVE_DESIGN_CC2'));", "ENDSEC;", "DATA;"
        ]
        solids = [self.solid(sh) for sh in shells]
        tail = ["ENDSEC;", "END-ISO-10303-21;"]
        Path(path).write_text("\n".join(head + self.lines + tail) + "\n", encoding="utf-8")
        return len(solids)


# --- reports ----------------------------------------------------------------
def make_record():
    g = geometry()
    cl = clearance()
    order = vertical_order()
    return {
        "status": STATUS,
        "scope": SCOPE,
        "printer": {"model": "Bambu A1 mini", "bed_mm": list(BED)},
        "size_mm": list(g["size"]),
        "bed_margins_mm": list(g["margins"]),
        "layout_scale": SCALE_LAYOUT,
        "bar": {"width_mm": BAR_W, "length_mm": BAR_L, "thickness_mm": BAR_T},
        "bolt": {"diameter_mm": BOLT_D, "clearance_hole_mm": HOLE_D,
                 "nut_af_mm": NUT_AF, "seat_af_mm": POCKET_AF},
        "slot_mm": SLOT,
        "weave": {"cycle": cycle_nodes(), "vertical_order": order,
                  "threaded_ply": THREAD_PLY,
                  "assembly": [1, 2, 3, f"{THREAD_PLY} (flex, thread last)"]},
        "clearances": cl,
        "shell_counts": {"printed": len(g["printed"]), "reference_bolts": len(g["bolts"])},
        "needs": NEEDLES,
    }


def table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return out


def markdown(rec):
    g = geometry()
    c = rec["clearances"]
    L = [
        "# Woven bolted base joint — printable test article, R0",
        "",
        f"**{STATUS}. {SCOPE}. {NO_CLAIM}.**",
        "",
        "## 1. What the sketches show, and what they do not",
        "",
        "The hand sketch numbers four members 1–4 and alternates them over and under at "
        "the corners, with bolts at the laps; the folded-paper model demonstrates the "
        "thread. No dimension on either image is reliable, so none is used as project data. "
        "The project still has no defined steel section: `fase2/miembros-R0.csv` is `PROV` "
        "and `fase2/miembros-R1-opciones.md` is `PROFILE_NOT_SELECTED`. This article is a "
        "joint-region mock-up, not a frame, not a section choice and not a release.",
        "",
        "## 2. The thing that changes the design",
        "",
        "A closed four-bar weave has **no rigid assembly order**. Each bar is under one "
        "neighbour and over the next, so the precedence graph is the cycle "
        + " → ".join(str(x) for x in rec["weave"]["cycle"]) + ". "
        f"A topological sort returns `{rec['weave']['vertical_order']}`, not an order. "
        f"Paper works because paper bends; PETG at {BAR_T:.1f} mm can too. Ply "
        f"**{THREAD_PLY}** is the marked flexible strip and is threaded last. The print "
        "tests exactly whether that move is possible and whether the bolts then lock it.",
        "",
        "## 3. Geometry (mixed scale, declared)",
        "",
        "The layout is 1:2 of a nominal 100 mm flat bar. The thickness is deliberately "
        "thinner so the strip can thread, and the fasteners are full size because printed "
        "threads below M6 are unreliable.",
        "",
    ]
    L += table(["Item", "Value", "Basis"], [
        ["Print envelope", "180 × 180 × 180 mm", "Bambu A1 mini (verified)"],
        ["Article size", " × ".join(f"{x:.1f}" for x in rec["size_mm"]) + " mm",
         "computed bounding box of printed shells"],
        ["Bar", f"{BAR_W:.0f} × {BAR_L:.0f} × {BAR_T:.1f} mm", "1:2 layout, flexural thickness"],
        ["Bolt / hole", f"M{BOLT_D:.0f} / Ø{HOLE_D:.1f} mm", f"clearance {c['hole_clearance_mm']:.1f} mm"],
        ["Nut seat", f"Ø{POCKET_AF:.1f} mm (hex approximated circular)", f"{c['nut_seat_clearance_mm']:.1f} mm clearance"],
        ["Wrench keep-out", f"Ø{WRENCH_D:.0f} × {WRENCH_H:.0f} mm", "tool access, not a printed part"],
        ["Panel slot", f"{SLOT:.0f} mm", "locating gap only — not a scaled sandwich wall"],
    ])
    L += [
        "",
        "## 4. Assembly sequence",
        "",
        "1. Lay ply 1 flat. 2. Place ply 2 over it at (30,30). 3. Place ply 3 over ply 2 "
        "at (30,120). 4. Bow and thread ply 4 from the open side: **under** ply 1 at "
        "(120,30), **over** ply 3 at (120,120). 5. Insert four M6 bolts from above, "
        "washers and free nuts below; tighten centre-outward as a handling convention "
        "only. Disassembly is the exact reverse.",
        "",
        "Captive nuts are not modelled; the test deliberately uses two-sided nut access, "
        "because wrench clearance is one of the things being measured.",
        "",
        "## 5. Numeric proofs and what to measure",
        "",
    ]
    L += table(["Crossing", "Lap", "Nearest other ply", "Spare over Ø24 wrench"], [
        [f"({a['crossing'][0]:.0f}, {a['crossing'][1]:.0f})",
         f"{a['lap'][0]}/{a['lap'][1]}", f"{a['nearest_other_ply_mm']:.1f} mm",
         f"{a['spare_mm']:.1f} mm"] for a in c["wrench"]
    ])
    L += [
        "",
        f"Hole edge margin {c['edge_margin_mm']:.1f} mm; ligament "
        f"{c['ligament_mm']:.1f} mm; minimum wrench spare "
        f"{c['min_wrench_spare_mm']:.1f} mm; bed margins "
        + ", ".join(f"{m:.0f}" for m in rec["bed_margins_mm"]) + " mm.",
        "",
        "Measure on the printed part: actual hole diameter at each lap; inter-ply gap; "
        "assembled stack height; minimum wrench swing; number of assembly steps; three "
        "assembly/disassembly cycles without member fracture.",
        "",
        "## 6. Files",
        "",
        "- `scripts/bolted_lap_prototype.py` — generator and self-test.",
        "- `fase1/prototipo/ply1.stl` … `ply4.stl` — four print bodies; PETG, 0.4 mm nozzle.",
        "- `fase1/prototipo/joint_3mf.3mf` — multi-object print file.",
        "- `fase1/prototipo/joint.step` — faceted STEP with four plies and reference bolts. "
        "Fusion import has **not** been verified here; do not call it a validated CAD part.",
        "- `knowledge/comparisons/bolted-lap-prototype.json` — the same numbers, machine readable.",
        "",
        "## 7. Boundaries",
        "",
        "This print validates assembly sequence and tool access only. It says nothing "
        "about steel or bolt capacity, preload, galvanic corrosion, thermal bridge, "
        "condensation in a Norwegian climate or regulatory compliance. No steel grade, "
        "bolt class, weld, plate thickness or EXC is selected. S355 remains rejected web "
        "copy. The EN 1993-1-8 joints row is **PENDING** and NS-EN 1090-2 is paywalled. "
        "Changing the base to a woven flat bar re-opens the insulated-junction detail "
        "(previously Ψ +0.027 with wrapped steel); it does not solve it. Only the "
        "responsible engineer may mark anything \"Approved for Fabrication\" (rules.md §5).",
        "",
        "Sources: Bambu Lab Wiki build volumes (18 May 2026); RepRap FFF Design Guide; "
        "Steel Construction Info on preloaded bolting; All3DP PETG vs PLA (19 Dec 2024).",
        "",
    ]
    return "\n".join(L)


# --- self test --------------------------------------------------------------
def selftest():
    rec = make_record()
    g = geometry()
    assert rec["weave"]["vertical_order"] is None
    assert rec["weave"]["cycle"] == [1, 2, 3, 4, 1]
    assert rec["weave"]["threaded_ply"] == THREAD_PLY
    assert rec["clearances"]["hole_clearance_mm"] == 0.4
    assert rec["clearances"]["nut_seat_clearance_mm"] >= 0.2
    assert rec["clearances"]["ligament_mm"] >= 1.5 * HOLE_D
    assert rec["clearances"]["min_wrench_spare_mm"] > 0
    assert SLOT == 34.0
    assert max(g["size"]) <= 180.0 and min(g["margins"]) >= 10.0
    assert all(s.watertight() for s in g["printed"])
    assert all(s.watertight() for s in g["bolts"])
    txt = markdown(rec)
    for needle in NEEDLES:
        assert needle in txt, needle
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        stl = td / "p.stl"
        ntri = write_stl(stl, g["printed"][:1])
        assert stl.read_bytes()[80:84] == struct.pack("<I", ntri)
        assert len(stl.read_bytes()) == 84 + 50 * ntri
        three_mf = td / "a.3mf"
        assert write_3mf(three_mf, {i: g["plies"][i] for i in range(1, 5)}) == 4
        with zipfile.ZipFile(three_mf) as z:
            assert "3D/3dmodel.model" in z.namelist()
        step = td / "a.step"
        nsol = StepWriter().write(step, g["printed"] + g["bolts"])
        step_txt = step.read_text(encoding="utf-8")
        assert nsol == step_txt.count("MANIFOLD_SOLID_BREP(") == len(g["printed"]) + len(g["bolts"])
        assert step_txt.rstrip().endswith("END-ISO-10303-21;")
    print(f"Prototype self-test OK: {g['size']} mm in a {BED[0]:.0f} mm bed, "
          f"{len(g['printed'])} printed shells, {len(g['bolts'])} reference bolt solids, "
          f"cycle {rec['weave']['cycle']}, min wrench spare "
          f"{rec['clearances']['min_wrench_spare_mm']:.1f} mm.")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out-dir", default="fase1/prototipo")
    ap.add_argument("--out-md", default="fase1/prototipo-union-atornillada-R0.md")
    ap.add_argument("--out-json", default="knowledge/comparisons/bolted-lap-prototype.json")
    a = ap.parse_args()
    if a.selftest:
        return 0 if selftest() else 1
    rec = make_record()
    g = geometry()
    outdir = Path(a.out_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    for i in range(1, 5):
        write_stl(outdir / f"ply{i}.stl", g["plies"][i])
    write_3mf(outdir / "joint_3mf.3mf", {i: g["plies"][i] for i in range(1, 5)})
    nsol = StepWriter().write(outdir / "joint.step", g["printed"] + g["bolts"])
    Path(a.out_md).write_text(markdown(rec), encoding="utf-8")
    rec["step_solids"] = nsol
    Path(a.out_json).write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote four STL bodies, one 3MF, one STEP ({nsol} solids), "
          f"{a.out_md} and {a.out_json}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
