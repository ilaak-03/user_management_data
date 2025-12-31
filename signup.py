import os
import boto3
from cognito_utils import get_secret_hash
from db import get_db_connection
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
from cognito_utils import get_cognito_client
cognito = get_cognito_client()
cognito = boto3.client(
    "cognito-idp",
    region_name=os.environ.get("AWS_REGION", "ap-south-1")
)

def handle_signup(
    *,
    email,
    password,
    address,
    postal_code,
    username=None,
    phone_number=None,
    city=None,
    state=None,
    country=None
):
    conn = None
    cursor = None

    try:
        # ---------- Cognito Signup ----------
        response = cognito.sign_up(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            SecretHash=get_secret_hash(email),
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
                *([{"Name": "phone_number", "Value": phone_number}] if phone_number else [])
            ]
        )

        cognito_sub = response["UserSub"]

        # ---------- DB Inserts ----------
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1️⃣ Insert into users
        cursor.execute(
            """
            INSERT INTO users (cognito_sub, username, email, phone_number)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (cognito_sub, username or email, email, phone_number)
        )

        user_id = cursor.fetchone()[0]

        # 2️⃣ Insert into user_cognito_attributes
        cursor.execute(
            """
            INSERT INTO user_cognito_attributes (user_id)
            VALUES (%s)
            """,
            (user_id,)
        )

        # 3️⃣ Insert into user_addresses
        cursor.execute(
            """
            INSERT INTO user_addresses (
                user_id, address, city, state, postal_code, country
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, address, city, state, postal_code, country)
        )

        conn.commit()

        return {
            "message": "Signup successful. Please verify your email.",
            "user_id": user_id
        }

    except Exception as e:
        if conn:
            conn.rollback()
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def handle_confirm_signup(email, code):
    try:
        cognito.confirm_sign_up(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            SecretHash=get_secret_hash(email),
            Username=email,
            ConfirmationCode=code
        )
        return {"message": "Email confirmed successfully"}

    except Exception as e:
        # Generalized exception for any Cognito error
        return {"error": str(e)}
