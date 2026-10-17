from src.data_loader import load_data
from src.preprocessing import clean_data
from src.analysis import analyze_restaurant_chains
from src.visualization import (
    plot_top_chains,
    plot_highest_rated_chains,
    plot_most_popular_chains
)
from src.report import save_reports


def main():
    df = load_data()

    df = clean_data(df)

    (
        chains,
        top_chains,
        highest_rated,
        most_popular
    ) = analyze_restaurant_chains(df)

    plot_top_chains(top_chains)
    plot_highest_rated_chains(highest_rated)
    plot_most_popular_chains(most_popular)

    save_reports(
        chains,
        top_chains,
        highest_rated,
        most_popular,
        len(df)
    )

    print("\nRestaurant Chain Analysis Completed Successfully!")


if __name__ == "__main__":
    main()
