import re
from typing import Optional

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize


def _english_stop_words() -> set[str]:
    try:
        return set(stopwords.words("english"))
    except LookupError:
        if not nltk.download("stopwords", quiet=True):
            raise RuntimeError(
                "NLTK stopwords are unavailable. Check network access or "
                "install the NLTK stopwords corpus manually."
            ) from None
        try:
            return set(stopwords.words("english"))
        except LookupError as exc:
            raise RuntimeError(
                "NLTK could not load its stopwords corpus after download."
            ) from exc


def clean_text(
    text: object,
    stop_words: Optional[set[str]] = None,
) -> str:
    if not isinstance(text, str):
        return ""

    if stop_words is None:
        stop_words = _english_stop_words()

    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = wordpunct_tokenize(text)
    meaningful_tokens = [
        token for token in tokens if token not in stop_words and len(token) > 2
    ]
    return " ".join(meaningful_tokens)


def preprocess_reviews(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = {"Review", "Rating"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Review data is missing required columns: {sorted(missing_columns)}"
        )

    result = df.copy()
    result["Review"] = result["Review"].fillna("").astype(str)
    result["Rating"] = pd.to_numeric(result["Rating"], errors="coerce")

    valid_rows = (
        result["Review"].str.strip().ne("")
        & result["Rating"].between(1, 5, inclusive="both")
    )
    excluded_count = int((~valid_rows).sum())
    result = result.loc[valid_rows].copy()

    if excluded_count:
        print(
            f"Excluded {excluded_count} review row(s) with blank text or "
            "ratings outside the valid 1-5 range."
        )

    if result.empty:
        return result.assign(
            Cleaned_Review=pd.Series(dtype="object"),
            Review_Length=pd.Series(dtype="int64"),
            Word_Count=pd.Series(dtype="int64"),
        )

    stop_words = _english_stop_words()
    result["Cleaned_Review"] = result["Review"].apply(
        lambda review: clean_text(review, stop_words)
    )
    result["Review_Length"] = result["Review"].str.len()
    result["Word_Count"] = result["Review"].str.split().str.len()
    return result
