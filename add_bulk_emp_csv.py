import pandas as pd
from GreenVolt_db import greenvolt

tablename = "Employees"

data = pd.read_csv('table_employees.csv')

data['Date_of_Birth'] = pd.to_datetime(data['Date_of_Birth'], dayfirst=True, errors='coerce')
data['Date_Hired'] = pd.to_datetime(data['Date_Hired'], dayfirst=True, errors='coerce')

greenvolt.insert_data_no_duplicate(table_name=tablename, df=data)