import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from src import keyword_analysis, review_length_analysis, text_preprocessing


class TextPreprocessingTests(unittest.TestCase):
    def test_clean_text_removes_urls_punctuation_numbers_and_stopwords(self):
        cleaned = text_preprocessing.clean_text(
            "The food was delicious! Visit https://example.com 123.",
            {"the", "was"},
        )

        self.assertEqual(cleaned, "food delicious visit")

    def test_preprocess_keeps_original_length_and_valid_empty_tokens(self):
        reviews = pd.DataFrame(
            {
                "Review": ["The food is warm.", "the and is", "  ", "Too low"],
                "Rating": [5, 3, 4, 0],
            }
        )

        with patch.object(
            text_preprocessing,
            "_english_stop_words",
            return_value={"the", "is", "and"},
        ):
            result = text_preprocessing.preprocess_reviews(reviews)

        self.assertEqual(len(result), 2)
        self.assertEqual(result["Review_Length"].tolist(), [17, 10])
        self.assertEqual(result["Word_Count"].tolist(), [4, 3])
        self.assertEqual(result["Cleaned_Review"].tolist(), ["food warm", ""])


class KeywordAnalysisTests(unittest.TestCase):
    def test_keywords_use_expected_rating_cutoffs(self):
        reviews = pd.DataFrame(
            {
                "Rating": [5, 4, 3, 2, 1],
                "Cleaned_Review": [
                    "delicious food",
                    "delicious tasty",
                    "neutral word",
                    "slow awful",
                    "slow awful",
                ],
            }
        )

        positive = keyword_analysis.get_keyword_frequencies(reviews, "positive")
        negative = keyword_analysis.get_keyword_frequencies(reviews, "negative")

        self.assertEqual(positive["delicious"], 2)
        self.assertNotIn("neutral", positive)
        self.assertEqual(negative["slow"], 2)
        self.assertNotIn("neutral", negative)


class ReviewLengthAnalysisTests(unittest.TestCase):
    def test_writes_rating_groups_charts_and_summary(self):
        reviews = pd.DataFrame(
            {
                "Review": [
                    "one two",
                    "one two three",
                    "one two three four five",
                    "one two three four five six seven",
                ],
                "Rating": [1, 3, 4, 5],
                "Review_Length": [7, 13, 23, 33],
                "Word_Count": [2, 3, 5, 7],
            }
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            charts_path = temporary_path / "charts"
            reports_path = temporary_path / "reports"
            charts_path.mkdir()
            reports_path.mkdir()

            with patch.object(
                review_length_analysis,
                "CHARTS_DIR",
                charts_path,
            ):
                with patch.object(
                    review_length_analysis,
                    "RATING_ANALYSIS_PATH",
                    reports_path / "rating_length_analysis.csv",
                ):
                    with patch.object(
                        review_length_analysis,
                        "SUMMARY_PATH",
                        reports_path / "summary.txt",
                    ):
                        rating_analysis, correlations = (
                            review_length_analysis.analyze_review_length(reviews)
                        )

            self.assertEqual(
                rating_analysis["Rating_Group"].tolist(),
                ["Low", "Medium", "High"],
            )
            self.assertEqual(
                rating_analysis["Review_Count"].tolist(),
                [1, 1, 2],
            )
            self.assertGreater(correlations.loc["Word_Count", "Rating"], 0)
            self.assertTrue(
                (charts_path / "review_length_distribution.png").exists()
            )
            self.assertTrue(
                (charts_path / "review_length_vs_rating.png").exists()
            )
            self.assertTrue(
                (reports_path / "rating_length_analysis.csv").exists()
            )
            self.assertTrue((reports_path / "summary.txt").exists())


if __name__ == "__main__":
    unittest.main()
