# Restaurant Ratings Analysis

## Project Overview

This Python project analyzes restaurant aggregate ratings and vote counts. It
prints the rating distribution, identifies the most common rating range,
calculates the average number of votes per restaurant, and creates charts and a
text report.

## Analysis

- Count restaurants at each aggregate rating.
- Group ratings into `0-1`, `1-2`, `2-3`, `3-4`, and `4-5` ranges and calculate
  each range's percentage.
- Identify the range containing the most restaurants.
- Calculate the mean vote count per restaurant.

Rating ranges include their lower boundary and exclude their upper boundary,
except the final `4-5` range, which also includes a valid rating of exactly
`5.0`.

## Requirements

- Python 3.9 or newer
- Pandas
- Matplotlib
- Seaborn

## Dataset

Place the restaurant CSV at `data/raw/Dataset.csv`. The file must include
`Aggregate rating` and `Votes` columns; additional columns are allowed.
Non-numeric values, missing values, ratings outside 0-5, and negative vote
counts are excluded from the analysis.

The dataset is not included in this repository. If a rating of `0` means
"unrated" in your dataset, note that zero ratings are included unless you
change the analysis.

## Run

From the project root, create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

On Command Prompt, activate with:

```bat
.venv\Scripts\activate.bat
```

The program prints the results and creates:

- `outputs/charts/rating_distribution.png`
- `outputs/charts/rating_range_distribution.png`
- `outputs/reports/restaurant_ratings_report.txt`

## Project Structure

```text
data/
└── raw/
    └── Dataset.csv
outputs/
├── charts/
└── reports/
src/
├── __init__.py
├── analysis.py
├── data_loader.py
└── visualization.py
main.py
requirements.txt
```