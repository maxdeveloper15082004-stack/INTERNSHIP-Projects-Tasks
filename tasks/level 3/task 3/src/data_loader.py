import pandas as pd

from config import DATA_PATH

REQUIRED_COLUMNS = [
    "Restaurant Name",
    "Price range",
    "Has Online delivery",
    "Has Table booking",
]


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    print("\n========== DATASET INFORMATION ==========")
    print("Dataset shape:", df.shape)
    print("\nFirst five rows:")
    print(df.head())
    print("\nColumn names:")
    print(df.columns.tolist())

    return df
