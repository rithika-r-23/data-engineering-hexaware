CREATE DATABASE shop_db;
USE shop_db;
CREATE TABLE products (
    product_id     INT PRIMARY KEY AUTO_INCREMENT,
    product_name   VARCHAR(100) NOT NULL,
    category       VARCHAR(50),
    price          DECIMAL(10,2),
    stock_quantity INT
);
INSERT INTO products (product_name, category, price, stock_quantity) VALUES
('Laptop',        'Electronics', 55000.00, 15),
('Smartphone',    'Electronics', 20000.00, 25),
('Office Chair',  'Furniture',    4500.00,  8),
('Notebook',      'Stationery',     60.00, 200),
('Running Shoes', 'Footwear',     2500.00, 12),
('Water Bottle',  'Accessories',   350.00,  5);
SELECT * FROM products;
SELECT product_name, price FROM products;

INSERT INTO products (product_name, category, price, stock_quantity)
VALUES ('Wireless Mouse', 'Electronics', 800.00, 40);

UPDATE products
SET price = 52000.00
WHERE product_id = 1;

UPDATE products
SET price = price * 1.10
WHERE category = 'Electronics';

UPDATE products
SET price = 52000.00
WHERE product_id = 1;

SELECT * FROM products WHERE price > 1000;
SELECT * FROM products WHERE stock_quantity < 10;
SELECT * FROM products WHERE category = 'Electronics';

SELECT * FROM products ORDER BY price DESC;
DELETE FROM products WHERE product_id = 6;
UPDATE products SET stock_quantity = 0 WHERE product_id = 4;
DELETE FROM products WHERE stock_quantity = 0;
DELETE FROM products WHERE stock_quantity = 0;

SELECT * FROM products;

