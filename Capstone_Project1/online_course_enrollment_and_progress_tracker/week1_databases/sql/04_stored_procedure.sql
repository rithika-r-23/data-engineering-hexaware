USE course_tracker;
DROP PROCEDURE IF EXISTS sp_student_completion;
DROP PROCEDURE IF EXISTS sp_update_progress;

DELIMITER $$


CREATE PROCEDURE sp_student_completion(IN p_student_id INT)
BEGIN
    SELECT s.student_id,
           s.full_name,
           COUNT(e.enrollment_id)                                         AS courses_enrolled,
           COALESCE(SUM(e.status = 'completed'), 0)                       AS courses_completed,
           COALESCE(ROUND(100 * SUM(e.status = 'completed')
                          / NULLIF(COUNT(e.enrollment_id), 0), 2), 0)     AS completion_percentage,
           COALESCE(ROUND(AVG(p.completion_pct), 2), 0)                   AS avg_progress_pct
    FROM students s
    LEFT JOIN enrollments e ON e.student_id = s.student_id
    LEFT JOIN progress    p ON p.enrollment_id = e.enrollment_id
    WHERE s.student_id = p_student_id
    GROUP BY s.student_id, s.full_name;
END$$

-- Bonus: update progress and auto-mark the enrollment completed at 100%
CREATE PROCEDURE sp_update_progress(IN p_enrollment_id INT, IN p_pct DECIMAL(5,2))
BEGIN
    UPDATE progress SET completion_pct = p_pct, last_updated = CURDATE()
    WHERE enrollment_id = p_enrollment_id;
    IF p_pct >= 100 THEN
        UPDATE enrollments SET status = 'completed' WHERE enrollment_id = p_enrollment_id;
    END IF;
END$$

DELIMITER ;

-- Try it
CALL sp_student_completion(1);
CALL sp_update_progress(1, 80);
