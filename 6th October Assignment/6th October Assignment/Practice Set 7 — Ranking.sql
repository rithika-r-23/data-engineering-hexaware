USE call_centre_db;

-- 1
SELECT *, RANK() OVER (ORDER BY calls_handled DESC) AS call_rank
FROM call_performance;
-- 2
SELECT *, ROW_NUMBER() OVER (ORDER BY calls_handled DESC) AS row_num
FROM call_performance;
-- 3
SELECT *, RANK() OVER (ORDER BY calls_handled DESC) AS call_rank
FROM call_performance;
-- 4
SELECT *, DENSE_RANK() OVER (ORDER BY calls_handled DESC) AS dense_rank_no
FROM call_performance;
-- 5
SELECT agent_name, calls_handled,
ROW_NUMBER() OVER (ORDER BY calls_handled DESC) AS row_num,
RANK() OVER (ORDER BY calls_handled DESC) AS rank_no,
DENSE_RANK() OVER (ORDER BY calls_handled DESC) AS dense_rank_no
FROM call_performance;
-- 6
SELECT team, agent_name, calls_handled,
RANK() OVER (PARTITION BY team ORDER BY calls_handled DESC) AS team_rank
FROM call_performance;
-- 7
SELECT *, RANK() OVER (ORDER BY customer_rating DESC) AS rating_rank
FROM call_performance;
-- 8
WITH ranked AS (
SELECT *, ROW_NUMBER() OVER (PARTITION BY team ORDER BY calls_handled DESC) AS rn
FROM call_performance
)
SELECT * FROM ranked WHERE rn <= 3;
-- 9
WITH ranked AS (
SELECT *, ROW_NUMBER() OVER (PARTITION BY agent_name ORDER BY calls_handled DESC) AS rn
FROM call_performance
)
SELECT * FROM ranked WHERE rn = 1;
-- 10
SELECT agent_name, SUM(calls_handled) AS total_calls,
RANK() OVER (ORDER BY SUM(calls_handled) DESC) AS agent_rank
FROM call_performance
GROUP BY agent_name;