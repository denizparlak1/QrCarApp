from fastapi import HTTPException
from firebase_admin import auth
import random
import string


async def set_custom_claims(uid, role):
    try:
        # Set custom user claims
        custom_claims = {
            "role": role
        }
        auth.set_custom_user_claims(uid, custom_claims)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def generate_random_email_password(domain="example.com"):
    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    email = f"{random_string}@{domain}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return email, password



