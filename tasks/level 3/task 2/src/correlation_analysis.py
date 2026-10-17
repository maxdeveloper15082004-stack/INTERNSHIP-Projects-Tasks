import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

from .config import CHARTS_DIR, CORRELATION_REPORT_PATH


def _correlation_result(function, votes, ratings) -> tuple[float, float]:
    if len(votes) < 2 or votes.nunique() < 2 or ratings.nunique() < 2:
        return np.nan, np.nan
    result = function(votes, ratings)
    return float(result.statistic), float(result.pvalue)


def _describe_pearson(value: float) -> tuple[str, str]:
    if not np.isfinite(value):
        return "undefined", "undefined"
    direction = "positive" if value > 0 else "negative" if value < 0 else "no"
    magnitude = abs(value)
    strength = (
        "weak" if magnitude < 0.3 else "moderate" if magnitude < 0.7 else "strong"
    )
    if value == 0:
        strength = "no"
    return direction, strength


def _format_number(value: float, precision: int = 4) -> str:
    return f"{value:.{precision}f}" if np.isfinite(value) else "undefined"


def analyze_correlation(df):
    print("\n========== CORRELATION ANALYSIS ==========")
    votes = df["Votes"]
    ratings = df["Aggregate rating"]

    pearson_corr, pearson_p = _correlation_result(pearsonr, votes, ratings)
    spearman_corr, spearman_p = _correlation_result(spearmanr, votes, ratings)
    relationship, strength = _describe_pearson(pearson_corr)

    print(f"Pearson correlation: {_format_number(pearson_corr)}")
    print(f"Pearson p-value: {_format_number(pearson_p, 6)}")
    print(f"Spearman correlation: {_format_number(spearman_corr)}")
    print(f"Spearman p-value: {_format_number(spearman_p, 6)}")
    print(
        f"\nPearson correlation indicates a {relationship} linear relationship."
    )
    print(f"Approximate linear relationship strength: {strength}")

    if np.isfinite(pearson_p):
        significance = (
            "statistically significant"
            if pearson_p < 0.05
            else "not statistically significant"
        )
        print(
            f"The Pearson correlation is {significance} "
            "at the 5% level."
        )
    else:
        print("Pearson statistical significance is undefined for these data.")

    fig, axis = plt.subplots(figsize=(10, 6))
    sns.regplot(
        data=df,
        x="Votes",
        y="Aggregate rating",
        scatter_kws={"alpha": 0.35},
        line_kws={"linewidth": 2},
        ax=axis,
    )
    axis.set_title("Restaurant Votes vs Aggregate Rating")
    axis.set_xlabel("Number of Votes")
    axis.set_ylabel("Aggregate Rating")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "votes_vs_rating.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    lines = [
        "VOTES AND RATINGS CORRELATION ANALYSIS",
        "=" * 45,
        f"Restaurants analyzed: {len(df)}",
        f"Pearson correlation: {_format_number(pearson_corr)}",
        f"Pearson p-value: {_format_number(pearson_p, 6)}",
        f"Spearman correlation: {_format_number(spearman_corr)}",
        f"Spearman p-value: {_format_number(spearman_p, 6)}",
        f"Pearson relationship direction: {relationship}",
        f"Approximate Pearson strength: {strength}",
        "Correlation does not establish causation.",
    ]
    if np.isfinite(pearson_p):
        lines.append(
            f"Pearson statistically significant at 5%: "
            f"{'yes' if pearson_p < 0.05 else 'no'}"
        )
    else:
        lines.append("Pearson statistical significance at 5%: undefined")
    CORRELATION_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\nCorrelation report saved.")
    print("Correlation chart saved.")

    return {
        "pearson_correlation": pearson_corr,
        "pearson_p_value": pearson_p,
        "spearman_correlation": spearman_corr,
        "spearman_p_value": spearman_p,
    }
