import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

from .config import (
    CHARTS_DIR,
    RATING_ANALYSIS_PATH,
    SUMMARY_PATH,
)

RATING_GROUPS = ("Low", "Medium", "High")


def _rating_group(rating: float) -> str:
    if rating <= 2:
        return "Low"
    if rating < 4:
        return "Medium"
    return "High"


def _correlation(function, word_counts: pd.Series, ratings: pd.Series):
    if len(word_counts) < 2 or word_counts.nunique() < 2 or ratings.nunique() < 2:
        return math.nan, math.nan
    result = function(word_counts, ratings)
    return float(result.statistic), float(result.pvalue)


def _format_statistic(value: float, precision: int = 4) -> str:
    return f"{value:.{precision}f}" if math.isfinite(value) else "undefined"


def analyze_review_length(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if df.empty:
        raise ValueError("Cannot analyze review lengths: no valid reviews.")

    print("\n========== REVIEW LENGTH ANALYSIS ==========")
    average_characters = float(df["Review_Length"].mean())
    average_words = float(df["Word_Count"].mean())
    shortest_review = int(df["Review_Length"].min())
    longest_review = int(df["Review_Length"].max())

    print(f"Average review length: {average_characters:.2f} characters")
    print(f"Average review word count: {average_words:.2f} words")
    print(f"Shortest review: {shortest_review} characters")
    print(f"Longest review: {longest_review} characters")

    rating_groups = df["Rating"].map(_rating_group)
    grouped = df.assign(Rating_Group=rating_groups).groupby(
        "Rating_Group",
        observed=False,
    )
    rating_analysis = (
        grouped.agg(
            Average_Characters=("Review_Length", "mean"),
            Average_Words=("Word_Count", "mean"),
            Review_Count=("Rating", "count"),
            Average_Rating=("Rating", "mean"),
        )
        .reindex(RATING_GROUPS)
        .rename_axis("Rating_Group")
        .reset_index()
    )
    rating_analysis.to_csv(RATING_ANALYSIS_PATH, index=False)

    print("\nAverage review length by rating group:")
    print(rating_analysis.to_string(index=False))

    figure, axis = plt.subplots(figsize=(10, 6))
    sns.histplot(
        data=df,
        x="Word_Count",
        bins=30,
        kde=df["Word_Count"].nunique() > 1,
        ax=axis,
    )
    axis.set_title("Distribution of Restaurant Review Lengths")
    axis.set_xlabel("Number of Words")
    axis.set_ylabel("Number of Reviews")
    figure.tight_layout()
    figure.savefig(CHARTS_DIR / "review_length_distribution.png", dpi=300)
    plt.close(figure)

    plot_data = df.assign(Rating_Group=rating_groups)
    figure, axis = plt.subplots(figsize=(9, 6))
    sns.boxplot(
        data=plot_data,
        x="Rating_Group",
        y="Word_Count",
        order=RATING_GROUPS,
        ax=axis,
    )
    axis.set_title("Review Length Across Rating Groups")
    axis.set_xlabel("Rating Group")
    axis.set_ylabel("Review Length (Words)")
    figure.tight_layout()
    figure.savefig(CHARTS_DIR / "review_length_vs_rating.png", dpi=300)
    plt.close(figure)

    pearson_corr, pearson_p = _correlation(
        pearsonr,
        df["Word_Count"],
        df["Rating"],
    )
    spearman_corr, spearman_p = _correlation(
        spearmanr,
        df["Word_Count"],
        df["Rating"],
    )
    correlation_data = df[["Review_Length", "Word_Count", "Rating"]].corr()

    print("\n========== CORRELATION ANALYSIS ==========")
    print(f"Pearson correlation: {_format_statistic(pearson_corr)}")
    print(f"Pearson p-value: {_format_statistic(pearson_p, 6)}")
    print(f"Spearman correlation: {_format_statistic(spearman_corr)}")
    print(f"Spearman p-value: {_format_statistic(spearman_p, 6)}")

    if math.isfinite(pearson_corr):
        relationship = (
            "positive"
            if pearson_corr > 0
            else "negative"
            if pearson_corr < 0
            else "no linear"
        )
        print(
            f"\nThe Pearson correlation indicates a {relationship} "
            "linear relationship."
        )
    else:
        print(
            "\nThe Pearson relationship is undefined because the data "
            "does not vary enough to calculate it."
        )

    significant = math.isfinite(pearson_p) and pearson_p < 0.05
    if significant:
        print("The linear association is statistically significant at the 5% level.")
    elif math.isfinite(pearson_p):
        print(
            "The linear association is not statistically significant at "
            "the 5% level."
        )
    else:
        print("Statistical significance cannot be assessed for this dataset.")

    with SUMMARY_PATH.open("w", encoding="utf-8") as file:
        file.write("RESTAURANT REVIEW ANALYSIS SUMMARY\n")
        file.write("=" * 40 + "\n")
        file.write(f"Total reviews analyzed: {len(df)}\n")
        file.write(f"Average review length: {average_characters:.2f} characters\n")
        file.write(f"Average review word count: {average_words:.2f} words\n")
        file.write(f"Shortest review: {shortest_review} characters\n")
        file.write(f"Longest review: {longest_review} characters\n")
        file.write(f"Pearson correlation: {_format_statistic(pearson_corr)}\n")
        file.write(f"Pearson p-value: {_format_statistic(pearson_p, 6)}\n")
        file.write(f"Spearman correlation: {_format_statistic(spearman_corr)}\n")
        file.write(f"Spearman p-value: {_format_statistic(spearman_p, 6)}\n")

    return rating_analysis, correlation_data
