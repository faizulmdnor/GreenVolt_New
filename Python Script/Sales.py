'''
Code Explanation
Step 1: Load data from the GreenVolt_db database.
Step 2: Prepares data by converting the YearMonth column to datetime and rounding totalSales.
Step 3: Aggregates sales data by year and month.
Step 4: Calculates moving averages for both monthly and yearly data.
Step 5 & Step 6: Uses linear regression to predict future sales for the next three months and three years, respectively.
Step 7: Combines actual, moving average, and predicted sales data into separate DataFrames (Sales_by_Months and Sales_by_Year) for display.
'''

# Import necessary libraries
from matplotlib import pyplot as plt
import pandas as pd
from GreenVolt_db import greenvolt
from sklearn.linear_model import LinearRegression
import numpy as np

# Step 1: Load Data from Database
sales_table = 'Monthly_Sales'
df_sales = greenvolt.query_table(sales_table)  # Query monthly sales data from the database

# Step 2: Data Preparation
# Convert 'YearMonth' to datetime and round 'totalSales' to 2 decimal places for consistency
df_sales['YearMonth'] = pd.to_datetime(df_sales['YearMonth'], format='%Y-%m')
df_sales['totalSales'] = df_sales['totalSales'].round(2)
first_year_month = df_sales['YearMonth'].min()  # Get the earliest date for future use

# Extract Year and Month from 'YearMonth' to create separate columns
df_sales['Year_Sales'] = df_sales['YearMonth'].dt.strftime('%Y')
df_sales['Month_Sales'] = df_sales['YearMonth'].dt.strftime('%m')

# Step 3: Aggregate Sales Data
# Group and sum sales by year and round to 2 decimal places, then rename the column for clarity
df_sales_Years = df_sales.groupby(by='Year_Sales').agg({'totalSales': 'sum'}).round(2)
df_sales_Years = df_sales_Years.rename(columns={'totalSales': 'TotalSales_Year'})

# Group and sum sales by month and rename column
df_sales_Months = df_sales.groupby(by='YearMonth').agg({'totalSales': 'sum'}).round(2)
df_sales_Months = df_sales_Months.rename(columns={'totalSales': 'TotalSales_Month'})

# Step 4: Calculate Moving Averages
# Calculate a 3-month rolling average for monthly sales, rounded to 2 decimal places
df_sales_Months['3 Months Mov Avg'] = df_sales_Months['TotalSales_Month'].rolling(window=3).mean().round(2)

# Calculate a 3-year rolling average for yearly sales, rounded to 2 decimal places
df_sales_Years['3 Years Mov Avg'] = df_sales_Years['TotalSales_Year'].rolling(window=3).mean().round(2)

# Step 5: Predict Next 3 Months Using Linear Regression
# Prepare data for monthly regression
df_sales_Months['Month_Num'] = np.arange(len(df_sales_Months))  # Generate sequential numbers for months
X_months = df_sales_Months['Month_Num'].values.reshape(-1, 1)
y_months = df_sales_Months['TotalSales_Month'].values

# Train linear regression model and make predictions for the next 3 months
model_month = LinearRegression()
model_month.fit(X_months, y_months)
future_months = np.arange(len(df_sales_Months) + 3).reshape(-1, 1)
pred_months = model_month.predict(future_months)
pred_months_rounded = np.round(pred_months, 2)

# Create a date range for predictions starting from the first available month
sales_yearmonth = pd.date_range(first_year_month, periods=len(pred_months_rounded), freq='M').strftime('%Y-%m')

# Combine the actual data, moving averages, and predictions into a DataFrame
Sales_by_Months = pd.DataFrame({
    'Total_Sales': df_sales_Months['TotalSales_Month'],
    'Sales Moving Average': df_sales_Months['3 Months Mov Avg'],
    'Sales Regression': pred_months_rounded
}, index=sales_yearmonth)

# Step 6: Predict Next 3 Years Using Linear Regression
# Prepare data for yearly regression
df_sales_Years['Year_Num'] = np.arange(len(df_sales_Years))  # Generate sequential numbers for years
X_years = df_sales_Years['Year_Num'].values.reshape(-1, 1)
y_years = df_sales_Years['TotalSales_Year'].values

# Train linear regression model and make predictions for the next 3 years
model_year = LinearRegression()
model_year.fit(X_years, y_years)
future_years = np.arange(len(df_sales_Years) + 3).reshape(-1, 1)
pred_years = model_year.predict(future_years)
pred_years_rounded = np.round(pred_years, 2)

# Create a date range for predictions starting from the first available year
first_year = df_sales_Years.index.min()
years_sales = pd.date_range(first_year, periods=len(pred_years_rounded), freq='Y').strftime('%Y')

# Combine the actual data, moving averages, and predictions into a DataFrame
Sales_by_Year = pd.DataFrame({
    'Total_Sales': df_sales_Years['TotalSales_Year'],
    'Sales Moving Average': df_sales_Years['3 Years Mov Avg'],
    'Sales Regression': pred_years_rounded
}, index=years_sales)

# Step 7: Display Results
print("Monthly Sales Data with Prediction:\n", Sales_by_Months, "\n")
print("Yearly Sales Data with Prediction:\n", Sales_by_Year)
Sales_by_Months.to_csv('../Data Files/GreenVolt_Monthly_Sales.csv')
Sales_by_Year.to_csv('../Data Files/GreenVolt_Yearly_Sales.csv')