import os
import uuid
import boto3

from flask import current_app
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    's3', 
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_S3_REGION_NAME')
)

def upload_photo_to_s3(file_data, file_name):
    """Uploads a photo to the specified S3 bucket and returns the file's public URL and s3 key."""
    file_extension = file_name.split('.')[-1]
    s3_key = f"{uuid.uuid4()}.{file_extension}"
    try:
        s3_client.upload_fileobj(
            file_data,
            os.getenv('AWS_S3_BUCKET_NAME'),
            s3_key,
            ExtraArgs={
                'ContentType': file_data.content_type, 
                'ACL': 'public-read'  # Makes the file publicly accessible
            }
        )

        public_url = public_url = (
            f"https://{os.getenv('AWS_S3_BUCKET_NAME')}"
            f".s3.{os.getenv('AWS_S3_REGION_NAME')}"
            f".amazonaws.com/{s3_key}"
        )
        return public_url, s3_key
    except Exception as e:
        current_app.logger.error(f"Failed to upload file {file_name} to S3: {e}")
        return None, None

def delete_photo_from_s3(s3_key):
    """Deletes a photo from the specified S3 bucket."""
    try:
        s3_client.delete_object(
            Bucket=os.getenv('AWS_S3_BUCKET_NAME'),
            Key=s3_key
        )
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to delete file {s3_key} from S3: {e}")
        return False
