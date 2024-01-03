from datetime import datetime, timezone
import os
from typing import Optional
from starlette.background import BackgroundTask
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from app.deps import get_current_user
import io
from app.models.response import ResponseModel
from app.activities.activity_db import (
    ActivitySchema,
    find_activities as db_find_activities,
    find_activity as db_find_activity
)
import boto3
import pandas
from app.users.user_db import SystemUser

from app.utils.aws_s3 import(
   get_object as s3_get_object,
   get_object_attributes as s3_get_object_attributes,
   download2temp as s3_download2temp,
   hasNewerFile as s3_hasNewerFile
)

router = APIRouter()

class ActivityRequest(BaseModel):
    box_number : str
    activity_number : str
    language:str
    last_modified:str

@router.get("/")
def find_activities(user: SystemUser = Depends(get_current_user)):
   activities = db_find_activities()
   return activities

@router.get("/csv")
def find_activities(user: SystemUser = Depends(get_current_user)):
    activities = db_find_activities()
    df = pandas.DataFrame(activities)
    stream = io.StringIO()
    df.to_csv(stream, index = False)
    response = StreamingResponse(iter([stream.getvalue()]),
                        media_type="text/csv"
    )

    response.headers["Content-Disposition"] = "attachment; filename=activites.csv"

    return response
@router.post("/download")
def download_activity(request : ActivityRequest, user: SystemUser = Depends(get_current_user)):
   activity = db_find_activity(request.box_number, request.activity_number, request.language.upper())
   
   if activity:
    
    s3response = s3_get_object(activity["file"])
    s3_modified_time = s3response["LastModified"]
    if s3_hasNewerFile(s3_modified_time,request.last_modified):
        mp3file = s3_download2temp(activity["file"])
        return FileResponse(mp3file, 
                            headers={"last_modified":s3_modified_time.strftime('%Y%m%d%H%M%S')}, media_type="audio/mpeg",background=BackgroundTask(os.remove, mp3file))
    

   raise HTTPException(status_code=404, detail="Activity not found")


def cleanup(temp_file):
    os.remove(temp_file)


