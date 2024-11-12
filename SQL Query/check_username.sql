--to check employees without username.

SELECT *
FROM Employees e
LEFT JOIN Usernames u
ON e.emp_id = u.emp_id
WHERE u.Username IS NULL

select * from vw_Employees
where Department = 'Sales'