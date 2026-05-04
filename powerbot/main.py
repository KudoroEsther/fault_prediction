from fastapi import FastAPI
from api import diagnose, health, predict

app = FastAPI(title="PowerBot")

app.include_router(health.router)
app.include_router(predict.router)
app.include_router(diagnose.router)
