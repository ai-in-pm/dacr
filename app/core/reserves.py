from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ReserveType(Enum):
    COMPUTATIONAL = "computational"
    STORAGE = "storage"
    ENGAGEMENT = "engagement"

class ReserveManager:
    """Manages the virtual reserves backing the Digital AI Currency"""
    
    def __init__(self):
        self._reserves: Dict[ReserveType, Decimal] = {
            ReserveType.COMPUTATIONAL: Decimal('0'),
            ReserveType.STORAGE: Decimal('0'),
            ReserveType.ENGAGEMENT: Decimal('0')
        }
        self._reserve_weights = {
            ReserveType.COMPUTATIONAL: Decimal('0.4'),
            ReserveType.STORAGE: Decimal('0.3'),
            ReserveType.ENGAGEMENT: Decimal('0.3')
        }
        
    async def add_to_reserves(self, reserve_type: ReserveType, amount: Decimal) -> bool:
        """
        Adds value to a specific reserve type
        
        Args:
            reserve_type: Type of reserve to modify
            amount: Amount to add
            
        Returns:
            bool: Success status
        """
        if amount <= 0:
            logger.error(f"Invalid amount for reserve addition: {amount}")
            return False
            
        self._reserves[reserve_type] += amount
        logger.info(f"Added {amount} to {reserve_type.value} reserves")
        return True
        
    async def remove_from_reserves(self, reserve_type: ReserveType, amount: Decimal) -> bool:
        """
        Removes value from a specific reserve type
        
        Args:
            reserve_type: Type of reserve to modify
            amount: Amount to remove
            
        Returns:
            bool: Success status
        """
        if amount <= 0 or amount > self._reserves[reserve_type]:
            logger.error(f"Invalid amount for reserve removal: {amount}")
            return False
            
        self._reserves[reserve_type] -= amount
        logger.info(f"Removed {amount} from {reserve_type.value} reserves")
        return True
        
    async def get_total_reserves(self) -> Decimal:
        """Calculates the total value of all reserves in USD equivalent"""
        total = Decimal('0')
        for reserve_type in ReserveType:
            weighted_value = self._reserves[reserve_type] * self._reserve_weights[reserve_type]
            total += weighted_value
        return total
        
    async def get_reserve_status(self) -> Dict[str, Decimal]:
        """Returns the current status of all reserves"""
        return {
            reserve_type.value: amount 
            for reserve_type, amount in self._reserves.items()
        }
        
    async def validate_reserves(self) -> bool:
        """
        Validates that reserves meet minimum requirements
        
        Returns:
            bool: Whether reserves are valid
        """
        total_reserves = await self.get_total_reserves()
        # Implement specific validation logic here
        return total_reserves > 0
