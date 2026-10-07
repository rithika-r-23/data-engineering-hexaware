DROP DATABASE IF EXISTS restaurant_menu_db;
CREATE DATABASE restaurant_menu_db;

USE restaurant_menu_db;
CREATE TABLE menu_items (
item_id INT PRIMARY KEY,
item_name VARCHAR(100),
category VARCHAR(50),
price DECIMAL(10,2),
available_qty INT
);

INSERT INTO menu_items VALUES
(1, 'Chicken Biryani', 'Main Course', 320, 25),
(2, 'Paneer Tikka', 'Starter', 240, 15),
(3, 'Masala Dosa', 'Breakfast', 120, 30),
(4, 'Veg Burger', 'Fast Food', 180, 10),
(5, 'Cold Coffee', 'Beverage', 150, 20),
(6, 'Chicken Burger', 'Fast Food', 220, 8),
(7, 'Idli', 'Breakfast', 80, 40),
(8, 'Fresh Lime', 'Beverage', 90, 0);

-- 1
SELECT * FROM menu_items;
-- 2
SELECT item_name, price FROM menu_items;
-- 3
INSERT INTO menu_items VALUES (9, 'Gulab Jamun', 'Dessert', 100, 20);
-- 4
UPDATE menu_items SET price = 350 WHERE item_name = 'Chicken Biryani';
-- 5
UPDATE menu_items SET price = price + price * 0.10 WHERE category = 'Fast Food';
-- 6
UPDATE menu_items SET available_qty = available_qty - 2 WHERE item_name = 'Veg Burger';
-- 7
DELETE FROM menu_items WHERE available_qty = 0;
-- 8
SELECT * FROM menu_items WHERE price > 200;
-- 9
SELECT * FROM menu_items WHERE price BETWEEN 100 AND 250;
-- 10
SELECT * FROM menu_items WHERE category = 'Breakfast';
-- 11
SELECT * FROM menu_items WHERE category = 'Breakfast' OR category = 'Beverage';
-- 12
SELECT * FROM menu_items WHERE item_name LIKE '%Chicken%';
-- 13
SELECT * FROM menu_items ORDER BY price DESC;
-- 14
SELECT * FROM menu_items ORDER BY price DESC LIMIT 3;
-- 15
SELECT * FROM menu_items WHERE available_qty < 15;