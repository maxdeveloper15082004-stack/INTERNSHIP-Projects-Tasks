import pandas as pd

MINIMUM_RESTAURANTS = 10

def analyze_cuisine_combinations(
    df: pd.DataFrame,
    minimum_restaurants: int = MINIMUM_RESTAURANTS,
) -> dict[str, object]:
    """Summarize cuisine frequencies and ratings from prepared restaurant data."""
    required_columns = ["Cuisine Combination", "Aggregate rating"]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    if df.empty:
        raise ValueError("Cannot analyze an empty dataset.")
    if minimum_restaurants < 1:
        raise ValueError("minimum_restaurants must be at least 1.")

    combination_frequency = (
        df["Cuisine Combination"]
        .value_counts()
        .rename_axis("Cuisine Combination")
        .reset_index(name="Restaurant Count")
    )

    combination_ratings = (
        df.groupby("Cuisine Combination")
        .agg(
            **{
                "Restaurant Count": ("Aggregate rating", "size"),
                "Average Rating": ("Aggregate rating", "mean"),
                "Median Rating": ("Aggregate rating", "median"),
            }
        )
        .reset_index()
        .sort_values(
            ["Average Rating", "Restaurant Count", "Cuisine Combination"],
            ascending=[False, False, True],
        )
        .reset_index(drop=True)
    )

    individual_cuisines = (
        df["Cuisine Combination"]
        .str.split(", ")
        .explode()
        .value_counts()
        .rename_axis("Cuisine")
        .reset_index(name="Restaurant Count")
    )

    reliable_combinations = (
        combination_ratings[
            combination_ratings["Restaurant Count"] >= minimum_restaurants
        ]
        .copy()
        .reset_index(drop=True)
    )

    highest_rated_combination = (
        reliable_combinations.iloc[0] if not reliable_combinations.empty else None
    )

    return {
        "total_restaurants": len(df),
        "overall_average_rating": df["Aggregate rating"].mean(),
        "combination_frequency": combination_frequency,
        "combination_ratings": combination_ratings,
        "individual_cuisines": individual_cuisines,
        "reliable_combinations": reliable_combinations,
        "most_common_combination": combination_frequency.iloc[0],
        "highest_rated_combination": highest_rated_combination,
        "minimum_restaurants": minimum_restaurants,
    }
