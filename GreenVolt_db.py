import pandas as pd
import pyodbc

SERVER = 'FAIZULONXY\\SQLEXPRESS'
DATABASE = 'GreenVolt'
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')
cursor = conn.cursor()

class greenvolt:
    @staticmethod
    def query_table(table_name):
        sql_query = f"""
                SELECT *
                FROM {table_name}
        """
        df = pd.read_sql(sql_query, conn)
        return df

    @staticmethod
    def insert_data_no_duplicate(table_name, df):
        columns = ', '.join(df.columns)
        placeholder = ', '.join('?' * len(df.columns))
        columns_check = ' AND '.join([f"{col}=?" for col in df.columns])

        sql_check = f'''
            SELECT COUNT(*)
            FROM {table_name}
            WHERE 
            {columns_check}
        '''

        sql_insert = f'''
            INSERT INTO {table_name} ({columns}) VALUES ({placeholder})
        '''

        try:
            for index, row in df.iterrows():
                cursor.execute(sql_check, tuple(row))
                exists = cursor.fetchone()[0]>0

                if not exists:
                    cursor.execute(sql_insert, tuple(row))
                    conn.commit()
                    print(f"Insert data {tuple(row)} into {table_name} - SUCCESS")
                else:
                    print(f"Record already exists in the database.{tuple(row)}")
        except Exception as err:
            conn.rollback()
            print(f"Insert data into {table_name} - FAILED: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
