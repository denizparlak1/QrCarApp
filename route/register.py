from fastapi import APIRouter, HTTPException
from firebase_admin import auth

from auth.config import users_ref
from qr.qr_code_proccess import generate_qr_code
from schema.firebase.UserRegistration import UserRegistration

router = APIRouter()


@router.post("/register/")
async def register_user(user: UserRegistration):
    try:
        new_user = auth.create_user(
            email=user.email,
            password=user.password
        )
        qr_code_file = await generate_qr_code(new_user.uid)
        user_data = {
            "email": user.email,
            "userId": new_user.uid,
            "qr_code_file": qr_code_file,
            "messages": "",
            "phone": ""
        }

        # Set data in the Realtime Database
        users_ref.child(new_user.uid).set(user_data)

        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
