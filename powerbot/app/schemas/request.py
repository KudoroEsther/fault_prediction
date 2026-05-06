from pydantic import BaseModel, Field


class FaultFeaturesRequest(BaseModel):
    Va: float = Field(..., description="Phase A voltage")
    Vb: float = Field(..., description="Phase B voltage")
    Vc: float = Field(..., description="Phase C voltage")
    Ia: float = Field(..., description="Phase A current")
    Ib: float = Field(..., description="Phase B current")
    Ic: float = Field(..., description="Phase C current")
