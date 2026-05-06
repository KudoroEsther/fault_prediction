from pydantic import BaseModel


class PredictResponse(BaseModel):
    status: str
    fault_label: str
    confidence: float


class DiagnoseResponse(BaseModel):
    status: str
    fault_label: str
    confidence: float
    final_answer: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    vectorstore_ready: bool
