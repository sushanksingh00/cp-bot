from fastapi import APIRouter, Depends
from crud import * 
from externalapi import *
from fastapi import HTTPException
from services.auth_services import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Analytics"] # for swagger ui
)


@router.get("/contests")

def contest_info(current_user : AppUsers = Depends(get_current_user)):

    user = sessionLocal().scalar(select(Users).where(
        Users.app_user_id == current_user.id
    ))


    with sessionLocal() as session:
        contest_history = session.scalars(select(ContestPerformance)
                        .where(ContestPerformance.user_id == user.id)).all()
        contest_data = []
        for contest in contest_history:
            contest_data.append({
                "contest_name" : contest.contest_name,
                "rank" : contest.rank,
                "old_rating" : contest.old_rating,
                "new_rating" : contest.new_rating
            })
    return contest_data


@router.get("/daily-activity")
def daily_activity_info(current_user : AppUsers = Depends(get_current_user)):

    user = sessionLocal().scalar(select(Users).where(
        Users.app_user_id == current_user.id
    ))

    with sessionLocal() as session:
        daily_activity = session.scalars(select(DailyActivity).where(
            DailyActivity.user_id == user.id
        )).all()
        daily_data = []
        for day in daily_activity:
            daily_data.append({
                "date" : day.date,
                "problems_attempted" : day.problems_attempted,
                "problems_solved" : day.problems_solved
            })
    return daily_data





@router.get("/tags")
def tag_info(current_user : AppUsers = Depends(get_current_user)):

    user = sessionLocal().scalar(select(Users).where(
        Users.app_user_id == current_user.id
    ))

    with sessionLocal() as session:
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

def weak_tag_info(current_user : AppUsers = Depends(get_current_user)):

    user = sessionLocal().scalar(select(Users).where(
        Users.app_user_id == current_user.id
    ))

    with sessionLocal() as session:
        weakest_tag = session.scalars(select(TagPerformance).where(
            TagPerformance.user_id == user.id
        ).order_by(
            TagPerformance.weakness_score.desc()
        ).limit(3)).all()
        weak_tag_data = []
        for tag_ in weakest_tag:
            weak_tag_data.append(tag_.tag_name)

    return weak_tag_data

