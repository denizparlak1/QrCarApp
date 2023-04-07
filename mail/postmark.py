import os
from postmarker.core import PostmarkClient

POSTMARK_SERVER_TOKEN = os.environ['POSTMARK_TOKEN']


async def send_email_with_qr_code(qr_code_file,subject):
    postmark = PostmarkClient(server_token=POSTMARK_SERVER_TOKEN)

    # Create a dictionary with the template variables
    template_variables = {
        "subject": subject,
        "pdf_url": qr_code_file
    }


    # Send the email with a Postmark template
    postmark.emails.send_with_template(
        From="islem@qrpark.com.tr",
        To="onur_korkmaz_35@hotmail.com",
        TemplateId=os.environ['POSTMARK_TEMPLATE_ID'],
        TemplateModel=template_variables
    )
