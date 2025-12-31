import os
import json
import boto3
import pg8000
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# Cognito client
from cognito_utils import get_cognito_client

USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
cognito = get_cognito_client()

# Database connection from environment variables
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

def get_db_connection():
    return pg8000.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def handle_delete_user(event):
    headers = event.get("headers") or {}
    auth_header = headers.get("Authorization") or headers.get("authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"error": "Authorization header missing or invalid"}

    access_token = auth_header.replace("Bearer ", "")

    try:
        # 1. Get user info from Cognito access token
        user_info = cognito.get_user(AccessToken=access_token)
        email = next((a["Value"] for a in user_info["UserAttributes"] if a["Name"] == "email"), None)

        if not email:
            return {"error": "Email not found for user"}

        # 2. Delete user from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE email = %s RETURNING email", (email,))
        deleted = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        if not deleted:
            return {"error": f"No user found in database with email {email}"}

        # 3. Delete user from Cognito
        cognito.delete_user(AccessToken=access_token)

        # 4. Return success message
        return {"message": f"User with email {email} deleted successfully"}

    except cognito.exceptions.NotAuthorizedException:
        return {"error": "Invalid or expired token"}
    except Exception as e:
        return {"error": str(e)}
