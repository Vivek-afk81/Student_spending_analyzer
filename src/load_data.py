import pandas as pd

def load_transactions(path: str) -> pd.DataFrame:
    """
    load transcations data from csv file"""

    df=pd.read_csv(path)

    df["date"]=pd.to_datetime(df["date"], errors="coerce")
    df["timestamp"]=pd.to_datetime(df["timestamp"], errors="coerce")


    #keeping only debit transactions(expenses)
    df=df[df["transaction_type"]=="debit"].copy()

    #converting the negative amount into positive
    df["amount"]=df["amount"].abs()

    return df
