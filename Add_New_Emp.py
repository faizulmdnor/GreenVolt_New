from GreenVolt_db import greenvolt
import pandas as pd

tablename = 'Employees'

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
df = pd.DataFrame(new_emp)
print(df)
greenvolt.insert_data_no_duplicate(table_name=tablename, df=df)