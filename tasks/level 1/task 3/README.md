# Cognifyz Data Analysis Internship

## Level 1 — Task 3: Price Range Distribution

### Objective

Visualize the distribution of restaurant price ranges and calculate the percentage of restaurants belonging to each price range category.

### Technologies Used

- Python
- Pandas
- Matplotlib

### Analysis Process

1. Load the restaurant dataset.
2. Validate the `Price range` column.
3. Convert price range values to numeric data.
4. Handle missing or invalid price range values.
5. Count restaurants in each price range category.
6. Calculate the percentage of all restaurant records in each category.
7. Export the distribution results to a CSV file.
8. Generate a bar chart showing restaurant counts and percentages.

### Output Files

- `outputs/price_range_distribution.csv`
- `outputs/price_range_distribution.png`

### Percentage Formula

Percentage = (Restaurants in a price range / Total restaurant records) × 100

Missing or invalid price ranges are excluded from category counts. The percentage denominator is the total number of restaurant records, so the percentages may sum to less than 100% when records have missing or invalid price ranges.

### Internship

Cognifyz IT Solutions Pvt. Ltd.

Data Analysis Internship — Level 1, Task 3
