# Restaurant Chain Analysis

## Project Overview
This project analyzes restaurant chains using a restaurant dataset. It identifies potential chains by restaurant name and compares their outlet counts, average ratings, and popularity.

## Objectives

- Identify potential restaurant chains.
- Find chains with the highest number of outlets.
- Compare average ratings across chains.
- Measure popularity using total votes and average votes.
- Visualize results using bar charts.
- Export analysis results and a text report.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Project Structure

```
level-2-task-4-restaurant-chains/
├── data/
│   └── raw/
├── outputs/
│   ├── charts/
│   └── reports/
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── analysis.py
│   ├── visualization.py
│   └── report.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run

1. Clone or download the project.
2. Place the dataset at `data/raw/Dataset.csv`.
3. Create and activate a Python virtual environment.
4. Install dependencies:

```
python -m pip install -r requirements.txt
```

5. Run the project:

```
python main.py
```

## Analysis Metrics

- Outlet count
- Average rating
- Total votes
- Average votes per outlet
- Number of distinct cities
- Number of rated outlets

## Outputs
The project generates:

- A CSV containing all identified potential chains.
- A CSV containing the top chains by outlet count.
- A text report with key findings.
- Three bar charts comparing chain outlets, ratings, and popularity.

## Methodology
Restaurant names appearing more than once are treated as potential chains. Average ratings are calculated from valid ratings, while total votes are used as a measure of popularity. Chains must have at least three rated outlets to appear in the highest-rated comparison.

This is a name-based approximation. Repeated names do not always represent the same business, so the results should be interpreted accordingly.

## Conclusion
The analysis provides a data-driven comparison of restaurant chains based on their presence, customer ratings, and vote totals. It demonstrates data cleaning, group-by aggregation, ranking, visualization, and report generation using Python.
