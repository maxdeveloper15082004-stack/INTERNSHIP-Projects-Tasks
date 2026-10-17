from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"


def create_visualizations(df, results) -> None:
    """Create and save the rating histogram and rating-range bar chart."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x="Aggregate rating", bins=20, kde=True)
    plt.title("Distribution of Restaurant Aggregate Ratings")
    plt.xlabel("Aggregate Rating")
    plt.ylabel("Number of Restaurants")
    plt.tight_layout()
    plt.savefig(
        CHARTS_DIR / "rating_distribution.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()

    range_distribution = results["range_distribution"]
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=range_distribution.index.astype(str),
        y=range_distribution.values,
    )
    plt.title("Restaurant Count by Rating Range")
    plt.xlabel("Rating Range")
    plt.ylabel("Number of Restaurants")
    plt.tight_layout()
    plt.savefig(
        CHARTS_DIR / "rating_range_distribution.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()

    print("\nCharts saved successfully.")