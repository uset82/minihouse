#!/usr/bin/env python3
"""MiniHouse · D001 independent derivation of the symmetric overhanging beam.

Derives from equilibrium + Euler-Bernoulli integration (not from the report's
stated formulas) the expressions for M at the support and at midspan, and the
midspan deflection. Then evaluates the report's numerical case.

Units: m, N, Pa (EI in N*m^2). Origin x=0 at the left free end.
"""
import sympy as sp

x, L, a, q, EI = sp.symbols('x L a q EI', positive=True)

# Symmetry: supports at x=a and x=L-a. Total load qL,Reactions qL/2 each.
R = q * L / 2

# Bending moment in the central span a <= x <= L-a, from the right-hand
# convention M(x) = R(x-a) - q*x^2/2 (load from x=0 to x).
M = R * (x - a) - q * x**2 / 2

M_support = sp.simplify(M.subs(x, a))
M_mid = sp.simplify(M.subs(x, L / 2))

# EI*v'' = M  =>  v'' = M/EI. Integrate twice on the central span.
C1, C2 = sp.symbols('C1 C2')
vp = sp.integrate(M / EI, x) + C1
v = sp.integrate(vp, x) + C2

# Boundary conditions: v(a)=0 (support), v'(L/2)=0 (symmetry at midspan).
sol = sp.solve([sp.Eq(v.subs(x, a), 0), sp.Eq(vp.subs(x, L / 2), 0)], [C1, C2], dict=True)[0]
v_sol = sp.simplify(v.subs(sol))
delta_mid = sp.simplify(v_sol.subs(x, L / 2))

# Report's claimed expression for comparison.
delta_report = q / EI * (5 * (L - 2*a)**4 / 384 - a**2 * (L - 2*a)**2 / 16)

# Sign convention: v is measured positive UP in this derivation, so a downward
# sag is negative. The report quotes the downward MAGNITUDE (positive).
# Check the two symbolic forms are negatives of each other.
sign_relation = sp.simplify(delta_mid + delta_report)

print('=== Symbolic results ===')
print('M(x)          =', M)
print('M_A           =', M_support)
print('M_mid         =', sp.factor(M_mid))
print('delta_mid     =', sp.factor(delta_mid), '  (positive-up convention)')
print('report expr   =', sp.simplify(delta_report), '  (downward magnitude)')
print('sum (must=0)  =', sign_relation)

# Numerical case from the report.
vals = {L: 6.0, q: 2452.5, EI: 1.68e6}
results = {}
for av in (0.0, 1.2):
    dm = float(sp.N(delta_mid.subs(vals).subs(a, av)))
    mm = float(sp.N(M_mid.subs(vals).subs(a, av))) / 1000.0
    ma = float(sp.N(M_support.subs(vals).subs(a, av))) / 1000.0
    results[av] = abs(dm) * 1000
    print(f'\na={av} m : M_A={ma:.3f} kNm  M_mid={mm:.3f} kNm  |delta_mid|={abs(dm)*1000:.3f} mm')

assert sign_relation == 0, 'derived deflection is not the negative of the report expression'
assert abs(float(sp.N(M_mid.subs(vals).subs(a, 0))) / 1000 - 11.036) < 0.001
assert abs(float(sp.N(M_support.subs(vals).subs(a, 1.2))) / 1000 - (-1.766)) < 0.001
assert abs(results[0.0] - 24.634) < 0.01
assert abs(results[1.2] - 1.490) < 0.01
print('\nD001 VERIFIED: derivation reproduces M_A, M_mid and the two deflections.')
print('Sign convention documented: v positive up; report quotes downward magnitude.')
