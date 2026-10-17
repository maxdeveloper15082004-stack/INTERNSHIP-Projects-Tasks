from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    if "Price range" not in df.columns:
        raise ValueError("Required column 'Price range' was not found.")

    df["Price range"] = pd.to_numeric(df["Price range"], errors="coerce")
    return df


def analyze_price_ranges(df):
    total_restaurants = len(df)
    valid_prices = df["Price range"].dropna()

    if valid_prices.empty:
        raise ValueError("No valid values were found in the Price range column.")

    price_counts = (
        valid_prices.value_counts()
        .sort_index()
        .rename_axis("Price Range")
        .reset_index(name="Restaurant Count")
    )
    price_counts["Percentage (%)"] = (
        price_counts["Restaurant Count"] / total_restaurants * 100
    ).round(2)

    price_counts.to_csv(
        OUTPUT_DIR / "price_range_distribution.csv",
        index=False,
    )
    return price_counts, total_restaurants


def create_chart(price_counts):
    plt.figure(figsize=(9, 6))
    bars = plt.bar(
        price_counts["Price Range"].astype(str),
        price_counts["Restaurant Count"],
    )
    plt.bar_label(
        bars,
        labels=[
            f"{count}\n({percentage:.2f}%)"
            for count, percentage in zip(
                price_counts["Restaurant Count"],
                price_counts["Percentage (%)"],
            )
        ],
        padding=4,
    )
    plt.title("Restaurant Price Range Distribution")
    plt.xlabel("Price Range Category")
    plt.ylabel("Number of Restaurants")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "price_range_distribution.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    price_counts, total_restaurants = analyze_price_ranges(df)
    create_chart(price_counts)

    print("\nRESTAURANT PRICE RANGE DISTRIBUTION\n")
    print(price_counts.to_string(index=False))
    print(f"\nTotal restaurant records: {total_restaurants}")
    print(
        "Records with missing or invalid price ranges: "
        f"{total_restaurants - df['Price range'].notna().sum()}"
    )
    print("\nOUTPUT FILES")
    print(OUTPUT_DIR / "price_range_distribution.csv")
    print(OUTPUT_DIR / "price_range_distribution.png")


if __name__ == "__main__":
    main()
