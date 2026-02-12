from src.load_data import load_transactions
from src.monthly_anomaly import compute_monthly_spend, remove_incomplete_months,compute_monthly_baseline,detect_monthly_anomalies
from src.alert_generator import format_monthly_alert

def main():
    df=load_transactions("data/raw/transactions.csv")


    monthly = compute_monthly_spend(df)
    monthly_clean = remove_incomplete_months(monthly)
    monthly_with_baseline= compute_monthly_baseline(monthly_clean)
    
    flagged = detect_monthly_anomalies(monthly_with_baseline)
    
    print(f"\nTotal Monthly Alerts: {len(flagged)}")

    for _, row in flagged.iterrows():
        message = format_monthly_alert(row)
        print(message)


    



if __name__=="__main__":
    main()