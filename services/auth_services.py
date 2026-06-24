from crud import *
from fastapi import HTTPException, Request
from pwdlib import PasswordHash
from config import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta, timezone
import jwt


ACCESS_TOKEN_EXPIRE_MINUTES=30

password_hash = PasswordHash.recommended()
def get_hash_password(password):
    return password_hash.hash(password)
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def register_user(username, password, email):
    with sessionLocal() as session:
        username_user = session.scalar(select(AppUsers).where(
            AppUsers.username == username
        ))
        if username_user:
            raise HTTPException(401, detail="User already registered !")
        
        email_user = session.scalar(select(AppUsers).where(
            AppUsers.email == email
        ))
        if email_user:
            raise HTTPException(401, detail="Email Already Registered !")
        


        new_user = AppUsers(
            username = username,
            password = get_hash_password(password),
            email = email
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }
        

def login_user(username, password):
    with sessionLocal() as session:
        username_user = session.scalar(select(AppUsers).where(
            AppUsers.username == username
        ))
        if not username_user:
            raise HTTPException(401, detail="Username not Found !")
        
        if not verify_password(password, username_user.password):
            raise HTTPException(401, detail="Wrong Password Entered !")
        
        exp_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        print("exp time is", exp_time)

        token = jwt.encode({"id": username_user.id, "exp":exp_time}, SECRET_KEY, algorithm=ALGORITHM)
        
        
        return {"token" : token}

def get_current_user(request: Request): #is_auth
    token = request.headers.get("authorization")
    if not token:
        raise HTTPException(401, detail="Unautharized, token not available")
    
    token = token.split(" ")[-1]

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        raise HTTPException(401,detail=f"Unautharized, it is not a jwt token {e}")
    
    user_id = data["id"]
    exp_time = datetime.fromtimestamp(
        data["exp"],
        tz=timezone.utc
    )
    remaining = exp_time - datetime.now(timezone.utc)

    print("remaing time is", remaining)    

    with sessionLocal() as session:
        user_data = session.scalar(select(AppUsers).where(
            AppUsers.id == user_id
        ))
        if not user_data:
            raise HTTPException(401, detail="Unautharized, User details did not match")
        
        return user_data
        

