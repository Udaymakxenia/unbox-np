import datetime
import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.deps import get_current_user
from app.models.response import ResponseModel
from starlette.background import BackgroundTask
from app.users.user_db import SystemUser
from app.utils.aws_s3 import(
    get_object as s3_get_object,
    hasNewerFile as s3_hasNewerFile,
    download2temp as s3_download2temp
)

router = APIRouter()

AWS_OTA_FILE = "unbox_speaker/unboxnp_latest.bin"

class OTARequest(BaseModel):
    last_modified:str

@router.post("/download")
def find_latest_version(req: OTARequest, user: SystemUser = Depends(get_current_user)):
    print(req)
    s3response = s3_get_object(AWS_OTA_FILE)
    s3_modified_time = s3response["LastModified"]
    if s3_hasNewerFile(s3_modified_time,req.last_modified):
        s3file = s3_download2temp(AWS_OTA_FILE)
        return FileResponse(s3file, 
                            headers={"last_modified":s3_modified_time.strftime('%Y%m%d%H%M%S')}, media_type="application/octet-stream",background=BackgroundTask(os.remove, s3file))
    
    raise HTTPException(status_code=404, detail="file not found")