import pandas as pd


def clean_cuisine_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize cuisine combinations by trimming, deduplicating, and sorting."""
    df = df.copy()

    def normalize_cuisines(value: str) -> str:
        cuisines = {cuisine.strip() for cuisine in value.split(",") if cuisine.strip()}
        return ", ".join(sorted(cuisines, key=str.casefold))

    df["Cuisine Combination"] = df["Cuisines"].apply(normalize_cuisines)
    return df[df["Cuisine Combination"].str.len().gt(0)].copy()
