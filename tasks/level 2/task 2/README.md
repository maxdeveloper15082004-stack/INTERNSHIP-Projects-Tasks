# Cuisine Combination Analysis

## Project Overview

This project analyzes restaurant cuisine combinations to identify the most
common combinations and investigate whether certain combinations tend to have
higher aggregate ratings. It uses Python for data preparation, descriptive
analysis, and visualization.

## Objectives

- Identify common cuisine combinations and the number of restaurants offering each.
- Calculate average and median ratings for every combination.
- Identify the most common individual cuisines.
- Compare highly rated combinations after applying a minimum restaurant-count
  threshold.
- Save charts, CSV tables, and a text report.

## Requirements

- Python 3.9 or newer
- Packages listed in `requirements.txt`

## Setup

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Place the source dataset at `data/raw/Dataset.csv`. It must include the exact
columns `Cuisines` and `Aggregate rating`; additional columns are allowed.
The source dataset is not included in this repository.

## Run

From the project root, run:

```powershell
python main.py
```

The program validates the required columns, drops rows with missing/invalid
cuisines or ratings outside the 0–5 range, and creates the output directories
when needed.

## Project Structure

```text
data/
└── raw/
    └── Dataset.csv
outputs/
├── charts/
│   ├── top_cuisine_combinations.png
│   └── cuisine_average_ratings.png
└── reports/
    ├── cuisine_combination_report.txt
    ├── cuisine_combination_frequency.csv
    └── cuisine_combination_ratings.csv
src/
├── __init__.py
├── data_loader.py
├── preprocessing.py
├── analysis.py
└── visualization.py
main.py
requirements.txt
.gitignore
README.md
```

## Methodology

Cuisine names are trimmed, duplicate names within a restaurant are removed,
and names are sorted without regard to case to make cuisine order irrelevant.
Capitalization differences are retained. Combination ratings include restaurant
counts, means, and medians. The default minimum count for the higher-rating
comparison is 10 restaurants; this is a screening threshold, not a statistical
guarantee.

## Generated Outputs

- `outputs/charts/top_cuisine_combinations.png`: ten most frequent combinations.
- `outputs/charts/cuisine_average_ratings.png`: up to ten highest-rated
  combinations meeting the minimum count.
- `outputs/reports/cuisine_combination_frequency.csv`: counts for all combinations.
- `outputs/reports/cuisine_combination_ratings.csv`: counts and rating statistics
  for all combinations.
- `outputs/reports/cuisine_combination_report.txt`: key findings and summaries.

## Interpretation

The outputs describe this dataset; they do not show that a cuisine combination
causes a restaurant to receive a particular rating. Restaurant counts, location,
price, service, and other factors should also be considered. Compare combination
averages with the overall average and give more weight to findings supported by
more restaurants.
