# Online Shop Sales Analysis

Python project for cleaning, transforming, joining, and analyzing sales
data from an online store.

## Project Goal

The goal of the project is to analyze online shop sales data using
Python and Pandas. The workflow includes:

- loading and exploring CSV files
- checking data quality
- cleaning invalid and inconsistent records
- joining customer, order, product, and order-item data
- calculating revenue, cost, profit, and profit margin
- analyzing sales by product and category
- analyzing customer purchasing behavior

## Project Structure

onlineshop_sales_analysis/
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   └── order_items.csv
├── output/
│   ├── customers_clean.csv
│   ├── products_clean.csv
│   ├── orders_clean.csv
│   ├── order_items_clean.csv
│   └── sales_clean.csv
├── main.py
└── README.md

### Input Data

The analysis uses four CSV files:

customers.csv --- customer information
products.csv --- product information, prices, costs, and categories
orders.csv --- orders, customers, dates, and discounts
order_items.csv --- products and quantities belonging to eachorder

### Data Quality Checks

**The project checks the datasets for:**

- missing values
- duplicate records
- incorrect data types
- negative quantities
- product prices less than or equal to zero
- product costs greater than prices
- non-existent customer IDs
- non-existent product IDs
- invalid dates

Problematic records are inspected before a cleaning decision is made
instead of being automatically deleted.

### Data Cleaning

**The cleaning process includes:**

- removing a test customer with a missing country value and no orders
- removing duplicate orders
- removing products with invalid price/cost values and their related order items
- removing an order linked to a non-existent customer
- removing an order item linked to a non-existent product
- removing an order item with a negative quantity
- converting registration_date and order_date to datetime
- converting invalid date values to NaT
- standardizing country names

The cleaned source tables are saved as new CSV files in the output/
directory, while the original files remain unchanged.

### Data Transformation

The cleaned datasets are joined using their relationships:

customers → orders → order_items → products

The resulting dataset contains customer, order, product, quantity,
price, cost, discount, date, country, and category information.

**For each order item, the following metrics are calculated:**

Revenue = price × quantity × (1 - discount)
Total Cost = cost × quantity
Profit = Revenue - Total Cost
Profit Margin = Profit / Revenue

The final joined dataset is saved as output/sales_clean.csv.

**Analysis Results**

Overall Sales
Total orders: 33
Unique customers: 16
Units sold: 131
Total revenue: 14,683.15
Total cost: 8,640.00
Total profit: 6,043.15
Overall profit margin: 41.16%
Average order value: 444.94

**Product Analysis**

Best-selling product by quantity: Smartphone Case --- 15 units
Product with highest revenue: Laptop Pro --- 6,030.00
Product with highest profit: Laptop Pro --- 1,480.00
Product with highest profit margin: Smartphone Case --- 79.31%

**Category Analysis**

Category with highest revenue: Electronics --- 8,473.00
Category with highest profit: Electronics --- 2,823.00
Category with highest profit margin: Accessories --- 62.52%
Customer Analysis

The project creates a Top 10 customer table based on total revenue and
calculates the number of unique orders, total revenue, and total profit
for each customer.

**Among the Top 10 customers:**

Most orders: Marko Petrovic --- 6 orders
Highest spending: Marko Petrovic --- 3,886.25
Highest profit contribution: Marko Petrovic --- 1,391.25

Technologies

Python
Pandas
CSV
PyCharm

### How to Run

Install Pandas if it is not already installed:

pip install pandas

Run the project from the project root directory:

python main.py

The program prints the data-quality checks and analysis results to the
console and generates the cleaned CSV files in the output/ directory.