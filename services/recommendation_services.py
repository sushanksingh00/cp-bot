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

        if data["solved"]: continue

        contest_id, index = key

        update_recommendation_queue(session,
            user_id=user_id,
            problem_contest_id=contest_id,
            problem_index=index,
            recommendation_type="upsolve",
            reason=(
                "Attempted during contest "
                "but never solved."
            ),
            priority_score=75
        )