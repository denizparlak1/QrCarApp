from io import BytesIO

from fastapi import APIRouter, HTTPException, UploadFile
from firebase_admin import db

from auth.config import users_ref
from storage.firebase_storage import upload_to_firebase_storage, upload_to_gcs

router = APIRouter()


@router.get("/users/{userId}")
async def get_user(userId: str):
    # Query the user with the specified username
    query = users_ref.order_by_child('userId').equal_to(userId).limit_to_first(1).get()
    user_data = list(query.values())[0]

    if user_data:
        return {"photo": user_data.get('photo'), "message": user_data.get("messages"), "phone": user_data.get("phone"),
                "carPlate": user_data.get('carPlate')}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/users/add/avatar/{userId}")
async def add_avatar_api(userId: str, file: UploadFile):
    url = f'user/{userId}/{file.filename}'
    return upload_to_gcs(url,file.file)
