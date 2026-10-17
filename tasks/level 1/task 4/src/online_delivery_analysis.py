from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "Has Online delivery",
        "Aggregate rating"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Required column '{column}' was not found."
            )

    df["Has Online delivery"] = (
        df["Has Online delivery"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    df["Aggregate rating"] = pd.to_numeric(
        df["Aggregate rating"],
        errors="coerce"
    )

    return df


def analyze_online_delivery(df):
    total_restaurants = len(df)

    delivery_data = df[
        df["Has Online delivery"].isin(["yes", "no"])
    ].copy()

    if delivery_data.empty:
        raise ValueError(
            "No valid Yes/No values were found in "
            "'Has Online delivery'."
        )

    delivery_counts = (
        delivery_data["Has Online delivery"]
        .value_counts()
        .reindex(["yes", "no"], fill_value=0)
    )

    valid_delivery_records = len(delivery_data)

    delivery_summary = pd.DataFrame({
        "Online Delivery": ["Yes", "No"],
        "Restaurant Count": [
            delivery_counts["yes"],
            delivery_counts["no"]
        ]
    })

    delivery_summary["Percentage (%)"] = (
        delivery_summary["Restaurant Count"]
        / valid_delivery_records
        * 100
    ).round(2)

    delivery_summary.to_csv(
        OUTPUT_DIR / "online_delivery_percentage.csv",
        index=False
    )

    average_ratings = (
        delivery_data
        .groupby("Has Online delivery")["Aggregate rating"]
        .mean()
        .reindex(["yes", "no"])
    )

    rating_summary = pd.DataFrame({
        "Online Delivery": ["Yes", "No"],
        "Average Rating": [
            average_ratings["yes"],
            average_ratings["no"]
        ]
    })

    rating_summary["Average Rating"] = (
        rating_summary["Average Rating"].round(2)
    )

    rating_summary.to_csv(
        OUTPUT_DIR / "online_delivery_rating_comparison.csv",
        index=False
    )

    return (
        delivery_summary,
        rating_summary,
        total_restaurants,
        valid_delivery_records
    )


def create_delivery_chart(delivery_summary):
    plt.figure(figsize=(8, 6))

    bars = plt.bar(
        delivery_summary["Online Delivery"],
        delivery_summary["Percentage (%)"]
    )

    plt.bar_label(
        bars,
        labels=[
            f"{percentage:.2f}%"
            for percentage in delivery_summary["Percentage (%)"]
        ],
        padding=4
    )

    plt.title("Percentage of Restaurants Offering Online Delivery")
    plt.xlabel("Online Delivery")
    plt.ylabel("Restaurants (%)")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "online_delivery_percentage.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def create_rating_chart(rating_summary):
    plt.figure(figsize=(8, 6))

    bars = plt.bar(
        rating_summary["Online Delivery"],
        rating_summary["Average Rating"]
    )

    plt.bar_label(
        bars,
        labels=[
            f"{rating:.2f}" if pd.notna(rating) else "No rating data"
            for rating in rating_summary["Average Rating"]
        ],
        padding=4
    )

    plt.title("Average Rating: Online Delivery vs No Online Delivery")
    plt.xlabel("Online Delivery")
    plt.ylabel("Average Restaurant Rating")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "online_delivery_rating_comparison.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()

    (
        delivery_summary,
        rating_summary,
        total_restaurants,
        valid_delivery_records
    ) = analyze_online_delivery(df)

    create_delivery_chart(delivery_summary)
    create_rating_chart(rating_summary)

    print("\nONLINE DELIVERY ANALYSIS")
    print("=" * 45)

    print(f"Total restaurant records: {total_restaurants}")
    print(
        "Records with valid online delivery status: "
        f"{valid_delivery_records}"
    )

    print("\n1. ONLINE DELIVERY PERCENTAGE")
    print(delivery_summary.to_string(index=False))

    print("\n2. AVERAGE RATING COMPARISON")
    print(rating_summary.to_string(index=False))

    print("\n3. RATING COMPARISON RESULT")

    yes_rating = rating_summary.loc[
        rating_summary["Online Delivery"] == "Yes",
        "Average Rating"
    ].iloc[0]

    no_rating = rating_summary.loc[
        rating_summary["Online Delivery"] == "No",
        "Average Rating"
    ].iloc[0]

    if pd.isna(yes_rating) or pd.isna(no_rating):
        print("Insufficient rating data to compare both groups.")
    elif yes_rating > no_rating:
        print("Restaurants offering online delivery have a higher average rating.")
    elif no_rating > yes_rating:
        print("Restaurants without online delivery have a higher average rating.")
    else:
        print("Both groups have the same average rating.")

    print("\n4. OUTPUT FILES")
    print(OUTPUT_DIR / "online_delivery_percentage.csv")
    print(OUTPUT_DIR / "online_delivery_rating_comparison.csv")
    print(OUTPUT_DIR / "online_delivery_percentage.png")
    print(OUTPUT_DIR / "online_delivery_rating_comparison.png")


if __name__ == "__main__":
    main()
