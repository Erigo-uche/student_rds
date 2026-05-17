import psycopg2
import bleach
from flask import current_app
import logging

def connection():
    return psycopg2.connect(
        database = current_app.config["DB_NAME"],
        user = current_app.config["DB_USER"],
        password = current_app.config["DB_PASSWORD"],
        host = current_app.config["DB_HOST"],
        port = current_app.config["DB_PORT"]
    )

def get_students():
    try:
        with connection() as db:
            with db.cursor() as c:
                c.execute("SELECT * FROM students ORDER BY student_id")
                return c.fetchall()
    except psycopg2.Error:
        current_app.logger.exception("Failed to fetch students")
        raise 

def add_students(name):
    try:
        with connection() as db:
            with db.cursor() as c:
                c.execute("INSERT INTO students(fullname) VALUES (%s)", (bleach.clean(name),))
    except psycopg2.Error:
        current_app.logger.exception("Failed to add student")
        raise

def get_courses():
    try:
        with connection() as db:
            with db.cursor() as c:
                c.execute("SELECT * FROM courses")
                return c.fetchall()
    except psycopg2.Error:
        current_app.logger.exception("Failed to fetch courses")
        raise 

def get_grades(): 
    try:
        with connection() as db:
            with db.cursor() as c:
                c.execute("""
                    SELECT students.fullname, grades.course_code, grade.score, grades.grade
                    FROM grades
                    JOIN students ON grades.student_id = students.student_id
                    ORDER BY grades.grade
                """)
                return c.fetchall()
    except psycopg2.Error:
        current_app.logger.exception("Failed to fetch students' grades")
        raise 

def add_grades(student_id, course_code, score):
    try:
        with connection() as db:
            with db.cursor() as c:
                c.execute("INSERT INTO grades(student_id, course_id, score) VALUES (%s, %s, %s)", 
                          (student_id, course_code, score)
                          )
    except psycopg2.Error:
        current_app.logger.exception("Failed to add grade")
        raise

