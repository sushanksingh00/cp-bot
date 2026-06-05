from crud import *
from externalapi import *
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from services.analytics_serives import *
from services.recommendation_services import *
from services.sync_services import *
from services.auth_services import get_current_user
from schema import UserCreate, UserBase
from datetime import datetime, UTC

router = APIRouter(
    prefix="/sync",
    tags=["Sync"]
)

@router.post("/codeforces")
def sync(user: UserBase, current_user: AppUsers = Depends(get_current_user)):
    try:
        cf_data = fetch_cf_userdata(user.handle)[0]
        print("ye thik h sync wala")
        handle = cf_data["handle"]

    except Exception:
        raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")

    existing_user = fetch_user_by_handle(
        "codeforces",
        handle
    )

    if existing_user:
        update_user("codeforces", handle, cf_data["rating"],
                    cf_data["maxRating"], cf_data["rank"], cf_data["maxRank"], current_user.id)
    else:
        insert_user("codeforces", handle, cf_data["rating"],
                    cf_data["maxRating"], cf_data["rank"], cf_data["maxRank"], current_user.id)
        
    sync_user_contests(handle)
    compute_problem_attempt(handle)
    compute_daily_activity(handle)
    compute_tag_performance(handle)
    #skill estimate here
    compute_recommendation_queue(handle)

    return {"message": "User Synced Succesfully"}
