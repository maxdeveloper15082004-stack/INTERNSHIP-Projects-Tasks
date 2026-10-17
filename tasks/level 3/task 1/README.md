# Restaurant Reviews Analysis - Cognifyz Level 3

## Project overview

This project analyzes actual restaurant customer reviews. It identifies words
that occur frequently in high- and low-rated reviews, measures review length,
compares length across rating groups, and calculates Pearson and Spearman
correlations between word count and rating.

The supplied restaurant metadata includes aggregate ratings and rating
categories, but no customer review text. Metadata ratings are not treated as
reviews. The keyword and length analysis runs only when a separate review-text
file is present.

## Dataset requirements

Place the restaurant metadata CSV at `data/raw/Dataset.csv`. It must
include `Restaurant Name`, `Aggregate rating`, and `Rating text`.

To run the complete analysis, add `data/raw/restaurant_reviews.csv` with:

| Column | Description |
| --- | --- |
| `Review` | Actual customer review text |
| `Rating` | Numeric customer rating on a 1–5 scale |

The metadata file available for this task contains no review text, so no
keywords or review-length statistics can honestly be reported until the
separate review dataset is supplied. Example reviews should not be presented
as genuine customer data.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The first text-analysis run may download NLTK's English stopwords corpus.
Metadata inspection does not require that corpus.

## Run

From the project root:

```powershell
python src/main.py
```

The program inspects restaurant metadata first. If review text is missing, it
explains which file and columns are needed and exits without inventing
analysis. With a valid review dataset, it generates:

- `data/processed/cleaned_reviews.csv`
- `outputs/restaurant_reviews_analysis.csv`
- `outputs/charts/positive_keywords.png`
- `outputs/charts/negative_keywords.png`
- `outputs/charts/review_length_distribution.png`
- `outputs/charts/review_length_vs_rating.png`
- `outputs/reports/keyword_analysis.csv`
- `outputs/reports/rating_length_analysis.csv`
- `outputs/reports/summary.txt`

## Analysis details

- Reviews rated 4 or 5 are grouped as positive; reviews rated 1 or 2 are
  grouped as negative.
- Rating groups for length comparisons are Low (rating <= 2), Medium
  (2 < rating < 4), and High (rating >= 4).
- Character and word counts use the original review text; keyword counts use
  lowercased, URL/punctuation-stripped text with English stopwords removed.
- Pearson correlation measures linear association; Spearman correlation
  measures monotonic association. Neither indicates that review length causes
  a rating. Statistical tests may be undefined when the data does not vary
  enough.
- Frequent words are associations with a rating group, not proof that a word
  is inherently positive or negative. Negation and context are not modeled.

## Technologies

Python, Pandas, NumPy, Matplotlib, Seaborn, NLTK, and SciPy.
