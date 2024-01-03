

import datetime
from pydantic import BaseModel
from typing import Optional

from app.dbs.database import mongoClient


activity_coll = mongoClient().get_collection("activities")

class OTASchema(BaseModel):
    box_number : str
    activity_number : str
    file: str
    language:str
    last_modified:Optional[datetime.datetime]= None


def find_activities():
    activities = []
    for act in activity_coll.find({},{'_id': 0}):
        activities.append(act)
    return 

def find_activity(box_number, activity_number, language):
    print(f"{box_number},{activity_number},{language}")
    for act in activity_coll.find({
        "box_number":box_number,
        "activity_number":activity_number,
        "language":language
    },{'_id': 0}):
        print(act)
        return act
    return None