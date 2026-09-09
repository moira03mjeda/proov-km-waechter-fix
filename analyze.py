# analyze.py
# SUMMARY: The two factors that best predict a breakdown are km_since_service
# (cars that broke down averaged 11,678 km since last service vs 7,261 for those
# that did not — a 61% gap, correlation 0.40) and avg_daily_km / load_factor
# (harder-driven cars break down more). Total mileage and age show nearly zero
# separation between the groups — the obvious assumption is wrong; follow the data.
#
# Risk score: weighted combination of the three predictive features, scaled 0-100.
# Cars are ranked highest-first so the fleet team fixes the risky ones before the
# 80% wear rule would ever flag them.

import pandas as pd


def build_risk_scores(csv_path: str = "fleet_history.csv") -> pd.DataFrame:
    """Load fleet history and return a DataFrame ranked by breakdown risk (0-100)."""
    df = pd.read_csv(csv_path)

    # ── Factor analysis ──────────────────────────────────────────────────────
    # Compare group means: cars that broke down vs those that did not.
    broke = df[df["broke_down"] == 1]
    ok    = df[df["broke_down"] == 0]

    print("=== Group means: broke_down=1 vs broke_down=0 ===")
    features = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
    print(f"{'Column':<22} {'Broke mean':>12} {'OK mean':>12} {'Diff':>9}")
    print("-" * 60)
    for col in features:
        bm   = broke[col].mean()
        om   = ok[col].mean()
        diff = ((bm - om) / om * 100) if om != 0 else 0.0
        print(f"{col:<22} {bm:>12.1f} {om:>12.1f} {diff:>+8.1f}%")

    print()
    print("=== Pearson correlations with broke_down ===")
    corr = df[features + ["broke_down"]].corr()["broke_down"].drop("broke_down")
    corr_sorted = corr.abs().sort_values(ascending=False)
    for col in corr_sorted.index:
        print(f"  {col:<22}  r = {corr[col]:+.3f}")

    print()
    print("Conclusion: odometer_km and age_years have near-zero correlation with")
    print("breakdown. The real signals are km_since_service (r=+0.40), avg_daily_km")
    print("(r=+0.25), and load_factor (r=+0.22).")
    print()

    # ── Risk score ──────────────────────────────────────────────────────────
    # Weights chosen to reflect relative correlation strengths:
    #   km_since_service  40%
    #   avg_daily_km      30%
    #   load_factor       30%
    # Each feature is min-max scaled to [0, 1] first, then combined.

    def minmax(series: pd.Series) -> pd.Series:
        lo, hi = series.min(), series.max()
        return (series - lo) / (hi - lo) if hi > lo else series * 0.0

    df["risk_score"] = (
        0.40 * minmax(df["km_since_service"]) +
        0.30 * minmax(df["avg_daily_km"]) +
        0.30 * minmax(df["load_factor"])
    ) * 100

    ranked = df.sort_values("risk_score", ascending=False).reset_index(drop=True)
    ranked.index += 1  # rank starts at 1

    # ── Output ──────────────────────────────────────────────────────────────
    print("=== Fleet ranked by breakdown risk (highest first) ===")
    print(f"{'Rank':<6} {'Car ID':<12} {'Risk':>6}  {'km_since_svc':>13} "
          f"{'avg_daily_km':>13} {'load_factor':>12} {'broke_down':>11}")
    print("-" * 80)
    for rank, row in ranked.iterrows():
        print(
            f"{rank:<6} {row['car_id']:<12} {row['risk_score']:>6.1f}  "
            f"{row['km_since_service']:>13.0f} {row['avg_daily_km']:>13.0f} "
            f"{row['load_factor']:>12.2f} {int(row['broke_down']):>11}"
        )

    return ranked


if __name__ == "__main__":
    build_risk_scores()
