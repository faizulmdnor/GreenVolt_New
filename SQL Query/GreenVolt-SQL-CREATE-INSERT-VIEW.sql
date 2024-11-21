IF EXISTS (SELECT * FROM sys.databases WHERE name='GreenVolt')
BEGIN
	DROP DATABASE GreenVolt
END;


/**Create new database GreenVolt**/
CREATE DATABASE GreenVolt;

USE GreenVolt;

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

CREATE TABLE Status(
	status_id INT PRIMARY KEY,
	status VARCHAR(12)
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
	status_id INT,
	FOREIGN KEY (origin_country_id) REFERENCES Country(country_id),
	FOREIGN KEY (gender_id) REFERENCES Gender(gender_id),
	FOREIGN KEY (dept_id) REFERENCES Departments(dept_id),
	FOREIGN KEY (site_id) REFERENCES Sites(site_ID),
	FOREIGN KEY (pos_id) REFERENCES Positions(pos_id),
	FOREIGN KEY (status_id) REFERENCES Status(status_id)
);


CREATE TABLE Employees_Performance(
	emp_id INT,
	Year INT,
	category VARCHAR(15),
	scores INT,
	FOREIGN KEY (emp_id) REFERENCES Employees(emp_id)
)

CREATE TABLE Monthly_Sales (
	emp_id INT,
	YearMonth DATE,
	totalSales MONEY,
	FOREIGN KEY (emp_id) REFERENCES Employees(emp_id)
);

INSERT INTO Gender(gender_id, Gender) 
VALUES (310,'Female'), (311, 'Male')

INSERT INTO Status(status_id, status) 
VALUES (1, 'active'), (0, 'inactive')

