import sqlite3
import functools

# Reuse the decorator from the previous task
def with_db_connection(func):
    """Decorator that opens and closes the database connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# ✅ New decorator to manage transactions
def transactional(func):
    """Decorator to automatically commit or rollback database transactions"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()       # commit if everything is successful
            return result
        except Exception as e:
            conn.rollback()     # rollback if an error occurs
            print(f"Transaction failed: {e}")
            raise               # re-raise the error for debugging
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# 🔧 Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
