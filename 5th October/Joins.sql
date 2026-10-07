Drop database if exists Joins;
Create database Joins;
use Joins;


CREATE TABLE customers (
customer_id INT PRIMARY KEY,
customer_name VARCHAR(100),
city VARCHAR(50)
);

CREATE TABLE orders (
order_id INT PRIMARY KEY,
customer_id INT,
product_name VARCHAR(100),
amount DECIMAL(10,2)
);

INSERT INTO customers VALUES
(1, 'Amit Sharma', 'Hyderabad'),
(2, 'Sara Khan', 'Mumbai'),
(3, 'Rahul Verma', 'Delhi'),
(4, 'Neha Singh', 'Bangalore'),
(5, 'Imran Ali', 'Hyderabad'),
(6, 'Priya Rao', 'Pune'),
(7, 'Arjun Mehta', NULL);

INSERT INTO orders VALUES
(101, 1, 'Laptop', 55000),
(102, 2, 'Mobile', 25000),
(103, 1, 'Keyboard', 3000),
(104, 3, 'Monitor', 18000),
(105, 4, 'Laptop', 62000),
(106, 2, 'Headphones', 5000),
(107, 5, 'Tablet', 30000),
(108, 10, 'Printer', 22000),
(109, NULL, 'Mouse', 1500);

SELECT 
c.customer_id,
c.customer_name,
o.order_id,
o.product_name,
o.amount
FROM customers c
INNER JOIN orders o 
ON c.customer_id = o.customer_id;

SELECT 
c.customer_id,
c.customer_name,
o.order_id,
o.product_name,
o.amount
FROM customers c
LEFT JOIN orders o 
ON c.customer_id = o.customer_id;

SELECT 
c.customer_id,
c.customer_name,
o.order_id,
o.product_name,
o.amount
FROM customers c
RIGHT JOIN orders o 
ON c.customer_id = o.customer_id;

SELECT 
c.customer_id,
c.customer_name
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

SELECT 
o.order_id,
o.customer_id,
o.product_name,
o.amount
FROM customers c
RIGHT JOIN orders o
ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;