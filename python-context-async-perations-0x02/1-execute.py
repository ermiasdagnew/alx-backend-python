import sqlite3

class ExecuteQuery:
    """Context manager that executes a query with optional parameters"""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.results = None

    def __enter__(self):
        # Open connection and execute query
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results  # return the query results to the with block

    def __exit__(self, exc_type, exc_value, traceback):
        # Commit if no exception, rollback otherwise
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()


# Usage Example
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)  # Parameters must be a tuple

    # Execute the query using the context manager
    with ExecuteQuery("users.db", query, param) as results:
        for row in results:
            print(row)
