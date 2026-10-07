USE telecom_assessment;
-- 8
SELECT COUNT(*) AS total_payments,
SUM(amount) AS total_amount_collected
FROM payments;
-- 9
SELECT customer_id,
SUM(amount) AS total_payment_amount
FROM payments
GROUP BY customer_id;

-- 10
SELECT customer_id,
SUM(amount) AS total_payment_amount
FROM payments
GROUP BY customer_id
HAVING SUM(amount) > 2000;

-- 11

SELECT customer_id,
AVG(amount) AS average_payment_amount
FROM payments
GROUP BY customer_id;