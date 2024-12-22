from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from decimal import Decimal
from datetime import datetime

from ..core.reserves import ReserveManager, ReserveType
from ..deps import get_current_user
from ..schemas.reserves import ReserveStatus, ReserveHistory

router = APIRouter()

@router.get("/status", response_model=ReserveStatus)
async def get_reserve_status(
    reserve_manager: ReserveManager = Depends(ReserveManager),
    current_user: str = Depends(get_current_user)
):
    """Get current reserve status"""
    reserves = await reserve_manager.get_reserve_status()
    total = await reserve_manager.get_total_reserves()
    
    return {
        "reserves": reserves,
        "total": total,
        "timestamp": datetime.utcnow()
    }

@router.get("/history", response_model=List[ReserveHistory])
async def get_reserve_history(
    reserve_manager: ReserveManager = Depends(ReserveManager),
    current_user: str = Depends(get_current_user)
):
    """Get reserve history"""
    # This would typically fetch from a database
    return []
