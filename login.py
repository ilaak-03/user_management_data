import os
from botocore.exceptions import ClientError
from cognito_utils import  get_secret_hash
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
from cognito_utils import get_cognito_client

def handle_login(email, password):
    try:
        cognito = get_cognito_client()
        resp = cognito.initiate_auth(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password,
                "SECRET_HASH": get_secret_hash(email)
            }
        )

        return {
            "message": "Login successful",
            "id_token": resp["AuthenticationResult"]["IdToken"],
            "access_token": resp["AuthenticationResult"]["AccessToken"],
            "refresh_token": resp["AuthenticationResult"]["RefreshToken"]
        }

    except ClientError as e:
        # Handles:
        # - UserNotConfirmedException
        # - NotAuthorizedException
        # - UserNotFoundException
        return {"error": e.response["Error"]["Message"]}

    except Exception as e:
        return {"error": str(e)}
