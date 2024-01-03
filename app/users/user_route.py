from fastapi import APIRouter, Depends
from fastapi import status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.users.user_db import UserOut, UserAuth, find_user, add_user, SystemUser
from app.users.user_db import UserOut, UserAuth, TokenSchema

from uuid import uuid4

from app.utils.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from app.deps import get_current_user

router = APIRouter()
@router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    user = find_user(data.username)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'username': data.username,
        'name':data.name,
        'password': get_hashed_password(data.password),
        'id': str(uuid4())
    }
    await add_user(user)
    return user



@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    #print(f"username::{form_data.username}, 'password{form_data.password}")
    user = find_user(form_data.username)
   # print(f"user::{user}")
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    #print(f"verify password : {verify_password(form_data.password, hashed_pass)}")
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user['username'])#,
        #"refresh_token": create_refresh_token(user['username'])
    }

@router.get('/me', summary='Get details of currently logged in user', response_model=SystemUser)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user