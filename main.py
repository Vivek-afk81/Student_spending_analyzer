from src.load_data import load_transactions
from src.monthly_anomaly import compute_monthly_spend,remove_incomplete_months,compute_monthly_baseline,detect_monthly_anomalies,compute_monthly_features,detect_ml_anomalies



def main():
    df = load_transactions("data/raw/transactions.csv")

    """ Rule-based anomalies detection"""
    monthly = compute_monthly_spend(df)
    monthly_clean = remove_incomplete_months(monthly)
    monthly_with_baseline = compute_monthly_baseline(monthly_clean)
    rule_flagged = detect_monthly_anomalies(monthly_with_baseline)

    """ ML-based anomalies detection"""
    monthly_features = compute_monthly_features(df)
    ml_flagged = detect_ml_anomalies(monthly_features)

    print("Rule alerts:", len(rule_flagged))
    print("ML alerts:", len(ml_flagged))

    """ Comparing  overlap between rule based and ML based anomalies"""
    overlap = rule_flagged.merge(
        ml_flagged[["user_id", "year_month"]],
        on=["user_id", "year_month"]
    )

    print("Overlap count:", len(overlap))
    print(overlap[["user_id", "year_month"]])


if __name__ == "__main__":
    main()
