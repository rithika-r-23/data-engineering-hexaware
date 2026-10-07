USE telecom_assessment;
-- 12
SELECT c.customer_name,p.plan_name,p.monthly_charge,s.status
FROM customers c
JOIN subscriptions s
ON c.customer_id = s.customer_id
JOIN plans p
ON s.plan_id = p.plan_id;

-- 13
SELECT c.customer_id,c.customer_name,c.city,c.email,s.subscription_id,s.plan_id,s.start_date,s.status
FROM customers c
LEFT JOIN subscriptions s
ON c.customer_id = s.customer_id;

-- 14
SELECT s.subscription_id,s.customer_id,s.plan_id,s.start_date,s.status
FROM subscriptions s
LEFT JOIN customers c
ON s.customer_id = c.customer_id
LEFT JOIN plans p
ON s.plan_id = p.plan_id
WHERE c.customer_id IS NULL
OR p.plan_id IS NULL;