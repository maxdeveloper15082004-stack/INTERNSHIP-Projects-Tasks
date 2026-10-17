from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Dataset.csv"


def load_data(data_path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the restaurant dataset and retain valid cuisine/rating records."""
    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {data_path}\n"
            "Place Dataset.csv inside data/raw/."
        )

    df = pd.read_csv(data_path, encoding="utf-8-sig")
    required_columns = ["Cuisines", "Aggregate rating"]
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["Cuisines"] = df["Cuisines"].astype("string").str.strip()
    df["Aggregate rating"] = pd.to_numeric(
        df["Aggregate rating"],
        errors="coerce",
    )
    df = df.dropna(subset=required_columns).copy()
    df = df[
        df["Cuisines"].str.len().gt(0)
        & df["Aggregate rating"].between(0, 5)
    ].copy()

    if df.empty:
        raise ValueError("No valid records remain after cleaning.")

    return df
