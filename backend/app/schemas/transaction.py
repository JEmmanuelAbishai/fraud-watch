from datetime import datetime

from pydantic import BaseModel


class TransactionBase(BaseModel):
    account_id: str
    device_id: str | None = None
    amount: float
    merchant: str | None = None


class TransactionCreate(TransactionBase):
    id: str


class TransactionOut(TransactionBase):
    id: str
    is_fraud: bool | None = None
    fraud_score: float | None = None
    created_at: datetime

    class Config:
        from_attributes = True
