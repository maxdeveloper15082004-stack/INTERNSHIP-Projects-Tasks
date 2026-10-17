import pandas as pd

from config import CLEANED_DATA_PATH


def clean_data(df):
    df = df.copy()

    initial_rows = len(df)

    df = df.drop_duplicates()

    df["Price range"] = pd.to_numeric(df["Price range"], errors="coerce")

    service_columns = ["Has Online delivery", "Has Table booking"]

    for column in service_columns:
        df[column] = df[column].astype("string").str.strip().str.title()

    df = df.dropna(
        subset=[
            "Restaurant Name",
            "Price range",
            "Has Online delivery",
            "Has Table booking",
        ]
    )

    df = df[df["Price range"].isin([1, 2, 3, 4])]

    for column in service_columns:
        df = df[df[column].isin(["Yes", "No"])]

    df["Price range"] = df["Price range"].astype(int)

    df.to_csv(CLEANED_DATA_PATH, index=False)

    print("\n========== DATA CLEANING ==========")
    print("Original records:", initial_rows)
    print("Cleaned records:", len(df))
    print("Removed records:", initial_rows - len(df))
    print("\nCleaned dataset saved to:")
    print(CLEANED_DATA_PATH)

    return df
