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

## 🚀 Quick Preview

<p align="center">
  <img src="images/app_gif.gif" alt="CP Analytics Demo GIF" width="500">
</p>

<p align="center">
  <i>A quick walkthrough of CP Analytics showcasing authentication, Codeforces sync, analytics dashboard, contest insights, daily activity, tag analysis, and personalized recommendations.</i>
</p>


---

## 🎥 Project Demo

<p align="center">
  <a href="https://youtu.be/SYv24VIP74I">
    <img src="images/thumbnail.png" alt="CP Analytics Demo" width="500">
  </a>
</p>

<p align="center">
  <b>▶ Click the thumbnail above to watch the complete project walkthrough.</b>
</p>

---

## Live Demo

🌐 **Frontend:** https://cp-bot-main.onrender.com

📚 **Backend API:** https://cp-bot-1.onrender.com/docs

> **Note:** The live demo runs without a Celery worker due to Render's free-tier limitations. Background synchronization executes synchronously in production while retaining the complete Celery architecture for local development.

---

## Project Highlights

* JWT Authentication & Protected Routes
* Codeforces Profile & Contest Synchronization
* Analytics Engine for Performance Tracking
* Personalized Recommendation System
* Redis-based Dashboard Caching
* Celery Background Task Architecture
* Automated Testing with Pytest
* GitHub Actions Continuous Integration
* Dockerized Multi-Service Development Environment
* Production Deployment on Render

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
- Background Processing using Celery (with synchronous fallback for production deployment)

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

* Docker
* Docker Compose
* PostgreSQL
* Redis Caching
* Celery Background Tasks
* GitHub Actions CI
* Structured Logging
* Health Check Endpoints
* Production Deployment (Render)

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
                    (Vite + Tailwind)
                           │
                           ▼
                  FastAPI Backend
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
     PostgreSQL        Redis Cache     Celery Worker*
          │
          ▼
     Codeforces API

*The production deployment executes synchronization
synchronously because the Render free tier does not
support background workers.
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

* Docker
* Docker Compose
* GitHub Actions
* Render

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
DB_URL_TEST=

SECRET_KEY=
ALGORITHM=HS256

REDIS_HOST=redis
REDIS_URL=redis://redis:6379/0

USE_CELERY=true
USE_REDIS=true
RUN_MIGRATIONS=false

VITE_API_URL=http://localhost:8000
```


---

## Testing

Implemented using **Pytest** with a dedicated testing database.

### Authentication

* Register
* Login
* Invalid Credentials
* Protected Routes

### Analytics

* Dashboard
* Daily Activity
* Tag Analytics
* Contest Analytics
* Recommendations

### Test Infrastructure

* Pytest Fixtures
* FastAPI Dependency Overrides
* Separate Test Database
* GitHub Actions CI Pipeline

---
## Quick Start (Recommended)

Run the complete application using Docker Compose.

```bash
docker compose up --build
```

This starts:

* FastAPI Backend
* PostgreSQL
* Redis
* Celery Worker
* React Frontend

---
## Manual Setup

The order should be strictly followed

### 1. Start PostgreSQL

Ensure PostgreSQL is running and your database is created.

### 2. Start Redis

```bash
redis-server
```

### 3. Backend

```bash
pip install -r requirements.txt

alembic upgrade head

uvicorn main:app --reload
```

### 4. Celery Worker

```bash
celery -A tasks.task worker --loglevel=info
```

### 5. Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Future Improvements

* AI-powered Performance Insights
* Weekly Performance Reports
* Personalized Study Plans
* Multi-Platform Support (LeetCode, CodeChef, AtCoder)
* Real-time Notifications
* WebSocket-based Live Updates
* Monitoring & Metrics Dashboard
* OpenTelemetry Integration

---

## Learning Outcomes

This project provided hands-on experience with:

* Backend Engineering
* Full Stack Development
* REST API Design
* Authentication & Authorization
* Database Design
* SQLAlchemy ORM
* Database Migrations with Alembic
* Analytics Pipeline Design
* Recommendation Systems
* Redis Caching
* Background Processing with Celery
* Docker & Docker Compose
* Automated Testing with Pytest
* GitHub Actions CI
* Production Deployment
* Logging & Health Monitoring

---

## License

This project is licensed under the MIT License.

---

## Author

### Sushank Singh

B.Tech CSE
VIT-AP University

GitHub: https://github.com/sushanksingh00
LinkedIn: https://www.linkedin.com/in/sushank-singh-92a80731a/