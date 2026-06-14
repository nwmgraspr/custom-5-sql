"""library_sqlite_project.py - Project script

Author: Ralph Massaquoi
Date: 2026

"""
Purpose:
- Read files into a SQLite database.
- Use Python to automate SQL scripts (stored in files).
- Log the pipeline process.
"""

import sqlite3


def connect(db_name="library.db"):
    return sqlite3.connect(db_name)


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        member_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        genre TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        loan_id INTEGER PRIMARY KEY,
        member_id INTEGER,
        book_id INTEGER,
        loan_days INTEGER,
        FOREIGN KEY(member_id) REFERENCES members(member_id),
        FOREIGN KEY(book_id) REFERENCES books(book_id)
    );
    """)

    conn.commit()


def insert_data(conn):
    cursor = conn.cursor()

    members = [
        (1, "Alice", "Omaha"),
        (2, "Bob", "Lincoln"),
        (3, "Charlie", "Des Moines"),
        (4, "Diana", "Chicago"),
        (5, "Ethan", "Dallas"),
        (6, "Fiona", "Denver"),
        (7, "George", "Seattle"),
        (8, "Hannah", "Austin"),
        (9, "Ian", "Boston"),
        (10, "Julia", "Miami"),
        (11, "Kevin", "Phoenix"),
        (12, "Laura", "Atlanta")
    ]

    books = [
        (1, "1984", "Dystopian"),
        (2, "To Kill a Mockingbird", "Fiction"),
        (3, "The Hobbit", "Fantasy"),
        (4, "Dune", "Sci-Fi"),
        (5, "Moby Dick", "Classic"),
        (6, "Hamlet", "Drama"),
        (7, "Pride and Prejudice", "Romance"),
        (8, "The Catcher in the Rye", "Fiction"),
        (9, "Brave New World", "Dystopian"),
        (10, "The Great Gatsby", "Classic"),
        (11, "The Lord of the Rings", "Fantasy"),
        (12, "Fahrenheit 451", "Dystopian")
    ]

    loans = [
        (1, 1, 1, 7),
        (2, 2, 3, 5),
        (3, 3, 4, 10),
        (4, 4, 2, 6),
        (5, 5, 6, 4),
        (6, 6, 7, 8),
        (7, 7, 11, 12),
        (8, 8, 9, 3),
        (9, 9, 10, 9),
        (10, 10, 5, 11),
        (11, 11, 8, 2),
        (12, 12, 12, 14)
    ]

    cursor.executemany(
        "INSERT OR REPLACE INTO members VALUES (?, ?, ?);", members
    )
    cursor.executemany(
        "INSERT OR REPLACE INTO books VALUES (?, ?, ?);", books
    )
    cursor.executemany(
        "INSERT OR REPLACE INTO loans VALUES (?, ?, ?, ?);", loans
    )

    conn.commit()


def query_member_activity(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        m.name,
        m.city,
        COUNT(l.loan_id) AS total_loans,
        SUM(l.loan_days) AS total_days_borrowed
    FROM members m
    JOIN loans l ON m.member_id = l.member_id
    GROUP BY m.member_id
    ORDER BY total_loans DESC;
    """)

    return cursor.fetchall()


def query_book_popularity(conn):
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        b.title,
        b.genre,
        COUNT(l.loan_id) AS times_borrowed,
        AVG(l.loan_days) AS avg_loan_days
    FROM books b
    JOIN loans l ON b.book_id = l.book_id
    GROUP BY b.book_id
    ORDER BY times_borrowed DESC;
    """)

    return cursor.fetchall()


def main():
    conn = connect()

    create_tables(conn)
    insert_data(conn)

    print("\n📊 MEMBER ACTIVITY REPORT")
    for row in query_member_activity(conn):
        print(row)

    print("\n📊 BOOK POPULARITY REPORT")
    for row in query_book_popularity(conn):
        print(row)

    conn.close()


if __name__ == "__main__":
    main()
