-- Add 2 minutes to the current date and time
SELECT DATEADD(MINUTE, 2, GETDATE());

-- Retrieve employee information along with average performance scores
SELECT 
    e.emp_id,
    e.First_Name, 
    e.Last_Name, 
    e.Date_Hired,
    DATEDIFF(YEAR, e.Date_Hired, GETDATE()) AS working_year,
    ROUND(AVG(CAST(p.scores AS FLOAT)), 2) AS average_score
FROM 
    Employees e
LEFT JOIN 
    Employees_Performance p ON e.emp_id = p.emp_id
WHERE 
    p.scores IS NOT NULL
GROUP BY 
    e.emp_id, e.First_Name, e.Last_Name, e.Date_Hired
HAVING 
    AVG(p.scores) <= 2
ORDER BY 
    e.Date_Hired;
