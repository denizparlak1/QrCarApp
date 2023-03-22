import re
import datetime
import requests
from auth.config import bucket
from io import BytesIO
from storage.firebase_storage import upload_to_firebase_storage
from weasyprint import HTML


def extract_object_name(url: str) -> str:
    pattern = r"https://storage.googleapis.com/[^/]+/(.+)"
    match = re.search(pattern, url)
    return match.group(1) if match else None


async def generate_pdf(user_data_list,customer):
    # Prepare the HTML content with SVG images
    html_content = '<html><head><style>table, th, td {border: 1px solid black;}</style></head><body><table>'
    html_content += '<tr><th>Email</th><th>Şifre</th><th>QR Code</th></tr>'

    for user_data in user_data_list:
        object_name = extract_object_name(user_data["qr_code_file"])
        blob = bucket.blob(object_name)
        signed_url = blob.generate_signed_url(datetime.timedelta(minutes=10), method="GET")

        html_content += f'<tr><td>{user_data["email"]}</td><td>{user_data["password"]}</td><td><img src="{signed_url}"></td></tr>'

    html_content += '</table></body></html>'
    print(html_content)
    # Generate the PDF using WeasyPrint
    pdf_data = HTML(string=html_content).write_pdf()


    # Upload the PDF to Firebase Storage (use your existing function)
    blob = bucket.blob(f"pdfs/{customer}.pdf")
    blob.upload_from_file(BytesIO(pdf_data), content_type="application/pdf", predefined_acl="publicRead")
    pdf_url = blob.public_url
    return pdf_url
