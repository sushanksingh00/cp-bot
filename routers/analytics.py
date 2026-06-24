from fastapi import APIRouter, Depends
from crud import * 
from externalapi import *
from fastapi import HTTPException
from services.auth_services import get_current_user
from helpers import get_linked_cf_user
from schemas import ContestResponse, DailyActivityResponse, TagsResponse
from typing import List
from sqlalchemy import select, inspect

from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Analytics"] # for swagger ui
)


@router.get("/contests", response_model=List[ContestResponse])

def contest_info(current_user : AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):

    user = get_linked_cf_user(current_user.id, session)



    pk_column = inspect(ContestPerformance).primary_key[0]
    contest_history = session.scalars(select(ContestPerformance)
                    .where(ContestPerformance.user_id == user.id).order_by(pk_column.desc())).all()
    contest_data = []
    for contest in contest_history:
        contest_data.append({
            "contest_name" : contest.contest_name,
            "rank" : contest.rank,
            "old_rating" : contest.old_rating,
            "new_rating" : contest.new_rating
        })
    return contest_data


@router.get("/daily-activity", response_model=List[DailyActivityResponse])
def daily_activity_info(current_user : AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):

    user = get_linked_cf_user(current_user.id, session)


    daily_activity = session.scalars(select(DailyActivity).where(
        DailyActivity.user_id == user.id
    ).order_by(DailyActivity.date.desc()).limit(10)).all()
    daily_data = []
    for day in daily_activity:
        daily_data.append({
            "date" : day.date,
            "problems_attempted" : day.problems_attempted,
            "problems_solved" : day.problems_solved
        })
    return daily_data





@router.get("/tags", response_model=List[TagsResponse])
def tag_info(current_user : AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):

    user = get_linked_cf_user(current_user.id, session)


    tags = session.scalars(select(TagPerformance).where(
        TagPerformance.user_id == user.id
    )).all()
    tag_data = []
    for tag in tags:
        tag_data.append({
            "tag_name": tag.tag_name,
            "success_rate" : round(tag.success_rate, 2),
            "weakness_score" : round(tag.weakness_score, 2)
        })
    return tag_data

@router.get("/tags/weakest")

def weak_tag_info(current_user : AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):

    user = get_linked_cf_user(current_user.id, session )


    weakest_tag = session.scalars(select(TagPerformance).where(
        TagPerformance.user_id == user.id
    ).order_by(
        TagPerformance.weakness_score.desc()
    ).limit(3)).all()
    weak_tag_data = []
    for tag_ in weakest_tag:
        weak_tag_data.append(tag_.tag_name)

    return weak_tag_data

