from models import *
from database import Base, engine, sessionLocal
from sqlalchemy import select
from schemas import UserBase
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, date

def fetch_user_by_handle(platform:str, handle:str, session):

    stmt = select(Users).where(Users.handle == handle,
                                Users.platform == platform)
    user = session.scalar(stmt)
    if user:
        return user
    return None


def insert_user(platform: str,
                handle: str,
                curr_rating: int,
                max_rating:int,
                rank : str,
                max_rank :str,
                current_user_id:int, session):

    user = Users(platform=platform,
                    handle=handle,
                    curr_rating=curr_rating,
                    max_rating=max_rating,
                    rank=rank,
                    max_rank=max_rank,
                    app_user_id = current_user_id)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(platform: str,
                handle: str,
                curr_rating: int,
                max_rating:int,
                rank : str,
                max_rank :str,
                app_user_id:int, session):

    user = session.query(Users).filter(
        Users.handle==handle,
        Users.platform == platform
    ).first()

    if user is None: return None

    user.curr_rating = curr_rating
    user.max_rating = max_rating
    user.rank = rank
    user.max_rank = max_rank
    # Ensure this row gets an UPDATE even when values are unchanged.
    user.updated_at = datetime.utcnow()

    # Always bump last-sync timestamp even if values are unchanged.
    # Otherwise SQLAlchemy may skip emitting an UPDATE.
    user.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(user)
    return user

def delete_user(platform:str, handle:str, session):


    user = session.query(Users).filter(
        Users.platform == platform,
        Users.handle == handle
    ).first()

    if user is None: return None

    user_id = session.query(Users.id).filter(
        Users.platform ==platform,
        Users.handle == handle
    ).scalar()

    account_id = session.query(Users.app_user_id).filter(
        Users.platform ==platform,
        Users.handle == handle
    ).scalar()

    contest_entries = session.query(ContestPerformance).filter(
        ContestPerformance.user_id == user_id
    )

    problem_entries = session.query(ProblemAttempt).filter(
        ProblemAttempt.user_id == user_id
    )

    daily_activity_entries = session.scalars(select(DailyActivity).where(
        DailyActivity.user_id == user_id
    ))

    tag_performance_entries = session.scalars(select(TagPerformance).where(
        TagPerformance.user_id == user_id
    ))

    recommendation_queue_entries = session.scalars(select(RecommendationQueue).where(
        RecommendationQueue.user_id == user_id
    ))

    skill_estimate_entries = session.scalars(select(SkillEstimate).where(
        SkillEstimate.account_id == user_id
    ))

    for skill in skill_estimate_entries:
        session.delete(skill)

    for recommendation in recommendation_queue_entries:
        session.delete(recommendation)

    for tag in tag_performance_entries:
        session.delete(tag)

    for daily in daily_activity_entries:
        session.delete(daily)


    for problem in problem_entries:
        session.delete(problem)
    
    for contest in contest_entries:
        session.delete(contest)
        
    session.delete(user)
    session.commit()


def update_contest_performance(session,
                               contest_id: int,
                               contest_name: str,
                               rank: int,
                               old_rating: int,
                               new_rating : int,
                               handle :str,
                               platform: str,
                               problems_solved: int,
                               unsolved_upsolvable_count: int
                               ):

    user_id = session.query(Users.id).filter(Users.platform == platform,
                                    Users.handle == handle).scalar()
    
    if user_id is None:
        return None
    
    contest = session.query(
        ContestPerformance
    ).filter(
        ContestPerformance.user_id == user_id,
        ContestPerformance.contest_id == contest_id
    ).first()

    if contest:

        contest.contest_name = contest_name
        contest.rank = rank
        contest.old_rating = old_rating
        contest.new_rating = new_rating
        contest.problems_solved = problems_solved
        contest.unsolved_upsolvable_count = unsolved_upsolvable_count

    else:

        contest = ContestPerformance(
            user_id=user_id,
            contest_id=contest_id,
            contest_name=contest_name,
            rank=rank,
            old_rating=old_rating,
            new_rating=new_rating,
            problems_solved = problems_solved,
            unsolved_upsolvable_count=unsolved_upsolvable_count
        )

        session.add(contest)

    session.commit()
    session.refresh(contest)

    return contest
def update_problem_attempted(session,
                             user_id : int,
                             submission_id : int,
                             contest_id : int,
                             problem_index : str,
                             problem_name : str,
                             problem_rating: int,
                             verdict : str,
                             language: str,
                             tagsJSONB : JSONB,
                             submitted_at: datetime):


        existing_submission = session.scalar(
            select(ProblemAttempt).where(
                ProblemAttempt.submission_id == submission_id
            )
        )

        if existing_submission:
            return existing_submission

        submission = ProblemAttempt(
            user_id=user_id,
            contest_id=contest_id,
            submission_id=submission_id,
            problem_index=problem_index,
            problem_name=problem_name,
            problem_rating=problem_rating,
            verdict=verdict,
            language=language,
            tags_jsonb=tagsJSONB,
            submitted_at=submitted_at
        )

        session.add(submission)
        session.commit()
        session.refresh(submission)

        return submission
        


def update_daily_activity(session,
                          user_id: int,
                          date: date,
                          problems_attempted: int, 
                          problems_solved: int,
                          average_rating: int,
                          active_minutes: int | None,
                          contest_participated : bool,
                        ):

    daily_activity = session.scalar(select(DailyActivity).where(
        DailyActivity.user_id == user_id,
        DailyActivity.date == date
    ))

    if daily_activity:
        daily_activity.problems_attempted = problems_attempted
        daily_activity.problems_solved = problems_solved
        daily_activity.average_rating = average_rating
        daily_activity.active_minutes = active_minutes
        daily_activity.contest_participated = contest_participated

    else:
        daily_activity = DailyActivity(
            user_id = user_id,
            date = date,
            problems_solved = problems_solved,
            problems_attempted = problems_attempted,
            average_rating = average_rating,
            active_minutes = active_minutes,
            contest_participated = contest_participated,
        )
        session.add(daily_activity)

    session.commit()
    session.refresh(daily_activity)

    return daily_activity


def update_tag_performance(session,
                           user_id : int,
                           tag_name : str,
                           total_attempted : int,
                           total_solved : int,
                           success_rate : float,
                           avg_problem_rating: float,
                           hardest_solved_rating: int,
                           weakness_score : int):

    tag_row = session.scalar(select(TagPerformance).where(
        TagPerformance.user_id == user_id,
        TagPerformance.tag_name == tag_name
    ))

    if tag_row:
        tag_row.total_attempted = total_attempted
        tag_row.total_solved = total_solved
        tag_row.success_rate = success_rate
        tag_row.avg_problem_rating = avg_problem_rating
        tag_row.hardest_solved_rating = hardest_solved_rating
        tag_row.weakness_score = weakness_score


    else:

        tag_row = TagPerformance(
                    user_id = user_id,
                    tag_name = tag_name,
                    total_attempted = total_attempted,
                    total_solved = total_solved,
                    success_rate = success_rate,
                    avg_problem_rating = avg_problem_rating,
                    hardest_solved_rating = hardest_solved_rating,
                    weakness_score = weakness_score
        )
        session.add(tag_row)
    session.commit()
    session.refresh(tag_row)

    return tag_row

def update_recommendation_queue(session,
    user_id: int,
    problem_contest_id: int | None,
    problem_index: str | None,
    recommendation_type: str,
    reason: str,
    priority_score: int,
    is_completed: bool = False,
    is_dismissed: bool = False
):



    recommendation = session.scalar(
        select(RecommendationQueue).where(
            RecommendationQueue.user_id == user_id,
            RecommendationQueue.recommendation_type == recommendation_type,
            RecommendationQueue.problem_contest_id == problem_contest_id,
            RecommendationQueue.problem_index == problem_index )
    )

    if recommendation:

        recommendation.reason = reason
        recommendation.priority_score = priority_score
        recommendation.is_completed = is_completed
        recommendation.is_dismissed = is_dismissed

    else:

        recommendation = RecommendationQueue(
            user_id=user_id,
            problem_contest_id=problem_contest_id,
            problem_index=problem_index,
            recommendation_type=recommendation_type,
            reason=reason,
            priority_score=priority_score,
            is_completed=is_completed,
            is_dismissed=is_dismissed
        )

        session.add(recommendation)

    session.commit()
    session.refresh(recommendation)

    return recommendation
    

def update_skill_estimate(session,
    user_id,
    tag_name,
    estimated_rating,
    confidence_score,
    sample_size,
    trend
):



    row = session.scalar(select(SkillEstimate).where(
            SkillEstimate.account_id == user_id,
            SkillEstimate.tag_name == tag_name
        )
    )

    if row:

        row.estimated_rating = estimated_rating
        row.confidence = confidence_score
        row.sample_size = sample_size
        row.trend = trend

    else:

        row = SkillEstimate(
            account_id=user_id,
            tag_name=tag_name,
            estimated_rating=estimated_rating,
            confidence=confidence_score,
            sample_size=sample_size,
            trend=trend
        )

        session.add(row)

    session.commit()
    session.refresh(row)


def complete_upsolve_recommendation(
    session,
    user_id,
    contest_id,
    problem_index,
):
    recommendation = session.scalar(
        select(RecommendationQueue).where(
            RecommendationQueue.user_id == user_id,
            RecommendationQueue.recommendation_type == "upsolve",
            RecommendationQueue.problem_contest_id == contest_id,
            RecommendationQueue.problem_index == problem_index,
            RecommendationQueue.is_completed == False
        )
    )

    if recommendation:
        recommendation.is_completed = True
        session.commit()