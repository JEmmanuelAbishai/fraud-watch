from pydantic import BaseModel, Field


class FraudScoreRequest(BaseModel):
    transaction_id: str


class FraudScoreResponse(BaseModel):
    transaction_id: str
    fraud_probability: float = Field(ge=0.0, le=1.0)
    risk_level: str  # "low" | "medium" | "high"
    model_name: str
