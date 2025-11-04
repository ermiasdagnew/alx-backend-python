import sqlite3

class DatabaseConnection:
    """Custom class-based context manager for SQLite database connections"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Open the connection
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # this will be used inside the `with` block

    def __exit__(self, exc_type, exc_value, traceback):
        # Commit changes if no exception, else rollback
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
