from crud import *
from fastapi import HTTPException


def get_linked_cf_user(app_user_id: int, session):

    user = session.scalar(select(Users).where(
        Users.app_user_id == app_user_id
    ))
    if not user:
        raise HTTPException(404, detail="User is not synced or Does not exist in the database")
    return user