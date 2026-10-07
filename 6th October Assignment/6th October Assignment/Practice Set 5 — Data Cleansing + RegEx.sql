DROP DATABASE IF EXISTS registration_data_db;
CREATE DATABASE registration_data_db;
USE registration_data_db;

CREATE TABLE registrations (
registration_id INT PRIMARY KEY,
full_name VARCHAR(100),
email VARCHAR(100),
mobile VARCHAR(40),
city VARCHAR(50),
postal_code VARCHAR(20)
);

INSERT INTO registrations VALUES
(1, ' rohit sharma ', ' ROHIT@GMAIL.COM ', '+91-98765-43210', 'hyderabad ', '500001'),
(2, 'SARA KHAN', 'sara@yahoo.com', '99887 66554', ' MUMBAI ', '400001'),
(3, ' amit patel ', '', '(040)99887766', 'Hyderabad', '500 032'),
(4, 'Neha Singh ', NULL, '9876543210', 'BANGALORE', '560001'),
(5, 'imran ali', 'IMRAN@MAIL.COM ', '91 9988772211', NULL, '500084'),
(6, 'Priya Rao', 'priya@gmail', '98765-AB210', 'Pune', '411001');

-- 1
SELECT TRIM(full_name) AS full_name FROM registrations;
-- 2
SELECT UPPER(TRIM(full_name)) AS full_name FROM registrations;
-- 3
SELECT LOWER(TRIM(email)) AS email FROM registrations;
-- 4
SELECT NULLIF(TRIM(email), '') AS email FROM registrations;
-- 5
SELECT REPLACE(REPLACE(mobile, ' ', ''), '-', '') AS mobile FROM registrations;
-- 6
SELECT REGEXP_REPLACE(mobile, '[^0-9]', '') AS mobile FROM registrations;
-- 7
SELECT UPPER(TRIM(city)) AS city FROM registrations;
-- 8
SELECT * FROM registrations WHERE city IS NULL;
-- 9
SELECT * FROM registrations WHERE email IS NULL OR TRIM(email) = '';
-- 10
SELECT * FROM registrations
WHERE LOWER(TRIM(email)) REGEXP 'gmail\\.com$';
-- 11
SELECT * FROM registrations
WHERE email IS NOT NULL AND TRIM(email) <> ''
AND LOWER(TRIM(email)) NOT REGEXP '^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}$';
-- 12
SELECT registration_id, REGEXP_REPLACE(postal_code, '[^0-9]', '') AS postal_code
FROM registrations;
-- 13
SELECT * FROM registrations WHERE mobile REGEXP '[A-Za-z]';
-- 14
SELECT UPPER(TRIM(full_name)) AS name,
NULLIF(LOWER(TRIM(email)), '') AS email,
REGEXP_REPLACE(mobile, '[^0-9]', '') AS mobile,
UPPER(TRIM(city)) AS city
FROM registrations;
-- 15
CREATE TABLE registrations_clean AS
SELECT registration_id,
UPPER(TRIM(full_name)) AS full_name,
NULLIF(LOWER(TRIM(email)), '') AS email,
REGEXP_REPLACE(mobile, '[^0-9]', '') AS mobile,
UPPER(TRIM(city)) AS city,
REGEXP_REPLACE(postal_code, '[^0-9]', '') AS postal_code
FROM registrations;