# AI-Powered Competitive Programming Analytics Platform

A backend-focused analytics platform that collects competitive programming data from Codeforces, stores it in PostgreSQL, computes performance metrics, and generates personalized recommendations to help users improve their problem-solving skills.

## Features

### User Synchronization

* Sync Codeforces user profiles
* Fetch contest history
* Fetch submission history
* Store and update user statistics

### Analytics Engine

Compute:

* Daily activity metrics
* Tag-wise performance analysis
* Success rates by topic
* Average problem difficulty
* Hardest solved problem per tag
* Weakness scores

### Recommendation Engine

Generate personalized recommendations:

* Weak Tag Improvement
* Rating Push Suggestions
* Contest Preparation
* Consistency Boost
* Upsolve Recommendations

### Dashboard API

Provides:

* User profile summary
* Weakest tags
* Personalized recommendations
* Recent activity statistics

---

## Tech Stack

### Backend

* FastAPI
* Python

### Database

* PostgreSQL
* SQLAlchemy ORM

### Validation

* Pydantic

### External APIs

* Codeforces API

---

## Database Design

### Users

Stores platform-specific user information.

### ContestPerformance

Tracks contest participation and rating changes.

### ProblemAttempt

Stores every submission and associated metadata.

### DailyActivity

Aggregates daily practice statistics.

### TagPerformance

Tracks performance across problem topics.

### RecommendationQueue

Stores generated recommendations.

### SkillEstimate (Planned)

Future model for estimating user skill by topic.

---

## API Endpoints

### Sync

```http
POST /sync/codeforces
```

Synchronizes a Codeforces account and computes all analytics.

---

### User Information

```http
GET /users/{handle}
```

Returns user profile information.

---

### Contest History

```http
GET /users/{handle}/contests
```

Returns contest performance history.

---

### Daily Activity

```http
GET /users/{handle}/daily-activity
```

Returns daily practice statistics.

---

### Tag Analytics

```http
GET /users/{handle}/tags
```

Returns tag-wise performance metrics.

```http
GET /users/{handle}/tags/weakest
```

Returns the weakest tags.

---

### Recommendations

```http
GET /users/{handle}/recommendations
```

Returns generated recommendations.

```http
GET /users/{handle}/upsolve
```

Returns unsolved contest problems recommended for upsolving.

---

### Dashboard

```http
GET /users/{handle}/dashboard
```

Returns a consolidated dashboard view.

---

## Recommendation Types

| Type                 | Description                       |
| -------------------- | --------------------------------- |
| weak_tag_improvement | Focus on weak problem categories  |
| upsolve              | Revisit unsolved contest problems |
| rating_push          | Move to higher-rated problems     |
| consistency_boost    | Encourage regular practice        |
| contest_preparation  | Encourage contest participation   |

---

## Project Structure

```text
.
├── main.py
├── crud.py
├── models.py
├── schema.py
├── externalapi.py
├── recommendation.py
├── database.py
├── requirements.txt
```

Planned structure:

```text
.
├── routers/
├── services/
├── models/
├── schemas/
├── alembic/
```

---

## Future Improvements

* Service layer architecture
* Router modularization
* Alembic migrations
* Docker support
* Redis caching
* Background jobs
* Skill estimation engine
* AI-powered coaching insights
* Multi-platform support (LeetCode, GeeksforGeeks)

---

## Learning Goals

This project was built to gain hands-on experience with:

* Backend engineering
* REST API design
* Database modeling
* Analytics pipelines
* Recommendation systems
* FastAPI
* PostgreSQL
* SQLAlchemy

---

## Author

Sushank Singh

B.Tech Computer Science (Software Engineering)
VIT-AP University

GitHub: https://github.com/sushanksingh00
