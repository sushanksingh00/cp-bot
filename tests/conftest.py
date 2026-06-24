
from fastapi.testclient import TestClient
from main import app
import pytest
import uuid
from crud import delete_user
from database import Base, test_engine

from database import get_db
from database import test_engine
from sqlalchemy.orm import sessionmaker

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

from fastapi import Depends


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def user_data():
    unique_id = uuid.uuid4()
    return {
        "username" : f"user_{unique_id}",
        "email" : f"test_{unique_id}@test.com",
        "password" : "12345678"
    }

@pytest.fixture
def registered_user(db, client, user_data):
    client.post("/auth/register", json=user_data)

    app_user = db.scalar(select(AppUsers).where(
        AppUsers.username == user_data["username"]
    ))

    yield app_user

    db.delete(app_user)
    db.commit()


@pytest.fixture
def header_token(client, registered_user):
    response = client.post("/auth/login", json={
        "username" : registered_user.username,
        "password" : "12345678"
    })

    token = response.json()["token"]

    return {
        "Authorization" : f"Bearer {token}"
    }

@pytest.fixture
def synced_header_token(client, header_token):
    response = client.post(
        "/sync/codeforces",
        json={
            "platform" : "codeforces",
            "handle" : "Um_nik"
        },
        headers=header_token
    )

    task_id = response.json()["task_id"]

    status = check_status(client, task_id, header_token)

    assert status == "SUCCESS" 

    yield header_token

    delete_user("codeforces", "Um_nik")



import time
import pytest

def check_status(client, task_id, header_token):
    for _ in range(60):

        response = client.get(
            f"/sync/status/{task_id}",
            headers=header_token
        )

        status = response.json()["state"]

        if status == "SUCCESS":
            return status

        if status == "FAILURE":
            pytest.fail("Sync task failed")

        time.sleep(1)

    else:
        pytest.fail("Sync task timed out")








#independent tesitng of the every endpoint

import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_database():

    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db():

    connection = TestingSessionLocal()

    try:
        yield connection
    finally:
        connection.close()

def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


#fake cp user
import uuid
from models import Users, AppUsers
from sqlalchemy import select


# @pytest.fixture
# def app_user(db):
#     unique_id = uuid.uuid4()
#     new_user = AppUsers(
#         username = f"user_{unique_id}",
#         password = "123",
#         email = f"test_{unique_id}@test.com"
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     app_user_id = db.scalar(select(AppUsers.id).where(
#         AppUsers.username == f"user_{unique_id}"
#     ))

#     yield app_user_id

#     db.delete(new_user)
#     db.commit()

@pytest.fixture
def dashboard_user(db, registered_user):

    user = Users(
        platform="codeforces",
        handle=f"test_{uuid.uuid4()}",
        curr_rating=1500,
        max_rating=1600,
        rank="specialist",
        max_rank="specialist",
        app_user_id=registered_user.id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    db.delete(user)
    db.commit()


#daily activity fixture
from datetime import date
from models import DailyActivity


@pytest.fixture
def daily_activity(db, dashboard_user):

    daily = DailyActivity(
        user_id=dashboard_user.id,
        date=date.today(),
        problems_attempted=10,
        problems_solved=8,
        average_rating=1400,
        active_minutes=60,
        contest_participated=True
    )

    db.add(daily)
    db.commit()

    yield daily

    db.delete(daily)
    db.commit()

#tag performance 
from models import TagPerformance


@pytest.fixture
def tag_performance(db, dashboard_user):

    tag = TagPerformance(
        user_id=dashboard_user.id,
        tag_name="graphs",
        total_attempted=10,
        total_solved=7,
        success_rate=70.0,
        avg_problem_rating=1500,
        hardest_solved_rating=1800,
        weakness_score=120
    )

    db.add(tag)
    db.commit()

    yield tag

    db.delete(tag)
    db.commit()

#recommendation fixture
from models import RecommendationQueue


@pytest.fixture
def recommendation(db, dashboard_user):

    rec = RecommendationQueue(
        user_id=dashboard_user.id,
        problem_contest_id=1000,
        problem_index="A",
        recommendation_type="weak_tag_improvement",
        reason="Graphs need improvement",
        priority_score=90
    )

    db.add(rec)
    db.commit()

    yield rec

    db.delete(rec)
    db.commit()

#skill estimate fixute
from models import SkillEstimate


@pytest.fixture
def skill_estimate(db, dashboard_user):

    skill = SkillEstimate(
        account_id=dashboard_user.id,
        tag_name="graphs",
        estimated_rating=1450,
        confidence=0.85,
        sample_size=20,
        trend=0
    )

    db.add(skill)
    db.commit()

    yield skill

    db.delete(skill)
    db.commit()

#mega dashboard fixture
@pytest.fixture
def dashboard_data(
    dashboard_user,
    daily_activity,
    tag_performance,
    recommendation,
    skill_estimate
):
    return dashboard_user


from models import ContestPerformance


@pytest.fixture
def contest_performance(
    db,
    dashboard_user
):

    contest = ContestPerformance(
        user_id=dashboard_user.id,
        contest_id=123456,
        contest_name="Codeforces Round #999",
        rank=100,
        old_rating=1400,
        new_rating=1500,
        problems_solved=4,
        unsolved_upsolvable_count=2
    )

    db.add(contest)
    db.commit()
    db.refresh(contest)

    yield contest

    db.delete(contest)
    db.commit()