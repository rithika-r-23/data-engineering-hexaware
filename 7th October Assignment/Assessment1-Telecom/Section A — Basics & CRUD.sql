USE telecom_assessment;
-- 1
SELECT customer_name, city, email FROM customers;
-- 2
SELECT *
FROM customers WHERE city IN ('Hyderabad', 'Mumbai');
-- 3
SELECT * FROM customers WHERE customer_name LIKE '%a%';
-- 4
INSERT INTO customers VALUES (8, 'Karthik Kumar', 'Chennai', '9876543211', 'karthik@gmail.com');
-- 5
UPDATE customers SET city = 'Chennai' WHERE customer_id = 6;
-- 6
DELETE FROM customers WHERE customer_id = 8;
-- 7
SELECT *FROM customers ORDER BY customer_name ASC;