import pandas as pd


def clean_data(df):
    df = df.copy()

    df["Restaurant Name"] = (
        df["Restaurant Name"]
        .astype("string")
        .str.strip()
    )

    df["City"] = (
        df["City"]
        .astype("string")
        .str.strip()
    )

    df["Aggregate rating"] = pd.to_numeric(
        df["Aggregate rating"],
        errors="coerce"
    )

    df["Votes"] = pd.to_numeric(
        df["Votes"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Restaurant Name"]
    )

    df = df[
        df["Restaurant Name"].ne("")
    ].copy()

    df["Aggregate rating"] = df[
        "Aggregate rating"
    ].where(
        df["Aggregate rating"].between(0, 5)
    )

    df["Votes"] = df["Votes"].fillna(0).clip(lower=0)

    print("Data cleaning completed.")
    print(f"Rows available for analysis: {len(df)}")

    return df
