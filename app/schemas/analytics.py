from pydantic import BaseModel, ConfigDict
from typing import Dict
from decimal import Decimal
from datetime import datetime

class SupplyMetrics(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    current_supply: Decimal
    max_supply: Decimal
    min_supply: Decimal
    average_supply: Decimal

class TransactionMetrics(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    total_volume: Decimal
    average_daily_volume: Decimal
    total_active_users: int
    average_daily_users: float

class ReserveMetrics(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    current_reserves: Dict[str, Decimal]
    average_reserves: Dict[str, Decimal]
    min_reserves: Dict[str, Decimal]
    max_reserves: Dict[str, Decimal]
