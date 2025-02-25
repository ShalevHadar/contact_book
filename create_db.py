import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB", "contact_book")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "testpass")
DB_HOST = os.getenv("POSTGRES_HOST", "database")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# Connect to the default `postgres` database
conn = psycopg2.connect(
    dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
conn.autocommit = True

cursor = conn.cursor()

# Check if the database exists
cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
exists = cursor.fetchone()

if not exists:
    print(f"Database {DB_NAME} does not exist. Creating it now...")
    cursor.execute(f"CREATE DATABASE {DB_NAME}")
    print(f"Database {DB_NAME} created successfully.")
else:
    print(f"Database {DB_NAME} already exists. Skipping creation.")

cursor.close()
conn.close()
