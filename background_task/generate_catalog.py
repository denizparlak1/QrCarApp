import asyncio
import os
import zipfile

from fastapi import HTTPException
from firebase_admin import auth
from httpx import AsyncClient

from auth.config import users_ref, bucket
from mail.postmark import send_email_with_qr_code
from pdf.generate_pdf import generate_svg
from qr.qr_code_proccess import generate_qr_code
from schema.firebase.UserRegistration import UserRegistration, BulkRegisterRequest
from utils.util import set_custom_claims, generate_random_email_password


async def create_single_user(request):
    email, password = generate_random_email_password()
    try:
        customer = request.customer.replace(" ", "_")
        new_user = auth.create_user(email=email, password=password)
        await set_custom_claims(new_user.uid, request.role)
        qr_code_file = await generate_qr_code(new_user.uid, customer)

        user_data = {
            "email": email,
            "name": "",
            "surname": "",
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
            "first_login": True,
            "name_permission": True
        }

        users_ref.child(new_user.uid).set(user_data)

        return {"email": email, "password": password, "qr_code_file": qr_code_file}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def perform_background_tasks(request: BulkRegisterRequest, start_index: int, end_index: int, temp_dir: str,
                                   svg_file_paths: list):
    tasks = [create_single_user(request) for _ in range(end_index - start_index)]
    user_data_list = await asyncio.gather(*tasks)

    customer = request.customer.replace(" ", "_")
    svg_url = await generate_svg(user_data_list, customer)

    # Download the generated SVG file to the temporary directory
    svg_file_name = f"{customer}_chunk_{start_index // 30 + 1}.svg"
    svg_file_path = os.path.join(temp_dir, svg_file_name)
    svg_file_paths.append(svg_file_path)

    os.makedirs(temp_dir, exist_ok=True)

    async with AsyncClient() as client:
        response = await client.get(svg_url)

    with open(svg_file_path, "wb") as svg_file:
        svg_file.write(response.content)


async def send_email_with_all_qr_codes(customer: str, temp_dir: str, svg_file_paths: list):
    # Create a ZIP archive of the SVG files
    zip_file_name = f"{customer}_svgs.zip"
    zip_file_path = os.path.join(temp_dir, zip_file_name)

    with zipfile.ZipFile(zip_file_path, "w") as zip_file:
        for svg_file_path in svg_file_paths:
            zip_file.write(svg_file_path, os.path.basename(svg_file_path))

    # Upload the ZIP archive to the storage
    zip_blob = bucket.blob(f"archives/{zip_file_name}")
    zip_blob.upload_from_filename(zip_file_path, content_type="application/zip", predefined_acl="publicRead")
    zip_url = zip_blob.public_url

    # Send email with the ZIP archive
    await send_email_with_qr_code(zip_url, customer)
