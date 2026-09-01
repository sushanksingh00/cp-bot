from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from database import get_db
from sqlalchemy.orm import Session
from services.inference_services import get_solve_probability

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"]
)

class PredictRequest(BaseModel):
    handle: str
    problem_rating: int
    tags: List[str]

@router.post("/predict")
def predict_solve_probability(request: PredictRequest, session: Session = Depends(get_db)):
    """
    Predicts the probability of a user solving a specific problem.
    """
    result = get_solve_probability(
        handle=request.handle,
        problem_rating=request.problem_rating,
        tags=request.tags,
        session=session
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result
