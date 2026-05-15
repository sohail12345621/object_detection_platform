from fastapi import APIRouter
from app.api.routes import detection, analytics

router = APIRouter()

router.include_router(detection.router, prefix="/detect", tags=["detection"])
router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
