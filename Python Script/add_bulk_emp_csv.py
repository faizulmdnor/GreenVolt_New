# Importing the pandas library as 'pd', a common alias that simplifies referencing pandas functions.
import pandas as pd

# Importing a custom module named 'GreenVolt_db', specifically a function or class called 'greenvolt'.
# This likely contains custom database interaction functions for the 'GreenVolt' project.
from GreenVolt_db import greenvolt

# Defining the database table name as "Employees" to specify where data will be inserted.
tablename = "Employees"

# Reading a CSV file named 'table_employees.csv' and storing it in a DataFrame named 'data'.
# This file presumably contains employee information to be processed and loaded into the database.
data = pd.read_csv('../Data Files/table_employees.csv')

# Converting the 'Date_of_Birth' column in the DataFrame to datetime format.
# The 'dayfirst=True' argument interprets dates with the day as the first value, e.g., 'dd/mm/yyyy'.
# 'errors="coerce"' means that any invalid date entries will be replaced with NaT (Not a Time) instead of raising an error.
data['Date_of_Birth'] = pd.to_datetime(data['Date_of_Birth'], dayfirst=True, errors='coerce')

# Converting the 'Date_Hired' column in the DataFrame to datetime format, similar to 'Date_of_Birth'.
# Ensures all dates in 'Date_Hired' are standardized and invalid entries are marked as NaT.
data['Date_Hired'] = pd.to_datetime(data['Date_Hired'], dayfirst=True, errors='coerce')

# Calling the 'insert_data_no_duplicate' function from the 'greenvolt' module.
# This function inserts data from the DataFrame 'data' into the specified database table, 'Employees'.
# It presumably includes logic to check for and prevent duplicate entries based on unique employee data.
greenvolt.insert_data_no_duplicate(table_name=tablename, df=data)
