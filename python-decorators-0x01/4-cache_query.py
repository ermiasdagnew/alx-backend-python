import time
import sqlite3
import functools

# Cache dictionary to store query results
query_cache = {}

# Decorator from previous tasks
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


# ✅ New decorator for caching query results
def cache_query(func):
    """Decorator that caches database query results to avoid redundant calls"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else None
        
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            return query_cache[query]
        
        print(f"[CACHE MISS] Executing and caching result for: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result  # store in cache
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# ✅ First call will hit the database and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# ✅ Second call will return from cache (no DB hit)
users_again = fetch_users_with_cache(query="SELECT * FROM users")
