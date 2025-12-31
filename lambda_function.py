from dotenv import load_dotenv
# Load environment variables from .env
load_dotenv()
from flask import Flask, request, jsonify
from signup import handle_signup, handle_confirm_signup
from login import handle_login
from forgot_password import handle_forgot_password
from reset_password import handle_reset_password
from get_user import handle_get_user
from delete_user import handle_delete_user
from cognito_utils import get_cognito_client

app = Flask(__name__)

cognito = get_cognito_client()
# -------------------------
# READ (GET)
# -------------------------
@app.route("/auth/get-users", methods=["GET"])
def get_users():
    # pass request headers / args similar to event
    result = handle_get_user({
        "headers": dict(request.headers),
        "queryStringParameters": request.args
    })

    return jsonify(result), (400 if "error" in result else 200)


# -------------------------
# CREATE (POST)
# -------------------------
@app.route("/auth/signup", methods=["POST"])
def signup():
    body = request.get_json()

    result = handle_signup(
        email=body["email"],
        password=body["password"],
        username=body.get("username"),
        phone_number=body.get("phone_number"),
        address=body["address"],
        city=body.get("city"),
        state=body.get("state"),
        postal_code=body["postal_code"],
        country=body.get("country")
    )

    return jsonify(result), (400 if "error" in result else 200)


# -------------------------
# CONFIRM USER
# -------------------------
@app.route("/auth/confirm-signup", methods=["POST"])
def confirm_signup():
    body = request.get_json()

    result = handle_confirm_signup(
        body.get("email"),
        body.get("code")
    )

    return jsonify(result), (400 if "error" in result else 200)


# -------------------------
# LOGIN
# -------------------------
@app.route("/auth/login", methods=["POST"])
def login():
    body = request.get_json()

    result = handle_login(
        body.get("email"),
        body.get("password")
    )

    return jsonify(result), (400 if "error" in result else 200)


# -------------------------
# FORGOT PASSWORD
# -------------------------
@app.route("/auth/forgot-password", methods=["POST"])
def forgot_password():
    body = request.get_json()

    result = handle_forgot_password(
        body.get("email")
    )

    return jsonify(result), (400 if "error" in result else 200)


# -------------------------
# RESET PASSWORD
# -------------------------
@app.route("/auth/reset-password", methods=["POST"])
def reset_password():
    body = request.get_json()

    result = handle_reset_password(
        body.get("email"),
        body.get("code"),
        body.get("new_password")
    )

    return jsonify(result), (400 if "error" in result else 200)


# -------------------------
# DELETE USER
# -------------------------
@app.route("/auth/delete-user", methods=["DELETE"])
def delete_user():
    result = handle_delete_user({
        "headers": dict(request.headers),
        "queryStringParameters": request.args
    })

    return jsonify(result), (400 if "error" in result else 200)


# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
