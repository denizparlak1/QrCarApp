from fastapi import APIRouter, Response, HTTPException
from starlette.responses import StreamingResponse
from auth.config import bucket
from background_task.generate_catalog import create_sample_qr_background, create_single_user, \
    send_email_with_sample_qr_codes
from schema.firebase.UserRegistration import AdminRegistration, SampleRegisterRequest
from firebase_admin import auth
from fastapi import BackgroundTasks
from utils.util import set_custom_claims

router = APIRouter()


@router.get('/reports/')
async def get_reports():
    prefix = "catalogs/"

    blobs = bucket.list_blobs(prefix=prefix)

    files = []
    for blob in blobs:
        if not blob.name.endswith('/'):
            files.append(blob.name[len(prefix):])

    return {'files': files}


@router.get('/download/{filename}')
async def download_admin_report(filename: str):
    blob = bucket.blob(f"catalogs/{filename}")
    try:
        file_content = blob.download_as_bytes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    response = StreamingResponse(iter([file_content]), media_type='application/octet-stream')
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


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


@router.post('/admin/qr/create/sample/')
async def create_sample_qr(background_tasks: BackgroundTasks, user: SampleRegisterRequest):
    # Enqueue the task to create sample QR codes in the background
    svg_result = background_tasks.add_task(create_sample_qr_background, user)

    # Enqueue the task to send email with sample QR codes in the background
    background_tasks.add_task(send_email_with_sample_qr_codes, user.customer, svg_result)

    # Return an immediate message
    return {"message": "QR Oluşturma işlemi arka planda başlatıldı"}

