DROP DATABASE IF EXISTS call_centre_db;
CREATE DATABASE call_centre_db;
USE call_centre_db;

CREATE TABLE call_performance (
call_id INT PRIMARY KEY,
agent_name VARCHAR(100),
team VARCHAR(50),
calls_handled INT,
customer_rating DECIMAL(3,2),
performance_date DATE
);

INSERT INTO call_performance VALUES
(1, 'Aman', 'Alpha', 42, 4.50, '2026-09-01'),
(2, 'Sara', 'Alpha', 38, 4.70, '2026-09-01'),
(3, 'Ravi', 'Beta', 50, 4.20, '2026-09-01'),
(4, 'Neha', 'Beta', 45, 4.80, '2026-09-01'),
(5, 'Aman', 'Alpha', 48, 4.60, '2026-09-02'),
(6, 'Sara', 'Alpha', 44, 4.50, '2026-09-02'),
(7, 'Ravi', 'Beta', 46, 4.30, '2026-09-02'),
(8, 'Neha', 'Beta', 52, 4.90, '2026-09-02'),
(9, 'Kabir', 'Alpha', 41, 4.40, '2026-09-01'),
(10, 'Kabir', 'Alpha', 49, 4.60, '2026-09-02'),
(11, 'Pooja', 'Beta', 45, 4.70, '2026-09-01'),
(12, 'Pooja', 'Beta', 50, 4.80, '2026-09-02');

-- 1
SELECT *, SUM(calls_handled) OVER () AS total_calls
FROM call_performance;
-- 2
SELECT *, SUM(calls_handled) OVER (PARTITION BY team) AS team_total_calls
FROM call_performance;
-- 3
SELECT agent_name, team, calls_handled,
AVG(calls_handled) OVER (PARTITION BY team) AS team_avg_calls
FROM call_performance;
-- 4
SELECT *, AVG(customer_rating) OVER (PARTITION BY team) AS team_avg_rating
FROM call_performance;
-- 5
SELECT agent_name, performance_date, calls_handled,
SUM(calls_handled) OVER (PARTITION BY agent_name ORDER BY performance_date) AS running_total
FROM call_performance;
-- 6
SELECT team, performance_date, calls_handled,
SUM(calls_handled) OVER (PARTITION BY team ORDER BY performance_date) AS team_running_total
FROM call_performance;
-- 7
SELECT agent_name, team, calls_handled,
AVG(calls_handled) OVER (PARTITION BY team) AS team_avg,
calls_handled - AVG(calls_handled) OVER (PARTITION BY team) AS difference
FROM call_performance;
-- 8
SELECT agent_name, performance_date, calls_handled,
LAG(calls_handled) OVER (PARTITION BY agent_name ORDER BY performance_date) AS prev_day_calls
FROM call_performance;
-- 9
SELECT agent_name, performance_date, calls_handled,
calls_handled - LAG(calls_handled) OVER (PARTITION BY agent_name ORDER BY performance_date) AS difference
FROM call_performance;
-- 10
SELECT *, SUM(calls_handled) OVER (PARTITION BY agent_name) AS agent_total_calls
FROM call_performance;