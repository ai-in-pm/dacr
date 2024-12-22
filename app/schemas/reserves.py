from pydantic import BaseModel, ConfigDict
from typing import Dict
from decimal import Decimal
from datetime import datetime

class ReserveStatus(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    reserves: Dict[str, Decimal]
    total: Decimal
    timestamp: datetime

class ReserveHistory(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    reserve_type: str
    amount: Decimal
    timestamp: datetime
