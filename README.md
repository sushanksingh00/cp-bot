# AI-Powered Competitive Programming Analytics Platform

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Celery](https://img.shields.io/badge/Celery-Background%20Tasks-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

A full-stack analytics platform that syncs Codeforces profiles, computes competitive programming insights, tracks progress, identifies weaknesses, and generates personalized recommendations.

---

## Features

### Authentication

- JWT Authentication
- Register/Login
- Protected Routes

### Data Sync

- Codeforces Profile Sync
- Contest History Import
- Submission History Import
- Background Processing using Celery

### Analytics

- Rating Progression
- Contest Performance Analysis
- Daily Activity Tracking
- Tag-wise Performance Analysis
- Skill Estimation

### Recommendations

- Weak Topic Detection
- Rating Push Suggestions
- Consistency Tracking
- Upsolve Recommendations

### Infrastructure

- PostgreSQL
- Redis Caching
- Celery Workers
- Dockerized Setup

---

## Dashboard Preview

### Dashboard

![Dashboard](images/dashboard.png)

### Contest Analytics

![Contest Analytics](images/contest.png)

### Daily Activity

![Daily Activity](images/daily-activity.png)

### Tag Analytics

![Tag Analytics](images/tags.png)

### Recommendations

![Recommendations](images/recommendation.png)

### Sidebar Navigation

![Sidebar](images/sidebar.png)

---

## System Architecture

```text
React Frontend
        │
        ▼
FastAPI Backend
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
Postgres Redis Celery
        │
        ▼
Codeforces API
```

---

## Tech Stack

### Backend

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- JWT Authentication
- Redis
- Celery

### Frontend

- React
- Vite
- TailwindCSS
- Axios
- React Router

### Infrastructure

- Docker
- Docker Compose

---

## Project Structure

```text
.
├── backend
│   ├── routers
│   ├── services
│   ├── tasks
│   ├── core
│   ├── models.py
│   ├── crud.py
│   └── database.py
│
├── frontend
│   ├── src
│   │   ├── pages
│   │   ├── components
│   │   ├── services
│   │   └── routes
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Analytics Engine

The platform computes:

### Daily Activity

- Problems attempted
- Problems solved
- Success rate
- Activity streaks

### Tag Performance

- Success rate per tag
- Weakness score
- Topic ranking

### Contest Analytics

- Rating progression
- Contest trends
- Peak rating analysis

### Recommendations

Generated automatically from analytics data.

Types:

- Weak Tag Improvement
- Rating Push
- Consistency Boost
- Upsolve Problems
- Contest Preparation

---

## API Endpoints

### Authentication

```http
POST /auth/register
POST /auth/login
```

### Sync

```http
POST /sync/codeforces
GET /sync/status/{task_id}
```

### Dashboard

```http
GET /users/dashboard
```

### Analytics

```http
GET /users/contests
GET /users/daily-activity
GET /users/tags
GET /users/tags/weakest
```

### Recommendations

```http
GET /users/recommendations
GET /users/upsolve
```

---

## Environment Variables

```env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

DB_URL=

SECRET_KEY=
ALGORITHM=HS256

REDIS_HOST=redis
REDIS_URL=redis://redis:6379/0
```

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/sushanksingh00/cp-analytics-platform.git
cd cp-analytics-platform
```

### Backend

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

### Celery Worker

```bash
celery -A tasks.task worker --loglevel=info
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Docker Setup

```bash
docker compose up --build
```

Services started:

- FastAPI
- PostgreSQL
- Redis
- Celery Worker
- React Frontend

---

## Future Improvements

- AI Insights
- Weekly Performance Reports
- Personalized Study Plans
- GitHub Actions CI/CD
- Test Coverage
- Monitoring & Logging
- Public Deployment

---

## Learning Outcomes

This project helped me gain hands-on experience with:

- Backend Engineering
- Database Design
- Authentication Systems
- Analytics Pipelines
- Background Processing
- Redis Caching
- Docker & Containerization
- Full Stack Development

---

## Author

### Sushank Singh

B.Tech CSE (Software Engineering)
VIT-AP University

GitHub: https://github.com/sushanksingh00
LinkedIn: https://www.linkedin.com/in/sushank-singh-92a80731a/