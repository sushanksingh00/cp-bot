
from fastapi import APIRouter, Depends
from crud import * 
from externalapi import *
from fastapi import HTTPException
from services.auth_services import get_current_user
from helpers import get_linked_cf_user
from typing import List
from schemas import RecommendationResponse, UpsolveResponse
from sqlalchemy.orm import Session
from database import get_db

from core.logger import logger

router = APIRouter(
    prefix="/users",
    tags=["Recommendations"] # for swagger ui
)


@router.get("/recommendations", response_model=List[RecommendationResponse])

def recommendations_info(current_user : AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):

    user = get_linked_cf_user(current_user.id, session)


    rec_rows = session.scalars(select(RecommendationQueue).where(
        RecommendationQueue.user_id == user.id,
        RecommendationQueue.recommendation_type != "upsolve"
    )).all()

    recommnedation_data =[]
    for row in rec_rows:
        
        if row.recommendation_type == "consistency_boost":
            days_inactive  = row.reason.split(" ")[-2] # no activity for x days ....so -2
            if( days_inactive < '7'):
                continue

        recommnedation_data.append({
            "recommendation_type": row.recommendation_type,
            "reason": row.reason
        })
    return recommnedation_data

@router.get("/upsolve", response_model=List[UpsolveResponse])

def upsolve(current_user : AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):

    user = get_linked_cf_user(current_user.id, session)

    upsolve_rows = session.scalars(
        select(RecommendationQueue).where(
            RecommendationQueue.user_id == user.id,
            RecommendationQueue.recommendation_type == "upsolve",
            RecommendationQueue.is_dismissed == False
        )
    ).all()

    upsolve_data = []

    for row in upsolve_rows:
        upsolve_data.append({
            "problem_contest_id": row.problem_contest_id,
            "problem_index": row.problem_index,
            "is_completed": row.is_completed,
        })
    logger.info(upsolve_data)
    return upsolve_data

from schemas import MLRecommendationResponse, MLInsightResponse
from services.recommendation_services import generate_ml_recommendations, generate_problem_insights

@router.get("/personalized", response_model=List[MLRecommendationResponse])
def personalized_recommendations(current_user: AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):
    user = get_linked_cf_user(current_user.id, session)
    if not user:
        raise HTTPException(status_code=404, detail="Codeforces user not found")
        
    recommendations = generate_ml_recommendations(session, user.id)
    return recommendations

@router.get("/personalized/{problem_id}/insights", response_model=MLInsightResponse)
def personalized_problem_insights(problem_id: str, current_user: AppUsers = Depends(get_current_user), session: Session = Depends(get_db)):
    user = get_linked_cf_user(current_user.id, session)
    if not user:
        raise HTTPException(status_code=404, detail="Codeforces user not found")
        
    insights = generate_problem_insights(session, user.id, problem_id)
    return insights
