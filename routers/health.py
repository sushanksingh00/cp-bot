from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"] # for swagger ui
)

@router.get("/")
def health():
    return {
        "status": "healthy"
    }
