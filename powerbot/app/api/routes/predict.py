from fastapi import APIRouter, HTTPException

from powerbot.app.schemas.request import FaultFeaturesRequest
from powerbot.app.schemas.response import PredictResponse
from powerbot.app.services.prediction_service import predict_fault


router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictResponse)
def predict(payload: FaultFeaturesRequest) -> PredictResponse:
    try:
        return PredictResponse(**predict_fault(payload))
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
