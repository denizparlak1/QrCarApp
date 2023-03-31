import os

from fastapi import APIRouter, HTTPException
from firebase_admin import auth
from fastapi.responses import JSONResponse
from auth.config import users_ref
from pdf.generate_pdf import generate_pdf
from qr.qr_code_proccess import generate_qr_code
from schema.firebase.UserRegistration import UserRegistration, BulkRegisterRequest
from utils.util import set_custom_claims, generate_random_email_password

router = APIRouter()


@router.post("/register/")
async def register_user(user: UserRegistration):
    try:
        new_user = auth.create_user(
            email=user.email,
            password=user.password
        )

        await set_custom_claims(new_user.uid, user.role)
        qr_code_file = await generate_qr_code(new_user.uid)
        user_data = {
            "email": user.email,
            "userId": new_user.uid,
            "qr_code_file": qr_code_file,
            "message": "Kahve almaya çıktım 10 dakikaya döneceğim",
            "phone": "XXX XXX XXXX",
            "car_plate":"123 TC 123",
            "photo":os.environ['AVATAR'],
            "telegram":"@username",
            "telegram_permission":True,
            "whatsapp_permission": True,
            "phone_permission":True,
            "first_login":True
        }

        # Set data in the Realtime Database
        users_ref.child(new_user.uid).set(user_data)

        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bulk_register/")
async def bulk_register_users(request: BulkRegisterRequest):
    if request.count < 1 or request.count > 200:
        return JSONResponse(status_code=400, content={"detail": "Count must be between 1 and 200"})

    user_data_list = []
    for _ in range(request.count):
        email, password = generate_random_email_password()
        try:
            new_user = auth.create_user(email=email, password=password)
            await set_custom_claims(new_user.uid, request.role)
            qr_code_file = await generate_qr_code(new_user.uid)

            user_data = {
                "email": email,
                "userId": new_user.uid,
                "qr_code_file": qr_code_file,
                "messages": "",
                "phone": ""
            }

            # Set data in the Realtime Database
            users_ref.child(new_user.uid).set(user_data)
            user_data_list.append({"email":email,"password":password,"qr_code_file": qr_code_file})

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Generate PDF and return its URL
    pdf_url = await generate_pdf(user_data_list,request.customer)
    return {"pdf_url": pdf_url}
