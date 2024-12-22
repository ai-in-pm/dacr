from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from ..core.currency import CurrencyManager
from ..core.transactions import TransactionManager, TransactionType
from ..schemas.currency import (
    CurrencyInfo,
    IssuanceRequest,
    TransferRequest,
    TransactionResponse
)
from ..deps import get_current_user, get_currency_manager, get_transaction_manager

router = APIRouter()

@router.get("/info", response_model=CurrencyInfo)
async def get_currency_info(
    currency_manager: CurrencyManager = Depends(get_currency_manager)
):
    """Get current currency information"""
    supply = await currency_manager.get_supply()
    return {
        "total_supply": supply,
        "timestamp": datetime.utcnow()
    }

@router.post("/issue", response_model=TransactionResponse)
async def issue_currency(
    request: IssuanceRequest,
    currency_manager: CurrencyManager = Depends(get_currency_manager),
    transaction_manager: TransactionManager = Depends(get_transaction_manager),
    current_user: str = Depends(get_current_user)
):
    """Issue new currency"""
    if not await currency_manager.issue_currency(request.amount, request.reason):
        raise HTTPException(status_code=400, detail="Currency issuance failed")
        
    transaction = await transaction_manager.create_transaction(
        type=TransactionType.ISSUANCE,
        amount=request.amount,
        recipient=request.recipient,
        sender="DACR",
        metadata={"reason": request.reason}
    )
    
    await transaction_manager.execute_transaction(transaction.id)
    return transaction

@router.post("/transfer", response_model=TransactionResponse)
async def transfer_currency(
    request: TransferRequest,
    transaction_manager: TransactionManager = Depends(get_transaction_manager),
    current_user: str = Depends(get_current_user)
):
    """Transfer currency between addresses"""
    transaction = await transaction_manager.create_transaction(
        type=TransactionType.TRANSFER,
        amount=request.amount,
        sender=current_user,
        recipient=request.recipient,
        metadata=request.metadata
    )
    
    await transaction_manager.execute_transaction(transaction.id)
    return transaction
