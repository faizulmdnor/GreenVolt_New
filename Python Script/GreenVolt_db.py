import pandas as pd
import pyodbc

# Defining the SQL Server and database connection parameters.
SERVER = 'FAIZULONXY\\SQLEXPRESS'  # Specifies the server name.
DATABASE = 'GreenVolt_New'  # Specifies the database name.

# Establishing a connection to the SQL Server database using pyodbc.
# Trusted_Connection=yes indicates Windows Authentication is used.
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')
cursor = conn.cursor()  # Initializing a cursor to execute queries on the database.

class greenvolt:
    """
    Provides database interaction functionalities for the 'GreenVolt' database.

    This class contains methods for executing custom SQL queries and managing
    data within the 'GreenVolt' database. It allows retrieving data from specified
    tables and inserting data into tables while avoiding duplicate records. The
    static methods allow flexibility in querying and data manipulation without
    needing to instantiate the class.
    """

    @staticmethod
    def custom_query(sql_query):
        df = pd.read_sql(sql_query, conn)
        return df

    def query_table(table_name: str) -> pd.DataFrame:
        """
        Retrieves all data from a specified table in the 'GreenVolt' database.

        This method connects to the specified table within the 'GreenVolt' database and
        executes a SQL query to fetch all records. The results are loaded into a pandas
        DataFrame for easy data manipulation.

        :param table_name: Name of the SQL table from which data will be fetched.
        :type table_name: str
        :return: A DataFrame containing all records from the specified table.
        :rtype: pd.DataFrame
        """
        # SQL query to select all records from the specified table.
        sql_query = f"""
                SELECT *
                FROM {table_name}
        """
        # Executing the query and loading the results into a DataFrame.
        df = pd.read_sql(sql_query, conn)
        return df

    @staticmethod
    def insert_data_no_duplicate(table_name: str, df: pd.DataFrame) -> None:
        """
        Inserts data from a DataFrame into a specified SQL table, ensuring no duplicate records are inserted.

        This method iterates over each row in the provided DataFrame, checks if the row already exists in
        the target SQL table (based on all column values), and inserts it only if it does not exist, thereby
        preventing duplicate entries.

        :param table_name: Name of the SQL table where data will be inserted.
        :type table_name: str
        :param df: DataFrame containing the data to be inserted into the table.
        :type df: pd.DataFrame
        :return: None
        :rtype: None
        """
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
                    print(f"Record already exists in the database. {tuple(row)}")  # Message if duplicate found.

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
