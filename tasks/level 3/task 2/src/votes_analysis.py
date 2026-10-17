import matplotlib.pyplot as plt
import pandas as pd

from .config import (
    BOTTOM_10_REPORT_PATH,
    CHARTS_DIR,
    TOP_10_REPORT_PATH,
)


def analyze_votes(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    print("\n========== VOTES ANALYSIS ==========")
    top_10 = df.sort_values(
        by="Votes", ascending=False, kind="stable"
    ).head(10)
    bottom_10 = df.sort_values(
        by="Votes", ascending=True, kind="stable"
    ).head(10)

    top_10.to_csv(TOP_10_REPORT_PATH, index=False)
    bottom_10.to_csv(BOTTOM_10_REPORT_PATH, index=False)

    display_columns = ["Restaurant Name", "Votes", "Aggregate rating"]
    print("\nTop 10 Restaurants by Votes:")
    print(top_10[display_columns].to_string(index=False))
    print("\nBottom 10 Restaurants by Votes:")
    print(bottom_10[display_columns].to_string(index=False))

    print("\nMost-voted restaurant:")
    print(f"{top_10.iloc[0]['Restaurant Name']} - Votes: {top_10.iloc[0]['Votes']}")
    print("\nLeast-voted restaurant:")
    print(
        f"{bottom_10.iloc[0]['Restaurant Name']} "
        f"- Votes: {bottom_10.iloc[0]['Votes']}"
    )

    plot_votes(
        top_10,
        "Top 10 Restaurants by Number of Votes",
        "top_10_restaurants_votes.png",
    )
    plot_votes(
        bottom_10,
        "Bottom 10 Restaurants by Number of Votes",
        "bottom_10_restaurants_votes.png",
    )
    return top_10, bottom_10


def plot_votes(data: pd.DataFrame, title: str, filename: str) -> None:
    plot_data = data.sort_values("Votes", ascending=True, kind="stable")

    fig, axis = plt.subplots(figsize=(12, 7))
    axis.barh(plot_data["Restaurant Name"], plot_data["Votes"])
    axis.set_title(title)
    axis.set_xlabel("Number of Votes")
    axis.set_ylabel("Restaurant Name")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"\nChart saved: {filename}")
