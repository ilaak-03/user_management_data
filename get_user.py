import json
import boto3
from db import get_db_connection 
from cognito_utils import get_cognito_client

cognito = get_cognito_client()

def handle_get_user(event):
    try:
        access_token = event["headers"].get("Authorization", "").replace("Bearer ", "")

        response = cognito.get_user(AccessToken=access_token)

        user_attrs = {
            a["Name"]: a["Value"]
            for a in response.get("UserAttributes", [])
        }

        cognito_sub = user_attrs.get("sub")
        email = user_attrs.get("email")
        phone_number = user_attrs.get("phone_number")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                u.username,
                u.phone_number,
                a.address,
                a.city,
                a.state,
                a.postal_code,
                a.country
            FROM users u
            LEFT JOIN user_addresses a
            ON a.user_id = u.id
            WHERE u.cognito_sub = %s
            """,
            (cognito_sub,)
        )

        row = cursor.fetchone()
        return {
            "username": row[0] if row else None,
            "email": email,
            "phone_number": row[1] if row else None,
            "address": {
                "address": row[2] if row else None,
                "city": row[3] if row else None,
                "state": row[4] if row else None,
                "postal_code": row[5] if row else None,
                "country": row[6] if row else None
            }
        }

    except Exception as e:
        return {"error": str(e)}
