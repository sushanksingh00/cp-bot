
from fastapi import APIRouter
from crud import * 
from externalapi import *
from fastapi import HTTPException

router = APIRouter(
    prefix="/users",
    tags=["Recommendations"] # for swagger ui
)


@router.get("/{handle}/recommendations")
def recommendations_info(handle:str):
    try:
        cf_data = fetch_cf_userdata(handle)[0]
    except Exception:
        raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")
    
    handle = cf_data["handle"]
    user = fetch_user_by_handle("codeforces", handle)

    with sessionLocal() as session:
        rec_rows = session.scalars(select(RecommendationQueue).where(
            RecommendationQueue.user_id == user.id,
            RecommendationQueue.recommendation_type != "upsolve"
        )).all()

        recommnedation_data =[]
        for row in rec_rows:
            recommnedation_data.append({
                "recommendation_type": row.recommendation_type,
                "reason": row.reason
            })
    return recommnedation_data

@router.get("/{handle}/upsolve")
def upsolve(handle:str):
    try:
        cf_data = fetch_cf_userdata(handle)[0]
    except Exception:
        raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")
    
    handle = cf_data["handle"]
    user = fetch_user_by_handle("codeforces", handle)

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
