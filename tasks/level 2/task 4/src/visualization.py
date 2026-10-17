import os

import matplotlib.pyplot as plt
import seaborn as sns

CHART_DIR = "outputs/charts"


def create_output_folder():
    os.makedirs(CHART_DIR, exist_ok=True)


def plot_top_chains(top_chains):
    create_output_folder()

    if top_chains.empty:
        print("No restaurant chains found.")
        return

    data = top_chains.sort_values("outlet_count")

    plt.figure(figsize=(12, 7))

    sns.barplot(
        data=data,
        x="outlet_count",
        y="Restaurant Name"
    )

    plt.title("Top 10 Restaurant Chains by Number of Outlets")
    plt.xlabel("Number of Outlets")
    plt.ylabel("Restaurant Chain")
    plt.tight_layout()

    plt.savefig(
        f"{CHART_DIR}/top_restaurant_chains.png",
        dpi=300
    )

    plt.close()


def plot_highest_rated_chains(highest_rated):
    create_output_folder()

    if highest_rated.empty:
        print("No chains meet the rating comparison requirement.")
        return

    data = highest_rated.head(10).sort_values("average_rating")

    plt.figure(figsize=(12, 7))

    sns.barplot(
        data=data,
        x="average_rating",
        y="Restaurant Name"
    )

    plt.title("Top 10 Restaurant Chains by Average Rating")
    plt.xlabel("Average Rating")
    plt.ylabel("Restaurant Chain")
    plt.xlim(0, 5)
    plt.tight_layout()

    plt.savefig(
        f"{CHART_DIR}/highest_rated_chains.png",
        dpi=300
    )

    plt.close()


def plot_most_popular_chains(most_popular):
    create_output_folder()

    if most_popular.empty:
        print("No restaurant chains found.")
        return

    data = most_popular.head(10).sort_values("total_votes")

    plt.figure(figsize=(12, 7))

    sns.barplot(
        data=data,
        x="total_votes",
        y="Restaurant Name"
    )

    plt.title("Top 10 Restaurant Chains by Total Votes")
    plt.xlabel("Total Votes")
    plt.ylabel("Restaurant Chain")
    plt.tight_layout()

    plt.savefig(
        f"{CHART_DIR}/most_popular_chains.png",
        dpi=300
    )

    plt.close()

    print("\nCharts saved successfully.")
