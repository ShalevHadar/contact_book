import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse
from src.config import Config

db_url = urlparse(Config.DATABASE_URL)

def create_database():
    """Ensure the database exists before running migrations."""
    conn = psycopg2.connect(
        dbname="postgres",  # Connect to the default DB first
        user=db_url.username,
        password=db_url.password,
        host=db_url.hostname,
        port=db_url.port,
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Check if the database exists
    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_url.path[1:]])
    exists = cursor.fetchone()

    if not exists:
        print(f"Database {db_url.path[1:]} does not exist. Creating it now...")
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_url.path[1:])))
    else:
        print(f"Database {db_url.path[1:]} already exists.")

    cursor.close()
    conn.close()
