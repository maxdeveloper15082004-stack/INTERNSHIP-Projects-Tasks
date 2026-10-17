import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.config import (
        ANALYSIS_DATA_PATH,
        CLEANED_REVIEWS_PATH,
        REVIEWS_DATA_PATH,
        create_directories,
    )
    from src.data_loader import (
        inspect_restaurant_data,
        load_restaurant_data,
        load_review_data,
    )
    from src.keyword_analysis import analyze_keywords
    from src.review_length_analysis import analyze_review_length
    from src.text_preprocessing import preprocess_reviews
else:
    from .config import (
        ANALYSIS_DATA_PATH,
        CLEANED_REVIEWS_PATH,
        REVIEWS_DATA_PATH,
        create_directories,
    )
    from .data_loader import (
        inspect_restaurant_data,
        load_restaurant_data,
        load_review_data,
    )
    from .keyword_analysis import analyze_keywords
    from .review_length_analysis import analyze_review_length
    from .text_preprocessing import preprocess_reviews


def main() -> None:
    create_directories()
    print("=" * 60)
    print("COGNIFYZ LEVEL 3 - RESTAURANT REVIEWS ANALYSIS")
    print("=" * 60)

    restaurant_df = load_restaurant_data()
    inspect_restaurant_data(restaurant_df)

    if not REVIEWS_DATA_PATH.exists():
        print(
            "\nThe restaurant metadata has no customer review text, and "
            "the separate review dataset is not available."
        )
        print(
            "Add data/raw/restaurant_reviews.csv with actual 'Review' and "
            "'Rating' columns to run keyword and review-length analysis."
        )
        return

    reviews_df = load_review_data()
    cleaned_df = preprocess_reviews(reviews_df)
    if cleaned_df.empty:
        raise ValueError(
            "No valid reviews remain after checking review text and 1-5 ratings."
        )

    cleaned_df.to_csv(CLEANED_REVIEWS_PATH, index=False)
    cleaned_df.to_csv(ANALYSIS_DATA_PATH, index=False)
    print(f"\nCleaned reviews saved to: {CLEANED_REVIEWS_PATH}")

    analyze_keywords(cleaned_df)
    analyze_review_length(cleaned_df)
    print("\nAnalysis completed successfully!")


if __name__ == "__main__":
    main()
