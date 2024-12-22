import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app
from app.core.currency import CurrencyManager
from app.core.transactions import TransactionManager

client = TestClient(app)

@pytest.fixture
def currency_manager():
    return CurrencyManager()

@pytest.fixture
def transaction_manager():
    return TransactionManager()

def test_get_currency_info():
    response = client.get("/api/v1/currency/info")
    assert response.status_code == 200
    data = response.json()
    assert "total_supply" in data
    assert "timestamp" in data

@pytest.mark.asyncio
async def test_currency_issuance(currency_manager):
    amount = Decimal("1000")
    result = await currency_manager.issue_currency(amount, "Test issuance")
    assert result == True
    
    supply = await currency_manager.get_supply()
    assert supply == amount

@pytest.mark.asyncio
async def test_transaction_creation(transaction_manager):
    transaction = await transaction_manager.create_transaction(
        type="ISSUANCE",
        amount=Decimal("100"),
        recipient="test_address",
        sender="DACR",
        metadata={"reason": "test"}
    )
    
    assert transaction.id is not None
    assert transaction.amount == Decimal("100")
    assert transaction.status == "PENDING"
