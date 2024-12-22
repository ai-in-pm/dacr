from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, ConfigDict
import uuid
import logging

logger = logging.getLogger(__name__)

class ProposalType(str, Enum):
    PARAMETER_CHANGE = "parameter_change"
    RESERVE_ADJUSTMENT = "reserve_adjustment"
    FEATURE_ADDITION = "feature_addition"
    POLICY_UPDATE = "policy_update"

class ProposalStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"

class Vote(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    voter: str
    vote_weight: Decimal
    timestamp: datetime
    support: bool

class Proposal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: str
    type: ProposalType
    title: str
    description: str
    creator: str
    creation_time: datetime
    status: ProposalStatus
    voting_ends_at: datetime
    execution_delay: timedelta
    votes_for: Decimal = Decimal('0')
    votes_against: Decimal = Decimal('0')
    parameter_changes: Optional[Dict[str, Any]] = None

class GovernanceManager:
    """Manages the governance system for DACR"""
    
    def __init__(self):
        self._proposals: Dict[str, Proposal] = {}
        self._votes: Dict[str, Dict[str, Vote]] = {}  # proposal_id -> voter -> vote
        self._voting_period = timedelta(days=7)
        self._execution_delay = timedelta(days=2)
        self._proposal_threshold = Decimal('1000')  # Min DAC required to create proposal
        self._quorum_threshold = Decimal('0.4')  # 40% of total voting power
        
    async def create_proposal(
        self,
        creator: str,
        type: ProposalType,
        title: str,
        description: str,
        parameter_changes: Optional[Dict[str, Any]] = None
    ) -> Proposal:
        """Creates a new governance proposal"""
        proposal = Proposal(
            id=str(uuid.uuid4()),
            type=type,
            title=title,
            description=description,
            creator=creator,
            creation_time=datetime.utcnow(),
            status=ProposalStatus.PENDING,
            voting_ends_at=datetime.utcnow() + self._voting_period,
            execution_delay=self._execution_delay,
            parameter_changes=parameter_changes
        )
        
        self._proposals[proposal.id] = proposal
        self._votes[proposal.id] = {}
        logger.info(f"Created proposal {proposal.id}: {title}")
        return proposal
        
    async def cast_vote(
        self,
        proposal_id: str,
        voter: str,
        support: bool,
        vote_weight: Decimal
    ) -> bool:
        """Casts a vote on a proposal"""
        if proposal_id not in self._proposals:
            logger.error(f"Proposal {proposal_id} not found")
            return False
            
        proposal = self._proposals[proposal_id]
        if proposal.status != ProposalStatus.ACTIVE:
            logger.error(f"Proposal {proposal_id} is not active")
            return False
            
        if datetime.utcnow() > proposal.voting_ends_at:
            logger.error(f"Voting period for proposal {proposal_id} has ended")
            return False
            
        vote = Vote(
            voter=voter,
            vote_weight=vote_weight,
            timestamp=datetime.utcnow(),
            support=support
        )
        
        # Remove previous vote if exists
        if voter in self._votes[proposal_id]:
            old_vote = self._votes[proposal_id][voter]
            if old_vote.support:
                proposal.votes_for -= old_vote.vote_weight
            else:
                proposal.votes_against -= old_vote.vote_weight
                
        # Record new vote
        self._votes[proposal_id][voter] = vote
        if support:
            proposal.votes_for += vote_weight
        else:
            proposal.votes_against += vote_weight
            
        logger.info(f"Recorded vote from {voter} on proposal {proposal_id}")
        return True
        
    async def process_proposals(self) -> None:
        """Processes proposals and updates their status"""
        current_time = datetime.utcnow()
        
        for proposal in self._proposals.values():
            if proposal.status == ProposalStatus.PENDING:
                proposal.status = ProposalStatus.ACTIVE
                
            elif proposal.status == ProposalStatus.ACTIVE and current_time > proposal.voting_ends_at:
                total_votes = proposal.votes_for + proposal.votes_against
                
                # Check if quorum is reached
                if total_votes >= self._quorum_threshold:
                    if proposal.votes_for > proposal.votes_against:
                        proposal.status = ProposalStatus.PASSED
                        logger.info(f"Proposal {proposal.id} passed")
                    else:
                        proposal.status = ProposalStatus.REJECTED
                        logger.info(f"Proposal {proposal.id} rejected")
                else:
                    proposal.status = ProposalStatus.REJECTED
                    logger.info(f"Proposal {proposal.id} rejected due to insufficient quorum")
                    
    async def execute_proposal(self, proposal_id: str) -> bool:
        """Executes a passed proposal"""
        if proposal_id not in self._proposals:
            logger.error(f"Proposal {proposal_id} not found")
            return False
            
        proposal = self._proposals[proposal_id]
        if proposal.status != ProposalStatus.PASSED:
            logger.error(f"Proposal {proposal_id} is not in passed status")
            return False
            
        execution_time = proposal.voting_ends_at + proposal.execution_delay
        if datetime.utcnow() < execution_time:
            logger.error(f"Execution delay for proposal {proposal_id} has not elapsed")
            return False
            
        try:
            # Implement proposal execution logic here based on proposal type
            proposal.status = ProposalStatus.EXECUTED
            logger.info(f"Executed proposal {proposal_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to execute proposal {proposal_id}: {str(e)}")
            return False
            
    async def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        """Retrieves a proposal by ID"""
        return self._proposals.get(proposal_id)
        
    async def get_proposals(
        self,
        status: Optional[ProposalStatus] = None
    ) -> List[Proposal]:
        """Retrieves all proposals, optionally filtered by status"""
        if status:
            return [p for p in self._proposals.values() if p.status == status]
        return list(self._proposals.values())
        
    async def get_votes(self, proposal_id: str) -> List[Vote]:
        """Retrieves all votes for a proposal"""
        if proposal_id not in self._votes:
            return []
        return list(self._votes[proposal_id].values())
