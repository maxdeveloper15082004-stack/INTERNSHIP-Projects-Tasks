from pathlib import Path

from src.analysis import analyze_cuisine_combinations
from src.data_loader import load_data
from src.preprocessing import clean_cuisine_names
from src.visualization import create_visualizations

PROJECT_ROOT = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"


def save_results(results: dict[str, object]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    frequency_path = REPORTS_DIR / "cuisine_combination_frequency.csv"
    ratings_path = REPORTS_DIR / "cuisine_combination_ratings.csv"
    report_path = REPORTS_DIR / "cuisine_combination_report.txt"

    results["combination_frequency"].to_csv(frequency_path, index=False)
    results["combination_ratings"].to_csv(ratings_path, index=False)

    with report_path.open("w", encoding="utf-8") as report:
        report.write("CUISINE COMBINATION ANALYSIS REPORT\n")
        report.write("=" * 45 + "\n\n")
        report.write(f"Total restaurants analyzed: {results['total_restaurants']}\n")
        report.write(
            "Overall average restaurant rating: "
            f"{results['overall_average_rating']:.2f}\n\n"
        )

        report.write("TOP 10 MOST COMMON CUISINE COMBINATIONS\n")
        report.write("-" * 45 + "\n")
        report.write(results["combination_frequency"].head(10).to_string(index=False))

        report.write("\n\nTOP 10 HIGHEST-RATED COMBINATIONS\n")
        report.write(
            f"(At least {results['minimum_restaurants']} restaurants)\n"
        )
        report.write("-" * 45 + "\n")
        if not results["reliable_combinations"].empty:
            report.write(results["reliable_combinations"].head(10).to_string(index=False))
        else:
            report.write("No combinations met the minimum restaurant count.\n")

        report.write("\n\nTOP 10 INDIVIDUAL CUISINES\n")
        report.write("-" * 45 + "\n")
        report.write(results["individual_cuisines"].head(10).to_string(index=False))

        common = results["most_common_combination"]
        report.write("\n\nKEY FINDINGS\n")
        report.write("-" * 45 + "\n")
        report.write(f"Most common combination: {common['Cuisine Combination']}\n")
        report.write(f"Restaurant count: {common['Restaurant Count']}\n")

        highest = results["highest_rated_combination"]
        if highest is not None:
            report.write(
                "Highest-rated combination with sufficient data: "
                f"{highest['Cuisine Combination']}\n"
            )
            report.write(f"Average rating: {highest['Average Rating']:.2f}\n")
            report.write(f"Restaurant count: {highest['Restaurant Count']}\n")
            report.write(
                f"Overall average rating: {results['overall_average_rating']:.2f}\n"
            )
            report.write(
                "This is a descriptive comparison, not evidence that cuisine "
                "causes higher ratings.\n"
            )
        else:
            report.write(
                "No cuisine combination met the minimum restaurant count "
                "for the higher-rating comparison.\n"
            )

    print(f"\nFrequency results saved to: {frequency_path}")
    print(f"Rating results saved to: {ratings_path}")
    print(f"Report saved to: {report_path}")


def main() -> None:
    print("=" * 55)
    print("CUISINE COMBINATION ANALYSIS")
    print("=" * 55)

    df = clean_cuisine_names(load_data())
    if df.empty:
        raise ValueError("No restaurant records have usable cuisine names.")
    print(f"\nLoaded and prepared {len(df)} valid restaurant records.")

    results = analyze_cuisine_combinations(df)

    sections = [
        ("1. TOP 10 MOST COMMON CUISINE COMBINATIONS", "combination_frequency"),
        ("2. TOP 10 INDIVIDUAL CUISINES", "individual_cuisines"),
    ]
    for title, key in sections:
        print(f"\n{title}\n{'-' * 55}")
        print(results[key].head(10).to_string(index=False))

    print("\n3. TOP 10 HIGHEST-RATED COMBINATIONS")
    print(f"(At least {results['minimum_restaurants']} restaurants)")
    print("-" * 55)
    if results["reliable_combinations"].empty:
        print("No combinations meet the minimum restaurant count.")
    else:
        print(results["reliable_combinations"].head(10).to_string(index=False))

    print("\n4. OVERALL AVERAGE RESTAURANT RATING\n" + "-" * 55)
    print(f"{results['overall_average_rating']:.2f}")

    common = results["most_common_combination"]
    print("\n5. MOST COMMON CUISINE COMBINATION\n" + "-" * 55)
    print(f"Combination: {common['Cuisine Combination']}")
    print(f"Restaurant count: {common['Restaurant Count']}")

    highest = results["highest_rated_combination"]
    print("\n6. HIGHEST-RATED COMBINATION WITH SUFFICIENT DATA\n" + "-" * 55)
    if highest is None:
        print("No combination met the minimum restaurant count.")
    else:
        print(f"Combination: {highest['Cuisine Combination']}")
        print(f"Average rating: {highest['Average Rating']:.2f}")
        print(f"Restaurant count: {highest['Restaurant Count']}")

    create_visualizations(results)
    save_results(results)
    print("\nAnalysis completed successfully!")


if __name__ == "__main__":
    main()
