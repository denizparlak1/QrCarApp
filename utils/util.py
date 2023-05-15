from typing import Optional

from fastapi import HTTPException
from firebase_admin import auth
import random
import string

from auth.config import users_ref


async def set_custom_claims(uid, role, corporation_name=None):
    try:
        # Set custom user claims
        custom_claims = {
            "role": role
        }
        if corporation_name:
            custom_claims["corporation_name"] = corporation_name
        auth.set_custom_user_claims(uid, custom_claims)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def generate_random_email_password(domain="example.com"):
    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    email = f"{random_string}@{domain}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return email, password


def retrieve_user_device_id(user_id: str) -> Optional[str]:
    try:
        # Retrieve the device_id from the user data using user_id
        device_id = users_ref.child(user_id).child('device_id').get()
        print(device_id)
        return device_id
    except Exception as e:
        print(f"Failed to retrieve device ID: {str(e)}")
        return None
