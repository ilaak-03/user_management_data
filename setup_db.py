import os
import pg8000.native
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# Users table
CREATE_USERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    cognito_sub TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
"""

# User addresses table
CREATE_USER_ADDRESSES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS user_addresses (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    address TEXT NOT NULL,
    city TEXT,
    state TEXT,
    postal_code TEXT NOT NULL,
    country TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

# Cognito attributes table
CREATE_USER_COGNITO_ATTRIBUTES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS user_cognito_attributes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    nickname TEXT,
    middle_name TEXT,
    given_name TEXT,
    family_name TEXT,
    preferred_username TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

def create_tables():
    try:
        conn = pg8000.native.Connection(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        # Create tables
        conn.run(CREATE_USERS_TABLE_SQL)
        conn.run(CREATE_USER_ADDRESSES_TABLE_SQL)
        conn.run(CREATE_USER_COGNITO_ATTRIBUTES_TABLE_SQL)
        conn.close()
        print("All tables created successfully!")
    except Exception as e:
        print("Error creating tables:", str(e))

if __name__ == "__main__":
    create_tables()
