from core.celery_app import celery_app
import time
from services.analytics_serivces import *
from services.recommendation_services import *
from services.sync_services import *
from core.redis_client import redis_client

@celery_app.task
def long_task():
    print("started")
    time.sleep(2)
    print("finished")
    return "done"

@celery_app.task
def sync_user(handle_, app_user_id, session):
    # try:
    #     cf_data = fetch_cf_userdata(handle_)[0] 
    #     print("ye thik h sync wala")
    #     handle = cf_data["handle"] #actual handle
    #     print(handle)

    # except Exception:
    #     raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")

    cf_data = fetch_cf_userdata(handle_)[0]
    handle = cf_data["handle"]
    print(handle)

    existing_user = fetch_user_by_handle(
        "codeforces",
        handle
    )
    if existing_user:
        update_user("codeforces", handle, cf_data["rating"],
                    cf_data["maxRating"], cf_data["rank"], cf_data["maxRank"], app_user_id, session)
    else:
        insert_user("codeforces", handle, cf_data["rating"],
                    cf_data["maxRating"], cf_data["rank"], cf_data["maxRank"], app_user_id, session)
        
    with sessionLocal() as session:
        sync_user_contests(session, handle)
        compute_problem_attempt(session, handle)
        compute_daily_activity(session,handle)
        compute_tag_performance(session,handle)
        compute_skill_estimate(session,handle)
        compute_recommendation_queue(session,handle)

    db_user = fetch_user_by_handle(
        "codeforces",
        handle
    )

    print(f"dashboard:{db_user.id}")
    
    redis_client.delete(
        f"dashboard:{db_user.id}"
    )
    
    return {
        "message":"sync compleated",
        "handle":handle
    }