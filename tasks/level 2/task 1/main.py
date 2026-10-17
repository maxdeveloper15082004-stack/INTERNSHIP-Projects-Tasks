from pathlib import Path

from src.analysis import analyze_ratings
from src.data_loader import load_data
from src.visualization import create_visualizations


PROJECT_ROOT = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"


def save_report(results: dict[str, object]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "restaurant_ratings_report.txt"

    with report_path.open("w", encoding="utf-8") as file:
        file.write("RESTAURANT RATINGS ANALYSIS REPORT\n")
        file.write("=" * 40 + "\n\n")
        file.write(
            f"Total restaurants analyzed: "
            f"{results['total_restaurants']}\n"
        )
        file.write(
            f"Average votes per restaurant: "
            f"{results['average_votes']:.2f}\n\n"
        )
        file.write("RATING DISTRIBUTION\n")
        file.write("-" * 40 + "\n")
        for rating, count in results["rating_distribution"].items():
            file.write(f"Rating {rating}: {count} restaurants\n")

        file.write("\nRATING RANGE DISTRIBUTION\n")
        file.write("-" * 40 + "\n")
        for rating_range, count in results["range_distribution"].items():
            percentage = results["rating_percentages"][rating_range]
            file.write(
                f"{rating_range}: {count} restaurants "
                f"({percentage:.2f}%)\n"
            )

        file.write("\nKEY FINDING\n")
        file.write("-" * 40 + "\n")
        file.write(f"Most common rating range: {results['most_common_range']}\n")
        file.write(
            f"Restaurants in this range: "
            f"{results['most_common_range_count']}\n"
        )

    print(f"\nReport saved to: {report_path}")


def main() -> None:
    print("=" * 50)
    print("RESTAURANT RATINGS ANALYSIS")
    print("=" * 50)

    df = load_data()
    print(f"\nTotal valid restaurants: {len(df)}")
    results = analyze_ratings(df)

    print("\n1. AGGREGATE RATING DISTRIBUTION")
    print("-" * 40)
    print(results["rating_distribution"].to_string())

    print("\n2. RATING RANGE DISTRIBUTION")
    print("-" * 40)
    for rating_range, count in results["range_distribution"].items():
        percentage = results["rating_percentages"][rating_range]
        print(f"{rating_range}: {count} restaurants ({percentage:.2f}%)")

    print("\n3. MOST COMMON RATING RANGE")
    print("-" * 40)
    print(f"Rating range: {results['most_common_range']}")
    print(f"Number of restaurants: {results['most_common_range_count']}")

    print("\n4. AVERAGE NUMBER OF VOTES")
    print("-" * 40)
    print(f"{results['average_votes']:.2f}")

    create_visualizations(df, results)
    save_report(results)
    print("\nAnalysis completed successfully!")


if __name__ == "__main__":
    main()