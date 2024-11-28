from GreenVolt_db import greenvolt
import pandas as pd


SQL_QUERY = f'''
WITH SalaryWithAvg AS (
	SELECT
		e.*,
		s.salary,
		AVG(s.salary) OVER (PARTITION BY e.department) AS avg_department_salary
	FROM
		vw_Employees e
	LEFT JOIN 
		Salary s
	ON 
		e.emp_id = s.emp_id
),
TotalEmployees AS (
	SELECT 
		Department, 
		COUNT(*) AS Total_Emp
	FROM 
		vw_Employees
	GROUP BY 
		Department
)
SELECT 
	swa.Department, 
	COUNT(*) AS Num_of_Emp_Above_AVG_Dept_Salary,
	te.Total_Emp
FROM 
	SalaryWithAvg swa
JOIN 
	TotalEmployees te
ON 
	swa.Department = te.Department
WHERE 
	swa.salary > swa.avg_department_salary
GROUP BY 
	swa.Department, te.Total_Emp;

'''

df = greenvolt.custom_query(SQL_QUERY)
print(df)

correlation = df[['Num_of_Emp_Above_AVG_Dept_Salary', 'Total_Emp']].corr()
print(correlation)