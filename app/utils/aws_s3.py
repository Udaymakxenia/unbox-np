
from datetime import datetime, timezone
import boto3

from app.config import (
   AWS_BUCKET_NAME,
   AWS_ACCESS_KEY_ID,
   AWS_SECRET_ACCESS_KEY,
   AWS_REGION_NAME
)

import tempfile


s3client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)
def get_object_attributes(s3file:str):
     s3response = s3client.get_object_attributes(Bucket=AWS_BUCKET_NAME,Key=s3file,ObjectAttributes=['ETag'])
     return s3response

def get_object(s3file:str):
    print(f"AWS_BUCKET_NAME::{AWS_BUCKET_NAME}, mp3file::{s3file}")
    s3response = s3client.get_object(Bucket=AWS_BUCKET_NAME,Key=s3file)
    return s3response

def download2temp(s3file):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        s3client.download_fileobj(AWS_BUCKET_NAME,s3file, f)
        print(f"temp file ::{f.name}")
        return f.name
    
def hasNewerFile(s3_modified_time,req_time):
  # s3_modified_time = s3response["LastModified"] 
  # s3_format = "%Y-%m-%d %H:%M:%S%z"
   req_format = "%Y%m%d%H%M%S"
    
   s3_timestamp = s3_modified_time #datetime.strptime(s3_modified_time, s3_format)
   req_timestamp = datetime.strptime(req_time, req_format).astimezone(tz=timezone.utc)

   is_modified = (s3_timestamp > req_timestamp)
   #print(f"{s3_timestamp}, {req_timestamp}, {is_modified}")
   return is_modified