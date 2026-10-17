from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
CHARTS_DIR = OUTPUT_DIR / "charts"
REPORTS_DIR = OUTPUT_DIR / "reports"

RESTAURANT_DATA_PATH = RAW_DATA_DIR / "Dataset.csv"
REVIEWS_DATA_PATH = RAW_DATA_DIR / "restaurant_reviews.csv"

CLEANED_REVIEWS_PATH = PROCESSED_DATA_DIR / "cleaned_reviews.csv"
ANALYSIS_DATA_PATH = OUTPUT_DIR / "restaurant_reviews_analysis.csv"

TOP_KEYWORDS = 15

KEYWORD_ANALYSIS_PATH = REPORTS_DIR / "keyword_analysis.csv"
RATING_ANALYSIS_PATH = REPORTS_DIR / "rating_length_analysis.csv"
SUMMARY_PATH = REPORTS_DIR / "summary.txt"


def create_directories() -> None:
    for directory in (
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        CHARTS_DIR,
        REPORTS_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)
