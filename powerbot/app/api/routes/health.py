from fastapi import APIRouter

from powerbot.app.core.config import get_settings
from powerbot.app.schemas.response import HealthResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        model_loaded=settings.model_path.exists(),
        vectorstore_ready=settings.vectorstore_dir.exists(),
    )
