/**Create new database GreenVolt**/
CREATE DATABASE GreenVolt_New

/**
CREATE TABLE - Create most simple table which have no depending to others.
Example:
	Gender
	Departments
	Positions
	Country
	Sites
	Employees
**/

CREATE TABLE Gender (
	gender_id INT PRIMARY KEY,
	Gender VARCHAR(6)
);

CREATE TABLE Departments(
	dept_id INT PRIMARY KEY,
	Department VARCHAR(25)
);

CREATE TABLE Positions(
	pos_id INT PRIMARY KEY,
	dept_id INT, 
	Position VARCHAR(50),
	FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

CREATE TABLE Country(
	country_id INT PRIMARY KEY,
	Country VARCHAR(50)
);

CREATE TABLE Sites(
	site_id INT PRIMARY KEY,
	country_id INT,
	Site VARCHAR(50),
	FOREIGN KEY (country_id) REFERENCES Country(country_id)
);

CREATE TABLE Employees(
	emp_id INT PRIMARY KEY IDENTITY(101000, 1),
	First_Name VARCHAR(50),
	Last_Name VARCHAR(50),
	gender_id INT,
	origin_country_id INT,
	Date_of_Birth DATE,
	Date_Hired DATE,
	dept_id INT,
	site_id INT,
	pos_id INT,
	FOREIGN KEY (origin_country_id) REFERENCES Country(country_id),
	FOREIGN KEY (gender_id) REFERENCES Gender(gender_id),
	FOREIGN KEY (dept_id) REFERENCES Departments(dept_id),
	FOREIGN KEY (site_id) REFERENCES Sites(site_ID),
	FOREIGN KEY (pos_id) REFERENCES Positions(pos_id)
);

/**
Inserting data into table
	1. Gender
How to INSERT large data?
**/

INSERT INTO Gender(gender_id, Gender) 
VALUES (310,'Female')

INSERT INTO Gender(gender_id, Gender) 
VALUES (311, 'Male')

SELECT * FROM Gender
select * from Sites
select * from Country
select * from Departments
select * from Positions
select * from Employees

/**
Create View
**/
CREATE VIEW vw_Employees AS
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
	s.Site
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

select * from vw_Employees


CREATE TABLE Employees_Performance(
	emp_id INT,
	Year INT,
	category VARCHAR(15),
	FOREIGN KEY (emp_id) REFERENCES Employees(emp_id)
)

CREATE TABLE Monthly_Sales (
	emp_id INT,
	YearMonth VARCHAR(7) CHECK (YearMonth LIKE '[1-9][0-9][0-9][0-9]-[0-1][0-9]'),
	totalSales MONEY,
	FOREIGN KEY (emp_id) REFERENCES Employees(emp_id)
);
/*
Explanation
CHECK (YearMonth LIKE '[1-9][0-9][0-9][0-9]-[0-1][0-9]'): This constraint enforces that YearMonth follows a YYYY-MM format.
[1-9][0-9][0-9][0-9] ensures that the first four characters are a valid year.
[0-1][0-9] allows only valid two-digit months (00 to 12).
This constraint won�t allow inserting values with incorrect formats, ensuring that the data meets the YYYY-MM requirement.
*/

select * from Monthly_Sales

CREATE TABLE  Salary(
	emp_id INT,
	salary MONEY
	FOREIGN KEY (emp_id) REFERENCES Employees(emp_id)
);

SELECT e.*, s.salary
FROM vw_Employees e
left join Salary s
ON e.emp_id = s.emp_id

ALTER VIEW vw_employees AS
SELECT e.*, s.salary
FROM vw_Employees e
LEFT JOIN Salary s
ON e.emp_id = s.emp_id