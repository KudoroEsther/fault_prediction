from functools import lru_cache

import joblib

from powerbot.app.core.config import get_settings


@lru_cache(maxsize=1)
def load_prediction_pipeline():
    settings = get_settings()
    return joblib.load(settings.model_path)
