from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AnalyticsSummary(BaseModel):
    total_processed: int
    active_tasks: int

@router.get("/summary", response_model=AnalyticsSummary)
async def get_summary():
    # In a real app, this would query the database.
    # For now, it's a mock endpoint.
    return AnalyticsSummary(
        total_processed=0,
        active_tasks=0
    )
