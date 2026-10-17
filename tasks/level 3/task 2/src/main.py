import sys
from pathlib import Path

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.config import SUMMARY_REPORT_PATH, create_directories
    from src.correlation_analysis import analyze_correlation
    from src.data_cleaning import clean_data
    from src.data_loader import load_data
    from src.votes_analysis import analyze_votes
else:
    from .config import SUMMARY_REPORT_PATH, create_directories
    from .correlation_analysis import analyze_correlation
    from .data_cleaning import clean_data
    from .data_loader import load_data
    from .votes_analysis import analyze_votes


def main() -> None:
    create_directories()
    print("=" * 60)
    print("COGNIFYZ LEVEL 3 - TASK 2")
    print("RESTAURANT VOTES ANALYSIS")
    print("=" * 60)

    df = clean_data(load_data())
    if df.empty:
        raise ValueError("No valid restaurant records are available to analyze.")

    top_10, bottom_10 = analyze_votes(df)
    correlation_results = analyze_correlation(df)
    most_voted = df["Votes"].max()
    least_voted = df["Votes"].min()

    summary = [
        "RESTAURANT VOTES ANALYSIS SUMMARY",
        "=" * 40,
        f"Total restaurants analyzed: {len(df)}",
        f"Highest votes: {most_voted}",
        f"Lowest votes: {least_voted}",
        f"Average votes: {df['Votes'].mean():.2f}",
        f"Average rating: {df['Aggregate rating'].mean():.2f}",
        (
            "Pearson correlation: "
            f"{correlation_results['pearson_correlation']:.4f}"
            if np.isfinite(correlation_results["pearson_correlation"])
            else "Pearson correlation: undefined"
        ),
        (
            "Spearman correlation: "
            f"{correlation_results['spearman_correlation']:.4f}"
            if np.isfinite(correlation_results["spearman_correlation"])
            else "Spearman correlation: undefined"
        ),
        "",
        "TOP 10 RESTAURANTS",
        top_10[
            ["Restaurant Name", "Votes", "Aggregate rating"]
        ].to_string(index=False),
        "",
        "BOTTOM 10 RESTAURANTS",
        bottom_10[
            ["Restaurant Name", "Votes", "Aggregate rating"]
        ].to_string(index=False),
    ]
    SUMMARY_REPORT_PATH.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print("\n" + "=" * 60)
    print("TASK 2 ANALYSIS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nCheck the outputs folder for charts and reports.")


if __name__ == "__main__":
    main()
