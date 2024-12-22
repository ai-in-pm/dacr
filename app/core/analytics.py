from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class AnalyticsManager:
    """Manages system analytics and reporting"""
    
    def __init__(self):
        self._supply_history: List[Tuple[datetime, Decimal]] = []
        self._transaction_volume: Dict[datetime, Decimal] = defaultdict(Decimal)
        self._active_users: Dict[datetime, set] = defaultdict(set)
        self._reserve_history: Dict[datetime, Dict[str, Decimal]] = {}
        
    async def record_supply_change(self, amount: Decimal) -> None:
        """Records a change in total supply"""
        self._supply_history.append((datetime.utcnow(), amount))
        logger.info(f"Recorded supply change: {amount}")
        
    async def record_transaction(
        self,
        amount: Decimal,
        user_id: str,
        timestamp: Optional[datetime] = None
    ) -> None:
        """Records a transaction for volume tracking"""
        ts = timestamp or datetime.utcnow()
        date_key = ts.date()
        self._transaction_volume[date_key] += amount
        self._active_users[date_key].add(user_id)
        logger.info(f"Recorded transaction: {amount} DAC")
        
    async def record_reserve_state(
        self,
        reserves: Dict[str, Decimal],
        timestamp: Optional[datetime] = None
    ) -> None:
        """Records the state of reserves"""
        ts = timestamp or datetime.utcnow()
        self._reserve_history[ts] = reserves.copy()
        logger.info("Recorded reserve state")
        
    async def get_supply_metrics(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Decimal]:
        """Calculates supply metrics for a time period"""
        filtered_history = [
            (ts, amount) for ts, amount in self._supply_history
            if (not start_time or ts >= start_time) and
               (not end_time or ts <= end_time)
        ]
        
        if not filtered_history:
            return {
                "current_supply": Decimal('0'),
                "max_supply": Decimal('0'),
                "min_supply": Decimal('0'),
                "average_supply": Decimal('0')
            }
            
        amounts = [amount for _, amount in filtered_history]
        return {
            "current_supply": amounts[-1],
            "max_supply": max(amounts),
            "min_supply": min(amounts),
            "average_supply": sum(amounts) / len(amounts)
        }
        
    async def get_transaction_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, any]:
        """Calculates transaction metrics for a time period"""
        filtered_volume = {
            date: volume for date, volume in self._transaction_volume.items()
            if (not start_date or date >= start_date.date()) and
               (not end_date or date <= end_date.date())
        }
        
        filtered_users = {
            date: users for date, users in self._active_users.items()
            if (not start_date or date >= start_date.date()) and
               (not end_date or date <= end_date.date())
        }
        
        if not filtered_volume:
            return {
                "total_volume": Decimal('0'),
                "average_daily_volume": Decimal('0'),
                "total_active_users": 0,
                "average_daily_users": 0
            }
            
        total_volume = sum(filtered_volume.values())
        total_days = len(filtered_volume)
        unique_users = set().union(*filtered_users.values())
        
        return {
            "total_volume": total_volume,
            "average_daily_volume": total_volume / total_days,
            "total_active_users": len(unique_users),
            "average_daily_users": sum(len(users) for users in filtered_users.values()) / total_days
        }
        
    async def get_reserve_metrics(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Dict[str, Decimal]]:
        """Calculates reserve metrics for a time period"""
        filtered_history = {
            ts: reserves for ts, reserves in self._reserve_history.items()
            if (not start_time or ts >= start_time) and
               (not end_time or ts <= end_time)
        }
        
        if not filtered_history:
            return {
                "current_reserves": {},
                "average_reserves": {},
                "min_reserves": {},
                "max_reserves": {}
            }
            
        # Get the latest reserve state
        latest_ts = max(filtered_history.keys())
        current_reserves = filtered_history[latest_ts]
        
        # Calculate metrics for each reserve type
        reserve_types = set().union(*[reserves.keys() for reserves in filtered_history.values()])
        metrics = {
            "current_reserves": current_reserves,
            "average_reserves": {},
            "min_reserves": {},
            "max_reserves": {}
        }
        
        for reserve_type in reserve_types:
            values = [
                reserves.get(reserve_type, Decimal('0'))
                for reserves in filtered_history.values()
            ]
            metrics["average_reserves"][reserve_type] = sum(values) / len(values)
            metrics["min_reserves"][reserve_type] = min(values)
            metrics["max_reserves"][reserve_type] = max(values)
            
        return metrics
