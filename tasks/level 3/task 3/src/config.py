from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
CHARTS_DIR = OUTPUT_DIR / "charts"
REPORTS_DIR = OUTPUT_DIR / "reports"

DATA_PATH = RAW_DATA_DIR / "Dataset .csv"
CLEANED_DATA_PATH = PROCESSED_DATA_DIR / "cleaned_restaurant_data.csv"
ONLINE_REPORT_PATH = REPORTS_DIR / "online_delivery_analysis.csv"
TABLE_REPORT_PATH = REPORTS_DIR / "table_booking_analysis.csv"
COMPARISON_REPORT_PATH = REPORTS_DIR / "service_comparison.csv"
STATISTICAL_REPORT_PATH = REPORTS_DIR / "statistical_tests.txt"
SUMMARY_REPORT_PATH = REPORTS_DIR / "final_summary.txt"


def create_directories():
    directories = [RAW_DATA_DIR, PROCESSED_DATA_DIR, CHARTS_DIR, REPORTS_DIR]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
