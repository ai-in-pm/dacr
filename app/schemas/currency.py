from pydantic import BaseModel, Field
from typing import Dict, Optional
from decimal import Decimal
from datetime import datetime

class CurrencyInfo(BaseModel):
    total_supply: Decimal
    timestamp: datetime

class IssuanceRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)
    recipient: str
    reason: str

class TransferRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)
    recipient: str
    metadata: Optional[Dict[str, str]] = None

class TransactionResponse(BaseModel):
    id: str
    type: str
    amount: Decimal
    sender: Optional[str]
    recipient: str
    timestamp: datetime
    status: str
    metadata: Dict[str, str]
