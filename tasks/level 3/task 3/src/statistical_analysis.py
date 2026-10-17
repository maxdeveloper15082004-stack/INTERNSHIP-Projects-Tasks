import pandas as pd
from scipy.stats import chi2_contingency

from config import STATISTICAL_REPORT_PATH


def perform_chi_square_test(df, service_column):
    contingency_table = pd.crosstab(df["Price range"], df[service_column])

    chi2, p_value, degrees_of_freedom, expected = chi2_contingency(
        contingency_table
    )

    expected_df = pd.DataFrame(
        expected,
        index=contingency_table.index,
        columns=contingency_table.columns,
    )

    assumptions_met = (expected_df >= 5).all().all()

    if p_value < 0.05:
        conclusion = (
            "There is a statistically significant association "
            "between price range and service availability."
        )
    else:
        conclusion = (
            "There is insufficient statistical evidence of an "
            "association between price range and service availability."
        )

    return {
        "service": service_column,
        "chi_square": chi2,
        "p_value": p_value,
        "degrees_of_freedom": degrees_of_freedom,
        "conclusion": conclusion,
        "expected_counts_at_least_5": assumptions_met,
        "contingency_table": contingency_table,
    }


def analyze_service_associations(df):
    online_results = perform_chi_square_test(df, "Has Online delivery")
    table_results = perform_chi_square_test(df, "Has Table booking")

    results = [online_results, table_results]

    with open(STATISTICAL_REPORT_PATH, "w", encoding="utf-8") as file:
        file.write("CHI-SQUARE TEST RESULTS\n")
        file.write("=" * 45 + "\n\n")

        for result in results:
            file.write(f"Service: {result['service']}\n")
            file.write(f"Chi-square statistic: {result['chi_square']:.4f}\n")
            file.write(f"P-value: {result['p_value']:.6g}\n")
            file.write(
                f"Degrees of freedom: {result['degrees_of_freedom']}\n"
            )
            file.write(
                f"All expected cell counts >= 5: {result['expected_counts_at_least_5']}\n"
            )
            file.write(f"Conclusion: {result['conclusion']}\n\n")

    print("\n========== STATISTICAL TESTS ==========")

    for result in results:
        print(f"\nService: {result['service']}")
        print(f"Chi-square statistic: {result['chi_square']:.4f}")
        print(f"P-value: {result['p_value']:.6g}")
        print(f"Conclusion: {result['conclusion']}")

        if not result["expected_counts_at_least_5"]:
            print(
                "Warning: Some expected cell counts are below 5. "
                "Consider an appropriate alternative or combining "
                "categories if substantively justified."
            )

    return results
