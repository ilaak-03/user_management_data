import os
from cognito_utils import get_secret_hash
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
from cognito_utils import get_cognito_client

def handle_reset_password(email, code, new_password):
    try:
        cognito = get_cognito_client()
        cognito.confirm_forgot_password(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            SecretHash=get_secret_hash(email),
            Username=email,
            ConfirmationCode=code,
            Password=new_password
        )

        return {
            "message": "Password reset successful"
        }

    except Exception as e:
        return {"error": str(e)}
