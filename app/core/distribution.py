from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class RewardTier(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PREMIUM = "premium"

class RewardType(Enum):
    TASK_COMPLETION = "task_completion"
    ENGAGEMENT = "engagement"
    MILESTONE = "milestone"
    CONTRIBUTION = "contribution"

class DistributionManager:
    """Manages DAC distribution and rewards"""
    
    def __init__(self):
        self._reward_rates = {
            RewardTier.BASIC: Decimal('1.0'),
            RewardTier.INTERMEDIATE: Decimal('2.0'),
            RewardTier.ADVANCED: Decimal('5.0'),
            RewardTier.PREMIUM: Decimal('10.0')
        }
        self._tier_thresholds = {
            RewardTier.BASIC: Decimal('0'),
            RewardTier.INTERMEDIATE: Decimal('100'),
            RewardTier.ADVANCED: Decimal('1000'),
            RewardTier.PREMIUM: Decimal('10000')
        }
        self._user_balances: Dict[str, Decimal] = {}
        self._user_tiers: Dict[str, RewardTier] = {}
        
    async def calculate_reward(
        self,
        user_id: str,
        reward_type: RewardType,
        metadata: Dict[str, any]
    ) -> Decimal:
        """Calculates reward amount based on user tier and activity"""
        tier = await self.get_user_tier(user_id)
        base_rate = self._reward_rates[tier]
        
        multiplier = self._get_reward_multiplier(reward_type, metadata)
        return base_rate * multiplier
        
    async def distribute_reward(
        self,
        user_id: str,
        amount: Decimal,
        reward_type: RewardType
    ) -> bool:
        """Distributes rewards to a user"""
        try:
            current_balance = self._user_balances.get(user_id, Decimal('0'))
            self._user_balances[user_id] = current_balance + amount
            
            # Update user tier if necessary
            await self._update_user_tier(user_id)
            
            logger.info(f"Distributed {amount} DAC to user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to distribute reward to user {user_id}: {str(e)}")
            return False
            
    async def get_user_tier(self, user_id: str) -> RewardTier:
        """Gets the current tier of a user"""
        if user_id not in self._user_tiers:
            self._user_tiers[user_id] = RewardTier.BASIC
        return self._user_tiers[user_id]
        
    async def get_user_balance(self, user_id: str) -> Decimal:
        """Gets the current balance of a user"""
        return self._user_balances.get(user_id, Decimal('0'))
        
    async def _update_user_tier(self, user_id: str) -> None:
        """Updates user tier based on their total balance"""
        balance = self._user_balances.get(user_id, Decimal('0'))
        
        new_tier = RewardTier.BASIC
        for tier, threshold in self._tier_thresholds.items():
            if balance >= threshold:
                new_tier = tier
            else:
                break
                
        if user_id not in self._user_tiers or self._user_tiers[user_id] != new_tier:
            self._user_tiers[user_id] = new_tier
            logger.info(f"Updated user {user_id} to tier {new_tier.value}")
            
    def _get_reward_multiplier(
        self,
        reward_type: RewardType,
        metadata: Dict[str, any]
    ) -> Decimal:
        """Calculates reward multiplier based on activity type and metadata"""
        base_multiplier = Decimal('1.0')
        
        if reward_type == RewardType.TASK_COMPLETION:
            complexity = metadata.get('complexity', 1)
            base_multiplier *= Decimal(str(complexity))
        elif reward_type == RewardType.ENGAGEMENT:
            duration = metadata.get('duration', 0)
            base_multiplier *= Decimal(str(1 + duration / 3600))  # Duration in hours
        elif reward_type == RewardType.MILESTONE:
            importance = metadata.get('importance', 1)
            base_multiplier *= Decimal(str(importance * 2))
        elif reward_type == RewardType.CONTRIBUTION:
            impact = metadata.get('impact', 1)
            base_multiplier *= Decimal(str(impact * 1.5))
            
        return base_multiplier
