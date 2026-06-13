# AI-Powered Competitive Programming Analytics Platform

A FastAPI backend that collects competitive programming data from Codeforces, stores it in PostgreSQL, computes analytics, and generates personalized recommendations to help users improve.

## What it does

- Syncs a Codeforces profile into the app database
- Stores contest history, submission history, daily activity, tag performance, and recommendation queues
- Exposes authenticated APIs for dashboard, analytics, recommendations, and user profile data
- Uses JWT authentication for app users
- Uses Celery + Redis for asynchronous sync work
- Uses Docker Compose for local development

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT authentication
- Celery
- Redis
- Docker / Docker Compose
- Codeforces API

## Project Structure

```text
.
├── main.py
├── config.py
├── database.py
├── models.py
├── schema.py
├── crud.py
├── externalapi.py
├── routers/
├── services/
├── tasks/
├── core/
├── alembic/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Core Components

### Routers

- `routers/auth.py` - register/login
- `routers/sync.py` - sync Codeforces account and trigger Celery job
- `routers/users.py` - profile and dashboard APIs
- `routers/analytics.py` - contest, daily activity, and tag analytics
- `routers/recommendations.py` - recommendation endpoints

### Services

- `services/auth_services.py` - password hashing, login, JWT, auth dependency
- `services/sync_services.py` - Codeforces sync computations
- `services/analytics_serives.py` - analytics generation
- `services/recommendation_services.py` - recommendation generation

### Database Layer

- `models.py` contains SQLAlchemy models
- `crud.py` contains DB write/read helpers
- `database.py` sets up the SQLAlchemy engine and session factory
- `alembic/` contains migrations

### Background Jobs

- `tasks/task.py` defines the Celery task for sync
- `core/celery_app.py` configures the Celery app
- `core/redis_client.py` configures Redis access

## Environment Variables

Use a local `.env` file. A safe template is provided in `.env.example`.

Required values:

```env
POSTGRES_USER=sushank
POSTGRES_PASSWORD=change-me
POSTGRES_DB=aicpapp
DB_URL=postgresql+psycopg://sushank:change-me@postgres:5432/aicpapp
SECRET_KEY=change-me
ALGORITHM=HS256
REDIS_URL=redis://redis:6379/0
```

Notes:

- `.env` is ignored by Git
- `.env.example` is only a template for setup
- Do not commit real secrets

## Local Development

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the FastAPI app

```bash
uvicorn main:app --reload
```

### 3. Run the Celery worker

```bash
celery -A tasks.task worker --loglevel=info
```

## Docker Setup

The project includes Docker Compose for local development.

### Start services

```bash
docker compose up --build
```

### Services included

- PostgreSQL
- Redis
- FastAPI API server
- Celery worker

### Important Docker notes

- The compose file expects `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` to be present in your local environment
- The image build excludes local secret files through `.dockerignore`
- `password.txt`, `.env`, and `learn/` should not be baked into images

## API Endpoints

### Public

- `GET /` - health check
- `POST /auth/register` - register a new app user
- `POST /auth/login` - login and receive a JWT

### Authenticated

- `POST /sync/codeforces` - sync a Codeforces profile
- `GET /users/` - current user profile
- `GET /users/dashboard` - dashboard summary
- `DELETE /users/delete` - delete current user data
- `GET /users/contests` - contest analytics
- `GET /users/daily-activity` - daily activity analytics
- `GET /users/tags` - tag analytics
- `GET /users/tags/weakest` - weakest tags
- `GET /users/recommendations` - recommendation list
- `GET /users/upsolve` - upsolve recommendations

## Database Models

- `AppUsers` - app-level user accounts
- `Users` - linked Codeforces account per app user
- `ContestPerformance` - contest history and rating changes
- `ProblemAttempt` - submission-level history
- `DailyActivity` - daily aggregated activity
- `TagPerformance` - tag-wise analytics
- `RecommendationQueue` - generated recommendations
- `SkillEstimate` - planned skill-estimation model

## Recommendation Types

- `weak_tag_improvement`
- `upsolve`
- `rating_push`
- `consistency_boost`
- `contest_preparation`

## Learning Goals

This project is being built to practice:

- Backend architecture
- FastAPI routing and dependencies
- SQLAlchemy and migrations
- Authentication and JWT
- Analytics pipelines
- Recommendation generation
- Background processing with Celery
- Docker-based local development

## Author

Sushank Singh
B.Tech Computer Science (Software Engineering)
VIT-AP University

GitHub: https://github.com/sushanksingh00
