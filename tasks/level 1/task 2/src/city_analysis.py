from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required_columns = {"City", "Aggregate rating"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["City"] = df["City"].astype("string").str.strip()
    df["Aggregate rating"] = pd.to_numeric(
        df["Aggregate rating"],
        errors="coerce",
    )

    df = df.dropna(subset=["City"])
    return df[df["City"] != ""]


def analyze_restaurant_counts(df):
    city_counts = (
        df.groupby("City")
        .size()
        .reset_index(name="Restaurant Count")
        .sort_values("Restaurant Count", ascending=False)
        .reset_index(drop=True)
    )

    city_counts.to_csv(
        OUTPUT_DIR / "city_restaurant_counts.csv",
        index=False,
    )
    return city_counts


def analyze_average_ratings(df):
    rated_restaurants = df.dropna(subset=["Aggregate rating"])
    city_ratings = (
        rated_restaurants.groupby("City")
        .agg(
            Restaurant_Count=("Aggregate rating", "size"),
            Average_Rating=("Aggregate rating", "mean"),
        )
        .reset_index()
        .rename(
            columns={
                "Restaurant_Count": "Rated Restaurant Count",
                "Average_Rating": "Average Rating",
            }
        )
    )

    city_ratings["Average Rating"] = city_ratings["Average Rating"].round(2)
    city_ratings = city_ratings.sort_values(
        ["Average Rating", "Rated Restaurant Count"],
        ascending=[False, False],
    ).reset_index(drop=True)
    city_ratings.to_csv(
        OUTPUT_DIR / "city_average_ratings.csv",
        index=False,
    )
    return city_ratings


def create_restaurant_count_chart(city_counts):
    top_cities = city_counts.head(10).sort_values(
        "Restaurant Count",
        ascending=True,
    )

    plt.figure(figsize=(10, 6))
    bars = plt.barh(top_cities["City"], top_cities["Restaurant Count"])
    plt.bar_label(bars, padding=3)
    plt.title("Top 10 Cities by Number of Restaurants")
    plt.xlabel("Number of Restaurants")
    plt.ylabel("City")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "top_cities_by_restaurants.png",
        dpi=300,
    )
    plt.close()


def create_rating_chart(city_ratings):
    top_cities = (
        city_ratings.sort_values(
            ["Average Rating", "Rated Restaurant Count"],
            ascending=[False, False],
        )
        .head(10)
        .sort_values("Average Rating", ascending=True)
    )

    plt.figure(figsize=(10, 6))
    bars = plt.barh(top_cities["City"], top_cities["Average Rating"])
    plt.bar_label(bars, padding=3, fmt="%.2f")
    plt.title("Top 10 Cities by Average Restaurant Rating")
    plt.xlabel("Average Rating")
    plt.ylabel("City")
    plt.xlim(0, 5)
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "top_cities_by_rating.png",
        dpi=300,
    )
    plt.close()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()

    city_counts = analyze_restaurant_counts(df)
    city_ratings = analyze_average_ratings(df)

    if city_counts.empty:
        raise ValueError("The dataset contains no restaurants with a city.")

    highest_count_city = city_counts.iloc[0]
    highest_rated_city = city_ratings.iloc[0] if not city_ratings.empty else None

    summary = [
        {
            "Analysis": "City with the Highest Number of Restaurants",
            "City": highest_count_city["City"],
            "Value": int(highest_count_city["Restaurant Count"]),
        }
    ]

    if highest_rated_city is not None:
        summary.append(
            {
                "Analysis": "City with the Highest Average Rating",
                "City": highest_rated_city["City"],
                "Value": float(highest_rated_city["Average Rating"]),
            }
        )

    pd.DataFrame(summary).to_csv(
        OUTPUT_DIR / "city_analysis_summary.csv",
        index=False,
    )

    create_restaurant_count_chart(city_counts)
    if not city_ratings.empty:
        create_rating_chart(city_ratings)

    print("\nCITY WITH THE HIGHEST NUMBER OF RESTAURANTS")
    print(highest_count_city.to_string())

    print("\nTOP 10 CITIES BY NUMBER OF RESTAURANTS")
    print(city_counts.head(10).to_string(index=False))

    print("\nTOP 10 CITIES BY AVERAGE RATING")
    print(city_ratings.head(10).to_string(index=False))

    if highest_rated_city is not None:
        print("\nCITY WITH THE HIGHEST AVERAGE RATING")
        print(highest_rated_city.to_string())

    print("\nOUTPUT FILES SAVED TO:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()
