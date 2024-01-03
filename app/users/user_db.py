from uuid import UUID
from pydantic import BaseModel, Field
from app.dbs.database import mongoClient

class TokenSchema(BaseModel):
    access_token: str
   # refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

users = mongoClient().get_collection("users")

class UserAuth(BaseModel):
    username: str = Field(..., description="username")
    name:str
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    

class UserOut(BaseModel):
    username: str


class SystemUser(UserOut):
    name: str
    username: str


def user_helper(user) -> dict:
    return {
        "username":user["username"],
        "name":user["name"],
        "password":user["password"]
    }

def find_user(username:str):
    if username == "manish":
        user = {"username":"manish","name":"manish","password":"$2b$12$ym/VJJoHiIXiZmOlTFbqaOedB7RpNC9OviSL85yagF15KzRpX7nla","id":"8cdc2012-baff-43a5-b6f3-82402a611ac9"}
    #user = users.find_one({"username":username})
    if(user):
        return user_helper(user)
    return None

async def add_user(user: dict) -> dict:
    #pymongo.errors.DuplicateKeyError
    insertRes = users.insert_one(user)
    print(insertRes)
    return insertRes