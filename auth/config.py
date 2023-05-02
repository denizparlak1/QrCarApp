import os
import tempfile
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, firestore, db
from google.cloud import storage

load_dotenv()

firebase_json_path = os.environ['FIREBASE_KEY']
database_url = os.environ['FIREBASE_DATABASE_URL']
bucket_name = os.environ['BUCKET']
corp_bucket_name = os.environ['CORP_BUCKET']

def download_json_key(bucket_name, blob_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_path)

    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".json") as temp_credentials_file:
        blob.download_to_file(temp_credentials_file)
        temp_file_path = temp_credentials_file.name

    return temp_file_path

firebase_key_path = download_json_key(bucket_name, firebase_json_path)

cred = credentials.Certificate(firebase_key_path)
initialize_app(cred, {
    'databaseURL': database_url
})

storage_client = storage.Client.from_service_account_json(firebase_key_path)
bucket = storage_client.get_bucket(bucket_name)
corp_bucket = storage_client.get_bucket(corp_bucket_name)
users_ref = db.reference('users')
corp_ref = db.reference('corporate')

def get_firestore_client():
    return firestore.client()
