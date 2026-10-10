USE course_tracker;

CREATE INDEX idx_enr_student ON enrollments (student_id);
CREATE INDEX idx_enr_course  ON enrollments (course_id);
CREATE INDEX idx_enr_status  ON enrollments (course_id, status);
CREATE INDEX idx_students_name ON students (full_name);


SHOW INDEX FROM enrollments;
EXPLAIN SELECT * FROM enrollments WHERE student_id = 10;
EXPLAIN SELECT * FROM enrollments WHERE course_id = 3;
