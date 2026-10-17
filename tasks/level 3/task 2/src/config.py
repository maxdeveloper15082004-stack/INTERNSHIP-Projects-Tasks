from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
CHARTS_DIR = OUTPUT_DIR / "charts"
REPORTS_DIR = OUTPUT_DIR / "reports"

DATA_PATH = RAW_DATA_DIR / "Dataset.csv"
CLEANED_DATA_PATH = PROCESSED_DATA_DIR / "cleaned_restaurant_votes.csv"

TOP_10_REPORT_PATH = REPORTS_DIR / "top_10_restaurants.csv"
BOTTOM_10_REPORT_PATH = REPORTS_DIR / "bottom_10_restaurants.csv"
CORRELATION_REPORT_PATH = REPORTS_DIR / "correlation_results.txt"
SUMMARY_REPORT_PATH = REPORTS_DIR / "votes_analysis_summary.txt"


def create_directories() -> None:
    for directory in (
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        CHARTS_DIR,
        REPORTS_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)
