select e.First_Name, e.Position, e.emp_id, sum(totalSales) as TotalSales
from Monthly_Sales s
Left join vw_Employees e
ON s.emp_id = e.emp_id
Group by e.First_Name, e.Position, e.emp_id
order by TotalSales desc
OFFSET 10 ROW FETCH NEXT 2 ROW ONLY

select e.Site, SUM(s.totalSales) as TotalSales 
from Monthly_Sales s
Left join vw_Employees e
ON s.emp_id = e.emp_id
Group by e.Site
order by TotalSales desc
