select *
from vw_Employees
order by First_Name 

delete Employees
from Employees e
left join Usernames u
on u.emp_id = e.emp_id
where u.Username is null
