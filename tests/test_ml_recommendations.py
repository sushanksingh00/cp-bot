import pytest
from services.inference_services import MLPredictor, get_difficulty_band
from services.recommendation_services import generate_ml_recommendations
from models import Users, TagPerformance, ProblemAttempt

def test_difficulty_band():
    assert get_difficulty_band(0.9) == "Warm-up"
    assert get_difficulty_band(0.7) == "Recommended"
    assert get_difficulty_band(0.5) == "Stretch"
    assert get_difficulty_band(0.3) == "Challenging"
    assert get_difficulty_band(0.1) == "Advanced"

def test_ml_predictor_missing_features(monkeypatch):
    predictor = MLPredictor.get_instance()
    # Mocking features_dict to be missing features
    monkeypatch.setattr("services.inference_services.get_inference_features", lambda *args: {})
    
    with pytest.raises(ValueError, match="Feature mismatch"):
        predictor.predict(1, 1500, ["dp"], None)

def test_personalized_endpoint(client, header_token, dashboard_data, monkeypatch):
    # Mock CF problems
    def mock_fetch_cf_problems():
        return [
            {"contest_id": 1, "problem_index": "A", "name": "A", "tags": ["dp"], "rating": 1400},
            {"contest_id": 2, "problem_index": "B", "name": "B", "tags": ["math"], "rating": 1500},
        ]
    monkeypatch.setattr("services.recommendation_services.fetch_cf_problems", mock_fetch_cf_problems)
    
    # Mock get_solve_probability
    def mock_get_solve_prob(*args):
        return {
            "solve_probability": 0.74,
            "prediction": "likely_solve",
            "difficulty_band": "Recommended",
            "important_factors": []
        }
    monkeypatch.setattr("services.recommendation_services.get_solve_probability", mock_get_solve_prob)
    
    response = client.get(
        "/users/personalized",
        headers=header_token
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "solve_probability" in data[0]
        assert "difficulty_band" in data[0]
        assert "problem_id" in data[0]

def test_insights_endpoint(client, header_token, dashboard_data, monkeypatch):
    # Mock CF problems
    def mock_fetch_cf_problems():
        return [
            {"contest_id": 1, "problem_index": "A", "name": "A", "tags": ["dp"], "rating": 1400},
            {"contest_id": 2, "problem_index": "B", "name": "B", "tags": ["math"], "rating": 1500},
        ]
    monkeypatch.setattr("services.recommendation_services.fetch_cf_problems", mock_fetch_cf_problems)
    
    # Mock inference features
    monkeypatch.setattr("services.recommendation_services.get_inference_features", lambda *args: {
        "historical_solve_rate": 0.6,
        "recent_7d_solve_rate": 0.5,
        "recent_30d_solve_rate": 0.55,
        "total_attempts": 100,
        "rating_difference": 100,
        "avg_tag_success": 0.5,
        "avg_tag_familiarity": 10
    })
    
    # Mock get_solve_probability
    def mock_get_solve_prob(*args):
        return {
            "solve_probability": 0.74,
            "prediction": "likely_solve",
            "difficulty_band": "Recommended",
            "important_factors": []
        }
    monkeypatch.setattr("services.recommendation_services.get_solve_probability", mock_get_solve_prob)
    
    response = client.get(
        "/users/personalized/1A/insights",
        headers=header_token
    )

    assert response.status_code == 200
    data = response.json()
    
    assert "problem" in data
    assert data["problem"]["problem_id"] == "1A"
    assert "prediction" in data
    assert "recommendation" in data
    assert "user_performance" in data
    assert "topic_analysis" in data
    assert "model_signals" in data
    assert "insights" in data
