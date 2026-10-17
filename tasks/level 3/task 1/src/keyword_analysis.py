from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd

from .config import (
    CHARTS_DIR,
    KEYWORD_ANALYSIS_PATH,
    TOP_KEYWORDS,
)


def get_keyword_frequencies(
    df: pd.DataFrame,
    rating_type: str,
) -> Counter[str]:
    if rating_type == "positive":
        filtered = df.loc[df["Rating"] >= 4]
    elif rating_type == "negative":
        filtered = df.loc[df["Rating"] <= 2]
    else:
        raise ValueError("rating_type must be 'positive' or 'negative'")

    words = (
        word
        for review in filtered["Cleaned_Review"].dropna()
        for word in review.split()
    )
    return Counter(words)


def plot_keyword_frequencies(
    counter: Counter[str],
    title: str,
    filename: str,
) -> None:
    common_words = counter.most_common(TOP_KEYWORDS)
    figure, axis = plt.subplots(figsize=(11, 6))

    if common_words:
        keywords, frequencies = zip(*common_words)
        axis.barh(list(keywords)[::-1], list(frequencies)[::-1])
        axis.set_xlabel("Frequency")
        axis.set_ylabel("Keyword")
    else:
        axis.text(
            0.5,
            0.5,
            "No reviews in this rating group",
            ha="center",
            va="center",
            transform=axis.transAxes,
        )
        axis.set_axis_off()

    axis.set_title(title)
    figure.tight_layout()
    figure.savefig(CHARTS_DIR / filename, dpi=300)
    plt.close(figure)


def analyze_keywords(df: pd.DataFrame) -> pd.DataFrame:
    positive_words = get_keyword_frequencies(df, "positive")
    negative_words = get_keyword_frequencies(df, "negative")

    positive_df = pd.DataFrame(
        positive_words.most_common(TOP_KEYWORDS),
        columns=["Keyword", "Frequency"],
    )
    positive_df["Sentiment_Group"] = "Positive"

    negative_df = pd.DataFrame(
        negative_words.most_common(TOP_KEYWORDS),
        columns=["Keyword", "Frequency"],
    )
    negative_df["Sentiment_Group"] = "Negative"

    combined_df = pd.concat([positive_df, negative_df], ignore_index=True)
    combined_df.to_csv(KEYWORD_ANALYSIS_PATH, index=False)

    plot_keyword_frequencies(
        positive_words,
        "Most Common Words in High-Rated Reviews",
        "positive_keywords.png",
    )
    plot_keyword_frequencies(
        negative_words,
        "Most Common Words in Low-Rated Reviews",
        "negative_keywords.png",
    )

    print("\n========== POSITIVE KEYWORDS ==========")
    for word, frequency in positive_words.most_common(TOP_KEYWORDS):
        print(f"{word}: {frequency}")

    print("\n========== NEGATIVE KEYWORDS ==========")
    for word, frequency in negative_words.most_common(TOP_KEYWORDS):
        print(f"{word}: {frequency}")

    return combined_df
