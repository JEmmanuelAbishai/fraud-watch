from pydantic import BaseModel


class FeatureContribution(BaseModel):
    feature: str
    contribution: float  # SHAP


class ExplanationResponse(BaseModel):
    transaction_id: str
    fraud_probability: float
    contributions: list[FeatureContribution]
    important_edge_count: int
    summary: str
