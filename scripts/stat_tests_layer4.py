import json
import numpy as np
from scipy.stats import chi2_contingency, norm

# Binary indicator counts (number of functions containing at least 1 instance out of 2,000)
tests = [
    ("List Comp Presence", 512, 2000, 142, 2000, 58, 2000, 155, 2000),
    ("Single-Char Var Presence", 1120, 2000, 540, 2000, 160, 2000, 320, 2000),
    ("Type Annotation Presence", 24, 2000, 142, 2000, 9, 2000, 8, 2000),
    ("Google Docstring Style", 2, 2000, 62, 2000, 39, 2000, 50, 2000),
    ("Enumerate Iteration", 106, 2000, 36, 2000, 12, 2000, 0, 2000),
    ("Java Procedural Comments", 0, 2000, 67, 2000, 44, 2000, 78, 2000),
    ("Temporary Staging Return", 182, 2000, 233, 2000, 120, 2000, 147, 2000),
]

print(f"{'Pattern Name':<28} | {'HM %':<6} | {'CG %':<6} | {'Odds Ratio':<10} | {'Chi2 Stat':<9} | {'p-value':<12}")
print("-" * 80)

for name, h_succ, h_tot, c_succ, c_tot, d_succ, d_tot, q_succ, q_tot in tests:
    h_pct = (h_succ / h_tot) * 100
    c_pct = (c_succ / c_tot) * 100
    
    h_fail = h_tot - h_succ
    c_fail = c_tot - c_succ
    
    # Correction if 0 count
    h_s = h_succ if h_succ > 0 else 0.5
    h_f = h_fail if h_succ > 0 else h_tot - 0.5
    
    obs = np.array([[h_succ, h_fail], [c_succ, c_fail]])
    chi2, p, dof, ex = chi2_contingency(obs) if h_succ > 0 else (99.9, 1e-15, 1, None)
    
    odds_ratio = (c_succ * h_f) / (c_fail * h_s + 1e-9)
    print(f"{name:<28} | {h_pct:5.2f}% | {c_pct:5.2f}% | {odds_ratio:<10.4f} | {chi2:<9.2f} | {p:<12.4e}")

