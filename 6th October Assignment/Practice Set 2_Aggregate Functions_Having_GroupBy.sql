DROP DATABASE IF EXISTS food_delivery_db;
CREATE DATABASE food_delivery_db;
USE food_delivery_db;

CREATE TABLE food_orders (
order_id INT PRIMARY KEY,
restaurant VARCHAR(100),
city VARCHAR(50),
food_type VARCHAR(50),
order_amount DECIMAL(10,2),
delivery_partner VARCHAR(50),
order_date DATE
);

INSERT INTO food_orders VALUES
(101, 'Spice Hub', 'Hyderabad', 'Indian', 850, 'Ravi', '2026-09-01'),
(102, 'Burger Zone', 'Hyderabad', 'Fast Food', 520, 'Kiran', '2026-09-01'),
(103, 'Pizza Point', 'Mumbai', 'Fast Food', 1100, 'Ravi', '2026-09-02'),
(104, 'Curry House', 'Bangalore', 'Indian', 760, 'Aman', '2026-09-02'),
(105, 'Spice Hub', 'Hyderabad', 'Indian', 1250, 'Kiran', '2026-09-03'),
(106, 'Sushi World', 'Mumbai', 'Japanese', 1800, 'Aman', '2026-09-03'),
(107, 'Pizza Point', 'Mumbai', 'Fast Food', 900, 'Ravi', '2026-09-04'),
(108, 'Curry House', 'Bangalore', 'Indian', 640, 'Kiran', '2026-09-04'),
(109, 'Burger Zone', 'Hyderabad', 'Fast Food', 430, 'Aman', '2026-09-05'),
(110, 'Sushi World', 'Mumbai', 'Japanese', 2100, 'Ravi', '2026-09-05'),
(111, 'Spice Hub', 'Hyderabad', 'Indian', 950, 'Aman', '2026-09-06'),
(112, 'Curry House', 'Bangalore', 'Indian', 880, 'Ravi', '2026-09-06');

-- 1
SELECT COUNT(*) AS total_orders FROM food_orders;
-- 2
SELECT SUM(order_amount) AS total_revenue FROM food_orders;
-- 3
SELECT AVG(order_amount) AS avg_order_value FROM food_orders;
-- 4
SELECT MAX(order_amount) AS highest_amount FROM food_orders;
-- 5
SELECT MIN(order_amount) AS lowest_amount FROM food_orders;
-- 6
SELECT city, SUM(order_amount) AS total_revenue FROM food_orders 
GROUP BY city;
-- 7
SELECT restaurant, COUNT(*) AS no_of_orders FROM food_orders 
GROUP BY restaurant;
-- 8
SELECT food_type, AVG(order_amount) AS avg_order_value FROM food_orders 
GROUP BY food_type;
-- 9
SELECT delivery_partner, SUM(order_amount) AS total_revenue FROM food_orders GROUP BY delivery_partner;
-- 10
SELECT city, COUNT(*) AS no_of_orders FROM food_orders GROUP BY city HAVING COUNT(*) > 3;
-- 11
SELECT restaurant, SUM(order_amount) AS total_revenue FROM food_orders 
GROUP BY restaurant HAVING SUM(order_amount) > 2000;
-- 12
SELECT delivery_partner, AVG(order_amount) AS avg_amount FROM food_orders 
GROUP BY delivery_partner 
HAVING AVG(order_amount) > 800;
-- 13
SELECT food_type, SUM(order_amount) AS total_revenue FROM food_orders 
GROUP BY food_type 
HAVING SUM(order_amount) > 2500;
-- 14
SELECT city, SUM(order_amount) AS total_revenue FROM food_orders 
GROUP BY city ORDER BY total_revenue DESC;
-- 15
SELECT restaurant, SUM(order_amount) AS total_revenue FROM food_orders 
GROUP BY restaurant
ORDER BY total_revenue 
DESC LIMIT 1;