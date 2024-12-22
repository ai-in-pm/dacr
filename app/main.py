from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
import logging
import os

from .routers import currency, reserves, governance, analytics, auth
from .core.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Digital AI Currency Reserve (DACR)",
    description="API for managing the Digital AI Currency (DAC) system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefixes
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["auth"]
)
app.include_router(
    currency.router,
    prefix="/api/v1/currency",
    tags=["currency"]
)
app.include_router(
    reserves.router,
    prefix="/api/v1/reserves",
    tags=["reserves"]
)
app.include_router(
    governance.router,
    prefix="/api/v1/governance",
    tags=["governance"]
)
app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["analytics"]
)

@app.get("/")
async def root():
    """Root endpoint providing system status"""
    return {
        "name": "Digital AI Currency Reserve",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
