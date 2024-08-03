import requests
import os

def send_verification_email(to_email: str, token: str):
    url = "https://api.postmarkapp.com/email"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": "f6908cb0-1f58-43cc-bde2-0c8b658ace05"
    }
    data = {
        "From": "support@confusedcareers.com",  # Replace with your email address
        "To": to_email,
        "Subject": "Verify Your Email Address",
        "HtmlBody": f"<strong>Click the following link to verify your email address:</strong><br><a href='http://localhost:8000/verify/{token}'>Verify Email</a>",
        "MessageStream": "outbound"
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Verification email sent to {to_email}")
    else:
        print(f"Failed to send email: {response.json()}")
