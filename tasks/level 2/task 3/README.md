# Geographic Restaurant Analysis

## Project Overview
This project analyzes restaurant locations using longitude and latitude coordinates to identify geographic patterns and clusters.

It uses Python, Pandas, Folium, Matplotlib, NumPy, and Scikit-learn to perform geographic analysis and visualization.

## Objectives
- Plot restaurant locations on an interactive map.
- Identify cities with the highest restaurant counts.
- Analyze restaurant concentration by locality.
- Detect geographic clusters using DBSCAN.
- Visualize restaurant distributions and geographic clusters.
- Export analytical results into CSV and text reports.

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Folium
- Scikit-learn

## Project Structure
```text
level-2-task-3-geographic-analysis/
├── data/
│   └── raw/
│       └── Dataset.csv
├── outputs/
│   ├── maps/
│   ├── charts/
│   └── reports/
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── analysis.py
│   ├── clustering.py
│   └── visualization.py
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── .venv/
```

## Installation
Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Place the dataset at:

`data/raw/Dataset.csv`

## Run the Project
Execute:

```bash
python main.py
```

## Generated Outputs
### Interactive Map
`outputs/maps/restaurant_locations_map.html`

### Charts
- `outputs/charts/top_cities.png`
- `outputs/charts/geographic_clusters.png`

### Reports
- `outputs/reports/geographic_analysis_report.txt`
- `outputs/reports/city_restaurant_counts.csv`
- `outputs/reports/locality_restaurant_counts.csv`
- `outputs/reports/geographic_clusters.csv`

## Methodology
1. Load and validate restaurant data.
2. Clean longitude and latitude coordinates.
3. Analyze restaurant counts by city and locality.
4. Apply DBSCAN using Haversine geographic distance.
5. Generate an interactive restaurant map.
6. Visualize geographic clusters.
7. Export the results.

## Clustering Parameters
The initial DBSCAN configuration uses a neighborhood radius of 2 kilometers and a minimum of 10 samples.

These parameters can be adjusted based on the geographic scale and density of the dataset.

## Learning Outcomes
This project demonstrates data cleaning, geographic data analysis, interactive mapping, density-based clustering, data visualization, and report generation.

## Conclusion
The project identifies geographic areas with high restaurant concentrations and visualizes spatial patterns in the dataset. The findings describe the available restaurant records and should not automatically be interpreted as a complete representation of all restaurants in each city.
