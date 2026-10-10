
DROP DATABASE IF EXISTS course_tracker;
CREATE DATABASE course_tracker CHARACTER SET utf8mb4;
USE course_tracker;

CREATE TABLE students (
    student_id   INT PRIMARY KEY AUTO_INCREMENT,
    full_name    VARCHAR(100) NOT NULL,
    email        VARCHAR(120) NOT NULL UNIQUE,
    signup_date  DATE NOT NULL
);

CREATE TABLE courses (
    course_id      INT PRIMARY KEY AUTO_INCREMENT,
    course_name    VARCHAR(120) NOT NULL,
    category       VARCHAR(60),
    duration_hours INT CHECK (duration_hours > 0)
);

CREATE TABLE enrollments (
    enrollment_id   INT PRIMARY KEY AUTO_INCREMENT,
    student_id      INT NOT NULL,
    course_id       INT NOT NULL,
    enrollment_date DATE NOT NULL,
    status          ENUM('active','completed','dropped') NOT NULL DEFAULT 'active',
    CONSTRAINT fk_enr_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_enr_course  FOREIGN KEY (course_id)  REFERENCES courses(course_id)  ON DELETE CASCADE,
    CONSTRAINT uq_student_course UNIQUE (student_id, course_id)
);

CREATE TABLE progress (
    progress_id    INT PRIMARY KEY AUTO_INCREMENT,
    enrollment_id  INT NOT NULL UNIQUE,
    completion_pct DECIMAL(5,2) NOT NULL DEFAULT 0 CHECK (completion_pct BETWEEN 0 AND 100),
    last_updated   DATE NOT NULL,
    CONSTRAINT fk_prog_enr FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id) ON DELETE CASCADE
);
