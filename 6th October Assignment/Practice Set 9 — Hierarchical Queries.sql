DROP DATABASE IF EXISTS company_structure_db;
CREATE DATABASE company_structure_db;
USE company_structure_db;

CREATE TABLE staff_hierarchy (
employee_id INT PRIMARY KEY,
employee_name VARCHAR(100),
manager_id INT,
designation VARCHAR(100)
);

INSERT INTO staff_hierarchy VALUES
(1, 'Raj Malhotra', NULL, 'CEO'),
(2, 'Meera Shah', 1, 'CTO'),
(3, 'Vikram Rao', 1, 'Sales Director'),
(4, 'Aman Khan', 2, 'Engineering Manager'),
(5, 'Sara Ali', 2, 'Data Manager'),
(6, 'Rohit Das', 4, 'Developer'),
(7, 'Priya Singh', 4, 'Developer'),
(8, 'Kabir Ahmed', 5, 'Data Engineer'),
(9, 'Neha Rao', 5, 'Data Analyst'),
(10, 'Imran Sheikh', 3, 'Sales Manager'),
(11, 'Pooja Jain', 10, 'Sales Executive');

-- 1
SELECT * FROM staff_hierarchy WHERE manager_id IS NULL;
-- 2
SELECT * FROM staff_hierarchy
WHERE manager_id = (SELECT employee_id FROM staff_hierarchy WHERE designation = 'CEO');
-- 3
SELECT * FROM staff_hierarchy
WHERE manager_id = (SELECT employee_id FROM staff_hierarchy WHERE designation = 'CTO');
-- 4
WITH RECURSIVE org AS (
SELECT employee_id, employee_name, manager_id, designation
FROM staff_hierarchy
WHERE manager_id IS NULL
UNION ALL
SELECT s.employee_id, s.employee_name, s.manager_id, s.designation
FROM staff_hierarchy s
JOIN org o ON s.manager_id = o.employee_id
)
SELECT * FROM org;
-- 5
WITH RECURSIVE org AS (
SELECT employee_id, employee_name, manager_id, designation, 1 AS level_no
FROM staff_hierarchy
WHERE manager_id IS NULL
UNION ALL
SELECT s.employee_id, s.employee_name, s.manager_id, s.designation, o.level_no + 1
FROM staff_hierarchy s
JOIN org o ON s.manager_id = o.employee_id
)
SELECT * FROM org;
-- 6
WITH RECURSIVE team AS (
SELECT employee_id, employee_name, manager_id, designation
FROM staff_hierarchy
WHERE manager_id = (SELECT employee_id FROM staff_hierarchy WHERE employee_name = 'Meera Shah')
UNION ALL
SELECT s.employee_id, s.employee_name, s.manager_id, s.designation
FROM staff_hierarchy s
JOIN team t ON s.manager_id = t.employee_id
)
SELECT * FROM team;
-- 7
WITH RECURSIVE team AS (
SELECT employee_id, employee_name, manager_id, designation
FROM staff_hierarchy
WHERE manager_id = (SELECT employee_id FROM staff_hierarchy WHERE employee_name = 'Aman Khan')
UNION ALL
SELECT s.employee_id, s.employee_name, s.manager_id, s.designation
FROM staff_hierarchy s
JOIN team t ON s.manager_id = t.employee_id
)
SELECT * FROM team;
-- 8
SELECT e.employee_name AS employee, m.employee_name AS manager
FROM staff_hierarchy e
LEFT JOIN staff_hierarchy m ON e.manager_id = m.employee_id;
-- 9
WITH RECURSIVE org AS (
SELECT employee_id, manager_id, 1 AS level_no
FROM staff_hierarchy
WHERE manager_id IS NULL
UNION ALL
SELECT s.employee_id, s.manager_id, o.level_no + 1
FROM staff_hierarchy s
JOIN org o ON s.manager_id = o.employee_id
)
SELECT level_no, COUNT(*) AS total_employees
FROM org
GROUP BY level_no
ORDER BY level_no;
-- 10
WITH RECURSIVE org AS (
SELECT employee_id, employee_name, designation, 1 AS level_no,
CAST(employee_name AS CHAR(500)) AS path
FROM staff_hierarchy
WHERE manager_id IS NULL
UNION ALL
SELECT s.employee_id, s.employee_name, s.designation, o.level_no + 1,
CONCAT(o.path, ' > ', s.employee_name)
FROM staff_hierarchy s
JOIN org o ON s.manager_id = o.employee_id
)
SELECT employee_name, designation, level_no, path
FROM org
ORDER BY path;