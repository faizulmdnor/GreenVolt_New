from GreenVolt_db import greenvolt
import random

tablename = 'vw_Employees'
df = greenvolt.query_table(table_name=tablename)

def salary(start, end):
    """
    Generates a random salary value within a specified range.

    This function takes two arguments, representing the minimum and maximum
    salary range. It calculates a random floating-point number between these
    values, rounds it to two decimal places, and returns it.

    :param start: The minimum salary range limit.
    :param end: The maximum salary range limit.
    :return: A random salary value rounded to two decimal places within the
             specified range.
    """
    s = round(random.uniform(start, end), 2)
    return s

start_chief, end_chief = float(25000.00), float(35000.00)
start_exec_man, end_exec_man = float(17000.00), float(26000.00)
start_manager, end_manager = float(13000.00), float(18000.00)
start_else, end_else = float(3500.00), float(13500.00)

df['Position_1'] = df['Position'].str.lower()



for i, r in df.iterrows():
    position = r['Position_1']
    if 'chief' in position:
        df.loc[i, 'salary'] = salary(start=start_chief, end=end_chief)
    elif 'executive management' in position:
        df.loc[i, 'salary'] = salary(start=start_exec_man, end=end_exec_man)
    elif 'manager' in position:
        df.loc[i, 'salary'] = salary(start=start_manager, end=end_manager)
    else:
        df.loc[i, 'salary'] = salary(start=start_else, end=end_else)

# Correct selection of columns
emp_salary = df[['emp_id', 'salary']]

greenvolt.insert_data_no_duplicate(table_name='Salary', df=emp_salary)

