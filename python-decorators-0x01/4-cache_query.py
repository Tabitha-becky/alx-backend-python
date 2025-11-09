import time
import sqlite3 
import functools

def with_db_connection(func):
    """Decorator to handle database connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

query_cache = {}

def cache_query(func):
    """Decorator to cache query results based on SQL query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from kwargs or args
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)
        
        # Check if query result is in cache
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        
        # Execute function and cache the result
        print(f"Executing and caching query: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")