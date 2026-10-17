# Restaurant Price Range and Service Availability Analysis

## Cognifyz Technologies Internship — Level 3, Task 3

### Project Overview
This project analyzes whether restaurant price ranges are associated with the availability of online delivery and table booking.

Python is used to clean the dataset, calculate service availability percentages, visualize differences between price categories, and perform statistical tests.

### Objectives
- Analyze online delivery availability across price ranges.
- Analyze table booking availability across price ranges.
- Determine whether higher-priced restaurants are more likely to offer these services.
- Use chi-square tests to examine associations between price range and service availability.
- Generate charts and summary reports.

### Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy

### Project Structure

```text
cognifyz_level3_task3_price_services/
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
│   ├── charts/
│   └── reports/
├── src/
├── requirements.txt
├── README.md
└── .gitignore
```

### Installation
Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Dataset
Place the restaurant dataset in:

`data/raw/restaurant_data.csv`

Required columns:
- `Restaurant Name`
- `Price range`
- `Has Online delivery`
- `Has Table booking`

### Run the Project

```bash
python src/main.py
```

### Analysis Methods
- Data cleaning and validation.
- Percentage calculations by price range.
- Bar charts and heatmaps.
- Chi-square tests of independence.
- Automated report generation.

### Outputs
The project generates:
- Online delivery availability by price range.
- Table booking availability by price range.
- A comparison chart of both services.
- A service availability heatmap.
- Statistical test results.
- A final summary report.

### Conclusion
The results help determine whether service availability differs across restaurant price categories.

All conclusions should be based on the actual percentages and statistical test results generated from the dataset.
