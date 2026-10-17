# Cognifyz Data Analysis Internship

## Level 1 — Task 4: Online Delivery Analysis

### Objective

Determine the percentage of restaurants that offer online delivery and compare the average ratings of restaurants with and without online delivery.

### Technologies Used

- Python
- Pandas
- Matplotlib

### Analysis Performed

1. Loaded the Zomato restaurant dataset.
2. Identified restaurants offering and not offering online delivery.
3. Calculated the percentage of restaurants in each group.
4. Calculated the average rating for each group.
5. Compared average ratings.
6. Generated bar charts to visualize the results.
7. Exported analysis summaries to CSV files.

### Output Files

- `outputs/online_delivery_percentage.csv`
- `outputs/online_delivery_rating_comparison.csv`
- `outputs/online_delivery_percentage.png`
- `outputs/online_delivery_rating_comparison.png`

### Percentage Formula

Percentage offering online delivery =
(Restaurants offering online delivery / Restaurants with valid delivery status) × 100

### Rating Calculation

Average rating = Sum of valid restaurant ratings / Number of restaurants with valid ratings in that group

Missing delivery statuses are excluded from the delivery percentage calculation. Missing ratings are excluded from the average rating calculation.

### Internship

Cognifyz IT Solutions Pvt. Ltd.

Data Analysis Internship — Level 1, Task 4
