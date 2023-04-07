import base64
import os
from postmarker.core import PostmarkClient

POSTMARK_SERVER_TOKEN = os.environ['POSTMARK_TOKEN']


async def send_email_with_qr_code(qr_code_file,subject):
    postmark = PostmarkClient(server_token=POSTMARK_SERVER_TOKEN)

    postmark.emails.send(
        From="test@qrpark.com.tr",
        To="parlak.deniss@gmail.com",
        Subject=subject,
        TextBody="Proje için basılan QR kodlar ekde yer almaktadır.",
        HtmlBody="<h3>Proje için basılan QR kodlar ekde yer almaktadır.</h3>"
    )
