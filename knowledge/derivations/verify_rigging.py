#!/usr/bin/env python3
"""MiniHouse · D003 independent verification of sling geometry and leg distribution.

Verifies T = V/sin(a), H = V*cot(a) with a from the horizontal; reproduces the
sensitivity table in fase1/condiciones-transporte-izaje.md; and checks the
four-leg distribution warning (four legs are NOT W/4).
"""
import math

def geom(V, alpha_deg):
    a = math.radians(alpha_deg)
    return V / math.sin(a), V / math.tan(a)

print('=== Sensitivity table, V = 1 kN ===')
print(' alpha |   T/V  |   H/V')
for alpha in (90, 60, 45, 30):
    T, H = geom(1.0, alpha)
    print(f' {alpha:4d}  | {T:6.3f} | {H:6.3f}')

expected = {90: (1.000, 0.000), 60: (1.155, 0.577), 45: (1.414, 1.000), 30: (2.000, 1.732)}
for alpha, (Te, He) in expected.items():
    T, H = geom(1.0, alpha)
    assert abs(T - Te) < 0.001 and abs(H - He) < 0.001, f'failed at {alpha}'

# Report's hypothetical 3000 kg case, 4 legs, perfect sharing, alpha from horizontal
W = 3000 * 9.81 / 1000  # kN
V_leg = W / 4
print(f'\n=== Report hypothetical: W={W:.3f} kN, V per leg={V_leg:.4f} kN ===')
for alpha in (60, 30):
    T, H = geom(V_leg, alpha)
    print(f' alpha={alpha}: T={T:.3f} kN, H={H:.3f} kN')
assert abs(geom(V_leg, 60)[0] - 8.495) < 0.01
assert abs(geom(V_leg, 30)[0] - 14.715) < 0.01

# Four-leg distribution demonstration: 4 supports, 3 equilibrium equations.
# A rigid body on 4 supports is statically indeterminate to degree 1:
# sum(Vi) = W, sum(Vi*xi) = W*xG, sum(Vi*yi) = W*yG  -> 3 eq for 4 unknowns.
print('\n=== Four-leg distribution ===')
print('Equilibrium gives 3 independent equations for 4 unknown leg forces.')
print('Degree of indeterminacy = 4 - 3 = 1 -> distribution depends on stiffness,')
print('leg length tolerances, pre-tension, rigging geometry and CG position.')
print('Two-effective-leg pattern (S000): if only 2 of 4 legs carry, V_leg = W/2,')
print(f'which at alpha=60 gives T = {geom(W/2, 60)[0]:.3f} kN (vs {geom(W/4,60)[0]:.3f} kN for perfect 4-leg sharing).')
assert abs(geom(W/2, 60)[0] / geom(W/4, 60)[0] - 2.0) < 1e-9

print('\nD003 VERIFIED: sling geometry table and four-leg warning reproduced.')
