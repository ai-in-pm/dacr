from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Digital AI Currency Reserve"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Currency Configuration
    INITIAL_SUPPLY: float = 0.0
    MIN_RESERVE_RATIO: float = 0.95
    MAX_SUPPLY_GROWTH_RATE: float = 0.1  # 10% maximum growth rate
    
    # Reserve Configuration
    COMPUTATIONAL_RESERVE_WEIGHT: float = 0.4
    STORAGE_RESERVE_WEIGHT: float = 0.3
    ENGAGEMENT_RESERVE_WEIGHT: float = 0.3
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./dacr.db"
    
    # Governance Configuration
    MIN_PROPOSAL_THRESHOLD: float = 0.05  # 5% of total supply needed to create proposal
    VOTING_PERIOD_DAYS: int = 7
    EXECUTION_DELAY_HOURS: int = 24
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

@lru_cache()
def get_settings() -> Settings:
    """Returns cached settings instance"""
    return Settings()
