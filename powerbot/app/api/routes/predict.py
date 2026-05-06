from fastapi import APIRouter

from powerbot.app.schemas.request import FaultFeaturesRequest
from powerbot.app.schemas.response import PredictResponse
from powerbot.app.services.prediction_service import predict_fault


router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictResponse)
def predict(payload: FaultFeaturesRequest) -> PredictResponse:
    return PredictResponse(**predict_fault(payload))
