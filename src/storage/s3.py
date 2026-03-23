import boto3
import os
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logging

load_dotenv(override=True)

# Pulling from .env (make sure you updated your .env to use LocalStack settings)
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:4566")
S3_BUCKET_NAME = os.getenv("S3_BUCKET", "real-estate-pipeline-bucket") # <-- Updated this
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "test")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "test")

def create_s3_client():
    return boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name='us-east-1'
    )

def upload_file_to_s3(file_path, file_name):
    s3 = create_s3_client()
    try:
        logging.info(f"Started uploading {file_name} to S3 bucket {S3_BUCKET_NAME}")
        
        # LocalStack specific: create bucket if it doesn't exist yet
        try:
            s3.create_bucket(Bucket=S3_BUCKET_NAME)
        except Exception:
            pass 

        s3.upload_file(file_path, S3_BUCKET_NAME, file_name)
        logging.info(f"Successfully uploaded {file_name} to {S3_BUCKET_NAME}")
    except FileNotFoundError:
        logging.error(f"The file {file_path} was not found.")
    except NoCredentialsError:
        logging.error("Credentials not available.")
