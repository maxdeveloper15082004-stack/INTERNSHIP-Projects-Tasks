import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import create_directories, SUMMARY_REPORT_PATH
from data_loader import load_data
from data_cleaning import clean_data
from price_analysis import analyze_price_range
from statistical_analysis import analyze_service_associations


def main():
    create_directories()

    print("=" * 60)
    print("COGNIFYZ LEVEL 3 - TASK 3")
    print("PRICE RANGE VS ONLINE DELIVERY AND TABLE BOOKING")
    print("=" * 60)

    df = load_data()
    df = clean_data(df)

    if df.empty:
        print("No valid records remain after cleaning.")
        return

    comparison = analyze_price_range(df)
    statistical_results = analyze_service_associations(df)

    online_increases = (
        comparison["Online_Delivery_Percentage"].iloc[-1]
        > comparison["Online_Delivery_Percentage"].iloc[0]
    )
    table_increases = (
        comparison["Table_Booking_Percentage"].iloc[-1]
        > comparison["Table_Booking_Percentage"].iloc[0]
    )

    with open(SUMMARY_REPORT_PATH, "w", encoding="utf-8") as file:
        file.write("PRICE RANGE AND SERVICE AVAILABILITY ANALYSIS\n")
        file.write("=" * 50 + "\n\n")
        file.write(f"Total restaurants analyzed: {len(df)}\n\n")
        file.write("SERVICE AVAILABILITY BY PRICE RANGE\n")
        file.write(comparison.to_string(index=False))
        file.write("\n\n")
        file.write(
            "Online delivery percentage at lowest price range: "
            f"{comparison['Online_Delivery_Percentage'].iloc[0]:.2f}%\n"
        )
        file.write(
            "Online delivery percentage at highest price range: "
            f"{comparison['Online_Delivery_Percentage'].iloc[-1]:.2f}%\n"
        )
        file.write(
            "Table booking percentage at lowest price range: "
            f"{comparison['Table_Booking_Percentage'].iloc[0]:.2f}%\n"
        )
        file.write(
            "Table booking percentage at highest price range: "
            f"{comparison['Table_Booking_Percentage'].iloc[-1]:.2f}%\n\n"
        )
        file.write(
            "Does online delivery increase from the lowest "
            f"to highest price category? {online_increases}\n"
        )
        file.write(
            "Does table booking increase from the lowest "
            f"to highest price category? {table_increases}\n\n"
        )

        for result in statistical_results:
            file.write(f"{result['service']}: p-value = {result['p_value']:.6g}\n")
            file.write(f"{result['conclusion']}\n\n")

    print("\n" + "=" * 60)
    print("TASK 3 ANALYSIS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nCharts saved in outputs/charts/")
    print("Reports saved in outputs/reports/")


if __name__ == "__main__":
    main()
