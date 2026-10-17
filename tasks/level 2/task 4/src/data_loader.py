import pandas as pd

DATA_PATH = "data/raw/Dataset.csv"

REQUIRED_COLUMNS = [
    "Restaurant Name",
    "City",
    "Aggregate rating",
    "Votes"
]


def load_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    print("Dataset loaded successfully.")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    return df
