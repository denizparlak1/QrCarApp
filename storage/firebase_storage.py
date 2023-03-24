from auth.config import bucket, users_ref


def upload_to_firebase_storage(qr_codes,buffer, file_name):
    try:
        blob = bucket.blob(f"{qr_codes}/{file_name}")
        blob.upload_from_file(buffer, content_type="image/svg+xml")

        # Get the public URL of the QR code image
        qr_code_url = blob.public_url

        return qr_code_url
    except Exception as e:
        raise f"Error uploading to Firebase Storage: {e}"


def upload_to_gcs(url,file,userId):
    try:
        blob = bucket.blob(url)
        blob.upload_from_file(file)

        blob.acl.user('allUsers').grant_read()
        blob.acl.save()
        # Get the public URL of the QR code image
        public = blob.public_url
        users_ref.child(userId).update({"photo": public})
        return public
    except Exception as e:
        raise e


