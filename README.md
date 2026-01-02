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
- Get user details
- Delete user

## Tech Stack
- Python 3.14
- AWS Lambda
- AWS Cognito
- API Gateway
- boto3

## API Usage


POST /user
```json
{
  "action": "signup",
  "email": "user@example.com",
  "password": "Password@123"
}

{
  "action":"confirm-signup",
  "email": "user@emaple.com",
  "code":"12345"
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
  "code": "12345",
  "new_password": "NewPass@123"
}
```
### GET and DELETE Usage:
Key: Authorization,  Value: Bearer {{ACCESS_TOKEN}}
Add these in Headers tab and pass nothing in Body

### Local Testing:
Use POSTMAN with the API path with the local IP and test it