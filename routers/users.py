from fastapi import APIRouter, Depends
from crud import * 
from externalapi import *
from fastapi import HTTPException
from services.auth_services import get_current_user
from helpers import get_linked_cf_user
from core.redis_client import redis_client
import json
from schemas import ProfileResponse

from sqlalchemy.orm import Session
from database import get_db

from core.logger import logger

from config import USE_REDIS

router = APIRouter(
    prefix="/users",
    tags=["Users"] # for swagger ui
)


@router.get("/", response_model=ProfileResponse)
def profile(current_user : AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):
    
    user = get_linked_cf_user(current_user.id, session)


    # return {
    #     "handle" : user.handle,
    #     "curr_rating": user.curr_rating,
    #     "max_rating": user.max_rating,
    #     "rank": user.rank
    # }
    return user #user me se wo wo chiz nikal ke bhej dega simply


@router.get("/dashboard")
def dashboard(current_user : AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):

    user = get_linked_cf_user(current_user.id, session)

    cache_key = f"dashboard:{user.id}"

    if USE_REDIS:
        cache_dashboard = redis_client.get(cache_key)

        if cache_dashboard:
            logger.info("CACHE HIT")
            logger.info(cache_key)


            return json.loads(cache_dashboard)

    # try:
    #     cf_data = fetch_cf_userdata(handle)[0]

    # except Exception:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="User not found or Codeforces API failed"
    #     )

    # handle = cf_data["handle"]

    user = fetch_user_by_handle(
        "codeforces",
        user.handle,
        session
    )



    user_data = {
        "handle": user.handle,
        "platform": user.platform,
        "curr_rating": user.curr_rating,
        "max_rating": user.max_rating,
        "rank": user.rank,
        "max_rank": user.max_rank,
    }

    weakest_tags = session.scalars(
        select(TagPerformance)
        .where(
            TagPerformance.user_id == user.id
        )
        .order_by(
            TagPerformance.weakness_score.desc()
        )
        .limit(3)
    ).all()

    weak_tag_data = []

    for tag in weakest_tags:

        weak_tag_data.append({
            "tag_name": tag.tag_name,
            "success_rate": tag.success_rate,
            "weakness_score": tag.weakness_score
        })

    recommendations = session.scalars(
        select(RecommendationQueue)
        .where(
            RecommendationQueue.user_id == user.id,
            RecommendationQueue.is_completed == False,
            RecommendationQueue.is_dismissed == False
        )
    ).all()

    recommendation_data = []

    upsolve_count = 0

    for rec in recommendations:

        if rec.recommendation_type == "upsolve":
            upsolve_count += 1
            continue

        recommendation_data.append({
            "title": rec.recommendation_type.replace("_", " ").title(),
            "message": rec.reason
        })

    if upsolve_count:
        recommendation_data.append({
            "title": "Upsolve Problems",
            "message": f"You have {upsolve_count} contest problems waiting for upsolve."
        })

    recent_activity = session.scalars(
        select(DailyActivity)
        .where(
            DailyActivity.user_id == user.id
        )
        .order_by(
            DailyActivity.date.desc()
        )
    ).all()

    activity_data = []
    total_questions = 0
    total_days_active = 0

    for day in recent_activity:
        if(total_days_active < 7):
            activity_data.append({
                "date": day.date,
                "problems_attempted":
                    day.problems_attempted,

                "problems_solved":
                    day.problems_solved,

                "average_rating":
                    day.average_rating
            })
        total_questions += day.problems_solved
        total_days_active +=1

    contest_data = session.scalars(select(ContestPerformance).where(ContestPerformance.user_id == user.id)).all()
    total_contests = 0
    for contest in contest_data:
        total_contests += 1

    # return {
    #     "user": user_data,
    #     "weakest_tags": weak_tag_data,
    #     "recommendations": recommendation_data,
    #     "recent_activity": activity_data
    # }

    dashboard_data = {
        "user": user_data,
        "weakest_tags": weak_tag_data,
        "recommendations": recommendation_data,
        "recent_activity": activity_data,
        "total_contests": total_contests,
        "total_questions": total_questions,
        "total_days_active": total_days_active,
    }  
    
    if USE_REDIS: 
        redis_client.setex(
            cache_key,
            300,
            json.dumps(
                dashboard_data,
                default=str
            )
        )
    return dashboard_data




@router.delete("/delete") #need to be updated
def delete_user_route(current_user : AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):

    user = get_linked_cf_user(current_user.id, session)

    if user:
        delete_user(user.platform, user.handle, session)

    return {"message":"User deleted Succesfully"}



# @router.get("/{handle}/dashboard")
# def dashboard(handle: str):

#     try:
#         cf_data = fetch_cf_userdata(handle)[0]

#     except Exception:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found or Codeforces API failed"
#         )

#     handle = cf_data["handle"]

#     user = fetch_user_by_handle(
#         "codeforces",
#         handle
#     )

#     with sessionLocal() as session:

#         user_data = {
#             "handle": user.handle,
#             "platform": user.platform,
#             "curr_rating": user.curr_rating,
#             "max_rating": user.max_rating,
#             "rank": user.rank,
#             "max_rank": user.max_rank,
#         }

#         weakest_tags = session.scalars(
#             select(TagPerformance)
#             .where(
#                 TagPerformance.user_id == user.id
#             )
#             .order_by(
#                 TagPerformance.weakness_score.desc()
#             )
#             .limit(3)
#         ).all()

#         weak_tag_data = []

#         for tag in weakest_tags:

#             weak_tag_data.append({
#                 "tag_name": tag.tag_name,
#                 "success_rate": tag.success_rate,
#                 "weakness_score": tag.weakness_score
#             })

#         recommendations = session.scalars(
#             select(RecommendationQueue)
#             .where(
#                 RecommendationQueue.user_id == user.id,
#                 RecommendationQueue.is_completed == False,
#                 RecommendationQueue.is_dismissed == False
#             )
#         ).all()

#         recommendation_data = []

#         for rec in recommendations:

#             recommendation_data.append({
#                 "recommendation_type":
#                     rec.recommendation_type,

#                 "reason":
#                     rec.reason,

#                 "priority_score":
#                     rec.priority_score
#             })

#         recent_activity = session.scalars(
#             select(DailyActivity)
#             .where(
#                 DailyActivity.user_id == user.id
#             )
#             .order_by(
#                 DailyActivity.date.desc()
#             )
#             .limit(7)
#         ).all()

#         activity_data = []

#         for day in recent_activity:

#             activity_data.append({
#                 "date": day.date,
#                 "problems_attempted":
#                     day.problems_attempted,

#                 "problems_solved":
#                     day.problems_solved,

#                 "average_rating":
#                     day.average_rating
#             })

#     return {
#         "user": user_data,
#         "weakest_tags": weak_tag_data,
#         "recommendations": recommendation_data,
#         "recent_activity": activity_data
#     }




# @router.delete("/delete") #need to be updated
# def delete_user_route(user: UserBase):

#     existing_user = fetch_user_by_handle(
#         user.platform,
#         user.handle
#     )
#     if existing_user:
#         delete_user(user.platform, user.handle)

#     return {"message":"User deleted Succesfully"}
