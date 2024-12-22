from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from decimal import Decimal
from datetime import datetime

from ..core.analytics import AnalyticsManager
from ..deps import get_current_user
from ..schemas.analytics import SupplyMetrics, TransactionMetrics, ReserveMetrics

router = APIRouter()

@router.get("/supply", response_model=SupplyMetrics)
async def get_supply_metrics(
    analytics_manager: AnalyticsManager = Depends(AnalyticsManager),
    current_user: str = Depends(get_current_user)
):
    """Get supply metrics"""
    return await analytics_manager.get_supply_metrics()

@router.get("/transactions", response_model=TransactionMetrics)
async def get_transaction_metrics(
    analytics_manager: AnalyticsManager = Depends(AnalyticsManager),
    current_user: str = Depends(get_current_user)
):
    """Get transaction metrics"""
    return await analytics_manager.get_transaction_metrics()

@router.get("/reserves", response_model=ReserveMetrics)
async def get_reserve_metrics(
    analytics_manager: AnalyticsManager = Depends(AnalyticsManager),
    current_user: str = Depends(get_current_user)
):
    """Get reserve metrics"""
    return await analytics_manager.get_reserve_metrics()
