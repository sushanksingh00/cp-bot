from crud import *
from externalapi import *
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from services.analytics_serivces import *
from services.recommendation_services import *
from services.sync_services import *
from services.auth_services import get_current_user
from schemas import UserCreate, UserBase
from datetime import datetime, UTC
from celery.result import AsyncResult

from tasks.task import long_task, sync_user
from core.celery_app import celery_app

from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/sync",
    tags=["Sync"]
)

@router.post("/codeforces")
def sync(user: UserBase, current_user: AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):


    task = sync_user.delay(
        user.handle, #fake handle
        current_user.id, #app_user_id
        session
    )

    return {
        "task_id": task.id,
        "status": "queued"
    }

    # if existing_user:
    #     update_user("codeforces", handle, cf_data["rating"],
    #                 cf_data["maxRating"], cf_data["rank"], cf_data["maxRank"], current_user.id)
    # else:
    #     insert_user("codeforces", handle, cf_data["rating"],
    #                 cf_data["maxRating"], cf_data["rank"], cf_data["maxRank"], current_user.id)
        
    # with sessionLocal() as session:
    #     sync_user_contests(session, handle)
    #     compute_problem_attempt(session, handle)
    #     compute_daily_activity(session,handle)
    #     compute_tag_performance(session,handle)
    #     compute_skill_estimate(session,handle)
    #     compute_recommendation_queue(session,handle)

    # return {"message": "User Synced Succesfully"}

@router.get("/status/{task_id}")
def get_status(task_id: str):

    task = AsyncResult(task_id,
                       app=celery_app)

    return {
        "task_id": task_id,
        "state": task.state,
        "result": task.result
    }