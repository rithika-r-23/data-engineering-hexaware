USE telecom_assessment;
-- 15
SELECT customer_id,
TRIM(customer_name) AS customer_name,
LOWER(NULLIF(TRIM(email), '')) AS email,
REGEXP_REPLACE(mobile, '[^0-9]', '') AS mobile FROM customers;
-- 16
SELECT customer_id,customer_name,mobile FROM customers
WHERE mobile REGEXP '[A-Za-z]';