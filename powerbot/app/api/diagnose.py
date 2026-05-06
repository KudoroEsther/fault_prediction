from fastapi.middleware.cors import CORSMiddleware

import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np

# Loading the saved model
pipeline = joblib.load("best_pipeline.pkl")


#Initializing the application
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)