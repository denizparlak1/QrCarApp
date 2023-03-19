import os
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, firestore, db
from google.cloud import storage

load_dotenv()
secret_id = os.environ['FIREBASE_KEY']
database_url = os.environ['FIREBASE_DATABASE_URL']
bucket_name = os.environ['BUCKET']
cred = credentials.Certificate(secret_id)
initialize_app(cred,{
        'databaseURL': database_url
    })


storage_client = storage.Client.from_service_account_json(secret_id)
bucket = storage_client.get_bucket(bucket_name)

users_ref = db.reference('users')

def get_firestore_client():
    return firestore.client()
