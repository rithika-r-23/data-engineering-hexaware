CREATE DATABASE training_db;
USE training_db;

CREATE TABLE employees
(
emp_id INT PRIMARY KEY,
emp_name VARCHAR(100),
department VARCHAR(50),
salary DECIMAL(10,2),
city VARCHAR(50)
);
