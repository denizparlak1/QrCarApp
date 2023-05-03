from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile
from firebase_admin import auth
from auth.config import users_ref
from schema.user.schema import UpdateUserMessage, UpdateUserPhone, UpdateUserPassword, UpdateUserEmail, UpdateUserPlate, \
    UpdateUserTelegram, UpdateUserTelegramPermission, UpdateUserNamePermission, UpdateUserWhatsappPermission, \
    BaseUpdateUser, UpdateUserSMSPermission
from storage.firebase_storage import upload_to_gcs

router = APIRouter()


@router.get("/users/{userId}")
async def get_user(userId: str):
    # Query the user with the specified username
    query = users_ref.order_by_child('userId').equal_to(userId).limit_to_first(1).get()
    user_data = list(query.values())[0]

    if user_data:
        return {"mail": user_data.get('email'), "photo": user_data.get('photo'), "message": user_data.get("message"),
                "phone": user_data.get("phone"),
                "plate": user_data.get('car_plate'), "qr": user_data.get('qr_code_file'),
                "telegram": user_data.get('telegram'),
                'telegram_permission': user_data.get('telegram_permission'),
                'whatsapp_permission': user_data.get('whatsapp_permission'),
                'phone_permission': user_data.get('phone_permission'),
                'first_login': user_data.get('first_login'),
                'name': user_data.get('name'),
                'surname': user_data.get('surname'),
                'name_permission': user_data.get('name_permission'),
                'sms_permission': user_data.get('sms_permission'),
                'userId': user_data.get('userId')}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/add/avatar/{userId}")
async def add_avatar_api(userId: str, file: UploadFile):
    unique_id = uuid4()
    url = f'user/{userId}/{unique_id}_{file.filename}'
    return upload_to_gcs(url, file.file, userId)


@router.put("/user/update/message/")
async def update_message_api(user: UpdateUserMessage):
    try:
        users_ref.child(user.user_id).update({"message": user.message})
        return {"message": "Mesajınız Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/phone/")
async def update_phone_api(user: UpdateUserPhone):
    try:
        users_ref.child(user.user_id).update({"phone": user.phone})
        return {"message": "Telefon Numaranız Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/onboarding/permission/")
async def update_onboarding_api(user: BaseUpdateUser):
    try:
        users_ref.child(user.user_id).update({"first_login": False})
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/email/")
async def update_email_api(user: UpdateUserEmail):
    try:
        # Update the user's email in Firebase Authentication
        auth.update_user(user.user_id, email=user.email)
        users_ref.child(user.user_id).update({"email": user.email})
        return {"detail": "Email Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/password/")
async def update_password_api(user: UpdateUserPassword):
    try:
        # Update the user's email in Firebase Authentication
        auth.update_user(user.user_id, password=user.password)
        return {"detail": "Şifre Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/plate/")
async def update_plate_api(user: UpdateUserPlate):
    try:
        users_ref.child(user.user_id).update({"car_plate": user.plate})
        return {"message": "Araç Plakanız Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/telegram/")
async def update_telegram_api(user: UpdateUserTelegram):
    try:
        users_ref.child(user.user_id).update({"telegram": user.telegram})
        return {"message": "Telegram Kullanıcı İsmi Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/telegram/permission/")
async def update_telegram_permission_api(user: UpdateUserTelegramPermission):
    try:
        users_ref.child(user.user_id).update({"telegram_permission": user.permission})
        return {"message": "Telegram İzni Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/name/permission/")
async def update_name_permission_api(user: UpdateUserNamePermission):
    try:
        users_ref.child(user.user_id).update({"name_permission": user.permission})
        return {"message": "İsim İzni Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/whatsapp/permission/")
async def update_whatsapp_permission_api(user: UpdateUserWhatsappPermission):
    try:
        users_ref.child(user.user_id).update({"whatsapp_permission": user.permission})
        return {"message": "Whatsapp İzni Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/phone/permission/")
async def update_phone_permission_api(user: UpdateUserNamePermission):
    try:
        users_ref.child(user.user_id).update({"phone_permission": user.permission})
        return {"message": "Telefon Arama İzni Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/sms/permission/")
async def update_sms_permission_api(user: UpdateUserSMSPermission):
    try:
        users_ref.child(user.user_id).update({"sms_permission": user.permission})
        return {"message": "SMS İzni Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user/update/login/permission/")
async def update_user_login_permission_api(user: BaseUpdateUser):
    try:
        users_ref.child(user.user_id).update({"first_login": False})
        return {"message": "Kayıt İşlemi Tamamlandı"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/users/delete/")
async def delete_all_users():
    # Fetch all users
    users = []
    page = auth.list_users()
    while page:
        for user in page.users:
            users.append(user)
        page = page.get_next_page()

    # Delete all users
    for user in users:
        auth.delete_user(user.uid)

    return {"message": f"Deleted {len(users)} users."}
