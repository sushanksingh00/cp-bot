import os
import sys

# Add the project root to sys.path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import sessionLocal
from ml.features import get_inference_features
from services.inference_services import MLPredictor
from services.recommendation_services import generate_problem_insights
import numpy as np
import pandas as pd

def test_inference_features():
    session = sessionLocal()
    
    try:
        # Assuming there is a user with ID 1 or we can use a dummy ID
        # Wait, get_inference_features queries ProblemAttempt with user_id
        # We can just pick any user_id that might not have many attempts
        test_user_id = 999999 # Likely no attempts
        problem_rating = None
        tags = '["math", "greedy"]'
        
        print("Testing get_inference_features with sparse history...")
        features = get_inference_features(test_user_id, problem_rating, tags, session)
        
        print("Features generated:")
        for k, v in features.items():
            print(f"  {k}: {v} (type: {type(v)})")
            assert v is not None, f"Feature {k} is None!"
            assert not pd.isna(v), f"Feature {k} is NaN!"
            assert not np.isinf(v), f"Feature {k} is infinity!"
            assert isinstance(v, (int, float, np.number)), f"Feature {k} is not numeric!"
            
        print("All features are numeric and finite. Success!")
        
        # Test MLPredictor
        print("\nTesting MLPredictor.predict()...")
        predictor = MLPredictor.get_instance()
        if predictor.is_loaded:
            prob = predictor.predict(test_user_id, problem_rating, eval(tags), session)
            print(f"Prediction success! Probability: {prob}")
        else:
            print("Model not loaded, skipping predict test.")
            
    finally:
        session.close()

if __name__ == "__main__":
    test_inference_features()
