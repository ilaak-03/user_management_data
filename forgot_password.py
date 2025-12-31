import os
from cognito_utils import get_secret_hash
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
from cognito_utils import get_cognito_client

def handle_forgot_password(email):
    try:
        cognito = get_cognito_client()
        cognito.forgot_password(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            SecretHash=get_secret_hash(email),
            Username=email
        )

        return {
            "message": "Password reset code sent to registered email"
        }

    except Exception as e:
        return {"error": str(e)}
