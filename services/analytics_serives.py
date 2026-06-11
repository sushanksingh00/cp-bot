from crud import *
from services.recommendation_services import *
from datetime import timedelta

def compute_daily_activity(session, handle):

    user = fetch_user_by_handle( "codeforces", handle )

    rows = session.query(ProblemAttempt).filter(
        ProblemAttempt.user_id == user.id
    ).all()

    daily = {}

    for row in rows:
        day = row.submitted_at.date()
        if day not in daily:
            daily[day] = []
        daily[day].append(row)

    for day, submissions in daily.items():
        attempted = set()
        solved = set()

        ratings = []
        rating_seen = set()

        contest_participated = False

        for sub in submissions: 
            # submissions is list
            key = (sub.contest_id, sub.problem_index)

            attempted.add(key)
            if sub.verdict == "OK":
                solved.add(key)

            if key not in rating_seen:
                rating_seen.add(key)

                if sub.problem_rating is not None:
                    ratings.append(
                        sub.problem_rating
                    )

            if sub.contest_id is not None:
                contest_participated = True

        avg_rating = ( sum(ratings) / len(ratings) if ratings else None )

        update_daily_activity(session,
            user.id,
            day,
            len(attempted),
            len(solved),
            avg_rating,
            0,
            contest_participated,
        )
            

def compute_tag_performance(session,handle):
    user = fetch_user_by_handle("codeforces", handle)


    rows = session.query(ProblemAttempt).filter(ProblemAttempt.user_id == user.id).all()
    
    tag_data = {}
    for row in rows:
        for tag in row.tags_jsonb:
            if tag not in tag_data:
                tag_data[tag] = {
                    "attempted" : set(),
                    "solved" : set(),
                    "rating" : [],
                    "hardest_solved" : 0
                }
            
            tag_data[tag]["attempted"].add(row.problem_name)
            if row.verdict == "OK":
                tag_data[tag]["solved"].add(row.problem_name)

            if row.problem_rating:
                tag_data[tag]["hardest_solved"] = max(tag_data[tag]["hardest_solved"], row.problem_rating)
                tag_data[tag]["rating"].append(row.problem_rating)
            
    for tag, stats in tag_data.items():
        attempt_count = len(stats["attempted"])
        solved_count = len(stats["solved"])

        success_rate = (solved_count/attempt_count)*100

        avg_problem_rating = (sum(stats["rating"])/len(stats["rating"]) if stats["rating"] else 0) 

        weakness_score = (
            (1 - success_rate/100)
            * avg_problem_rating
            if avg_problem_rating else 0
        )

        confidence_rate = min(
            attempt_count / 50,
            1.0
        )



        update_tag_performance(session,
            user.id, 
            tag,
            attempt_count,
            solved_count,
            success_rate,
            avg_problem_rating,
            stats["hardest_solved"],
            weakness_score
        )



def compute_recommendation_queue(session,
    handle
):

    user = fetch_user_by_handle(
        "codeforces",
        handle
    )


    generate_weak_tag_recommendations(
        session,
        user.id
    )
    generate_consistency_recommendations(
        session,
        user.id
    )
    generate_rating_push_recommendations(
        session,
        user.id
    )
    generate_contest_preparation_recommendations(
        session,
        user.id
    )
    generate_upsolve_recommendations(
        session,
        user.id
    )

def compute_skill_estimate(session,handle):

    user = fetch_user_by_handle(
        "codeforces",
        handle
    )



    rows = session.query(ProblemAttempt).filter(
        ProblemAttempt.user_id == user.id).all()

    tag_data = {}

    for row in rows:

        for tag in row.tags_jsonb:
            if tag not in tag_data:
                tag_data[tag] = {
                    "solved_ratings": [],
                    "all_ratings": [],
                    "attempted": 0,
                    "solved": 0
                }

            tag_data[tag]["attempted"] += 1

            if row.problem_rating:
                tag_data[tag]["all_ratings"].append(row.problem_rating)

            if row.verdict == "OK":
                tag_data[tag]["solved"] += 1

                if row.problem_rating:
                    tag_data[tag]["solved_ratings"].append(row.problem_rating)

    for tag, stats in tag_data.items():

        sample_size = stats["attempted"]
        solved_ratings = stats["solved_ratings"]
        estimated_rating = (
            sum(solved_ratings)/len(solved_ratings)
            if solved_ratings
            else 0
        )

        confidence_score = min(sample_size / 50 , 1.0)

        trend = compute_tag_trend(session, user.id,tag)

        update_skill_estimate(session,
            user.id,
            tag,
            estimated_rating,
            confidence_score,
            sample_size,
            trend
        )

def compute_tag_trend(session,user_id,tag): #30 din phle solved avg rating vs ab ka solve avg rating fo that tag

    cutoff = (datetime.utcnow() - timedelta(days=30))



    rows = session.query(ProblemAttempt).filter(ProblemAttempt.user_id == user_id).all()

    recent = []
    old = []

    for row in rows:

        if tag not in row.tags_jsonb: continue

        if (row.verdict != "OK" or row.problem_rating is None): continue

        if row.submitted_at >= cutoff:
            recent.append(row.problem_rating)

        else:
            old.append(row.problem_rating)

    if not recent or not old:
        return 0

    recent_avg = (sum(recent)/len(recent))

    old_avg = (sum(old)/len(old))

    return recent_avg - old_avg