
from fastapi import APIRouter, Depends
from crud import * 
from externalapi import *
from fastapi import HTTPException
from services.auth_services import get_current_user
from helpers import get_linked_cf_user
from typing import List
from schemas import RecommendationResponse, UpsolveResponse

router = APIRouter(
    prefix="/users",
    tags=["Recommendations"] # for swagger ui
)


@router.get("/recommendations", response_model=List[RecommendationResponse])

def recommendations_info(current_user : AppUsers = Depends(get_current_user)):

    user = get_linked_cf_user(current_user.id)

    with sessionLocal() as session:
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

def upsolve(current_user : AppUsers = Depends(get_current_user)):

    user = get_linked_cf_user(current_user.id)

    with sessionLocal() as session:
        upsolve_rows = session.scalars(select(RecommendationQueue).where(
            RecommendationQueue.user_id == user.id,
            RecommendationQueue.recommendation_type == "upsolve"
        )).all()

        upsolve_data = []
        for row in upsolve_rows:
            upsolve_data.append({
                "problem_contest_id" : row.problem_contest_id,
                "problem_index" : row.problem_index,
            })
    return upsolve_data
