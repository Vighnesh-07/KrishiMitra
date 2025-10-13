# db.py

import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Global variable for the connection pool
db_pool = None

try:
    # Create a connection pool when the application starts.
    # minconn=1: The pool will always have at least 1 open connection.
    # maxconn=10: The pool can have a maximum of 10 open connections.
    db_pool = psycopg2.pool.SimpleConnectionPool(
        1, 10, dsn=os.getenv("DATABASE_URL")
    )
    print("✅ Database connection pool created successfully.")
except Exception as e:
    print(f"❌ Error creating database connection pool: {e}")
    # The application will not be able to connect to the database.

def get_db_connection():
    """Borrows a connection from the pool."""
    if db_pool:
        return db_pool.getconn()
    else:
        raise Exception("Database connection pool is not initialized.")

def release_db_connection(conn):
    """Returns a connection to the pool."""
    if db_pool:
        db_pool.putconn(conn)