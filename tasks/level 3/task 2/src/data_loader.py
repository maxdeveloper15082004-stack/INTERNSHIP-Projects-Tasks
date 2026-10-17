import pandas as pd

from .config import DATA_PATH


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    required_columns = {"Restaurant Name", "Votes", "Aggregate rating"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    print("\nDataset loaded successfully!")
    print(f"Dataset shape: {df.shape}")
    print("\nFirst five records:")
    print(df.head())
    return df
