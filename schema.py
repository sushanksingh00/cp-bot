from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

#base model -> to use pydantic methods 
#inherits from its base model -> to avoid the repeated fields
#    class Config:
#        from_attributes = True
#this is cuz ---- database return sqlalchemy orm object 
#and pydantic needs dict type objects 
#sqlalchemy returns obj stored in attributes 
#from attributes -> read from att too --> dict type

#app_user

class AppUserRegister(BaseModel):
    username : str
    email : EmailStr
    password : str

class AppUserLogin(BaseModel):
    username : str
    password : str
#users

class UserBase(BaseModel):
    platform: str
    handle: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    curr_rating: Optional[int] = None
    max_rating: Optional[int] = None

    rank: Optional[str] = None
    max_rank: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


#tag performance

class TagPerformanceBase(BaseModel):
    tag_name: str


class TagPerformanceResponse(TagPerformanceBase):
    id: int
    user_id: int

    total_attempted: int
    total_solved: int

    success_rate: float

    avg_problem_rating: Optional[float] = None
    hardest_solved_rating: Optional[int] = None

    weakness_score: Optional[float] = None

    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

#contest performance

class ContestPerformanceBase(BaseModel):
    contest_id: int
    contest_name: str


class ContestPerformanceResponse(
    ContestPerformanceBase
):
    id: int
    user_id: int

    rank: Optional[int] = None

    old_rating: Optional[int] = None
    new_rating: Optional[int] = None

    problems_solved: int

    unsolved_upsolvable_count: Optional[int] = None

    created_at: datetime

    class Config:
        from_attributes = True


#probelem attempted

class ProblemAttemptBase(BaseModel):
    contest_id: int

    submission_id: int

    problem_index: Optional[str] = None

    problem_name: Optional[str] = None

    problem_rating: Optional[int] = None

    verdict: Optional[str] = None

    language: Optional[str] = None

    tags_jsonb: Optional[List[str]] = None


class ProblemAttemptResponse(
    ProblemAttemptBase
):
    id: int
    user_id: int

    submitted_at: datetime

    class Config:
        from_attributes = True


#daily activity

class DailyActivityBase(BaseModel):
    date: date


class DailyActivityResponse(
    DailyActivityBase
):
    id: int
    user_id: int

    problems_attempted: Optional[int] = 0
    problems_solved: Optional[int] = 0

    average_rating: Optional[int] = None

    active_minutes: Optional[int] = 0

    contest_participated: bool = False

    created_at: datetime

    class Config:
        from_attributes = True


#recommendation queue

class RecommendationQueueBase(BaseModel):
    recommendation_type: str

    reason: Optional[str] = None


class RecommendationQueueResponse(
    RecommendationQueueBase
):
    id: int
    user_id: int

    problem_contest_id: Optional[int] = None

    problem_index: Optional[str] = None

    priority_score: Optional[int] = None

    is_completed: bool
    is_dismissed: bool

    generated_at: datetime

    class Config:
        from_attributes = True


#skill estimate

class SkillEstimateBase(BaseModel):
    tag_name: str


class SkillEstimateResponse(
    SkillEstimateBase
):
    id: int

    account_id: int

    estimated_rating: Optional[int] = None

    confidence: Optional[float] = None

    sample_size: Optional[int] = None

    trend: Optional[float] = None

    last_computed_at: datetime

    class Config:
        from_attributes = True