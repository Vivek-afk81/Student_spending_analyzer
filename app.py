import streamlit as st
from src.load_data import load_transactions
from src.monthly_anomaly import compute_monthly_spend, remove_incomplete_months,compute_monthly_baseline,detect_monthly_anomalies,compute_monthly_features,detect_ml_anomalies
import plotly.express as px

st.set_page_config(page_title="Student Spending Analyzer", layout="wide")

st.title(" Student Spending Analyzer Dashboard")

# Load data
df = load_transactions("data/raw/transactions.csv")

# --- RULE PIPELINE ---
monthly = compute_monthly_spend(df)
monthly_clean = remove_incomplete_months(monthly)
monthly_with_baseline = compute_monthly_baseline(monthly_clean)
rule_flagged = detect_monthly_anomalies(monthly_with_baseline)

# --- ML PIPELINE ---
monthly_features = compute_monthly_features(df)
ml_flagged = detect_ml_anomalies(monthly_features)

# --- USER SELECTOR ---
users = sorted(monthly_clean["user_id"].unique())
selected_user = st.selectbox("Select User", users)

st.subheader(f" Monthly Spending for {selected_user}")

# Filter selected user data
user_data = monthly_clean[monthly_clean["user_id"] == selected_user]

# Line chart
fig = px.line(
    user_data,
    x="year_month",
    y="amount",
    markers=True,
    title="Monthly Spending Trend"
)

st.plotly_chart(fig, use_container_width=True)

""" -------- RULE BASED ALERT ---------"""
user_rule_alert = rule_flagged[rule_flagged["user_id"] == selected_user]

if not user_rule_alert.empty:
    st.error(" Rule-Based Alert Triggered!")
    st.write(user_rule_alert[["year_month", "amount", "hist_mean", "pct_change"]])
else:
    st.success(" No Rule-Based Alert")

""" ----------- ML ALERT -----------"""
user_ml_alert = ml_flagged[ml_flagged["user_id"] == selected_user]

if not user_ml_alert.empty:
    st.warning(" ML-Based Alert Triggered!")
    st.write(user_ml_alert[["year_month", "total_spend", "num_transactions"]])
else:
    st.success(" No ML-Based Alert")