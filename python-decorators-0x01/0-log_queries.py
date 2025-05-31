import sqlite3
import functools
from datetime import datetime

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"[SQL LOG] Executing query: {query}")
        else:
            print("[SQL LOG] No query found to log.")
        return func(*args, **kwargs)
    return wrapper


def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO users (id, name, email) VALUES (1, "Alice", "alice@example.com")')
    cursor.execute('INSERT OR IGNORE INTO users (id, name, email) VALUES (2, "Bob", "bob@example.com")')
    conn.commit()
    conn.close()

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Setup the database and create the users table
setup_database()


# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")

print(users)
