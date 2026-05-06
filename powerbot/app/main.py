from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from powerbot.app.api.routes.diagnose import router as diagnose_router
from powerbot.app.api.routes.health import router as health_router
from powerbot.app.api.routes.predict import router as predict_router
from powerbot.app.core.config import get_settings
from powerbot.app.core.logging import configure_logging


configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(predict_router)
app.include_router(diagnose_router)


@app.get("/")
def root():
    return {"message": "Welcome to Transmission Line Fault Predictor"}
