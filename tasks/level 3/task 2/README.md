# Restaurant Votes Analysis

## Cognifyz Technologies Internship — Level 3, Task 2

This project ranks individual restaurant records by vote count and analyzes
the association between votes and aggregate ratings. It reports Pearson
linear and Spearman rank correlations. Correlation describes association; it
does not show that votes cause ratings or vice versa.

## Project structure

```text
cognifyz_level3_task2_votes_analysis/
├── data/
│   ├── raw/restaurant_data.csv
│   └── processed/cleaned_restaurant_votes.csv
├── outputs/
│   ├── charts/
│   └── reports/
├── src/
├── requirements.txt
├── README.md
└── .gitignore
```

The original restaurant dataset is stored unchanged in `data/raw/`. The
cleaning step writes a separate processed copy. Results are calculated for
individual restaurant records; locations belonging to the same chain are not
combined.

## Requirements and setup

Python 3.9 or later is recommended. From this project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The raw CSV must include `Restaurant Name`, `Votes`, and `Aggregate rating`.
The provided dataset is placed at `data/raw/restaurant_data.csv`.

## Run

```powershell
python src/main.py
```

The script removes duplicate rows; coerces votes and ratings to numeric
values; excludes missing names/values, negative or fractional vote counts,
non-finite numbers, and ratings outside 0–5. It retains zero votes.

## Analysis and outputs

- Top and bottom 10 restaurant records by votes (stable ordering for ties).
- Pearson correlation and p-value for linear association.
- Spearman correlation and p-value for monotonic association.
- Horizontal vote charts and a votes-versus-rating regression scatter plot.
- A cleaned CSV, ranking CSV files, and text analysis reports.

Generated files:

```text
data/processed/cleaned_restaurant_votes.csv
outputs/charts/top_10_restaurants_votes.png
outputs/charts/bottom_10_restaurants_votes.png
outputs/charts/votes_vs_rating.png
outputs/reports/top_10_restaurants.csv
outputs/reports/bottom_10_restaurants.csv
outputs/reports/correlation_results.txt
outputs/reports/votes_analysis_summary.txt
```

Correlation coefficients are undefined when there are too few observations
or either variable is constant; the report labels those values accordingly.
The strength labels are approximate guidelines, not universal thresholds.
