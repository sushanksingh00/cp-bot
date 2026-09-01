import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import ProblemAttempt

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise RuntimeError("DB_URL is not set. Check your .env file.")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def extract_raw_dataset(output_path="ml/data/raw_dataset.csv"):
    """
    Extracts raw problem attempt data from the database.
    Ensures data is ordered chronologically per user to avoid future leakage when building features.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    attempts = []
    try:
        session = SessionLocal()
        # Query all attempts, ordered by user and time
        # This is critical for temporal feature engineering without leakage
        attempts = session.query(ProblemAttempt).order_by(
            ProblemAttempt.user_id, 
            ProblemAttempt.submitted_at
        ).all()
        session.close()
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Falling back to dummy data generation.")
        
    data = []
    for attempt in attempts:
        data.append({
            "id": attempt.id,
            "user_id": attempt.user_id,
            "contest_id": attempt.contest_id,
            "submission_id": attempt.submission_id,
            "problem_index": attempt.problem_index,
            "problem_name": attempt.problem_name,
            "problem_rating": attempt.problem_rating,
            "verdict": attempt.verdict,
            "language": attempt.language,
            "tags_jsonb": attempt.tags_jsonb,
            "submitted_at": attempt.submitted_at
        })
        
    df = pd.DataFrame(data)
    
    if df.empty:
        print("Warning: No problem attempts found in database.")
        # Create a mock dataset for development if no data exists
        print("Creating dummy data for development...")
        df = create_dummy_data()
        
    # Target variable
    df['solved'] = (df['verdict'] == 'OK').astype(int)
    
    df.to_csv(output_path, index=False)
    print(f"Dataset extracted successfully to {output_path} with {len(df)} records.")
    return df

def create_dummy_data():
    """Create some dummy data if the DB is empty so the pipeline can be built."""
    from datetime import datetime, timedelta
    import random
    
    now = datetime.utcnow()
    data = []
    
    tags_pool = [
        ["math", "greedy"], ["dp"], ["graphs", "dfs and similar"], 
        ["implementation"], ["data structures", "trees"]
    ]
    
    user_ratings = {1: 1500, 2: 1200, 3: 2100}
    
    for user_id, u_rating in user_ratings.items():
        for i in range(100):
            problem_rating = random.choice([800, 1000, 1200, 1400, 1600, 1800, 2000, 2200])
            tags = random.choice(tags_pool)
            
            # Simple probability logic for dummy data
            prob = 0.5 + (u_rating - problem_rating) * 0.001
            prob = max(0.1, min(0.9, prob))
            
            is_solved = random.random() < prob
            verdict = 'OK' if is_solved else random.choice(['WRONG_ANSWER', 'TIME_LIMIT_EXCEEDED'])
            
            data.append({
                "id": user_id * 1000 + i,
                "user_id": user_id,
                "contest_id": random.randint(1000, 2000),
                "submission_id": random.randint(100000, 900000),
                "problem_index": random.choice(["A", "B", "C", "D", "E"]),
                "problem_name": f"Problem {i}",
                "problem_rating": problem_rating,
                "verdict": verdict,
                "language": "Python 3",
                "tags_jsonb": tags,
                "submitted_at": now - timedelta(days=100-i)
            })
            
            # If they solved it, their rating goes up slightly
            if is_solved:
                u_rating += 10
            else:
                u_rating -= 5
                
    return pd.DataFrame(data)

if __name__ == "__main__":
    extract_raw_dataset()
