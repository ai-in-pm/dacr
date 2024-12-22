from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel
import uuid
import logging

logger = logging.getLogger(__name__)

class TransactionType(Enum):
    ISSUANCE = "issuance"
    TRANSFER = "transfer"
    REDEMPTION = "redemption"
    BURN = "burn"
    REWARD = "reward"

class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Transaction(BaseModel):
    id: str
    type: TransactionType
    amount: Decimal
    sender: Optional[str]
    recipient: str
    timestamp: datetime
    status: TransactionStatus
    metadata: Dict[str, str]

class TransactionManager:
    """Manages DAC transactions and maintains transaction history"""
    
    def __init__(self):
        self._transactions: Dict[str, Transaction] = {}
        self._pending_transactions: Dict[str, Transaction] = {}
        
    async def create_transaction(
        self,
        type: TransactionType,
        amount: Decimal,
        recipient: str,
        sender: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> Transaction:
        """Creates a new transaction"""
        transaction = Transaction(
            id=str(uuid.uuid4()),
            type=type,
            amount=amount,
            sender=sender,
            recipient=recipient,
            timestamp=datetime.utcnow(),
            status=TransactionStatus.PENDING,
            metadata=metadata or {}
        )
        
        self._pending_transactions[transaction.id] = transaction
        logger.info(f"Created transaction {transaction.id} of type {type.value}")
        return transaction
        
    async def execute_transaction(self, transaction_id: str) -> bool:
        """Executes a pending transaction"""
        if transaction_id not in self._pending_transactions:
            logger.error(f"Transaction {transaction_id} not found")
            return False
            
        transaction = self._pending_transactions[transaction_id]
        
        try:
            # Implement transaction-specific logic here
            transaction.status = TransactionStatus.COMPLETED
            self._transactions[transaction_id] = transaction
            del self._pending_transactions[transaction_id]
            logger.info(f"Executed transaction {transaction_id}")
            return True
        except Exception as e:
            transaction.status = TransactionStatus.FAILED
            logger.error(f"Failed to execute transaction {transaction_id}: {str(e)}")
            return False
            
    async def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Retrieves a transaction by ID"""
        return (
            self._transactions.get(transaction_id) or 
            self._pending_transactions.get(transaction_id)
        )
        
    async def get_transactions_by_address(
        self,
        address: str,
        type: Optional[TransactionType] = None,
        status: Optional[TransactionStatus] = None
    ) -> List[Transaction]:
        """Retrieves transactions for a specific address"""
        transactions = []
        for tx in self._transactions.values():
            if (tx.sender == address or tx.recipient == address):
                if type and tx.type != type:
                    continue
                if status and tx.status != status:
                    continue
                transactions.append(tx)
        return transactions
        
    async def get_transaction_history(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Transaction]:
        """Retrieves transaction history within a time range"""
        transactions = []
        for tx in self._transactions.values():
            if start_time and tx.timestamp < start_time:
                continue
            if end_time and tx.timestamp > end_time:
                continue
            transactions.append(tx)
        return sorted(transactions, key=lambda x: x.timestamp)
