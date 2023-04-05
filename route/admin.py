from fastapi import APIRouter, Response, HTTPException
from starlette.responses import StreamingResponse

from auth.config import bucket

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

