import base64
import os
from postmarker.core import PostmarkClient

POSTMARK_SERVER_TOKEN = os.environ['POSTMARK_TOKEN']


async def send_email_with_qr_code(qr_code_file):
    postmark = PostmarkClient(server_token=POSTMARK_SERVER_TOKEN)

    postmark.emails.send(
        From="test@qrpark.com.tr",
        To="parlak.deniss@gmail.com",
        Subject="Your QR Code",
        TextBody="Please find your QR code attached.",
        HtmlBody="<p>Please find your QR code attached.</p>"
    )
