import sqlite3


def write_record(date, record):
    with sqlite3.connect("local.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                value TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT INTO records (date, value) VALUES (?, ?)
        ''', (date, record))
        conn.commit()


def read_record(date):
    with sqlite3.connect("local.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT value FROM records
            WHERE date = ?
        ''', (date,))
        return cursor.fetchone()
