WITH EmployeeAvgSalaryByDepartment AS (
	SELECT 
		emp_id,
		First_Name,
		Department,
		Salary,
		avg(Salary) OVER(PARTITION BY Department) AS avg_salary
	FROM
		vw_employees
)
SELECT 
	emp_id,
	First_Name,
	Department,
	Salary,
	avg_salary
FROM
	EmployeeAvgSalaryByDepartment
WHERE
	Salary <= avg_salary;

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
