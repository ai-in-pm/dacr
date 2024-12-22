from pydantic import BaseModel, ConfigDict
from typing import Dict, Optional, Any
from decimal import Decimal
from datetime import datetime

from ..core.governance import ProposalType, ProposalStatus

class ProposalCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    type: ProposalType
    title: str
    description: str
    parameter_changes: Optional[Dict[str, Any]] = None

class ProposalResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: str
    type: ProposalType
    title: str
    description: str
    creator: str
    creation_time: datetime
    status: ProposalStatus
    votes_for: Decimal
    votes_against: Decimal
    parameter_changes: Optional[Dict[str, Any]] = None

class VoteRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    proposal_id: str
    support: bool
    vote_weight: Decimal

class VoteResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    proposal_id: str
    voter: str
    support: bool
    vote_weight: Decimal
