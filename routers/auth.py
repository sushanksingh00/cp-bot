from fastapi import APIRouter
from crud import * 
from externalapi import *
from fastapi import HTTPException
from services.auth_services import register_user, login_user
from schemas import AppUserLogin, AppUserRegister

router = APIRouter(
    prefix="/auth",
    tags=["Auth"] # for swagger ui
)

@router.post("/register")
def register(user: AppUserRegister):
    return register_user(user.username, 
                         user.password, 
                         user.email)

@router.post("/login")
def login(user: AppUserLogin):
    return login_user(user.username, user.password)

from fastapi import Depends

