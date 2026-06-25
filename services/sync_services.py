from crud import *
from externalapi import *
from fastapi import FastAPI, HTTPException
from datetime import UTC

from core.logger import logger

def sync_user_contests(session, handle):
    try :
        cf_contest_data = fetch_cf_contest_history(handle) # a list of dict of contests
        cf_submission_data = fetch_cf_submission_history(handle) # a list of dict of submissions for each prob

    except Exception:
        logger.exception("User not found or codeforces API failed")
        raise HTTPException(status_code=404, detail="User not Found or Codeforces API failed")
    
    for contest in cf_contest_data:

        attempted = set()
        solved = set()
        contest_id = contest['contest_id']

        for sub in cf_submission_data:
            if contest_id != sub["contest_id"]:
                continue

            attempted.add(sub["problem_index"])

            if sub["verdict"] == "OK":
                solved.add(sub["problem_index"])

            
        problems_solved = len(solved)
        total_problems = len(attempted)
        
        update_contest_performance(session,
                                   contest["contest_id"],
                                   contest["contest_name"],
                                   contest["rank"],
                                   contest["old_rating"],
                                   contest["new_rating"],
                                   handle,
                                   "codeforces",
                                   problems_solved,
                                   total_problems-problems_solved)
        
    return {"message": "Contest data synced succesfully"}
        


def compute_problem_attempt(session, handle):
    try:
        cf_submission_data = fetch_cf_submission_history(handle)
        problem_set = fetch_cf_problems()
    except Exception:
        logger.exception("Either CF API is not Working or Username not found")
        raise HTTPException(status_code=404, detail="Either CF API is not Working or Username not found")

    db_user = fetch_user_by_handle("codeforces", handle, session)
    if db_user is None:
        # User must exist in DB before we can attach activity rows.
        return {"message": "User not found in DB"}

    problem_lookup = {}
    for problem in problem_set:
        contest_id = problem.get("contest_id")
        index = problem.get("problem_index")
        if contest_id is None or index is None:
            continue
        problem_lookup[(contest_id, index)] = problem
    
    for sub in cf_submission_data:
        submission_ts = sub.get("creation_time_seconds") or sub.get("creation_time_secands")
        if submission_ts is None:
            continue

        submitted_at = datetime.fromtimestamp(submission_ts, UTC)

        problem = problem_lookup.get((sub.get("problem_contest_id"), sub.get("problem_index")))
        if not problem:
            continue

        update_problem_attempted(session,
            db_user.id,
            sub["submission_id"],
            sub["contest_id"],
            sub.get("problem_index"),
            problem.get("problem_name"),
            problem.get("rating"),
            sub.get("verdict"),
            sub.get("programmingLanguage"),
            problem.get("tags", []),
            submitted_at,
        )
    #compute_daily_activity(handle)
    #compute_tag_performance(handle)

    return {"message":"problem Attempted synced succesfully"}
