import sqlite3
import functools
import os

DB_FILE = 'users.db'

def initialize_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com"))
        conn.commit()
        conn.close()

def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"[LOG] Executing SQL Query: {query}")
        return func(query, *args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    initialize_db()
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
