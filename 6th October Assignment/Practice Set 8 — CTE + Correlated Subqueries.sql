DROP DATABASE IF EXISTS insurance_claims_db;
CREATE DATABASE insurance_claims_db;
USE insurance_claims_db;

CREATE TABLE insurance_claims (
claim_id INT PRIMARY KEY,
customer_name VARCHAR(100),
insurance_type VARCHAR(50),
claim_amount DECIMAL(12,2),
branch VARCHAR(50)
);

INSERT INTO insurance_claims VALUES
(1, 'Ajay Kumar', 'Health', 75000, 'Hyderabad'),
(2, 'Meena Shah', 'Motor', 45000, 'Mumbai'),
(3, 'Rohit Jain', 'Health', 125000, 'Hyderabad'),
(4, 'Sara Ali', 'Travel', 30000, 'Delhi'),
(5, 'Vikas Rao', 'Motor', 85000, 'Mumbai'),
(6, 'Nisha Singh', 'Health', 60000, 'Delhi'),
(7, 'Imran Khan', 'Travel', 55000, 'Hyderabad'),
(8, 'Pooja Patel', 'Motor', 40000, 'Delhi'),
(9, 'Karan Mehta', 'Health', 150000, 'Mumbai'),
(10, 'Farah Ahmed', 'Travel', 35000, 'Hyderabad');

-- 1
WITH type_total AS (
SELECT insurance_type, SUM(claim_amount) AS total_claims
FROM insurance_claims
GROUP BY insurance_type
)
SELECT * FROM type_total;
-- 2
WITH branch_total AS (
SELECT branch, SUM(claim_amount) AS total_claims
FROM insurance_claims
GROUP BY branch
)
SELECT * FROM branch_total;
-- 3
WITH type_total AS (
SELECT insurance_type, SUM(claim_amount) AS total_claims
FROM insurance_claims
GROUP BY insurance_type
)
SELECT * FROM type_total WHERE total_claims > 200000;
-- 4
WITH avg_claim AS (
SELECT AVG(claim_amount) AS avg_amount FROM insurance_claims
)
SELECT c.*
FROM insurance_claims c, avg_claim a
WHERE c.claim_amount > a.avg_amount;
-- 5
WITH type_total AS (
SELECT insurance_type, SUM(claim_amount) AS total_claims
FROM insurance_claims
GROUP BY insurance_type
)
SELECT insurance_type, total_claims,
RANK() OVER (ORDER BY total_claims DESC) AS type_rank
FROM type_total;
-- 6
WITH type_total AS (
SELECT insurance_type, SUM(claim_amount) AS type_amount
FROM insurance_claims
GROUP BY insurance_type
),
branch_total AS (
SELECT branch, SUM(claim_amount) AS branch_amount
FROM insurance_claims
GROUP BY branch
)
SELECT c.claim_id, c.customer_name, c.insurance_type, c.branch,
c.claim_amount, t.type_amount, b.branch_amount
FROM insurance_claims c
JOIN type_total t ON c.insurance_type = t.insurance_type
JOIN branch_total b ON c.branch = b.branch;
-- 7
SELECT * FROM insurance_claims c
WHERE claim_amount > (SELECT AVG(claim_amount) FROM insurance_claims
WHERE insurance_type = c.insurance_type);
-- 8
SELECT * FROM insurance_claims c
WHERE claim_amount > (SELECT AVG(claim_amount) FROM insurance_claims
WHERE branch = c.branch);
-- 9
SELECT * FROM insurance_claims c
WHERE claim_amount = (SELECT MAX(claim_amount) FROM insurance_claims
WHERE insurance_type = c.insurance_type);
-- 10
SELECT customer_name, branch, claim_amount
FROM insurance_claims c
WHERE claim_amount > (SELECT AVG(claim_amount) FROM insurance_claims
WHERE branch = c.branch);