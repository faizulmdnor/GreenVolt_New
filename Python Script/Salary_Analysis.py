from GreenVolt_db import greenvolt
import pandas as pd


SQL_QUERY_1 = f'''
WITH EmployeeAvgSalaryByDepartment AS (
    SELECT 
        emp_id,
        First_Name,
        Department,
        Salary,
        AVG(Salary) OVER (PARTITION BY Department) AS avg_salary
    FROM
        vw_employees
)
SELECT 
    Department,
    COUNT(CASE WHEN Salary < avg_salary THEN emp_id END) AS [NumberOfEmp_Below_Avg_Salary],
    COUNT(CASE WHEN Salary > avg_salary THEN emp_id END) AS [NumberOfEmp_Above_Avg_Salary],
	COUNT(emp_id) as Total,
    MAX(avg_salary) AS avg_salary -- avg_salary is constant within each department
FROM 
    EmployeeAvgSalaryByDepartment
GROUP BY Department
ORDER BY [NumberOfEmp_Below_Avg_Salary] DESC;

'''

df = greenvolt.custom_query(SQL_QUERY_1)
print(df)

SQL_QUERY_2="""
    SELECT * FROM Salary
"""

df2 = greenvolt.custom_query(SQL_QUERY_2)
print(df2)

dup_emp_id = df2['emp_id'].duplicated(keep='first')
print(dup_emp_id)

correlation_1 = df[['NumberOfEmp_Below_Avg_Salary', 'Total']].corr()
print(correlation_1)

correlation_2 = df[['NumberOfEmp_Above_Avg_Salary', 'Total']].corr()
print(correlation_2)