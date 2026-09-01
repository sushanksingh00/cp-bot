import os
import joblib
import pandas as pd
import numpy as np
import logging
from pydantic import BaseModel
from sqlalchemy.orm import Session
from crud import fetch_user_by_handle
from ml.features import get_inference_features

logger = logging.getLogger(__name__)

def get_difficulty_band(probability: float) -> str:
    if probability >= 0.80:
        return "Warm-up"
    elif probability >= 0.65:
        return "Recommended"
    elif probability >= 0.45:
        return "Stretch"
    elif probability >= 0.25:
        return "Challenging"
    else:
        return "Advanced"

class MLPredictor:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def __init__(self, model_dir="ml/models"):
        self.model_path = os.path.join(model_dir, "best_model.pkl")
        self.features_path = os.path.join(model_dir, "feature_cols.pkl")
        
        self.model = None
        self.feature_cols = None
        self.is_loaded = False
        
        self.load_model()
        
    def load_model(self):
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.features_path):
                self.model = joblib.load(self.model_path)
                self.feature_cols = joblib.load(self.features_path)
                self.is_loaded = True
                logger.info(f"ML Model loaded successfully with {len(self.feature_cols)} features.")
            else:
                logger.warning("Warning: Model files not found. Inference will not work.")
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            
    def predict(self, user_id: int, problem_rating: int, tags: list, session: Session):
        if not self.is_loaded:
            logger.error("Predict called but ML model is not loaded.")
            raise ValueError("Model not loaded")
            
        features_dict = get_inference_features(user_id, problem_rating, tags, session)
        
        # Strict Feature Validation
        missing_features = [col for col in self.feature_cols if col not in features_dict]
        if missing_features:
            logger.error(f"Missing features during inference: {missing_features}")
            raise ValueError(f"Feature mismatch: Missing {len(missing_features)} features.")
            
        # Format for model exactly maintaining order
        input_data = {col: features_dict[col] for col in self.feature_cols}
        df = pd.DataFrame([input_data])
        
        # Predict probability
        if hasattr(self.model, "predict_proba"):
            prob = self.model.predict_proba(df)[0, 1]
        else:
            prob = self.model.predict(df)[0]
            
        # Prediction class
        pred = "likely_solve" if prob > 0.5 else "unlikely_solve"
        
        # Basic interpretability (which features are strongest)
        important_factors = []
        if hasattr(self.model, "feature_importances_"):
            importances = self.model.feature_importances_
            # Get top 3 factors for this specific prediction simply by multiplying value * importance
            weighted_factors = [(self.feature_cols[i], importances[i] * input_data[self.feature_cols[i]]) for i in range(len(self.feature_cols))]
            weighted_factors.sort(key=lambda x: abs(x[1]), reverse=True)
            
            for feat, weight in weighted_factors[:3]:
                impact = "High" if abs(weight) > np.percentile(np.abs([x[1] for x in weighted_factors]), 75) else "Medium"
                direction = "Positive" if weight > 0 else "Negative"
                important_factors.append(f"{feat}: {direction} impact ({impact})")
                
        return prob, pred, important_factors

def get_solve_probability(handle: str, problem_rating: int, tags: list, session: Session):
    predictor = MLPredictor.get_instance()
    if not predictor.is_loaded:
        return {"error": "Model not ready."}
        
    user = fetch_user_by_handle("codeforces", handle, session)
    if not user:
        return {"error": "User not found."}
        
    try:
        prob, pred, factors = predictor.predict(user.id, problem_rating, tags, session)
        difficulty_band = get_difficulty_band(prob)
        
        return {
            "solve_probability": round(prob, 4),
            "prediction": pred,
            "difficulty_band": difficulty_band,
            "confidence": "High" if prob > 0.8 or prob < 0.2 else "Medium",
            "important_factors": factors
        }
    except ValueError as e:
        logger.error(f"Inference error for user {handle}: {str(e)}")
        return {"error": str(e)}
