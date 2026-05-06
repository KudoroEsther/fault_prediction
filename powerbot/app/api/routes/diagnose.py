from fastapi import APIRouter, HTTPException

from powerbot.app.schemas.request import FaultFeaturesRequest
from powerbot.app.schemas.response import DiagnoseResponse


router = APIRouter(tags=["diagnosis"])


@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(payload: FaultFeaturesRequest) -> DiagnoseResponse:
    try:
        from powerbot.app.services.diagnosis_service import diagnose_fault

        return DiagnoseResponse(**diagnose_fault(payload))
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
