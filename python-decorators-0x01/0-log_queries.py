import sqlite3
import functools
import os

# Ensure the database exists
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
        # Insert sample data
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com"))
        conn.commit()
        conn.close()

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"[LOG] Executing SQL Query: {query}")
        return func(query, *args, **kwargs)
    return wrapper

# Function to fetch all users
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Initialize database and fetch users
if __name__ == "__main__":
    initialize_db()
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
