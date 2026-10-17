import os

REPORT_DIR = "outputs/reports"


def save_reports(
    chains,
    top_chains,
    highest_rated,
    most_popular,
    total_restaurants
):
    os.makedirs(REPORT_DIR, exist_ok=True)

    chains.to_csv(
        f"{REPORT_DIR}/restaurant_chain_analysis.csv",
        index=False
    )

    top_chains.to_csv(
        f"{REPORT_DIR}/top_restaurant_chains.csv",
        index=False
    )

    report_path = f"{REPORT_DIR}/restaurant_chain_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("RESTAURANT CHAIN ANALYSIS REPORT\n")
        file.write("=" * 45 + "\n\n")

        file.write(
            f"Total restaurant records analyzed: {total_restaurants}\n"
        )

        file.write(
            f"Potential restaurant chains identified: {len(chains)}\n\n"
        )

        file.write("TOP 10 CHAINS BY NUMBER OF OUTLETS\n")
        file.write("-" * 45 + "\n")

        if top_chains.empty:
            file.write("No potential chains found.\n")
        else:
            file.write(
                top_chains[
                    ["Restaurant Name", "outlet_count"]
                ].to_string(index=False)
            )
            file.write("\n\n")

        file.write("TOP 10 CHAINS BY AVERAGE RATING\n")
        file.write("-" * 45 + "\n")

        if highest_rated.empty:
            file.write("No chains meet the rating comparison requirement.\n")
        else:
            file.write(
                highest_rated[
                    [
                        "Restaurant Name",
                        "average_rating",
                        "rated_outlets"
                    ]
                ].head(10).to_string(index=False)
            )
            file.write("\n\n")

        file.write("TOP 10 CHAINS BY TOTAL VOTES\n")
        file.write("-" * 45 + "\n")

        if most_popular.empty:
            file.write("No potential chains found.\n")
        else:
            file.write(
                most_popular[
                    [
                        "Restaurant Name",
                        "total_votes",
                        "outlet_count"
                    ]
                ].head(10).to_string(index=False)
            )
            file.write("\n")

    print("\nReports saved successfully.")
