from sqlalchemy import Integer, String, Boolean, Column, DateTime, ForeignKey, Float, UniqueConstraint, Date, Text
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from database import Base

class AppUsers(Base):
    __tablename__ = "app_users"
    id = Column(Integer, primary_key=True, nullable=False)

    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("username", "email"),
    )


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)

    platform = Column(String, nullable=False)
    handle = Column(String, nullable=False)

    curr_rating = Column(Integer)
    max_rating = Column(Integer)

    rank = Column(String)
    max_rank = Column(String)

    app_user_id = Column(
        Integer,
        ForeignKey("app_users.id"),
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = ( 
        UniqueConstraint("platform", "handle"),
    )

class TagPerformance(Base):
    __tablename__ = "tag_performance"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    tag_name = Column(String, nullable=False)

    total_attempted = Column(Integer, default=0)
    total_solved = Column(Integer, default=0)

    success_rate = Column(Float, default=0)

    avg_problem_rating = Column(Float)
    hardest_solved_rating = Column(Integer)

    weakness_score = Column(Float)

    updated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "tag_name"),
    )

class ContestPerformance(Base):
    __tablename__ = "contest_performance"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    contest_id = Column(Integer)
    contest_name = Column(String)

    rank = Column(Integer)

    old_rating = Column(Integer)
    new_rating = Column(Integer)

    problems_solved = Column(Integer, default=0)


    unsolved_upsolvable_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "contest_id"
        ),
    )

class ProblemAttempt(Base):
    __tablename__ = "problem_attempt"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    contest_id = Column(Integer, nullable=False)

    submission_id = Column(Integer, nullable=False)
    problem_index = Column(String)

    problem_name = Column(String)
    problem_rating = Column(Integer)

    verdict = Column(String)

    language = Column(String)
    tags_jsonb = Column(JSONB)#["dp", "graphs"]

    submitted_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("submission_id"),
    )

class DailyActivity(Base):
    __tablename__ = "daily_activity"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  

    date = Column(Date)

    problems_attempted = Column(Integer)
    problems_solved = Column(Integer)

    average_rating = Column(Integer)
    active_minutes = Column(Integer) #x min
    contest_participated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "date"), # one row per account per day
    )


class RecommendationQueue(Base):
    __tablename__ = "recommendation_queue"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  

    problem_contest_id = Column(Integer)
    problem_index = Column(String) # A B C

    recommendation_type = Column(String)
    """
    weak_tag_improvement
    upsolve
    rating_push
    consistency_boost
    contest_preparation
    """
    reason = Column(Text)

    priority_score = Column(Integer)
    is_completed = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)

    generated_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
    UniqueConstraint(
        "user_id",
        "recommendation_type",
        "problem_contest_id",
        "problem_index"
        ),
    )

class SkillEstimate(Base): #just rearrangement of the tag performancer
    __tablename__ = "skill_estimate"

    id = Column(Integer, primary_key=True)

    account_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    tag_name = Column(String, nullable=False)

    estimated_rating = Column(Integer)

    confidence = Column(Float)

    sample_size = Column(Integer)

    trend = Column(Float)

    last_computed_at = Column(
        DateTime,
        default=datetime.utcnow
    )
