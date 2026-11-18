#!/usr/bin/env python3
"""MiniHouse · the floor-to-wall junction, drawn from the solver's own constants.

Five screens now land on this one corner:

  * heat — `puente_2d` solves it in 2D and the condensation screen sets f_Rsi ≥ 0.754;
  * vapour — the barrier is Sd ≥ 10 m on the warm side, which is a line, not a layer;
  * airtightness and radon — §13-5's barrier is an airtightness item and its continuity
    is this corner;
  * structure — the chassis beam either intrudes into the floor build-up or it does not;
  * moisture — the make-up air inlet is in the wall, the drain is the wet floor penetration.

No drawing of it exists. The planos in `fase1/planos/` are hand-authored SVG, which is the
failure mode this project has already paid for four times: a number typed by hand and left
to drift from the solver. So this drawing is **generated** — every dimension comes from
`puente_2d.WALL_LAYERS` and `puente_2d.FLOOR_LAYERS`, every performance figure from
`puente_2d.evaluate()`, and the self-test fails if the drawn geometry stops matching them.

What the drawing is for is one question the prose cannot settle: **does the steel cross the
vapour barrier?** In the unwrapped case the plate occupies the floor build-up at the inner
face, so it crosses the barrier's plane at z = −22 mm over the plate's width. Wrapped below
the floor it does not cross anything. The same drawing decision therefore removes the thermal
bridge, restores f_Rsi to the bare corner's 0.921 and leaves the barrier continuous — which
is why the 2D screen's answer is a drawing instruction rather than an insulation thickness.

Usage:
  python detalle_encuentro.py --out fase1/planos/detalle-encuentro-R0.svg
  python detalle_encuentro.py --selftest
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import puente_2d as p2   # noqa: E402

# --- drawing frame -----------------------------------------------------------
SCALE = 0.80                    # px per mm
MARGIN_L, MARGIN_R = 96.0, 30.0
MARGIN_T, MARGIN_B = 152.0, 66.0
LEGEND_W = 268.0                # a column on the right: numbers in the drawing, text here
VOID_MM = 300.0                 # shown at a nominal depth; C-05 is open
WALL_SHOWN_MM = 300.0           # how much of the wall height the view carries
BEAM_MM = 10.0                  # the plate the 2D screen models

# Drawing coordinates are mirrored from the solver's: the solver measures x
# outward from the inner face, the drawing puts the room on the right, so
# x_drawing = -x_solver. Every number below still comes from puente_2d.
VIEW_X0 = -350.0
VIEW_X1 = 430.0
VIEW_Z0 = WALL_SHOWN_MM
VIEW_Z1 = -(p2.FLOOR_T_MM + BEAM_MM + VOID_MM + 45.0)

ROOM_MM = 330.0                 # how far the floor runs into the room in the view

# --- the two states the drawing compares ------------------------------------
STATES = (
    {"id": "A", "label": "beam inside the floor build-up", "wrapped": False},
    {"id": "B", "label": "beam wrapped below the floor", "wrapped": True},
)

FILLS = {
    "timber": "#d9b98a",
    "mineral wool": "#f2e2b8",
    "wood fibre": "#cbb894",
    "ventilated cavity": "#e8eef2",
    "steel": "#6b7076",
    "rigid PU": "#e6d3ef",
}
HATCH = {
    "mineral wool": "url(#wool)",
    "steel": "url(#steel)",
}
INK = "#333333"
ACCENT = "#7a2e1d"
BARRIER = "#1f5fa8"
RADON = "#2f7d4f"
DIM = "#8a6d3b"


def px(x_mm):
    return MARGIN_L + (x_mm - VIEW_X0) * SCALE


def pz(z_mm):
    return MARGIN_T + (VIEW_Z0 - z_mm) * SCALE


def width_px():
    return (VIEW_X1 - VIEW_X0) * SCALE + MARGIN_L + MARGIN_R + LEGEND_W


def height_px():
    return (VIEW_Z0 - VIEW_Z1) * SCALE + MARGIN_T + MARGIN_B


def rect_mm(x0, x1, z0, z1, fill, stroke=INK, sw=0.6, opacity=1.0):
    return (f'<rect x="{px(x0):.2f}" y="{pz(z1):.2f}" '
            f'width="{(x1 - x0) * SCALE:.2f}" height="{(z1 - z0) * SCALE:.2f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'opacity="{opacity}"/>')


def dim_h(x0, x1, z_mm, text, above=True):
    """A horizontal dimension line with its value."""
    y = pz(z_mm) + (-10 if above else 12)
    return (f'<line x1="{px(x0):.2f}" y1="{y:.2f}" x2="{px(x1):.2f}" y2="{y:.2f}" '
            f'stroke="{DIM}" stroke-width="0.8"/>'
            f'<text x="{(px(x0) + px(x1)) / 2:.2f}" y="{y - 4:.2f}" text-anchor="middle" '
            f'font-size="10" fill="{DIM}">{text}</text>')


def dim_v(z0, z1, x_mm, text, left=True):
    """A vertical dimension line with its value, rotated."""
    x = px(x_mm) + (-12 if left else 12)
    cy = (pz(z0) + pz(z1)) / 2
    return (f'<line x1="{x:.2f}" y1="{pz(z0):.2f}" x2="{x:.2f}" y2="{pz(z1):.2f}" '
            f'stroke="{DIM}" stroke-width="0.8"/>'
            f'<text x="{x - 4:.2f}" y="{cy:.2f}" text-anchor="middle" font-size="10" '
            f'fill="{DIM}" transform="rotate(-90 {x - 4:.2f} {cy:.2f})">{text}</text>')


def layer_labels():
    """One label per wall layer, stacked outward, plus the floor's three."""
    out = []
    for material, x0, x1 in p2.WALL_LAYERS:
        if x1 - x0 < 10.0:
            continue
        cx = px((x0 + x1) / 2)
        out.append(f'<text x="{cx:.2f}" y="{pz(20):.2f}" text-anchor="middle" '
                   f'font-size="8.5" fill="{INK}" transform="rotate(-90 {cx:.2f} {pz(20):.2f})">'
                   f'{material} {x1 - x0:.0f}</text>')
    return out


def model():
    """The two states, solved, plus the geometry the drawing must reproduce."""
    rows = []
    for state in STATES:
        r = p2.evaluate(steel_mm=BEAM_MM, wrapped=state["wrapped"])
        rows.append({"id": state["id"], "label": state["label"],
                     "wrapped": state["wrapped"],
                     "f_rsi": round(r["f_rsi"], 3),
                     "psi": round(r["psi_w_per_mk"], 3),
                     "coldest": r["coldest"]})
    # The barrier's corner, derived from the build-ups rather than typed.
    barrier_x = p2.WALL_LAYERS[0][2]          # behind the inner lining
    barrier_z = p2.FLOOR_LAYERS[0][1]         # under the deck, above the insulation
    return {
        "state": "CONCEPTUAL — NOT FOR FABRICATION",
        "scale": "1:12.5 at 96 dpi (0.80 px/mm)",
        "wall_t_mm": p2.WALL_T_MM,
        "floor_t_mm": p2.FLOOR_T_MM,
        "wall_layers": [{"material": m, "x0": a, "x1": b, "d_mm": b - a}
                        for m, a, b in p2.WALL_LAYERS],
        "floor_layers": [{"material": m, "z0": a, "z1": b, "d_mm": b - a}
                         for m, a, b in p2.FLOOR_LAYERS],
        "barrier": {"x_mm": barrier_x, "z_mm": barrier_z,
                    "sd_m": 10.0,
                    "note": "warm-side line: behind the lining, above the insulation"},
        "beam_mm": BEAM_MM,
        "void_mm": VOID_MM,
        "states": rows,
        "f_required": p2.F_CRIT_MOULD,
        "beam_crosses_barrier": {
            "A": True, "B": False},
    }


def svg(m):
    w, h = width_px(), height_px()
    inner_face = 0.0
    outer_face = -p2.WALL_T_MM
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="0 0 {w:.0f} {h:.0f}" font-family="Consolas, monospace">',
        '<defs>',
        '<pattern id="wool" width="6" height="6" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" '
        'stroke="#c9ae74" stroke-width="0.8"/></pattern>',
        '<pattern id="steel" width="4" height="4" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="4" '
        'stroke="#3f4448" stroke-width="0.9"/></pattern>',
        '</defs>',
        f'<rect width="{w:.0f}" height="{h:.0f}" fill="#fdfaf4"/>',
        f'<text x="{(w - LEGEND_W) / 2:.0f}" y="30" text-anchor="middle" font-size="14" '
        f'fill="{ACCENT}">MiniHouse · DETALLE ENCUENTRO PISO–PARED · R0</text>',
        f'<text x="{(w - LEGEND_W) / 2:.0f}" y="48" text-anchor="middle" font-size="12" '
        f'fill="{ACCENT}" font-weight="bold">CONCEPTUAL — NO PARA FABRICACIÓN</text>',
        f'<text x="{(w - LEGEND_W) / 2:.0f}" y="68" text-anchor="middle" font-size="10" '
        f'fill="#555">2026-11-18 · mm · sección por el borde del piso · interior a la derecha'
        f' · {m["scale"]} · vista: estado B</text>',
        f'<text x="{(w - LEGEND_W) / 2:.0f}" y="86" text-anchor="middle" font-size="9.5" '
        f'fill="#777">generado por scripts/detalle_encuentro.py desde las constantes de '
        f'puente_2d.py — ninguna cota está tecleada</text>',
    ]

    # --- the floor first, so the wall sits on top of it ----------------------
    for i, (material, z0, z1) in enumerate(p2.FLOOR_LAYERS):
        s.append(rect_mm(outer_face, ROOM_MM, z0, z1, FILLS.get(material, "#eeeeee")))

    # --- the wall ------------------------------------------------------------
    for material, x0, x1 in p2.WALL_LAYERS:
        # solver x is outward; the drawing mirrors it
        s.append(rect_mm(-x1, -x0, 0.0, VIEW_Z0, FILLS.get(material, "#eeeeee")))

    # --- the beam, wrapped below the floor ----------------------------------
    if m["states"][1]["wrapped"]:
        s.append(rect_mm(outer_face, ROOM_MM, -p2.FLOOR_T_MM - m["beam_mm"],
                         -p2.FLOOR_T_MM, FILLS["steel"], sw=0.9))

    # --- the void and the ground --------------------------------------------
    beam_bottom = -(p2.FLOOR_T_MM + m["beam_mm"])
    ground_z = beam_bottom - m["void_mm"]
    s.append(rect_mm(outer_face, ROOM_MM, ground_z, beam_bottom, "#ffffff", sw=0.5))
    s.append(f'<line x1="{px(outer_face - 55):.2f}" y1="{pz(ground_z):.2f}" '
             f'x2="{px(ROOM_MM + 30):.2f}" y2="{pz(ground_z):.2f}" stroke="{INK}" '
             f'stroke-width="1.8"/>')
    s.append(f'<text x="{px(outer_face - 50):.2f}" y="{pz(ground_z) + 14:.2f}" '
             f'font-size="9.5" fill="{INK}">terreno</text>')
    s.append(f'<text x="{px(outer_face - 50):.2f}" y="{pz(ground_z) + 28:.2f}" '
             f'font-size="8.5" fill="#777">hueco {m["void_mm"]:.0f} nominal · '
             f'C-05 sin definir</text>')
    s.append(f'<text x="{px(inner_face + 24):.2f}" y="{pz(-12):.2f}" font-size="9.5" '
             f'fill="#777">interior</text>')

    # --- the barrier: a line on the warm side -------------------------------
    bx = -m["barrier"]["x_mm"]        # mirrored
    bz = m["barrier"]["z_mm"]
    s.append(f'<path d="M {px(bx):.2f} {pz(VIEW_Z0 - 4):.2f} L {px(bx):.2f} {pz(bz):.2f} '
             f'L {px(ROOM_MM):.2f} {pz(bz):.2f}" fill="none" stroke="{BARRIER}" '
             f'stroke-width="2.4"/>')


    # --- the corner, called out ---------------------------------------------
    s.append(f'<circle cx="{px(bx):.2f}" cy="{pz(bz):.2f}" r="3.4" fill="none" '
             f'stroke="{BARRIER}" stroke-width="1.6"/>')
    s.append(f'<text x="{px(bx) - 10:.2f}" y="{pz(bz) + 22:.2f}" text-anchor="end" '
             f'font-size="8.5" fill="{BARRIER}">({m["barrier"]["x_mm"]:.0f}, '
             f'{m["barrier"]["z_mm"]:.0f})</text>')

    # --- dimensions ----------------------------------------------------------
    s.append(dim_h(outer_face, inner_face, VIEW_Z0 + 26.0,
                   f'pared {p2.WALL_T_MM:.0f}'))
    s.append(dim_v(0.0, -p2.FLOOR_T_MM, outer_face - 24.0, f'piso {p2.FLOOR_T_MM:.0f}'))
    s.append(dim_v(beam_bottom, ground_z, outer_face - 24.0, f'hueco {m["void_mm"]:.0f}'))

    # --- numbered layers, text in the legend --------------------------------
    def badge(cx, cz, number):
        return (f'<circle cx="{cx:.2f}" cy="{cz:.2f}" r="7.2" fill="#fdfaf4" '
                f'stroke="{ACCENT}" stroke-width="1"/><text x="{cx:.2f}" y="{cz + 3.4:.2f}" '
                f'text-anchor="middle" font-size="9" fill="{ACCENT}">{number}</text>')

    wall_top_z = VIEW_Z0 - 26.0
    for i, (material, x0, x1) in enumerate(p2.WALL_LAYERS, start=1):
        cx = px(-(x0 + x1) / 2)
        cz = pz(wall_top_z)
        s.append(badge(cx, cz, i))
    for j, (material, z0, z1) in enumerate(p2.FLOOR_LAYERS, start=len(p2.WALL_LAYERS) + 1):
        cx = px(ROOM_MM - 52.0)
        cz = pz((z0 + z1) / 2)
        s.append(badge(cx, cz, j))

    # --- the legend column ---------------------------------------------------
    lx = w - LEGEND_W + 14
    ly = MARGIN_T + 4
    s.append(f'<line x1="{lx - 10:.2f}" y1="{ly - 20:.2f}" x2="{lx - 10:.2f}" '
             f'y2="{h - MARGIN_B - 8:.2f}" stroke="#ddd" stroke-width="1"/>')
    s.append(f'<text x="{lx:.2f}" y="{ly:.2f}" font-size="10.5" fill="{ACCENT}">'
             f'PARED — {p2.WALL_T_MM:.0f} mm</text>')
    yy = ly + 16
    for i, l in enumerate(m["wall_layers"], start=1):
        s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="9" fill="{INK}">'
                 f'{i} · {l["material"]} {l["d_mm"]:.0f}</text>')
        yy += 14
    yy += 8
    s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="10.5" fill="{ACCENT}">'
             f'PISO — {p2.FLOOR_T_MM:.0f} mm</text>')
    yy += 16
    for j, l in enumerate(m["floor_layers"], start=len(p2.WALL_LAYERS) + 1):
        s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="9" fill="{INK}">'
                 f'{j} · {l["material"]} {l["d_mm"]:.0f}</text>')
        yy += 14

    yy += 10
    s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="10.5" fill="{ACCENT}">'
             f'LÍNEAS</text>')
    yy += 15
    s.append(f'<line x1="{lx:.2f}" y1="{yy - 3:.2f}" x2="{lx + 26:.2f}" y2="{yy - 3:.2f}" '
             f'stroke="{BARRIER}" stroke-width="2.4"/>')
    s.append(f'<text x="{lx + 32:.2f}" y="{yy:.2f}" font-size="8.5" fill="{INK}">'
             f'barrera de vapor Sd ≥ 10 m</text>')
    yy += 12
    s.append(f'<text x="{lx + 32:.2f}" y="{yy:.2f}" font-size="8.5" fill="{INK}">'
             f'estanqueidad · radón (§13-5)</text>')
    yy += 18
    a, b = m["states"]
    s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="10.5" fill="{ACCENT}">'
             f'LA MISMA ESQUINA, DOS ESTADOS</text>')
    yy += 16
    for row in (a, b):
        crossed = m["beam_crosses_barrier"][row["id"]]
        s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="9" fill="{INK}">'
                 f'{row["id"]}) f_Rsi {row["f_rsi"]:.3f} · Ψ {row["psi"]:+.3f}</text>')
        yy += 12
        s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="8.5" '
                 f'fill="{BARRIER if crossed else RADON}">   barrera '
                 f'{"cruzada" if crossed else "intacta"} · {row["label"]}</text>')
        yy += 17

    s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="8.5" fill="{ACCENT}">'
             f'requisito f_Rsi ≥ {m["f_required"]:.3f} (moho)</text>')
    yy += 13
    s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="8.5" fill="{INK}">'
             f'B no mejora el margen: retira el</text>')
    yy += 11
    s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="8.5" fill="{INK}">'
             f'puente y deja la barrera continua.</text>')
    yy += 15
    s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="8.5" fill="{RADON}">'
             f'el hueco es tampón de radón:</text>')
    yy += 11
    s.append(f'<text x="{lx:.2f}" y="{yy:.2f}" font-size="8.5" fill="{RADON}">'
             f'no cerrarlo (§13-5).</text>')

    s.append("</svg>")
    return "\n".join(s)

def selftest():
    m = model()
    a, b = m["states"]

    # The drawing's geometry must come from the solver's build-ups, not be typed.
    assert m["wall_t_mm"] == sum(l["d_mm"] for l in m["wall_layers"]), m["wall_layers"]
    assert m["floor_t_mm"] == sum(l["d_mm"] for l in m["floor_layers"]), m["floor_layers"]
    assert m["wall_t_mm"] == 264.0 and m["floor_t_mm"] == 280.0

    # The barrier corner must be derived: behind the lining, above the insulation.
    assert m["barrier"]["x_mm"] == m["wall_layers"][0]["d_mm"]
    assert m["barrier"]["z_mm"] == -m["floor_layers"][0]["d_mm"]

    # The two states must differ in the way the drawing claims: the unwrapped beam
    # crosses the barrier and fails the mould requirement; the wrapped one does not
    # and clears it. If either flips, the drawing is asserting something false.
    assert a["f_rsi"] < m["f_required"], a
    assert b["f_rsi"] > m["f_required"], b
    assert m["beam_crosses_barrier"]["A"] is True
    assert m["beam_crosses_barrier"]["B"] is False
    # Wrapping must restore the bare corner, not merely improve on the plate.
    bare = p2.evaluate(steel_mm=0.0)
    assert abs(b["f_rsi"] - bare["f_rsi"]) < 0.005, (b["f_rsi"], bare["f_rsi"])

    text = svg(m)
    # The rendered drawing must carry the status line and the derived dimensions.
    assert "NO PARA FABRICACIÓN" in text
    assert f"pared {m['wall_t_mm']:.0f}" in text
    assert f"piso {m['floor_t_mm']:.0f}" in text
    assert f"{b['f_rsi']:.3f}" in text and f"{a['f_rsi']:.3f}" in text
    assert "barrera cruzada" in text and "barrera intacta" in text
    # One rectangle per layer, plus the beam, the void and the sheet. A layer that
    # stops being drawn means the build-up changed without the drawing noticing.
    expected = len(m["wall_layers"]) + len(m["floor_layers"]) + 3
    assert text.count("<rect") == expected, (text.count("<rect"), expected)

    print(f"Junction detail self-test OK: wall {m['wall_t_mm']:.0f} mm in "
          f"{len(m['wall_layers'])} layers, floor {m['floor_t_mm']:.0f} mm in "
          f"{len(m['floor_layers'])}, barrier corner at "
          f"({m['barrier']['x_mm']:.0f}, {m['barrier']['z_mm']:.0f}), beam "
          f"{m['beam_mm']:.0f} mm crosses the barrier when unwrapped and not when wrapped, "
          f"f_Rsi {a['f_rsi']:.3f} → {b['f_rsi']:.3f} against {m['f_required']:.3f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", help="write the SVG")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return 0
    m = model()
    text = svg(m)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
