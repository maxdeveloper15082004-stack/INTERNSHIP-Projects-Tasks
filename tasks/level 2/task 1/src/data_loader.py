from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Dataset.csv"


def load_data() -> pd.DataFrame:
    """Load, validate, and clean the restaurant dataset."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Place Dataset.csv inside data/raw/"
        )

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    required_columns = ["Aggregate rating", "Votes"]
    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["Aggregate rating"] = pd.to_numeric(
        df["Aggregate rating"], errors="coerce"
    )
    df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce")
    df = df.dropna(subset=required_columns).copy()
    df = df[
        df["Aggregate rating"].between(0, 5) & (df["Votes"] >= 0)
    ].copy()

    if df.empty:
        raise ValueError("No valid restaurant records remain after cleaning.")

    return df