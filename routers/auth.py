from fastapi import APIRouter
from crud import * 
from externalapi import *
from fastapi import HTTPException
from services.auth_services import register_user, login_user
from schemas import AppUserLogin, AppUserRegister
from sqlalchemy.orm import Session
from database import get_db

from fastapi import Depends

router = APIRouter(
    prefix="/auth",
    tags=["Auth"] # for swagger ui
)

@router.post("/register")
def register(user: AppUserRegister, session: Session = Depends(get_db)):
    return register_user(user.username, 
                         user.password, 
                         user.email, session)

@router.post("/login")
def login(user: AppUserLogin, session: Session = Depends(get_db)):
    return login_user(user.username, user.password, session)

from fastapi import Depends

