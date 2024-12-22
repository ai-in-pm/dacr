from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
from datetime import datetime

from .base import Base
from ..core.transactions import TransactionType, TransactionStatus

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True)
    type = Column(SQLEnum(TransactionType))
    amount = Column(Numeric(precision=36, scale=18), nullable=False)
    sender = Column(String, nullable=True)
    recipient = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    status = Column(SQLEnum(TransactionStatus))
    metadata = Column(JSON, nullable=True)

class Balance(Base):
    __tablename__ = "balances"

    address = Column(String, primary_key=True)
    amount = Column(Numeric(precision=36, scale=18), nullable=False)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())

class Reserve(Base):
    __tablename__ = "reserves"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    amount = Column(Numeric(precision=36, scale=18), nullable=False)
    timestamp = Column(DateTime, default=func.now())
