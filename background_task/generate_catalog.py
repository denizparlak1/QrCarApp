import asyncio
import os
from fastapi import HTTPException
from firebase_admin import auth
from auth.config import users_ref
from mail.postmark import send_email_with_qr_code
from pdf.generate_pdf import generate_svg
from qr.qr_code_proccess import generate_qr_code
from schema.firebase.UserRegistration import UserRegistration, BulkRegisterRequest
from utils.util import set_custom_claims, generate_random_email_password


async def create_single_user(request):
    email, password = generate_random_email_password()
    try:
        customer = request.customer.replace(" ","_")
        new_user = auth.create_user(email=email, password=password)
        await set_custom_claims(new_user.uid, request.role)
        qr_code_file = await generate_qr_code(new_user.uid, customer)

        user_data = {
            "email": email,
            "userId": new_user.uid,
            "qr_code_file": qr_code_file,
            "message": "Kahve almaya çıktım 10 dakikaya döneceğim",
            "phone": "XXX XXX XXXX",
            "car_plate": "123 TC 123",
            "photo": os.environ['AVATAR'],
            "telegram": "@username",
            "telegram_permission": True,
            "whatsapp_permission": True,
            "phone_permission": True,
            "first_login": True
        }

        users_ref.child(new_user.uid).set(user_data)
        return {"email": email, "password": password, "qr_code_file": qr_code_file}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def perform_background_tasks(request: BulkRegisterRequest):
    tasks = [create_single_user(request) for _ in range(request.count)]
    user_data_list = await asyncio.gather(*tasks)

    pdf_url = await generate_svg(user_data_list, request.customer)

    await send_email_with_qr_code(pdf_url, request.customer)
