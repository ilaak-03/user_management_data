from dotenv import load_dotenv
# Load environment variables from .env
load_dotenv()
import os
import hmac
import hashlib
import base64
import boto3


def get_cognito_client():
    region = os.environ.get("AWS_REGION", "ap-south-1")
    return boto3.client("cognito-idp", region_name=region)


def get_secret_hash(username):
    msg = username + os.environ["COGNITO_CLIENT_ID"]
    key = os.environ["COGNITO_CLIENT_SECRET"]
    dig = hmac.new(
        key.encode("utf-8"),
        msg.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()
