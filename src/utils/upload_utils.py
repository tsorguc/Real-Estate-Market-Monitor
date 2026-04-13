import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from dotenv import load_dotenv

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logging

load_dotenv()
SCOPES = os.getenv("SCOPES", "https://www.googleapis.com/auth/drive.file").split(',')
CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
FOLDER_ID = os.getenv("FOLDER_ID")

def authenticate_drive():
    """Authenticates the user and returns the Drive service object."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE or not os.path.exists(CLIENT_SECRET_FILE):
                logging.error(f"Client secret file {CLIENT_SECRET_FILE} not found or not specified.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    return build('drive', 'v3', credentials=creds)

def upload_image(service, image_path, folder_id=None):
    """Uploads a single image to Google Drive."""
    try:
        file_metadata = {
            'name': os.path.basename(image_path),
            'parents': [folder_id or FOLDER_ID]
        }
        media = MediaFileUpload(image_path, mimetype='image/jpeg', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logging.info(f"File ID: {file.get('id')} uploaded successfully.")
        return file.get('id')
    except Exception as e:
        logging.error(f"Error uploading image {image_path}: {e}")
        return None

def upload_batch(image_paths):
    """Uploads a batch of images to Google Drive."""
    service = authenticate_drive()
    if not service:
        return []
    
    uploaded_ids = []
    for path in image_paths:
        file_id = upload_image(service, path)
        if file_id:
            uploaded_ids.append(file_id)
    return uploaded_ids
