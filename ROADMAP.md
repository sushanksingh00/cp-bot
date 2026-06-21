# ROADMAP.md

# AI-Powered Competitive Programming Analytics Platform

---

# Current Status

## Backend

### Data Ingestion

* [x] Users
* [x] ContestPerformance
* [x] ProblemAttempt

### Analytics

* [x] DailyActivity
* [x] TagPerformance
* [x] RecommendationQueue
* [ ] SkillEstimate

### APIs

* [x] User APIs
* [x] Analytics APIs
* [x] Recommendation APIs
* [x] Dashboard API

### Database

* [x] PostgreSQL
* [x] SQLAlchemy Models
* [x] Constraints
* [x] Relationships

---

# PHASE 1 — Backend Engineering Foundations

## Goal

Learn how real backend projects are structured.

### Tasks

#### Architecture Cleanup

* [ ] Fix TagPerformance deduplication bug
* [x] Create services layer
* [x] Move sync logic into services
* [x] Move analytics logic into services
* [x] Move recommendation logic into services

#### Router Refactor

* [x] users.py
* [x] analytics.py
* [x] recommendations.py
* [x] sync.py

#### Configuration

* [x] Environment variables
* [x] config.py
* [x] Remove hardcoded DB credentials

### Learn

* Service Layer Pattern
* Separation of Concerns
* Project Structure
* Configuration Management

### Outcome

You can build maintainable backend systems instead of large script-like applications.

---

# PHASE 2 — Database Engineering

## Goal

Learn how production databases evolve.

### Tasks

#### Alembic

* [x] Install Alembic
* [x] Initialize migrations
* [x] Create first migration
* [x] Upgrade database
* [x] Downgrade database

#### Database Improvements

* [ ] Add indexes
* [ ] Review constraints
* [ ] Optimize queries

### Learn

* Database migrations
* Schema versioning
* Production database workflows

### Outcome

You stop relying on create_all() and start working like backend teams do.

---

# PHASE 3 — Authentication & Security

## Goal

Learn how real applications manage users and access control.

### Database

* [x] Create AppUser model
* [x] Add email field
* [x] Add hashed_password field
* [x] Alembic migration

### Security

* [x] Password hashing
* [x] Password verification
* [x] bcrypt/passlib

### Authentication APIs

* [x] Register endpoint
* [x] Login endpoint

### JWT

* [x] Generate access token
* [x] Verify token
* [x] Decode token

### Protected Routes

* [x] Current user endpoint
* [x] Protected dashboard endpoint
* [x] Protected recommendation endpoint

### Learn

* Authentication
* Authorization
* JWT
* Password Hashing
* FastAPI Dependencies

### Outcome

Users can securely register, login, and access their own data.

---

# PHASE 4 — Advanced Analytics


* [x] DELETE USER KO SAHI KARDO


## Goal

Turn data into intelligence.

### SkillEstimate

* [x] Estimated rating per tag
* [x] Confidence score
* [x] Sample size
* [x] Trend calculation

### Progress Analytics

* [x] Rating progression
* [x] Tag progression
* [x] Activity streaks
* [x] Contest trend analysis

### New APIs

* [x] /skills
* [x] /progress
* [x] /contest-analysis

### Learn

* Analytics systems
* Data modeling
* Metric design

### Outcome

Project becomes an analytics platform instead of a data storage app.

---

# PHASE 5 — Background Processing

## Goal

Learn scalable backend architecture.

### Redis

* [x] Install Redis
* [x] Redis fundamentals
* [x] Cache dashboard responses

### Celery

* [x] Setup Celery
* [x] Setup workers
* [x] Setup task queue

### Async Processing

* [x] Background user sync
* [x] Background analytics generation
* [x] Job status tracking

### Learn

* Queues
* Workers
* Distributed systems
* Caching

### Outcome

Long-running jobs no longer block requests.

---

# PHASE 6 — DevOps Foundations

## Goal

Learn deployment and infrastructure.

### Docker

* [x] Dockerfile
* [x] Docker Compose

### Services

* [x] FastAPI container
* [x] PostgreSQL container
* [x] Redis container

### Deployment

* [x] Environment configuration
* [x] Production deployment

### Learn

* Containers
* Linux basics
* Infrastructure

### Outcome

You can run the complete backend stack anywhere.

---
# PHASE 7 — Frontend Foundations

## Goal

Start becoming a Full Stack Developer.

### Learn React

* [x] Components
* [x] Props
* [x] State
* [x] useEffect
* [x] useState
* [x] Routing

### Project Setup

* [x] Vite
* [x] React
* [x] TailwindCSS

### API Integration

* [x] Auth integration
* [x] Dashboard integration
* [x] Analytics integration

### Outcome

Frontend can consume all backend APIs.

---

# PHASE 8 — Dashboard UI

## Goal

Build the complete user experience.

### Pages

* [x] Login
* [x] Register
* [x] Dashboard
* [x] Recommendations

### Dashboard

* [x] User profile
* [x] Current rating
* [x] Max rating
* [x] Weak tags
* [x] Strong tags
* [x] Skill estimates

### Outcome

Complete full-stack application.

---

# PHASE 9 — Data Visualization

## Goal

Present analytics professionally.

### Charts

* [x] Rating graph
* [x] Tag performance graph
* [ ] Activity graph
* [x] Contest performance graph

### Heatmaps

* [x] Daily activity heatmap

### Libraries

* [x] Recharts

### Outcome

Analytics become visually useful.

---

# PHASE 10 — Testing

## Goal

Learn professional software development.

### Unit Testing

* [ ] Analytics tests
* [ ] Recommendation tests
* [ ] SkillEstimate tests

### Integration Testing

* [ ] API tests
* [ ] Database tests
* [ ] Auth tests

### Learn

* Pytest
* Mocking
* Test design

### Outcome

You can refactor safely and catch regressions.

---

# PHASE 11 — AI Layer

## Goal

Add intelligent features using AI.

### Features

* [ ] AI Insights
* [ ] Weekly Improvement Reports
* [ ] Personalized Study Plans
* [ ] Weakness Explanations

### Outcome

Platform provides personalized guidance instead of only analytics.

---

# PHASE 12 — Resume-Level Engineering

## Goal

Polish the project to production and portfolio quality.

### Engineering

* [ ] GitHub Actions
* [ ] Logging
* [ ] Health Checks
* [ ] API Docs
* [ ] Architecture Docs

### Platform Expansion

* [ ] LeetCode Integration
* [ ] CodeChef Integration

### Deployment

* [ ] Public Deployment
* [ ] Demo Video
* [ ] Portfolio Entry

### Outcome

Production-ready portfolio project suitable for internships and software engineering roles.
