from src.load_data import load_transactions

def main():
    df=load_transactions("data/raw/transactions.csv")

    print("Loaded rows:",len(df))
    print("Columns:",df.columns.tolist())
    print(df.head())


if __name__=="__main__":
    main()