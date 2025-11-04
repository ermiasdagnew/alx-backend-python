import sqlite3

# 1️⃣ Class-based context manager
class DatabaseConnection:
    """Custom class-based context manager for SQLite database"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()


# 2️⃣ Use the context manager with the with statement
with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # ✅ This line is required
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)
