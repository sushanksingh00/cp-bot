from fastapi import FastAPI
from database import engine
from models import Base

#once alembic is doing we remove this
#Base.metadata.create_all(bind=engine) # this is create table if not exist

app = FastAPI(
    title= "AI Analytics for CP"
)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", #frontend ka origin
        "https://cp-bot-main.onrender.com/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers.sync import router as sync_router
from routers.health import router as healh_router
from routers.users import router as user_router
from routers.recommendations import router as recommendation_router
from routers.analytics import router as analytics_router
from routers.auth import router as auth_router


app.include_router(sync_router)
app.include_router(healh_router)
app.include_router(user_router)
app.include_router(recommendation_router)
app.include_router(analytics_router)
app.include_router(auth_router)

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Analytics for CP"
    }
















#from fastapi.responses import JSONResponse



# from externalapi import *
# from crud import *
# from schema import UserCreate, UserBase
# from datetime import datetime, UTC

# from services.analytics_serives import *
# from services.recommendation_services import *
# from services.sync_services import *


# @app.delete("/delete") #need to be updated
# def delete_user_route(user: UserBase):

#     existing_user = fetch_user_by_handle(
#         user.platform,
#         user.handle
#     )
#     if existing_user:
#         delete_user(user.platform, user.handle)

#     return {"message":"User deleted Succesfully"}


# def compute_recommendation_queue(
#     handle
# ):

#     user = fetch_user_by_handle(
#         "codeforces",
#         handle
#     )

#     with sessionLocal() as session:
#         generate_weak_tag_recommendations(
#             session,
#             user.id
#         )
#         generate_consistency_recommendations(
#             session,
#             user.id
#         )
#         generate_rating_push_recommendations(
#             session,
#             user.id
#         )
#         generate_contest_preparation_recommendations(
#             session,
#             user.id
#         )
#         generate_upsolve_recommendations(
#             session,
#             user.id
#         )



# @app.get("/users/{handle}")
# def profile(handle: str):
    
#     try:
#         cf_data = fetch_cf_userdata(handle)[0]
#     except Exception:
#         raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")


#     return {
#         "handle" : cf_data["handle"],
#         "curr_rating": cf_data["rating"],
#         "max_rating": cf_data["maxRating"],
#         "rank": cf_data["rank"]
#     }

# @app.get("/users/{handle}/contests")
# def contest_info(handle:str):
#     try:
#         cf_data = fetch_cf_userdata(handle)[0]
#     except Exception:
#         raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")
    
#     handle = cf_data["handle"]
#     user = fetch_user_by_handle("codeforces", handle)

#     with sessionLocal() as session:
#         contest_history = session.scalars(select(ContestPerformance)
#                         .where(ContestPerformance.user_id == user.id)).all()
#         contest_data = []
#         for contest in contest_history:
#             contest_data.append({
#                 "contest_name" : contest.contest_name,
#                 "rank" : contest.rank,
#                 "old_rating" : contest.old_rating,
#                 "new_rating" : contest.new_rating
#             })
#     return contest_data


# @app.get("/users/{handle}/daily-activity")
# def daily_activity_info(handle: str):
#     try:
#         cf_data = fetch_cf_userdata(handle)[0]
#     except Exception:
#         raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")
    
#     handle = cf_data["handle"]
#     user = fetch_user_by_handle("codeforces", handle)

#     with sessionLocal() as session:
#         daily_activity = session.scalars(select(DailyActivity).where(
#             DailyActivity.user_id == user.id
#         )).all()
#         daily_data = []
#         for day in daily_activity:
#             daily_data.append({
#                 "date" : day.date,
#                 "problems_attempted" : day.problems_attempted,
#                 "problems_solved" : day.problems_solved
#             })
#     return daily_data





# @app.get("/users/{handle}/tags")
# def tags_info(handle: str):
#     try:
#         cf_data = fetch_cf_userdata(handle)[0]
#     except Exception:
#         raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")
    
#     handle = cf_data["handle"]
#     user = fetch_user_by_handle("codeforces", handle)

#     with sessionLocal() as session:
#         tags = session.scalars(select(TagPerformance).where(
#             TagPerformance.user_id == user.id
#         )).all()
#         tag_data = []
#         for tag in tags:
#             tag_data.append({
#                 "tag_name": tag.tag_name,
#                 "success_rate" : round(tag.success_rate, 2),
#                 "weakness_score" : round(tag.weakness_score, 2)
#             })
#     return tag_data

# @app.get("/users/{handle}/tags/weakest")
# def weak_tag_info(handle: str):
#     try:
#         cf_data = fetch_cf_userdata(handle)[0]
#     except Exception:
#         raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")
    
#     handle = cf_data["handle"]
#     user = fetch_user_by_handle("codeforces", handle)

#     with sessionLocal() as session:
#         weakest_tag = session.scalars(select(TagPerformance).where(
#             TagPerformance.user_id == user.id
#         ).order_by(
#             TagPerformance.weakness_score.desc()
#         ).limit(3)).all()
#         weak_tag_data = []
#         for tag_ in weakest_tag:
#             weak_tag_data.append(tag_.tag_name)

#     return weak_tag_data


# @app.get("/users/{handle}/recommendations")
# def recommendations_info(handle:str):
#     try:
#         cf_data = fetch_cf_userdata(handle)[0]
#     except Exception:
#         raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")
    
#     handle = cf_data["handle"]
#     user = fetch_user_by_handle("codeforces", handle)

#     with sessionLocal() as session:
#         rec_rows = session.scalars(select(RecommendationQueue).where(
#             RecommendationQueue.user_id == user.id,
#             RecommendationQueue.recommendation_type != "upsolve"
#         )).all()

#         recommnedation_data =[]
#         for row in rec_rows:
#             recommnedation_data.append({
#                 "recommendation_type": row.recommendation_type,
#                 "reason": row.reason
#             })
#     return recommnedation_data

# @app.get("/users/{handle}/upsolve")
# def upsolve(handle:str):
#     try:
#         cf_data = fetch_cf_userdata(handle)[0]
#     except Exception:
#         raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")
    
#     handle = cf_data["handle"]
#     user = fetch_user_by_handle("codeforces", handle)

#     with sessionLocal() as session:
#         upsolve_rows = session.scalars(select(RecommendationQueue).where(
#             RecommendationQueue.user_id == user.id,
#             RecommendationQueue.recommendation_type == "upsolve"
#         )).all()

#         upsolve_data = []
#         for row in upsolve_rows:
#             upsolve_data.append({
#                 "problem_contest_id" : row.problem_contest_id,
#                 "problem_index" : row.problem_index,
#             })
#     return upsolve_data


# @app.get("/users/{handle}/dashboard")
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







# @app.post("/sync/codeforces")
# def sync(user: UserBase):
#     try:
#         cf_data = fetch_cf_userdata(user.handle)[0]
#         print("ye thik h sync wala")

#     except Exception:
#         raise HTTPException(status_code=404, detail="User not found or Codeforces API failed")

#     existing_user = fetch_user_by_handle(
#         "codeforces",
#         cf_data["handle"]
#     )

#     if existing_user:
#         update_user("codeforces", cf_data["handle"], cf_data["rating"],
#                     cf_data["maxRating"], cf_data["rank"], cf_data["maxRank"])
#     else:
#         insert_user("codeforces", cf_data["handle"], cf_data["rating"],
#                     cf_data["maxRating"], cf_data["rank"], cf_data["maxRank"])
        
#     sync_user_contests(cf_data["handle"])
#     print(cf_data["handle"])
#     compute_problem_attempt(cf_data["handle"])
#     compute_recommendation_queue(cf_data["handle"])
#     return {"message": "User Synced Succesfully"}




# def sync_user_contests(handle):
#     try :
#         cf_contest_data = fetch_cf_contest_history(handle) # a list of dict of contests
#         cf_submission_data = fetch_cf_submission_history(handle) # a list of dict of submissions for each prob

#     except Exception:
#         raise HTTPException(status_code=404, detail="User not Found or Codeforces API failed")
    
#     for contest in cf_contest_data:

#         attempted = set()
#         solved = set()
#         contest_id = contest['contest_id']

#         for sub in cf_submission_data:
#             if contest_id != sub["contest_id"]:
#                 continue

#             attempted.add(sub["problem_index"])

#             if sub["verdict"] == "OK":
#                 solved.add(sub["problem_index"])

            
#         problems_solved = len(solved)
#         total_problems = len(attempted)
        
#         update_contest_performance(contest["contest_id"],
#                                    contest["contest_name"],
#                                    contest["rank"],
#                                    contest["old_rating"],
#                                    contest["new_rating"],
#                                    handle,
#                                    "codeforces",
#                                    problems_solved,
#                                    total_problems-problems_solved)
        
#     return {"message": "Contest data synced succesfully"}
        

# def compute_problem_attempt(handle):
#     try:
#         cf_submission_data = fetch_cf_submission_history(handle)
#         problem_set = fetch_cf_problems()
#     except Exception:
#         raise HTTPException(status_code=404, detail="Either CF API is not Working or Username not found")

#     db_user = fetch_user_by_handle("codeforces", handle)
#     if db_user is None:
#         # User must exist in DB before we can attach activity rows.
#         return {"message": "User not found in DB"}

#     problem_lookup = {}
#     for problem in problem_set:
#         contest_id = problem.get("contest_id")
#         index = problem.get("problem_index")
#         if contest_id is None or index is None:
#             continue
#         problem_lookup[(contest_id, index)] = problem
    
#     for sub in cf_submission_data:
#         submission_ts = sub.get("creation_time_seconds") or sub.get("creation_time_secands")
#         if submission_ts is None:
#             continue

#         submitted_at = datetime.fromtimestamp(submission_ts, UTC)

#         problem = problem_lookup.get((sub.get("problem_contest_id"), sub.get("problem_index")))
#         if not problem:
#             continue

#         update_problem_attempted(
#             db_user.id,
#             sub["submission_id"],
#             sub["contest_id"],
#             sub.get("problem_index"),
#             problem.get("problem_name"),
#             problem.get("rating"),
#             sub.get("verdict"),
#             sub.get("programmingLanguage"),
#             problem.get("tags", []),
#             submitted_at,
#         )
#     compute_daily_activity(handle)
#     compute_tag_performance(handle)

#     return {"message":"problem Attempted synced succesfully"}

# def compute_daily_activity(handle):

#     user = fetch_user_by_handle( "codeforces", handle )

#     with sessionLocal() as session:
#         rows = session.query(ProblemAttempt).filter(
#             ProblemAttempt.user_id == user.id
#         ).all()

#         daily = {}

#         for row in rows:
#             day = row.submitted_at.date()
#             if day not in daily:
#                 daily[day] = []
#             daily[day].append(row)

#         for day, submissions in daily.items():
#             attempted = set()
#             solved = set()

#             ratings = []
#             rating_seen = set()

#             contest_participated = False

#             for sub in submissions: 
#                 # submissions is list
#                 key = (sub.contest_id, sub.problem_index)

#                 attempted.add(key)
#                 if sub.verdict == "OK":
#                     solved.add(key)

#                 if key not in rating_seen:
#                     rating_seen.add(key)

#                     if sub.problem_rating is not None:
#                         ratings.append(
#                             sub.problem_rating
#                         )

#                 if sub.contest_id is not None:
#                     contest_participated = True

#             avg_rating = ( sum(ratings) / len(ratings) if ratings else None )

#             update_daily_activity(
#                 user.id,
#                 day,
#                 len(attempted),
#                 len(solved),
#                 avg_rating,
#                 0,
#                 contest_participated,
#             )
            

# def compute_tag_performance(handle):
#     user = fetch_user_by_handle("codeforces", handle)
#     with sessionLocal() as session:

#         rows = session.query(ProblemAttempt).filter(ProblemAttempt.user_id == user.id).all()
        
#         tag_data = {}
#         for row in rows:
#             for tag in row.tags_jsonb:
#                 if tag not in tag_data:
#                     tag_data[tag] = {
#                         "attempted" : set(),
#                         "solved" : set(),
#                         "rating" : [],
#                         "hardest_solved" : 0
#                     }
                
#                 tag_data[tag]["attempted"].add(row.problem_name)
#                 if row.verdict == "OK":
#                     tag_data[tag]["solved"].add(row.problem_name)

#                 if row.problem_rating:
#                     tag_data[tag]["hardest_solved"] = max(tag_data[tag]["hardest_solved"], row.problem_rating)
#                     tag_data[tag]["rating"].append(row.problem_rating)
                
#         for tag, stats in tag_data.items():
#             attempt_count = len(stats["attempted"])
#             solved_count = len(stats["solved"])

#             success_rate = (solved_count/attempt_count)*100

#             avg_problem_rating = (sum(stats["rating"])/len(stats["rating"]) if stats["rating"] else 0) 

#             weakness_score = (
#                 (1 - success_rate/100)
#                 * avg_problem_rating
#                 if avg_problem_rating else 0
#             )

#             confidence_rate = min(
#                 attempt_count / 50,
#                 1.0
#             )



#             update_tag_performance(
#                 user.id, 
#                 tag,
#                 attempt_count,
#                 solved_count,
#                 success_rate,
#                 avg_problem_rating,
#                 stats["hardest_solved"],
#                 weakness_score
#             )

