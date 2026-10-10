USE course_tracker;


INSERT INTO students (full_name, email, signup_date)
VALUES ('Test Student', 'test.student@example.com', CURDATE());

-- New enrollment (use the id of the student just created) + its progress row
SET @new_student = LAST_INSERT_ID();
INSERT INTO enrollments (student_id, course_id, enrollment_date, status)
VALUES (@new_student, 1, CURDATE(), 'active');
SET @new_enrollment = LAST_INSERT_ID();
INSERT INTO progress (enrollment_id, completion_pct, last_updated)
VALUES (@new_enrollment, 0, CURDATE());


SELECT s.full_name, c.course_name, e.enrollment_date, e.status, p.completion_pct
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses  c ON c.course_id  = e.course_id
JOIN progress p ON p.enrollment_id = e.enrollment_id
ORDER BY e.enrollment_date DESC
LIMIT 20;


SELECT c.course_name, COUNT(*) AS total_enrolled
FROM enrollments e JOIN courses c ON c.course_id = e.course_id
GROUP BY c.course_name ORDER BY total_enrolled DESC;

SELECT c.course_name,
       COUNT(*)                                   AS enrolled,
       SUM(e.status = 'completed')                AS completed,
       SUM(e.status = 'dropped')                  AS dropped,
       ROUND(100 * SUM(e.status = 'completed') / COUNT(*), 1) AS completion_rate_pct
FROM enrollments e JOIN courses c ON c.course_id = e.course_id
GROUP BY c.course_name ORDER BY completion_rate_pct DESC;

UPDATE progress SET completion_pct = 45, last_updated = CURDATE()
WHERE enrollment_id = @new_enrollment;

UPDATE progress SET completion_pct = 100, last_updated = CURDATE()
WHERE enrollment_id = @new_enrollment;
UPDATE enrollments SET status = 'completed' WHERE enrollment_id = @new_enrollment;


DELETE FROM students WHERE student_id = @new_student;
