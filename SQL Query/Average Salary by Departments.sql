SELECT COUNT(*) as [Number of Emp below average salary]
FROM (
	SELECT *, AVG(salary) OVER (PARTITION BY department) as avg_depart_salary
	FROM vw_employees
	)AS SubQuery
WHERE salary <= avg_depart_salary

SELECT COUNT(*) as [Number of Emp above average salary]
FROM (
	SELECT *, AVG(salary) OVER (PARTITION BY department) as avg_depart_salary
	FROM vw_employees
	)AS SubQuery
WHERE salary >= avg_depart_salary

SELECT *, ROUND(AVG(salary) OVER (PARTITION BY department), 2) as avg_depart_salary
FROM vw_employees



