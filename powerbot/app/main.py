from fastapi import FastAPI
from app.api import diagnose, health, predict

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="PowerBot")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(predict.router)
app.include_router(diagnose.router)
