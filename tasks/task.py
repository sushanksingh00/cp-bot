from core.celery_app import celery_app
import time

from services.analytics_serivces import *
from services.recommendation_services import *
from services.sync_services import *

from core.redis_client import redis_client
from database import sessionLocal

from core.logger import logger

from config import USE_REDIS


@celery_app.task
def long_task():
    logger.info("started")
    time.sleep(2)
    logger.info("finished")
    return "done"


@celery_app.task
def sync_user(handle_, app_user_id):

    with sessionLocal() as session:

        logger.debug("TEST DB:", session.bind.url)

        cf_data = fetch_cf_userdata(handle_)[0]
        handle = cf_data["handle"]

        logger.debug(handle)

        existing_user = fetch_user_by_handle(
            "codeforces",
            handle,
            session
        )

        if existing_user:
            update_user(
                "codeforces",
                handle,
                cf_data["rating"],
                cf_data["maxRating"],
                cf_data["rank"],
                cf_data["maxRank"],
                app_user_id,
                session
            )
        else:
            insert_user(
                "codeforces",
                handle,
                cf_data["rating"],
                cf_data["maxRating"],
                cf_data["rank"],
                cf_data["maxRank"],
                app_user_id,
                session
            )

        sync_user_contests(session, handle)
        compute_problem_attempt(session, handle)
        compute_daily_activity(session, handle)
        compute_tag_performance(session, handle)
        compute_skill_estimate(session, handle)
        compute_recommendation_queue(session, handle)

        db_user = fetch_user_by_handle(
            "codeforces",
            handle,
            session
        )

    logger.info(f"dashboard:{db_user.id}")

    if USE_REDIS:
        redis_client.delete(
            f"dashboard:{db_user.id}"
        )

    return {
        "message": "sync completed",
        "handle": handle
    }