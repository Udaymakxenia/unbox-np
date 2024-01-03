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
import pandas
import io
from app.users.user_db import SystemUser
from datetime import datetime
router = APIRouter()
from app.config import(
    DATA_ROOT
)

def list_files(startpath):
    filelist = []

    for root, dirs, files in os.walk(startpath):
        for file in files:
            #append the file name to the list
            filelist.append(os.path.join(root,file))
    return filelist
   
def create_json(filelist):
    activites_json = []

    for name in filelist:
        print(name)
        modification_time = os.path.getmtime(name)
        last_modified_date = datetime.fromtimestamp(modification_time)
        act_file = name.replace(DATA_ROOT,"")
        print(act_file)
        act_dir,act_file =  act_file.split("\\")
        act_number = act_file[:-5][1:]
        act_lang = act_file[:-4][-1:]
        act = {
            "box_number" : str(act_dir),
            "activity_number" : str(act_number),
            "language" : act_lang,
            "last_modified" :  last_modified_date.strftime("%d%m%y%H%M%S")
        }
        activites_json.append(act)
    return activites_json
    
class ActivityRequest(BaseModel):
    box_number : str
    activity_number : str
    language:str
    last_modified:str

@router.get("/")
def find_activities(user: SystemUser = Depends(get_current_user)):
    tree_data = list_files(DATA_ROOT)
    activities = create_json(tree_data)
    return activities

@router.get("/csv")
def find_activities(user: SystemUser = Depends(get_current_user)):
    tree_data = list_files(DATA_ROOT)
    activities = create_json(tree_data)
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
   activity_file = os.path.join(DATA_ROOT,request.box_number,(request.box_number+request.activity_number+request.language).upper() + ".mp3")
   print(f"activity_file:{activity_file}")

   modification_time = os.path.getmtime(activity_file)
   last_modified_date = datetime.fromtimestamp(modification_time)
   return FileResponse(activity_file, 
                            headers={"last_modified":last_modified_date.strftime('%Y%m%d%H%M%S')}, media_type="audio/mpeg")
   

def cleanup(temp_file):
    os.remove(temp_file)


