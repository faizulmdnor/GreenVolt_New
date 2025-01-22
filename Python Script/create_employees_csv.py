from GreenVolt_db import greenvolt

sql_query = f"""
    SELECT 
        e.emp_id,
        e.First_Name,
        e.Last_Name,
        g.Gender,
        c.Country,
        e.Date_of_Birth,
        e.Date_Hired,
        d.Department,
        p.Position,
        s.Site,
        sal.salary
    FROM Employees e
    LEFT JOIN Gender g
    ON e.gender_id = g.gender_id
    LEFT JOIN Country c
    ON c.country_id = e.origin_country_id
    LEFT JOIN Departments d
    ON d.dept_id = e.dept_id
    LEFT JOIN Sites s
    ON s.site_id = e.site_id 
    LEFT JOIN Positions p
    ON p.pos_id = e.pos_id
    LEFT JOIN Salary sal
    ON sal.emp_id = e.emp_id
"""

table_name = 'vw_Employees'
data = greenvolt.custom_query(sql_query=sql_query)

data.to_csv(f"..\Data Files\employees_info.csv", index=False)