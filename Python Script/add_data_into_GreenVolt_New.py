from GreenVolt_db import greenvolt
import pandas as pd

data = pd.read_csv('../Data Files/Positions.csv')
table_name = 'Positions'

greenvolt.insert_data_no_duplicate(table_name=table_name, df=data)