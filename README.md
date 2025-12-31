# User Authentication Lambda (AWS Cognito)

This project implements user authentication using:
- AWS Lambda (Python)
- API Gateway (REST)
- AWS Cognito (signup, login, forgot/reset password)

## Features
- Signup
- Login
- Forgot password
- Reset password

## Tech Stack
- Python 3.14
- AWS Lambda
- AWS Cognito
- API Gateway
- boto3

## API Usage

### Signup
POST /user
```json
{
  "action": "signup",
  "email": "user@example.com",
  "password": "Password@123"
}

{
  "action": "login",
  "email": "user@example.com",
  "password": "Password@123"
}

{
  "action": "forgot_password",
  "email": "user@example.com"
}

{
  "action": "reset_password",
  "email": "user@example.com",
  "new_password": "NewPass@123"
}


