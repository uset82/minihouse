#!/usr/bin/env python3
"""Auditoria independiente de r1_gable_options (WorkBuddy). Solo lectura."""
import json
import math

j = json.load(open(r"knowledge\comparisons\r1-gable-options.json", encoding="utf-8"))
L, B, eave = 6.0, 3.0, 3.0
ok = True
for o in j["options"]:
    p = math.radians(o["pitch_deg"])
    rise = (B / 2) * math.tan(p)
    slope = (B / 2) / math.cos(p)
    checks = {
        "rise": abs(o["rise_mm"] - rise * 1000) < 0.1,
        "ridge": abs(o["ridge_z_mm"] - (eave + rise) * 1000) < 0.1,
        "slope_len": abs(o["slope_length_mm"] - slope * 1000) < 0.1,
        "roof2": abs(o["roof_surface_two_slopes_m2"] - 2 * L * slope) < 0.001,
        "gables2": abs(o["gable_end_area_two_m2"] - B * rise) < 0.001,
        "wind_long": abs(o["projected_wind_area_long_m2"] - L * (eave + rise)) < 0.001,
        "wind_end": abs(o["projected_wind_area_end_m2"] - B * (eave + rise / 2)) < 0.001,
        "minmass": abs(o["min_mass_for_1p2_m2_per_t_t"] - max(L * (eave + rise), B * (eave + rise / 2)) / 1.2) < 0.01,
    }
    bad = [k for k, v in checks.items() if not v]
    print(f"{o['pitch_deg']:>4.0f} deg: {'OK' if not bad else 'FALLO ' + str(bad)}  ridge={o['ridge_z_mm']} mm, minmass={o['min_mass_for_1p2_m2_per_t_t']} t")
    ok = ok and not bad
print("GEOMETRIA INDEPENDIENTE:", "COINCIDE" if ok else "DIVERGE")
# loaded heights
for o in j["options"]:
    for v in o["loaded_height_examples_mm"]:
        assert abs(v["loaded_height_mm"] - (o["ridge_z_mm"] + v["deck_plus_support_mm"])) < 0.1
print("LOADED HEIGHTS: OK")