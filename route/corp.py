import os
import uuid
from typing import List
import random
from fastapi import APIRouter, HTTPException
from firebase_admin import auth, db
from auth.config import corp_bucket, corp_ref
from qr.qr_code_proccess import generate_qr_code
from reponse.response_model import CorporationUser
from schema.corp.user import GetQrData, CreateUser, CreateCorporationAdmin, ListCorporationUser, DeleteUser
from schema.firebase.UserRegistration import UserRegistration
from utils.util import set_custom_claims

router = APIRouter()


@router.post("/corp/register/")
async def register_user(user: UserRegistration):
    try:
        # qr_code_file = await generate_corp_qr_code(new_user.uid, user.customer)
        user_id = uuid.uuid4()
        user_data = {
            "name": "",
            "surname": "",
            "email": user.email,
            "userId": user_id,
            "qr_code_file": "",
            "message": "Kahve almaya çıktım 10 dakikaya döneceğim",
            "phone": "XXX XXX XXXX",
        }

        corporate.child().child(user_id).set(user_data)

        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/qrcode/')
async def get_corp_qr(qrdata: GetQrData):
    # Get a reference to the folder in your bucket

    folder = corp_bucket.get_blob(f'{qrdata.corp_name}/')

    # List all the blobs in the folder
    blobs = corp_bucket.list_blobs(prefix=folder.name)

    # Generate public URLs for each blob and add them to a list
    urls = [blob.public_url for blob in blobs][1:]

    return {'urls': urls}


@router.post("/create/corp/user/")
async def create_corp_user_api(user: CreateUser):
    # Reference to the users node under the specified firma_id
    users_ref = db.reference(f"corporate/{user.corporation_name}/users")
    user_id = uuid.uuid4()
    new_user_ref = users_ref.child(str(user_id))
    # Push the new user data under a new user_id node
    new_user_ref.set({
        "id": str(user_id),
        "mail": user.mail,
        "name": user.name,
        "surname": user.surname,
        "phone": user.phone,
        "username": user.name + " " + user.surname
    })

    # Return the new user_id
    return True


@router.post("/create/corp/admin/")
async def create_corp_admin_api(user: CreateCorporationAdmin):
    try:
        # Create new Firebase user
        new_user = auth.create_user(
            email=user.email,
            password=user.password
        )

        # Set custom claims for user
        await set_custom_claims(new_user.uid, user.role,user.corporation_name)

        return {"success": True}

    except Exception as e:
        raise HTTPException(e)


@router.get('/corp/user/{corporation_name}', response_model=List[CorporationUser])
async def get_corp_users(corporation_name: str):
    try:
        corporation_ref = db.reference(f'corporate/{corporation_name}/users')
        all_users = corporation_ref.get()

        user_list = []
        for user in all_users.values():
            user_list.append(CorporationUser(
                id = user['id'],
                mail=user['mail'],
                name=user['name'],
                surname=user['surname'],
                phone=user['phone'],
                username = user['username']
            ))

        return user_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/corp/user/delete/")
async def delete_corp_user_api(user: DeleteUser):
    ref = db.reference(f"/corporations/{user.corporation_name}/users")
    user_ref = ref.child(str(user.user_id))
    print(user_ref.get())
    if user_ref.get() is not None:
        user_ref.delete()
        return {"success": True, "message": "User successfully deleted"}
    else:
        return {"success": False, "message": "User not found"}
