"""custom_sqlite_project.py - Project script (example).

Author: Ralph Massaquoi
Date: 2026

Purpose:
- Read files into a SQLite database.
- - Use Python to automate SQL scripts (stored in files).
- Log the pipeline process.


import sqlite3


def create_connection(db_name="school.db"):
    return sqlite3.connect(db_name)


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        major TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course_id INTEGER,
        grade REAL,
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(course_id) REFERENCES courses(course_id)
    );
    """)

    conn.commit()


def insert_data(conn):
    cursor = conn.cursor()

    students = [
        (1, "Alice", "Computer Science"),
        (2, "Bob", "Mathematics"),
        (3, "Charlie", "Physics"),
    ]

    courses = [(1, "Database Systems"), (2, "Calculus"), (3, "Physics I")]

    enrollments = [
        (1, 1, 1, 95),
        (2, 1, 2, 88),
        (3, 2, 2, 92),
        (4, 3, 3, 85),
        (5, 2, 1, 78),
    ]

    cursor.executemany("INSERT OR REPLACE INTO students VALUES (?, ?, ?);", students)
    cursor.executemany("INSERT OR REPLACE INTO courses VALUES (?, ?);", courses)
    cursor.executemany(
        "INSERT OR REPLACE INTO enrollments VALUES (?, ?, ?, ?);", enrollments
    )

    conn.commit()


#  SQL QUERY 1: Student enrollment summary
def query_student_summary(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        s.name,
        s.major,
        COUNT(e.course_id) AS courses_taken,
        ROUND(AVG(e.grade), 2) AS avg_grade
    FROM students s
    JOIN enrollments e ON s.student_id = e.student_id
    GROUP BY s.student_id;
    """)

    return cursor.fetchall()


#  SQL QUERY 2: Course performance
def query_course_performance(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        c.course_name,
        COUNT(e.student_id) AS total_students,
        ROUND(AVG(e.grade), 2) AS avg_course_grade
    FROM courses c
    JOIN enrollments e ON c.course_id = e.course_id
    GROUP BY c.course_id;
    """)

    return cursor.fetchall()


def main():
    conn = create_connection()

    create_tables(conn)
    insert_data(conn)

    print("\n📊 STUDENT SUMMARY")
    for row in query_student_summary(conn):
        print(row)

    print("\n📊 COURSE PERFORMANCE")
    for row in query_course_performance(conn):
        print(row)

    conn.close()


if __name__ == "__main__":
    main()
