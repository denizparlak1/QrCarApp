import asyncio
import os
import tempfile

from fastapi import BackgroundTasks
from fastapi import APIRouter, HTTPException
from firebase_admin import auth
from fastapi.responses import JSONResponse
from auth.config import users_ref
from background_task.generate_catalog import perform_background_tasks, send_email_with_all_qr_codes
from mail.postmark import send_email_with_qr_code
from pdf.generate_pdf import generate_svg
from qr.qr_code_proccess import generate_qr_code
from schema.firebase.UserRegistration import UserRegistration, BulkRegisterRequest, AdminRegistration
from utils.util import set_custom_claims, generate_random_email_password

router = APIRouter()


@router.post('/admin/register/')
async def admin_register(user: AdminRegistration):
    try:
        new_user = auth.create_user(
            email=user.email,
            password=user.password
        )
        await set_custom_claims(new_user.uid, user.role)

        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register/")
async def register_user(user: UserRegistration):
    try:
        new_user = auth.create_user(
            email=user.email,
            password=user.password
        )

        await set_custom_claims(new_user.uid, user.role)
        qr_code_file = await generate_qr_code(new_user.uid, user.customer)
        user_data = {
            "email": user.email,
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

        # Set data in the Realtime Database
        users_ref.child(new_user.uid).set(user_data)

        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bulk_register/")
async def bulk_register_users(background_tasks: BackgroundTasks, request: BulkRegisterRequest):
    if request.count < 1 or request.count > 1000:
        return JSONResponse(status_code=400, content={"detail": "Count must be between 1 and 1000"})

    total_count = request.count * request.cycle

    # Calculate the number of chunks
    chunk_size = 30
    num_chunks = (total_count + chunk_size - 1) // chunk_size

    # Create a temporary directory to store the generated SVG files
    with tempfile.TemporaryDirectory() as temp_dir:
        svg_file_paths = []

        for i in range(num_chunks):
            background_tasks.add_task(perform_background_tasks, request, i * chunk_size,
                                      min((i + 1) * chunk_size, total_count), temp_dir, svg_file_paths)

        background_tasks.add_task(send_email_with_all_qr_codes, request.customer, temp_dir, svg_file_paths)

    return {"message": "QR Oluşturma işlemi info@qrpark.com.tr adresine iletilecek"}
