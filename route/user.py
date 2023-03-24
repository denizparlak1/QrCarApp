from fastapi import APIRouter, HTTPException, UploadFile

from firebase_admin import auth
from auth.config import users_ref
from schema.user.schema import UpdateUserMessage, UpdateUserPhone, UpdateUserPassword, UpdateUserEmail, UpdateUserPlate
from storage.firebase_storage import upload_to_firebase_storage, upload_to_gcs

router = APIRouter()


@router.get("/users/{userId}")
async def get_user(userId: str):
    # Query the user with the specified username
    query = users_ref.order_by_child('userId').equal_to(userId).limit_to_first(1).get()
    user_data = list(query.values())[0]

    if user_data:
        return {"photo": user_data.get('photo'), "message": user_data.get("message"), "phone": user_data.get("phone"),
                "plate": user_data.get('car_plate')}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/add/avatar/{userId}")
async def add_avatar_api(userId: str, file: UploadFile):
    url = f'user/{userId}/{file.filename}'
    return upload_to_gcs(url, file.file,userId)


@router.put("/user/update/message/")
async def update_message_api(user: UpdateUserMessage):
    try:
        users_ref.child(user.user_id).update({"messages": user.message})
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
        users_ref.child(user.user_id).update({"carPlate": user.plate})
        return {"message": "Araç Plakanız Güncellendi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
