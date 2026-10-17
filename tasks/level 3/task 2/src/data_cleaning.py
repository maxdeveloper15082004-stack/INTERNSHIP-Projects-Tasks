import numpy as np
import pandas as pd

from .config import CLEANED_DATA_PATH


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    initial_rows = len(cleaned)

    cleaned = cleaned.drop_duplicates()
    cleaned["Restaurant Name"] = (
        cleaned["Restaurant Name"].astype("string").str.strip()
    )
    cleaned["Votes"] = pd.to_numeric(cleaned["Votes"], errors="coerce")
    cleaned["Aggregate rating"] = pd.to_numeric(
        cleaned["Aggregate rating"], errors="coerce"
    )
    cleaned = cleaned.dropna(
        subset=["Restaurant Name", "Votes", "Aggregate rating"]
    )

    valid_names = cleaned["Restaurant Name"].str.len() > 0
    valid_numbers = (
        np.isfinite(cleaned["Votes"])
        & np.isfinite(cleaned["Aggregate rating"])
    )
    valid_values = (
        (cleaned["Votes"] >= 0)
        & (cleaned["Votes"] % 1 == 0)
        & cleaned["Aggregate rating"].between(0, 5)
    )
    cleaned = cleaned[valid_names & valid_numbers & valid_values].copy()
    cleaned["Votes"] = cleaned["Votes"].astype("int64")

    cleaned.to_csv(CLEANED_DATA_PATH, index=False)

    print("\n========== DATA CLEANING ==========")
    print(f"Original records: {initial_rows}")
    print(f"Cleaned records: {len(cleaned)}")
    print(f"Removed records: {initial_rows - len(cleaned)}")
    print(f"\nCleaned dataset saved to: {CLEANED_DATA_PATH}")
    return cleaned
