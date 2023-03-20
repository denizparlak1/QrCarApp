import qrcode
import qrcode.image.svg
from io import BytesIO
from storage.firebase_storage import upload_to_firebase_storage


async def generate_qr_code(user_id: str):
    qr_factory = qrcode.image.svg.SvgImage
    qr_code = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        image_factory=qr_factory
    )

    # Construct the URL with the user ID
    url = f"https://daglarapp.ey.r.appspot.com/user/{user_id}"
    qr_code.add_data(url)
    qr_code.make(fit=True)

    img = qr_code.make_image(fill_color="black", back_color="white")
    file_name = f"{user_id}.svg"

    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    qr_code_url = upload_to_firebase_storage(buffer, file_name)
    buffer.close()

    return qr_code_url

