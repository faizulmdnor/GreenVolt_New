import pandas as pd
import pyodbc
from datetime import datetime

to_date = datetime.today().strftime('%Y-%m-%d')

def query_employees(conn):
    sql_query = f"""SELECT e.emp_id, e.First_Name, e.Last_Name 
            FROM Employees e
            LEFT JOIN Usernames u
            ON e.emp_id = u.emp_id
            WHERE u.Username IS NULL
    """
    df = pd.read_sql(sql_query, conn)
    if not df.empty:
        return df
    else:
        print('No new username to create.')
    return df

def check_existing_username(cursor, username):
    sql_query = "SELECT * FROM Usernames WHERE Username = ?"
    counter = 1
    while True:
        cursor.execute(sql_query, username)
        result = cursor.fetchone()
        if not result:
            break
        username = f"{username}{counter}"
        counter += 1
    new_username = username
    return new_username

def insert_into_usernames(conn, cursor, emp_id, username):
    sql_query = "INSERT INTO Usernames (emp_id, Username) VALUES (?, ?)"

    try:
        cursor.execute(sql_query, (emp_id, username))
        conn.commit()
        print(f"Username {username} inserted into table Usernames")
    except Exception as e:
        print(f"Insert username into table Usernames FAILED: {e}")
        conn.rollback()

def employees_details(conn):
    sql_query = f"""
            SELECT *
            FROM Employees e
            LEFT JOIN Usernames u
            ON e.emp_id = u.emp_id
            WHERE u.Username IS NULL
        """
    try:
        df = pd.read_sql(sql_query, conn)
        if not df.empty:
            return df
        else:
            print('No new username to create.')

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

SERVER = 'FAIZULONXY\\SQLEXPRESS'
DATABASE = 'GreenVolt'
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')
cursor = conn.cursor()


try:
    df_data = query_employees(conn)
    df_data['Username'] = df_data['First_Name'] + '_' + df_data['Last_Name']
    df_data['Username'] = df_data['Username'].str.lower().str.replace(' ', '')
    for i, r in df_data.iterrows():
        base_username = r['Username']
        new_username = check_existing_username(cursor, base_username)
        if base_username != new_username:
            print(f"Username {base_username} already exists. New username: {new_username}")
            r['Username'] = new_username
        else:
            print(f"Username {base_username} is available.")

        insert_into_usernames(conn, cursor, r['emp_id'], r['Username'])

finally:
    cursor.close()
    conn.close()
