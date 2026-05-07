from functools import lru_cache

import joblib

from powerbot.app.core.config import get_settings


@lru_cache(maxsize=1)
def load_prediction_pipeline():
    settings = get_settings()
    try:
        return joblib.load(settings.model_path)
    except (ModuleNotFoundError, SyntaxError) as exc:
        raise RuntimeError(
            "Unable to load the saved prediction pipeline. "
            "The serialized model depends on the legacy 'Feature_engineer' "
            "module path. Ensure the root-level compatibility shim exists "
            "and does not contain merge-conflict markers, or retrain the "
            "model with 'python scripts/train_model.py'."
        ) from exc
