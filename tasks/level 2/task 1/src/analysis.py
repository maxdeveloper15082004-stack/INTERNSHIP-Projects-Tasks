import pandas as pd


def analyze_ratings(df: pd.DataFrame) -> dict[str, object]:
    """Calculate rating counts, range counts, percentages, and average votes."""
    ratings = df["Aggregate rating"]
    rating_distribution = ratings.value_counts().sort_index()

    rating_labels = ["0-1", "1-2", "2-3", "3-4", "4-5"]
    analyzed_df = df.copy()
    analyzed_df["Rating Range"] = pd.cut(
        analyzed_df["Aggregate rating"],
        bins=[0, 1, 2, 3, 4, float("inf")],
        labels=rating_labels,
        right=False,
        include_lowest=True,
    )

    range_distribution = (
        analyzed_df["Rating Range"]
        .value_counts(sort=False)
        .reindex(rating_labels, fill_value=0)
    )
    rating_percentages = range_distribution / len(analyzed_df) * 100
    most_common_range = range_distribution.idxmax()

    return {
        "total_restaurants": len(analyzed_df),
        "rating_distribution": rating_distribution,
        "range_distribution": range_distribution,
        "rating_percentages": rating_percentages,
        "most_common_range": most_common_range,
        "most_common_range_count": int(range_distribution[most_common_range]),
        "average_votes": analyzed_df["Votes"].mean(),
    }