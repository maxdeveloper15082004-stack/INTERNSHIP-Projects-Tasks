from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"


def create_visualizations(results: dict[str, object]) -> None:
    """Save charts for frequent and highly rated cuisine combinations."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    top_combinations = (
        results["combination_frequency"]
        .head(10)
        .sort_values("Restaurant Count")
    )

    plt.figure(figsize=(12, 7))
    sns.barplot(
        data=top_combinations,
        x="Restaurant Count",
        y="Cuisine Combination",
        color=sns.color_palette()[0],
    )
    plt.title("Top 10 Most Common Cuisine Combinations")
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Cuisine Combination")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "top_cuisine_combinations.png", dpi=300)
    plt.close()

    top_rated = (
        results["reliable_combinations"]
        .head(10)
        .sort_values("Average Rating")
    )

    plt.figure(figsize=(12, 7))
    if not top_rated.empty:
        sns.barplot(
            data=top_rated,
            x="Average Rating",
            y="Cuisine Combination",
            color=sns.color_palette()[1],
        )
        plt.xlim(0, 5)
        plt.title(
            "Top 10 Highest-Rated Cuisine Combinations "
            f"(At Least {results['minimum_restaurants']} Restaurants)"
        )
        plt.xlabel("Average Aggregate Rating")
        plt.ylabel("Cuisine Combination")
    else:
        plt.text(
            0.5,
            0.5,
            "No combinations meet the minimum restaurant count.",
            ha="center",
            va="center",
        )
        plt.title("Highest-Rated Cuisine Combinations")
        plt.axis("off")

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "cuisine_average_ratings.png", dpi=300)
    plt.close()
    print(f"\nCharts saved to: {CHARTS_DIR}")
