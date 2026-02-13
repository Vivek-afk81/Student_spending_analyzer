import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def compute_monthly_spend(expenses: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate expenses per user per month
    """

    monthly = (
        expenses
        .groupby(["user_id","year_month"])["amount"]
        .sum()
        .reset_index()
    )


    return monthly

def remove_incomplete_months(monthly: pd.DataFrame) -> pd.DataFrame:
    """
    Remove months that appear incomplete based on transaction volume.
    For now, we manually exclude November 2025.
    """

    monthly_clean = monthly[monthly["year_month"] != "2025-11"].copy()

    return monthly_clean

def compute_monthly_baseline(monthly: pd.DataFrame) -> pd.DataFrame:
    """
    compute historical mean and percent change for the user
    """

    monthly = monthly.sort_values(["user_id", "year_month"]).copy()

    monthly["hist_count"] = (
        monthly
        .groupby("user_id")
        .cumcount()
    )

    #Historical mean

    monthly["hist_mean"] = (
        monthly
        .groupby("user_id")["amount"]
        .apply(lambda x: x.expanding().mean().shift(1))
        .reset_index(
            level=0,
            drop=True
        )
    )

    # percent change

    monthly["pct_change"]=(
        (monthly["amount"]-monthly["hist_mean"])
        /monthly['hist_mean']
    )

    return monthly


def detect_monthly_anomalies(
    monthly: pd.DataFrame,
    min_history: int = 2,
    threshold: float = 0.60) -> pd.DataFrame:
    
    """
    Detect monthly anomalies based on percent deviation
    and minimum historical months required.
    """

    monthly["monthly_alert"] = (
        (monthly["hist_count"] >= min_history) &
        (monthly["pct_change"].abs() > threshold)
    )

    flagged = monthly[monthly["monthly_alert"]].copy()

    return flagged


## adding monthly features for ML

def compute_monthly_features(expenses: pd.DataFrame) -> pd.DataFrame:
    """
    Compute basic monthly behavioral features per user.
    """

    monthly_features = (
        expenses
        .groupby(["user_id", "year_month"])
        .agg(
            total_spend=("amount", "sum"),
            num_transactions=("amount", "count"),
            avg_transaction=("amount", "mean"),
            max_transaction=("amount", "max"),
        )
        .reset_index()
    )

    return monthly_features




def detect_ml_anomalies(monthly_features: pd.DataFrame) -> pd.DataFrame:
    """
    Use Isolation Forest to detect anomalous monthly behavior.
    """

    # Remove incomplete month
    monthly_features = monthly_features[
        monthly_features["year_month"] != "2025-11"
    ].copy()

    feature_cols = [
        "total_spend",
        "num_transactions",
        "avg_transaction",
        "max_transaction",
    ]

    X = monthly_features[feature_cols]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Isolation Forest
    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    monthly_features["ml_anomaly"] = model.fit_predict(X_scaled)

    # Convert: -1 = anomaly, 1 = normal
    monthly_features["ml_anomaly"] = (
        monthly_features["ml_anomaly"] == -1
    )

    flagged = monthly_features[monthly_features["ml_anomaly"]].copy()

    return flagged
