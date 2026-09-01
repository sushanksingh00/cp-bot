import requests

#------------------------------------------------------------------
#--------------------CODEFORCES------------------------------------
#------------------------------------------------------------------

def fetch_cf_userdata(user_id: str):
    url =  f"https://codeforces.com/api/user.info?handles={user_id}"
    response = requests.get(url, timeout=10)
    data = response.json()

    if data["status"] != "OK":
        print("cf submission me error")
        raise Exception("Codeforces API failed")
    
    user_data = []
    
    for result in data["result"]:
        
        # Some Codeforces users may be unrated; those keys can be absent.
        user_data.append({
                "lastOnlineTimeSeconds": result.get("lastOnlineTimeSeconds"),
                "rating": result.get("rating"),
                "titlePhoto": result.get("titlePhoto"),
                "rank": result.get("rank"),
                "handle": result.get("handle"),
                "maxRating": result.get("maxRating"),
                "registrationTimeSeconds": result.get("registrationTimeSeconds"),
                "maxRank": result.get("maxRank"),
                })

    return user_data

def fetch_cf_submission_history(user_id: str):
    url =  f"https://codeforces.com/api/user.status?handle={user_id}"
    response = requests.get(url, timeout=10)
    data = response.json()

    if data["status"] != "OK":
        raise Exception("Codeforces API failed")
    
    submission = []
    for result in data["result"]:

        problem = result["problem"]

        creation_time_seconds = result.get("creationTimeSeconds")

        submission.append({
            "handle": user_id,
            # Backward-compat alias (older code used this key name).
            "user_id": user_id,
                "submission_id": result["id"],
                "contest_id": result["contestId"],
                "programmingLanguage": result["programmingLanguage"],
                "verdict": result["verdict"],
                "passedTestCount": result["passedTestCount"],
                "timeConsumedMillis": result["timeConsumedMillis"],
                "memoryConsumedBytes": result["memoryConsumedBytes"],
                "problem_contest_id": problem["contestId"],
                "problem_index": problem["index"],
                "problem_name": problem["name"],
                "problem_type": problem["type"],
                "problem_tags": problem["tags"],
            # Prefer the correctly-spelled key.
            "creation_time_seconds": creation_time_seconds,
            # Backward-compat alias for existing code paths.
            "creation_time_secands": creation_time_seconds,

        })
    return submission



def fetch_cf_contest_history(handle: str):
    url = (
        f"https://codeforces.com/api/user.rating?handle={handle}"
    )

    response = requests.get(url, timeout=10)
    data = response.json()

    if data["status"] != "OK":
        raise Exception("Codeforces API failed")

    contests = []
    for result in data["result"]:
        contests.append({
            "contest_id": result["contestId"],
            "contest_name": result["contestName"],
            "handle": result["handle"],
            "rank": result["rank"],
            "rating_update_time": result["ratingUpdateTimeSeconds"],
            "old_rating": result["oldRating"],
            "new_rating": result["newRating"],
            "rating_change": result["newRating"] - result["oldRating"]
        })
    return contests

import time

_cf_problems_cache = None
_cf_problems_cache_time = 0

def fetch_cf_problems():
    global _cf_problems_cache, _cf_problems_cache_time
    
    # Cache for 1 hour (3600 seconds)
    current_time = time.time()
    if _cf_problems_cache is not None and (current_time - _cf_problems_cache_time) < 3600:
        return _cf_problems_cache
        
    url = (
        f"https://codeforces.com/api/problemset.problems"
    )
    response = requests.get(url, timeout=10)
    data = response.json()

    if data["status"] != "OK":
        print("cf pset me error")
        raise Exception("Codeforces API failed")
    
    problems = data.get("result", {}).get("problems", [])

    problem_set = []
    for problem in problems:
        problem_set.append({
            "contest_id": problem.get("contestId"),
            "problem_index": problem.get("index"),
            "problem_name": problem.get("name"),
            "tags": problem.get("tags", []),
            "rating": problem.get("rating"),
        })

    _cf_problems_cache = problem_set
    _cf_problems_cache_time = current_time
    
    return problem_set
#------------------------------------------------------------------
#--------------------LEETCODE--------------------------------------
#------------------------------------------------------------------

def fetch_lc_userdata(user_id:str):
    url = f"https://alfa-leetcode-api.onrender.com/{user_id}/profile"
    response = requests.get(url)
    if response:
        print(response.json())
    return {"message": "username invalid"}

#------------------------------------------------------------------
#--------------------GFG-------------------------------------------
#------------------------------------------------------------------

# def fetch_gfg_userdata(user_id:str):
#     url = f"https://geeks-for-geeks-api.vercel.app/{user_id}"
#     response = requests.get(url)
#     if response:
#         print(response.json())
#     return {"message": "username invalid"}


if __name__ == "__main__":
    # Manual debug helpers (won't run when imported by FastAPI)
    fetch_cf_submission_history("sushanksingh")

#https://codeforces.com/api/problemset.problems 
#all problems with tags and name