from fastapi import APIRouter, HTTPException
from firebase_admin import db

from auth.config import users_ref

router = APIRouter()


@router.get("/users/{userId}")
async def get_user(userId: str):
    # Query the user with the specified username
    query = users_ref.order_by_child('userId').equal_to(userId).limit_to_first(1).get()
    user_data = list(query.values())[0]

    if user_data:
        return {"message": user_data.get("messages"), "phone": user_data.get("phone")}
    else:
        raise HTTPException(status_code=404, detail="User not found")


