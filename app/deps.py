from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime

from .core.config import get_settings
from .core.currency import CurrencyManager
from .core.transactions import TransactionManager
from .core.distribution import DistributionManager
from .core.analytics import AnalyticsManager
from .core.governance import GovernanceManager
from .models.base import SessionLocal

settings = get_settings()

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency for database session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Core managers as dependencies
def get_currency_manager() -> CurrencyManager:
    return CurrencyManager()

def get_transaction_manager() -> TransactionManager:
    return TransactionManager()

def get_distribution_manager() -> DistributionManager:
    return DistributionManager()

def get_analytics_manager() -> AnalyticsManager:
    return AnalyticsManager()

def get_governance_manager() -> GovernanceManager:
    return GovernanceManager()

# Authentication dependency
async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
