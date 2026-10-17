from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Dataset .csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def main():
    
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Place your CSV file inside the data/raw folder."
        )
        
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    if "Cuisines" not in df.columns:
        raise ValueError("Cuisines column not found in dataset.")

    total_restaurants = len(df)

    cuisines = (
        df["Cuisines"].dropna().astype(str).str.split(",").explode().str.strip()
    )

    cuisines = cuisines[cuisines != ""]

    cuisine_counts = cuisines.value_counts()

    top_three = (
        cuisine_counts.head(3).rename_axis("Cuisine").reset_index(name="Restaurant Count")
    )

    top_three["Percentage (%)"] = (
        top_three["Restaurant Count"]
        / total_restaurants
        * 100
    ).round(2)

    results_path = OUTPUT_DIR / "top_3_cuisines.csv"
    top_three.to_csv(results_path, index=False)

    plt.figure(figsize=(9, 5))

    bars = plt.bar(
        top_three["Cuisine"],
        top_three["Restaurant Count"]
    )

    plt.title("Top 3 Most Common Cuisines")
    plt.xlabel("Cuisine")
    plt.ylabel("Number of Restaurants")
    plt.bar_label(bars, padding=3)
    plt.tight_layout()

    chart_path = OUTPUT_DIR / "top_3_cuisines.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()

    print("\nTop 3 Most Common Cuisines\n")
    print(top_three.to_string(index=False))
    print(f"\nTotal restaurant records: {total_restaurants}")
    print(f"Results saved to: {results_path}")
    print(f"Chart saved to: {chart_path}")


if __name__ == "__main__":
    main()