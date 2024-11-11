# Importing the 'greenvolt' module from 'GreenVolt_db', likely a custom database module that provides functions for data insertion and handling.
from GreenVolt_db import greenvolt

# Importing the pandas library as 'pd' to handle data structures and data analysis.
import pandas as pd

# Setting the variable 'tablename' to 'Employees', indicating that this is the target database table for the data insertion.
tablename = 'Employees'

# Defining a dictionary 'new_emp' that contains data for new employee records.
# Each key represents a column in the 'Employees' table, and the associated lists are the values for each new record:
# "First_Name" - First names of the new employees.
# "Last_Name" - Last names of the new employees.
# "gender_id" - Gender identifiers, where 311 could represent a specific gender.
# "origin_country_id" - Country of origin identifiers, likely from a predefined list of countries.
# "Date_of_Birth" - Birth dates of the new employees, provided in a standard date format (yyyy-mm-dd).
# "Date_Hired" - Hiring dates for the employees, all set to '2024-11-11' in this example.
# "dept_id" - Department identifiers for the employees, indicating their assigned departments.
# "site_id" - Site location identifiers, representing the office or branch location of each employee.
# "pos_id" - Position identifiers for job roles or titles within the organization.
# "status_id" - Employment status identifiers, where '1' might signify active status.
new_emp = {
    "First_Name":["Redzuan", "Gary"],
    "Last_Name":["Ahmad", "McGuirre"],
    "gender_id":[311, 311],
    "origin_country_id":[1000, 7000],
    "Date_of_Birth":["2004-10-18", "1987-04-14"],
    "Date_Hired":["2024-11-11", "2024-11-11"],
    "dept_id": [2010, 4010],
    "site_id": [1002, 1001],
    "pos_id": [2014, 4013],
    "status_id": [1, 1],
}

# Creating a DataFrame 'df' from the 'new_emp' dictionary.
# The DataFrame structure allows us to handle, analyze, and manipulate tabular data easily before inserting it into the database.
df = pd.DataFrame(new_emp)

# Printing the DataFrame to view its structure and confirm the data before proceeding with insertion.
print(df)

# Calling the 'insert_data_no_duplicate' function from the 'greenvolt' module.
# This function inserts the data in 'df' into the specified database table, 'Employees', while preventing duplicate entries.
# Ensures that only unique records are added to maintain data integrity.
greenvolt.insert_data_no_duplicate(table_name=tablename, df=df)
