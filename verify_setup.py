"""
Confirm the project environment is set up correctly.

    python verify_setup.py

Checks that you are inside the virtual environment, that every package is imported, and that the statistical functions are reachable.
"""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED = [
    ("pandas", "data frames"),
    ("numpy", "arrays and maths"),
    ("scipy", "ANOVA and Levene's test"),
    ("statsmodels", "regression and Tukey HSD"),
    ("matplotlib", "figures"),
    ("seaborn", "box plots"),
]

def main() -> int:
    ok = True
    print("Python")
    print(f"  version    : {sys.version.split()[0]}")
    print(f"  executable : {sys.executable}")

    in_venv = sys.prefix != sys.base_prefix
    marker = ".venv" in sys.executable.replace("\\", "/")
    if in_venv:
        print("  virtualenv : ACTIVE" + ("  (.venv)" if marker else ""))
    else:
        ok = False
        print("  virtualenv : NOT ACTIVE  <-- activate it before installing")

    print("\nPackages")
    for name, why in REQUIRED:
        try:
            mod = __import__(name)
            ver = getattr(mod, "__version__", "?")
            print(f"  {name:<12} {ver:<10} {why}")
        except ImportError:
            ok = False
            print(f"  {name:<12} {'MISSING':<10} {why}")

    print("\nThe functions this project calls")
    checks = [
        ("scipy.stats.f_oneway", "one-way ANOVA"),
        ("scipy.stats.levene", "homogeneity of variance"),
        ("scipy.stats.shapiro", "normality"),
        ("statsmodels.formula.api.ols", "regression with interaction"),
        ("statsmodels.stats.multicomp.pairwise_tukeyhsd", "Tukey HSD post-hoc"),
    ]
    for path, why in checks:
        module, _, attr = path.rpartition(".")
        try:
            mod = __import__(module, fromlist=[attr])
            getattr(mod, attr)
            print(f"  OK      {path:<48} {why}")
        except Exception as exc:
            ok = False
            print(f"  FAILED  {path:<48} {type(exc).__name__}")

    print("\nData")
    data = Path("data")
    expected = ["results.csv", "races.csv", "status.csv"]
    if not data.exists():
        print("  data/ folder not created")
    else:
        for f in expected:
            p = data / f
            print(f"  {'found   ' if p.exists() else 'missing '} data/{f}")

    print("\n" + ("Environment is ready." if ok else
                  "Something above needs fixing before you continue."))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
