from pathlib import Path

import pandas as pd

from powerbot.app.schemas.request import FaultFeaturesRequest


def features_to_frame(payload: FaultFeaturesRequest) -> pd.DataFrame:
    return pd.DataFrame([payload.model_dump()])


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
