# Importing necessary libraries:
# - pandas for handling data in DataFrame structures,
# - pyodbc for connecting and interacting with an SQL database,
# - datetime for obtaining and formatting current date.
import pandas as pd
import pyodbc
from datetime import datetime

# Getting the current date in the format 'YYYY-MM-DD' and storing it in the variable 'to_date'.
to_date = datetime.today().strftime('%Y-%m-%d')

# Function to query employees without a username in the database.
# This function takes a database connection ('conn') as an argument and retrieves employee details from the 'Employees' table
# who currently don't have an entry in the 'Usernames' table.
def query_employees(conn):
    # SQL query to select employee IDs, first names, and last names where no username is assigned.
    sql_query = f"""SELECT e.emp_id, e.First_Name, e.Last_Name 
            FROM Employees e
            LEFT JOIN Usernames u
            ON e.emp_id = u.emp_id
            WHERE u.Username IS NULL
    """
    # Running the query and storing the result in a DataFrame.
    df = pd.read_sql(sql_query, conn)
    # Checking if the DataFrame is empty. If not, return the DataFrame; else, print a message.
    if not df.empty:
        return df
    else:
        print('No new username to create.')
    return df

# Function to check if a given username already exists in the 'Usernames' table.
# This function loops until a unique username is found by appending a counter to avoid duplicates.
def check_existing_username(cursor, username):
    sql_query = "SELECT * FROM Usernames WHERE Username = ?"
    counter = 1
    # Loop to check for username availability.
    while True:
        cursor.execute(sql_query, username)
        result = cursor.fetchone()
        # If no existing username is found, exit the loop.
        if not result:
            break
        # Append a counter to the username if it already exists.
        username = f"{username}{counter}"
        counter += 1
    new_username = username
    return new_username

# Function to insert a new username into the 'Usernames' table.
# If insertion fails, it rolls back the transaction.
def insert_into_usernames(conn, cursor, emp_id, username):
    sql_query = "INSERT INTO Usernames (emp_id, Username) VALUES (?, ?)"
    try:
        # Executing the insertion query.
        cursor.execute(sql_query, (emp_id, username))
        conn.commit()  # Commit the transaction to save the changes.
        print(f"Username {username} inserted into table Usernames")
    except Exception as e:
        print(f"Insert username into table Usernames FAILED: {e}")
        conn.rollback()  # Rollback in case of an error.

# Function to retrieve employee details that don't have associated usernames.
# This function fetches all data from the 'Employees' table and related columns, joining with the 'Usernames' table.
def employees_details(conn):
    sql_query = f"""
            SELECT *
            FROM Employees e
            LEFT JOIN Usernames u
            ON e.emp_id = u.emp_id
            WHERE u.Username IS NULL
        """
    try:
        # Execute the query and load results into a DataFrame.
        df = pd.read_sql(sql_query, conn)
        if not df.empty:
            return df
        else:
            print('No new username to create.')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Connection setup for SQL Server using pyodbc.
# Defining server and database names, establishing a connection, and initializing a cursor for query execution.
SERVER = 'FAIZULONXY\\SQLEXPRESS'
DATABASE = 'GreenVolt'
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')
cursor = conn.cursor()

try:
    # Retrieving employees without usernames and storing them in 'df_data'.
    df_data = query_employees(conn)
    # Creating a base username by concatenating the first and last names, converting to lowercase, and removing spaces.
    df_data['Username'] = df_data['First_Name'] + '_' + df_data['Last_Name']
    df_data['Username'] = df_data['Username'].str.lower().str.replace(' ', '')

    # Iterating over each row to check for duplicate usernames and insert unique usernames into the database.
    for i, r in df_data.iterrows():
        base_username = r['Username']
        # Check if 'base_username' already exists, and if so, adjust it to ensure uniqueness.
        new_username = check_existing_username(cursor, base_username)
        if base_username != new_username:
            print(f"Username {base_username} already exists. New username: {new_username}")
            r['Username'] = new_username  # Update the username if it was modified.
        else:
            print(f"Username {base_username} is available.")

        # Insert the employee ID and final username into the 'Usernames' table.
        insert_into_usernames(conn, cursor, r['emp_id'], r['Username'])

# Close the cursor and database connection after completing all operations.
finally:
    cursor.close()
    conn.close()
