from fastapi import APIRouter, Depends, HTTPException
from typing import List
from decimal import Decimal

from ..core.governance import GovernanceManager, ProposalType, ProposalStatus
from ..deps import get_current_user
from ..schemas.governance import (
    ProposalCreate,
    ProposalResponse,
    VoteRequest,
    VoteResponse
)

router = APIRouter()

@router.post("/proposals", response_model=ProposalResponse)
async def create_proposal(
    request: ProposalCreate,
    governance_manager: GovernanceManager = Depends(GovernanceManager),
    current_user: str = Depends(get_current_user)
):
    """Create a new proposal"""
    proposal = await governance_manager.create_proposal(
        creator=current_user,
        type=request.type,
        title=request.title,
        description=request.description,
        parameter_changes=request.parameter_changes
    )
    return proposal

@router.get("/proposals", response_model=List[ProposalResponse])
async def list_proposals(
    status: ProposalStatus = None,
    governance_manager: GovernanceManager = Depends(GovernanceManager),
    current_user: str = Depends(get_current_user)
):
    """List all proposals"""
    return await governance_manager.get_proposals(status=status)

@router.post("/vote", response_model=VoteResponse)
async def vote_on_proposal(
    request: VoteRequest,
    governance_manager: GovernanceManager = Depends(GovernanceManager),
    current_user: str = Depends(get_current_user)
):
    """Vote on a proposal"""
    success = await governance_manager.cast_vote(
        proposal_id=request.proposal_id,
        voter=current_user,
        support=request.support,
        vote_weight=request.vote_weight
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to cast vote")
        
    return {
        "proposal_id": request.proposal_id,
        "voter": current_user,
        "support": request.support,
        "vote_weight": request.vote_weight
    }
