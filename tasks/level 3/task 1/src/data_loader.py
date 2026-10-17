import pandas as pd

from .config import RESTAURANT_DATA_PATH, REVIEWS_DATA_PATH


def _load_csv(path, description: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"{description} not found: {path}")

    return pd.read_csv(path, encoding="utf-8-sig")


def load_restaurant_data() -> pd.DataFrame:
    df = _load_csv(RESTAURANT_DATA_PATH, "Restaurant dataset")
    required_columns = {"Restaurant Name", "Aggregate rating", "Rating text"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Restaurant dataset is missing required columns: "
            f"{sorted(missing_columns)}"
        )
    return df


def load_review_data() -> pd.DataFrame:
    df = _load_csv(
        REVIEWS_DATA_PATH,
        "Review dataset",
    )
    required_columns = {"Review", "Rating"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Review dataset is missing required columns: "
            f"{sorted(missing_columns)}"
        )
    return df


def inspect_restaurant_data(df: pd.DataFrame) -> None:
    print("\n========== RESTAURANT DATASET ==========")
    print(f"Shape: {df.shape}")
    print(f"\nColumns:\n{df.columns.tolist()}")
    print(f"\nFirst five rows:\n{df.head()}")
    print(f"\nMissing values:\n{df.isnull().sum()}")

    if "Aggregate rating" in df.columns:
        print("\nAggregate rating statistics:")
        print(pd.to_numeric(df["Aggregate rating"], errors="coerce").describe())

    if "Rating text" in df.columns:
        print("\nRating category counts:")
        print(df["Rating text"].value_counts(dropna=False))

    if "Review" not in df.columns:
        print("\nNOTE: This dataset does not contain actual review text.")
