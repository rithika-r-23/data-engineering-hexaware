CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;
CREATE TABLE sales_orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    product_category VARCHAR(50),
    product_name VARCHAR(100)
    quantity INT,
    unit_price DECIMAL(10,2),
    salesperson VARCHAR(100),
    order_date DATE
);
INSERT INTO sales_orders VALUES
(101, 'Amit Sharma', 'Hyderabad', 'Electronics', 'Laptop', 1, 55000, 'Rahul', '2026-01-05'),
(102, 'Sara Khan', 'Mumbai', 'Electronics', 'Mobile', 2, 25000, 'Neha', '2026-01-06'),
(103, 'Vikram Rao', 'Hyderabad', 'Furniture', 'Office Chair', 4, 7000, 'Rahul', '2026-01-07'),
(104, 'Meera Nair', 'Bangalore', 'Electronics', 'Tablet', 3, 18000, 'Arjun', '2026-01-08'),
(105, 'Ravi Kumar', 'Delhi', 'Furniture', 'Desk', 2, 15000, 'Neha', '2026-01-10'),
(106, 'Fatima Ali', 'Hyderabad', 'Accessories', 'Keyboard', 5, 2500, 'Rahul', '2026-01-11'),
(107, 'Arjun Mehta', 'Mumbai', 'Accessories', 'Mouse', 10, 1200, 'Arjun', '2026-01-12'),
(108, 'Priya Singh', 'Bangalore', 'Electronics', 'Laptop', 2, 60000, 'Neha', '2026-01-15'),
(109, 'Sameer Khan', 'Hyderabad', 'Furniture', 'Bookshelf', 3, 9000, 'Rahul', '2026-01-16'),
(110, 'Anjali Verma', 'Delhi', 'Electronics', 'Mobile', 4, 22000, 'Arjun', '2026-01-18'),
(111, 'Kiran Reddy', 'Hyderabad', 'Accessories', 'Headphones', 6, 3000, 'Neha', '2026-01-20'),
(112, 'Sneha Patel', 'Mumbai', 'Furniture', 'Office Chair', 5, 7500, 'Rahul', '2026-01-21'),
(113, 'Raj Malhotra', 'Delhi', 'Accessories', 'Keyboard', 8, 2800, 'Arjun', '2026-01-23'),
(114, 'Nisha Gupta', 'Bangalore', 'Electronics', 'Monitor', 3, 16000, 'Neha', '2026-01-24'),
(115, 'Imran Sheikh', 'Hyderabad', 'Electronics', 'Mobile', 3, 24000, 'Rahul', '2026-01-25'),
(116, 'Pooja Rao', 'Mumbai', 'Furniture', 'Desk', 2, 14000, 'Arjun', '2026-01-26'),
(117, 'Adil Khan', 'Delhi', 'Electronics', 'Laptop', 1, 58000, 'Neha', '2026-01-28'),
(118, 'Kavya Reddy', 'Hyderabad', 'Accessories', 'Mouse', 7, 1500, 'Rahul', '2026-01-29'),
(119, 'Mohit Jain', 'Bangalore', 'Furniture', 'Desk', 3, 15500, 'Arjun', '2026-01-30'),
(120, 'Zoya Ahmed', 'Mumbai', 'Electronics', 'Monitor', 2, 17000, 'Neha', '2026-02-01');

SELECT * 
FROM sales_orders
WHERE city = 'Hyderabad'
AND unit_price = 10000;

SELECT * 
FROM sales_orders
WHERE city = 'Hyderabad'
AND unit_price > 10000;

SELECT SUM(quantity * unit_price) AS total_sales
FROM sales_orders;

SELECT SUM(quantity * unit_price) AS total_sales
FROM sales_orders;

SELECT COUNT(*) FROM sales_orders;

SELECT AVG(unit_price) AS average_price
FROM sales_orders;

SELECT MAX(unit_price) AS highest_price
FROM sales_orders;

SELECT salesperson,
COUNT(*) AS total_orders
FROM sales_orders
GROUP BY salesperson;

SELECT city,
SUM(quantity * unit_price) AS total_sales
FROM sales_orders
WHERE product_category = 'Electronics'
GROUP BY city
HAVING SUM(quantity * unit_price) > 50000
ORDER BY total_sales DESC;

SELECT city,
SUM(quantity * unit_price) AS total_sales
FROM sales_orders
WHERE product_category = 'Electronics'
GROUP BY city
HAVING SUM(quantity * unit_price) > 50000
ORDER BY total_sales ASC;