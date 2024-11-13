import random
import pandas as pd
from datetime import datetime
from GreenVolt_db import greenvolt  # Custom module for database interactions.

# Set the current date in 'YYYY-MM' format
todate = datetime.now().strftime('%Y-%m')

# Step 1: Query employee data from the database
employees = 'vw_Employees'
df_employees = greenvolt.query_table(employees)

# Step 2: Filter data to include only Sales department roles, excluding 'Sales Analyst' and 'Sales Engineer'
df_sales = df_employees[(df_employees['Department'] == 'Sales') &
                        (df_employees['Position'] != 'Sales Analyst') &
                        (df_employees['Position'] != 'Sales Engineer')]

# Step 3: Reset index after filtering to maintain a clean, sequential index
df_sales.reset_index(drop=True, inplace=True)

# Step 4: Convert 'Date_Hired' to datetime format and extract only the Year-Month part
df_sales['Date_Hired'] = pd.to_datetime(df_sales['Date_Hired'])
df_sales['Month_hired'] = df_sales['Date_Hired'].dt.strftime('%Y-%m')

# Step 5: Get a sorted list of all unique hire months in the Sales department
df_sales_hired = sorted(df_sales['Month_hired'])

# Step 6: Create a DataFrame of hire months and generate a full range of Year-Months up to the current month
sales_month = pd.DataFrame(df_sales_hired, columns=['YearMonth'])
full_range = pd.date_range(sales_month['YearMonth'].min(), todate, freq='MS').strftime('%Y-%m')

# Step 7: Initialize an empty list to store monthly sales data for each salesperson
monthly_sales = []

# Step 8: Loop through each salesperson in the filtered DataFrame
for i, j in df_sales.iterrows():
    # Step 9: For each salesperson, loop through the full range of months (from earliest hire month to the current date)
    for m in range(len(full_range)-1):
        # Check if the salesperson's hire month is on or before the current month in the range
        if j['Month_hired'] <= full_range[m]:
            # Generate a random sales amount for the current month
            total_sales = round(random.uniform(0, 100000), 2)
            # Create a dictionary with salesperson ID, month, and sales amount
            sales_info = {
                'emp_id': j['emp_id'],
                'YearMonth': full_range[m],
                'totalSales': total_sales
            }

            # Add the monthly sales data to the list
            monthly_sales.append(sales_info)

# Step 10: Convert the list of dictionaries into a DataFrame for monthly sales
df_monthly_sales = pd.DataFrame(monthly_sales)

# Step 11: Insert the monthly sales data into the 'Monthly_Sales' table, ensuring no duplicate entries
sales_table = 'Monthly_Sales'
greenvolt.insert_data_no_duplicate(sales_table, df_monthly_sales)

# Step 12: Print the DataFrame to review the final monthly sales data
print(df_monthly_sales)

# Step 13: Pivot the DataFrame to display 'emp_id' as the index and 'YearMonth' as columns with sales values
df_monthly_sales_pivot = df_monthly_sales.pivot(index='emp_id', columns='YearMonth', values='totalSales')

# Step 14: Export the pivoted DataFrame to a CSV file for further use or review
df_monthly_sales_pivot.to_csv('../Data Files/Total Sales_GreenVolt_New.csv')

# Step 15: Print the pivoted DataFrame to review the data structure
print(df_monthly_sales_pivot)
