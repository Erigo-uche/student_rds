CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL     
);

COPY students(student_id, fullname)
FROM '/seed/student.csv'
DELIMITER ','
CSV HEADER;

SELECT setval(
    pg_get_serial_sequence('students', 'student_id'),
    MAX(student_id)
) FROM students;

CREATE TABLE courses (
    course_code VARCHAR(6) PRIMARY KEY,
    course VARCHAR(100) NOT NULL
);

COPY courses(course_code, course)
FROM '/seed/course.csv'
DELIMITER ','
CSV HEADER;


CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    course_code VARCHAR(6) NOT NULL,
    score DECIMAL(5,2) CHECK (score BETWEEN 0 AND 100),
    grade CHAR(1) GENERATED ALWAYS AS (
        CASE 
            WHEN score >= 70 THEN 'A'
            WHEN score >= 60 THEN 'B'
            WHEN score >= 50 THEN 'C'
            WHEN score >= 45 THEN 'D'
            WHEN score >= 40 THEN 'E'
            ELSE 'F'
        END
        
    ) STORED,

    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_student
        FOREIGN KEY(student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_course
        FOREIGN KEY(course_code)
        REFERENCES courses(course_code)
        ON DELETE CASCADE, 

    CONSTRAINT unique_student
        UNIQUE(student_id)
);

COPY grades(student_id, course_code, score)
FROM '/seed/grades.csv'
DELIMITER ','
CSV HEADER;
