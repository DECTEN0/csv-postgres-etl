import pandas as pd

def transform(df):

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove rows with missing customer names
    df = df.dropna(subset=["customer_name"])

    # Fill missing dates
    df["order_date"] = df["order_date"].fillna("2025-01-01")

    # Convert date column
    df["order_date"] = pd.to_datetime(df["order_date"])

    # Create derived column
    df["total_amount"] = df["quantity"] * df["price"]

    return df