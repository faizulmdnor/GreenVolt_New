# Purpose of this script:
# This script is designed to connect to an SQL Server database ('GreenVolt') and interact with a specified table within that database.
# It provides functionality to:
# 1. Query all data from a specified table and load it into a pandas DataFrame.
# 2. Insert new records into a table while checking for duplicates to avoid inserting the same data multiple times.
#    If a duplicate record is found, it skips insertion for that record.
#
# The script uses a 'greenvolt' class containing two static methods:
# - query_table(table_name): Executes a SQL query to retrieve all data from the specified table and returns it as a DataFrame.
# - insert_data_no_duplicate(table_name, df): Checks each row in a DataFrame for existing records in the specified table.
#   If a record does not exist, it inserts the row; otherwise, it skips it to prevent duplicates.
#
# This script includes error handling for database operations, and resources are released by closing the connection and cursor at the end.

# Importing necessary libraries:
# - pandas to handle data in DataFrame format.
# - pyodbc to connect to and interact with the SQL Server database.
import pandas as pd
import pyodbc

# Defining the SQL Server and database connection parameters.
SERVER = 'FAIZULONXY\\SQLEXPRESS'  # Specifies the server name.
DATABASE = 'GreenVolt'  # Specifies the database name.

# Establishing a connection to the SQL Server database using pyodbc.
# Trusted_Connection=yes indicates Windows Authentication is used.
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')
cursor = conn.cursor()  # Initializing a cursor to execute queries on the database.


# Defining the 'greenvolt' class containing methods for querying and inserting data.
class greenvolt:

    # Static method to retrieve all data from a specified table.
    # table_name: The name of the SQL table from which data will be fetched.
    @staticmethod
    def query_table(table_name):
        # SQL query to select all records from the specified table.
        sql_query = f"""
                SELECT *
                FROM {table_name}
        """
        # Executing the query and loading the results into a DataFrame.
        df = pd.read_sql(sql_query, conn)
        return df

    # Static method to insert data into the specified table while checking for duplicates.
    # table_name: The SQL table where data will be inserted.
    # df: DataFrame containing the data to be inserted.
    @staticmethod
    def insert_data_no_duplicate(table_name, df):
        # Preparing the SQL statement components for insertion and duplicate checks.
        columns = ', '.join(df.columns)  # Converts column names to a comma-separated string.
        placeholder = ', '.join('?' * len(df.columns))  # Placeholder for parameterized query.

        # Setting up condition to check if the record exists in the table based on all column values.
        columns_check = ' AND '.join([f"{col}=?" for col in df.columns])

        # SQL query to check for existing records in the table to avoid duplicates.
        sql_check = f'''
            SELECT COUNT(*)
            FROM {table_name}
            WHERE 
            {columns_check}
        '''

        # SQL insert query to add a new record if it does not already exist.
        sql_insert = f'''
            INSERT INTO {table_name} ({columns}) VALUES ({placeholder})
        '''

        # Try-except block to handle database operations and catch errors.
        try:
            # Looping through each row in the DataFrame to perform insertion or duplicate check.
            for index, row in df.iterrows():
                cursor.execute(sql_check, tuple(row))  # Checking if the record exists.
                exists = cursor.fetchone()[0] > 0  # Fetches the count result; exists=True if count > 0.

                # If the record does not exist, insert it into the table.
                if not exists:
                    cursor.execute(sql_insert, tuple(row))  # Executes the insert statement.
                    conn.commit()  # Commits the transaction to save changes.
                    print(f"Insert data {tuple(row)} into {table_name} - SUCCESS")
                else:
                    print(f"Record already exists in the database.{tuple(row)}")  # Message if duplicate found.

        # Rollback if an exception occurs during insertion.
        except Exception as err:
            conn.rollback()  # Rolls back any uncommitted transactions.
            print(f"Insert data into {table_name} - FAILED: {err}")

        # Ensuring resources are released by closing the cursor and connection.
        finally:
            if cursor:  # Checks if cursor exists before closing.
                cursor.close()
            if conn:  # Checks if connection exists before closing.
                conn.close()
