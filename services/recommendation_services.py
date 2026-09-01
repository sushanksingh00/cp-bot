from crud import *

def generate_weak_tag_recommendations(session, user_id):

    weakest_tags = session.scalars(select(TagPerformance)
        .where(TagPerformance.user_id == user_id)
        .order_by(TagPerformance.weakness_score.desc())
        .limit(3)).all()

    reason = "Focus on:\n"

    for tag in weakest_tags:
        reason += (f"{tag.tag_name} "
            f"(success rate "
            f"{tag.success_rate:.1f}%)\n")
    update_recommendation_queue(session,
        user_id=user_id,
        problem_contest_id=None,
        problem_index=None,
        recommendation_type="weak_tag_improvement",
        reason=reason,
        priority_score=85
    )

def generate_consistency_recommendations(
    session,
    user_id
):

    latest_activity = session.scalar(select(DailyActivity)
            .where(DailyActivity.user_id == user_id)
            .order_by(DailyActivity.date.desc()))

    if not latest_activity: return


    inactive_days = (date.today()- latest_activity.date).days


    update_recommendation_queue(session,
        user_id=user_id,
        problem_contest_id=None,
        problem_index=None,
        recommendation_type="consistency_boost",
        reason=(
            f"No activity for "
            f"{inactive_days} days"
        ),
        priority_score=95
    )

def generate_rating_push_recommendations( session, user_id ):

    strong_tags = session.scalars(select(TagPerformance)
        .where(TagPerformance.user_id == user_id,
                TagPerformance.success_rate >= 70)).all()

    if not strong_tags:
        return

    avg_rating = (sum(tag.avg_problem_rating for tag in strong_tags if tag.avg_problem_rating) / len(strong_tags))

    target = int(avg_rating + 100)

    update_recommendation_queue(session,
        user_id=user_id,
        problem_contest_id=None,
        problem_index=None,
        recommendation_type="rating_push",
        reason=(
            f"You seem comfortable at "
            f"{int(avg_rating)}. "
            f"Try {target}-rated problems."
        ),
        priority_score=70
    )

def generate_contest_preparation_recommendations(session,user_id):

    contests = session.scalars(
        select(ContestPerformance)
        .where(ContestPerformance.user_id == user_id)
    ).all()

    if len(contests) < 3:

        update_recommendation_queue(
            user_id=user_id,
            problem_contest_id=None,
            problem_index=None,
            recommendation_type="contest_preparation",
            reason=(
                "Participate in more contests "
                "to improve rating."
            ),
            priority_score=60
        )

def generate_upsolve_recommendations(session,user_id):

    problems = {}

    rows = session.scalars( select(ProblemAttempt)
        .where(ProblemAttempt.user_id == user_id)).all()

    for row in rows:

        key = (row.contest_id, row.problem_index)
        if key not in problems:
            problems[key] = { "solved": False }
        if row.verdict == "OK":
            problems[key]["solved"] = True

    for key, data in problems.items():

        contest_id, index = key

        if data["solved"]:
            complete_upsolve_recommendation(
                session,
                user_id=user_id,
                contest_id=contest_id,
                problem_index=index
            )
            continue

        # ML Integration: Calculate probability of solving this upsolve
        user = session.query(Users).filter(Users.id == user_id).first()
        ml_prob = "Unknown"
        ml_impact = ""
        
        try:
            from services.inference_services import get_solve_probability
            # We don't have the exact problem rating/tags at hand without joining, 
            # so we'll fetch them from the attempt row.
            attempt_row = session.scalars(select(ProblemAttempt).where(
                ProblemAttempt.user_id == user_id, 
                ProblemAttempt.contest_id == contest_id, 
                ProblemAttempt.problem_index == index
            )).first()
            
            if attempt_row and attempt_row.problem_rating:
                ml_res = get_solve_probability(user.handle, attempt_row.problem_rating, attempt_row.tags_jsonb, session)
                if "solve_probability" in ml_res:
                    prob = ml_res["solve_probability"] * 100
                    ml_prob = f"{prob:.1f}%"
                    
                    if ml_res["important_factors"]:
                        ml_impact = f"\nML Insight: {ml_res['important_factors'][0]}"
        except Exception:
            pass

        reason = (
            f"Attempted during contest but never solved.\n"
            f"Predicted Solve Probability: {ml_prob}{ml_impact}"
        )

        update_recommendation_queue(session,
            user_id=user_id,
            problem_contest_id=contest_id,
            problem_index=index,
            recommendation_type="upsolve",
            reason=reason,
            priority_score=75
        )

import random
from externalapi import fetch_cf_problems

def generate_ml_recommendations(session, user_id):
    from services.inference_services import get_solve_probability
    
    user = session.query(Users).filter(Users.id == user_id).first()
    if not user:
        return []
        
    try:
        all_problems = fetch_cf_problems()
    except Exception:
        return []
        
    if not all_problems:
        return []
        
    attempted = session.query(ProblemAttempt.contest_id, ProblemAttempt.problem_index).filter(ProblemAttempt.user_id == user_id).all()
    attempted_set = {(str(r[0]), str(r[1])) for r in attempted}
    
    weak_tags_rows = session.query(TagPerformance.tag_name).filter(
        TagPerformance.user_id == user_id, 
        TagPerformance.total_attempted >= 5
    ).order_by(TagPerformance.success_rate.asc()).limit(5).all()
    
    weak_tags = {r[0] for r in weak_tags_rows}
    
    user_rating = user.curr_rating or 1500
    min_rating = user_rating - 200
    max_rating = user_rating + 400
    
    candidates = []
    for p in all_problems:
        cid = str(p.get("contest_id"))
        idx = str(p.get("problem_index"))
        rating = p.get("rating")
        
        if (cid, idx) in attempted_set:
            continue
            
        if rating is not None and min_rating <= rating <= max_rating:
            candidates.append(p)
            
    if not candidates:
        return []
        
    sample_size = min(50, len(candidates))
    candidates_sample = random.sample(candidates, sample_size)
    
    scored_recommendations = []
    
    for p in candidates_sample:
        rating = p.get("rating")
        tags = p.get("tags", [])
        
        ml_res = get_solve_probability(user.handle, rating, tags, session)
        if "error" in ml_res:
            continue
            
        prob = ml_res["solve_probability"]
        difficulty_band = ml_res["difficulty_band"]
        
        prob_score = 1.0 - abs(0.70 - prob)
        
        weak_tag_overlap = set(tags).intersection(weak_tags)
        tag_bonus = 0.2 * len(weak_tag_overlap)
        
        total_score = prob_score + tag_bonus
        
        reasons = []
        if difficulty_band == "Recommended":
            reasons.append("Matches your current difficulty level.")
        elif difficulty_band == "Stretch":
            reasons.append("Slightly above your recent solving level, making it a useful stretch problem.")
        elif difficulty_band == "Warm-up":
            reasons.append("Good for a quick warm-up.")
        elif difficulty_band == "Challenging":
            reasons.append("This will be a tough challenge.")
            
        if weak_tag_overlap:
            reasons.append(f"Targets one of your weaker topics ({', '.join(weak_tag_overlap)}).")
            
        reason_str = " ".join(reasons) if reasons else "Based on your historical performance."
        
        scored_recommendations.append({
            "problem_id": f"{p.get('contest_id')}{p.get('problem_index')}",
            "rating": rating,
            "tags": tags,
            "solve_probability": prob,
            "difficulty_band": difficulty_band,
            "reason": reason_str,
            "score": total_score
        })
        
    scored_recommendations.sort(key=lambda x: x["score"], reverse=True)
    return scored_recommendations[:5]

def generate_problem_insights(session, user_id, problem_id):
    from services.inference_services import get_solve_probability
    from ml.features import get_inference_features
    from fastapi import HTTPException
    import re
    
    user = session.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    try:
        all_problems = fetch_cf_problems()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch Codeforces problems")
        
    match = re.match(r'^(\d+)(.+)$', problem_id)
    if not match:
        print(f"INSIGHTS REQUEST FAILED (Regex): problem_id={problem_id}")
        raise HTTPException(status_code=400, detail="Invalid problem ID format")
    cid, idx = match.groups()
    
    print(f"INSIGHTS REQUEST:\nproblem_id={problem_id}\nparsed_contest_id={cid}\nparsed_problem_index={idx}")
    
    target_p = None
    for p in all_problems:
        if str(p.get("contest_id")) == cid and str(p.get("problem_index")) == idx:
            target_p = p
            break
            
    print(f"PROBLEM LOOKUP:\nsource=all_problems (len={len(all_problems)})\nfound={target_p is not None}")
            
    if not target_p:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    rating = target_p.get("rating")
    tags = target_p.get("tags", [])
    
    # 1. Model Signals & User Performance
    features = get_inference_features(user.id, rating, tags, session)
    
    # 2. Prediction
    ml_res = get_solve_probability(user.handle, rating, tags, session)
    if "error" in ml_res:
        raise HTTPException(status_code=500, detail=ml_res["error"])
        
    prob = ml_res["solve_probability"]
    difficulty_band = ml_res["difficulty_band"]
    
    # 3. Recommendation Logic
    prob_score = 1.0 - abs(0.70 - prob)
    
    weak_tags_rows = session.query(TagPerformance).filter(
        TagPerformance.user_id == user_id, 
        TagPerformance.total_attempted >= 5
    ).order_by(TagPerformance.success_rate.asc()).limit(5).all()
    
    weak_tags_names = {r.tag_name for r in weak_tags_rows}
    weak_tag_overlap = set(tags).intersection(weak_tags_names)
    tag_bonus = 0.2 * len(weak_tag_overlap)
    
    total_score = prob_score + tag_bonus
    
    reasons = []
    if difficulty_band == "Recommended":
        reasons.append("Matches your current difficulty level.")
    elif difficulty_band == "Stretch":
        reasons.append("Slightly above your recent solving level, making it a useful stretch problem.")
    elif difficulty_band == "Warm-up":
        reasons.append("Good for a quick warm-up.")
    elif difficulty_band == "Challenging":
        reasons.append("This will be a tough challenge.")
        
    if weak_tag_overlap:
        reasons.append(f"Targets one of your weaker topics ({', '.join(weak_tag_overlap)}).")
        
    reason_str = " ".join(reasons) if reasons else "Based on your historical performance."
    
    # 4. Topic Analysis
    topic_analysis = []
    for tag in tags:
        tag_perf = session.query(TagPerformance).filter(
            TagPerformance.user_id == user_id,
            TagPerformance.tag_name == tag
        ).first()
        
        if tag_perf:
            status = "weak" if tag_perf.tag_name in weak_tags_names else "average"
            if tag_perf.success_rate > 0.7 and tag_perf.total_attempted >= 5:
                status = "strong"
                
            topic_analysis.append({
                "tag": tag,
                "attempts": tag_perf.total_attempted,
                "solved": tag_perf.total_solved,
                "solve_rate": tag_perf.success_rate,
                "status": status
            })
        else:
            topic_analysis.append({
                "tag": tag,
                "attempts": 0,
                "solved": 0,
                "solve_rate": 0.0,
                "status": "untested"
            })
            
    # 5. Build insights list
    insights = []
    
    overall_solve = features.get("historical_solve_rate", 0)
    
    if weak_tag_overlap:
        insights.append(f"Your performance on {', '.join(weak_tag_overlap)} problems is below your overall solving rate.")
        
    insights.append(f"This problem falls within your {difficulty_band.lower()} range.")
    insights.append(f"Your predicted probability of solving this problem is {int(prob * 100)}%.")
    
    recent_7 = features.get("recent_7d_solve_rate", 0)
    if recent_7 > overall_solve + 0.05:
        insights.append("Your recent 7-day activity shows improvement above your historical average.")
    elif recent_7 < overall_solve - 0.05 and features.get("recent_7d_attempts", 0) > 0:
        insights.append("Your recent 7-day solve rate has been slightly lower than usual.")
        
    return {
        "problem": {
            "problem_id": problem_id,
            "name": target_p.get("problem_name"),
            "rating": rating,
            "tags": tags,
            "url": f"https://codeforces.com/problemset/problem/{cid}/{idx}"
        },
        "prediction": {
            "solve_probability": prob,
            "difficulty_band": difficulty_band
        },
        "recommendation": {
            "score": total_score,
            "targeted_weak_tags": list(weak_tag_overlap),
            "reason": reason_str
        },
        "user_performance": {
            "overall_solve_rate": overall_solve,
            "recent_7d_solve_rate": features.get("recent_7d_solve_rate", 0),
            "recent_30d_solve_rate": features.get("recent_30d_solve_rate", 0),
            "total_attempts": features.get("total_attempts", 0),
            "total_solved": int(overall_solve * features.get("total_attempts", 0))
        },
        "topic_analysis": topic_analysis,
        "model_signals": {
            "difficulty_relative_to_user": features.get("rating_difference", 0),
            "historical_performance": features.get("historical_solve_rate", 0),
            "recent_performance": features.get("recent_30d_solve_rate", 0),
            "topic_performance": features.get("avg_tag_success", 0),
            "topic_familiarity": features.get("avg_tag_familiarity", 0)
        },
        "insights": insights
    }