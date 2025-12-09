"""
Price Tracking & Spike Detection System
=========================================
Tracks historical pricing data and detects price spikes.

Who Visions LLC - Shared by Unk & Yuki
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class PriceSnapshot:
    """Single price point in time."""
    timestamp: str
    service: str
    sku_id: str
    sku_description: str
    price_type: str  # 'input', 'output', 'storage', etc.
    price_per_unit: float
    unit: str
    tier_start: Optional[float] = None
    metadata: Optional[Dict] = None


@dataclass
class PriceSpike:
    """Detected price spike event."""
    timestamp: str
    service: str
    sku_id: str
    sku_description: str
    price_type: str
    previous_price: float
    current_price: float
    percentage_increase: float
    absolute_increase: float
    severity: str  # 'low', 'medium', 'high', 'critical'
    days_since_last_check: int


class PriceTracker:
    """Tracks pricing history and detects spikes."""
    
    def __init__(self, storage_path: str = "data/price_history.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.history: List[PriceSnapshot] = self._load_history()
    
    def _load_history(self) -> List[PriceSnapshot]:
        """Load price history from storage."""
        if not self.storage_path.exists():
            return []
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return [PriceSnapshot(**item) for item in data]
        except Exception as e:
            print(f"Error loading price history: {e}")
            return []
    
    def _save_history(self):
        """Save price history to storage."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump([asdict(snapshot) for snapshot in self.history], f, indent=2)
        except Exception as e:
            print(f"Error saving price history: {e}")
    
    def record_price(
        self,
        service: str,
        sku_id: str,
        sku_description: str,
        price_type: str,
        price_per_unit: float,
        unit: str,
        tier_start: Optional[float] = None,
        metadata: Optional[Dict] = None
    ):
        """Record a price snapshot."""
        snapshot = PriceSnapshot(
            timestamp=datetime.utcnow().isoformat(),
            service=service,
            sku_id=sku_id,
            sku_description=sku_description,
            price_type=price_type,
            price_per_unit=price_per_unit,
            unit=unit,
            tier_start=tier_start,
            metadata=metadata or {}
        )
        
        self.history.append(snapshot)
        self._save_history()
    
    def get_latest_price(
        self,
        service: str,
        sku_id: str,
        price_type: Optional[str] = None
    ) -> Optional[PriceSnapshot]:
        """Get the most recent price for a SKU."""
        matches = [
            s for s in self.history
            if s.service == service and s.sku_id == sku_id
            and (price_type is None or s.price_type == price_type)
        ]
        
        if not matches:
            return None
        
        return max(matches, key=lambda x: x.timestamp)
    
    def get_price_history(
        self,
        service: Optional[str] = None,
        sku_id: Optional[str] = None,
        price_type: Optional[str] = None,
        days: Optional[int] = None
    ) -> List[PriceSnapshot]:
        """Get price history with optional filters."""
        filtered = self.history
        
        if service:
            filtered = [s for s in filtered if s.service == service]
        
        if sku_id:
            filtered = [s for s in filtered if s.sku_id == sku_id]
        
        if price_type:
            filtered = [s for s in filtered if s.price_type == price_type]
        
        if days:
            cutoff = datetime.utcnow() - timedelta(days=days)
            filtered = [
                s for s in filtered
                if datetime.fromisoformat(s.timestamp.replace('Z', '+00:00')) >= cutoff
            ]
        
        return sorted(filtered, key=lambda x: x.timestamp)
    
    def detect_spikes(
        self,
        service: Optional[str] = None,
        threshold_percentage: float = 10.0,
        days_lookback: int = 30
    ) -> List[PriceSpike]:
        """
        Detect price spikes above threshold.
        
        Args:
            service: Filter by service name
            threshold_percentage: Minimum percentage increase to consider a spike
            days_lookback: How many days to look back for comparison
        """
        spikes = []
        cutoff_date = datetime.utcnow() - timedelta(days=days_lookback)
        
        # Group by service + sku_id + price_type
        groups: Dict[Tuple[str, str, str], List[PriceSnapshot]] = {}
        
        for snapshot in self.history:
            if service and snapshot.service != service:
                continue
            
            key = (snapshot.service, snapshot.sku_id, snapshot.price_type)
            if key not in groups:
                groups[key] = []
            groups[key].append(snapshot)
        
        for (svc, sku, ptype), snapshots in groups.items():
            # Sort by timestamp
            sorted_snapshots = sorted(snapshots, key=lambda x: x.timestamp)
            
            if len(sorted_snapshots) < 2:
                continue
            
            # Compare latest with previous
            latest = sorted_snapshots[-1]
            latest_time = datetime.fromisoformat(latest.timestamp.replace('Z', '+00:00'))
            
            # Find the most recent price before the cutoff or the previous one
            previous = None
            for snap in reversed(sorted_snapshots[:-1]):
                snap_time = datetime.fromisoformat(snap.timestamp.replace('Z', '+00:00'))
                if snap_time < latest_time and snap.price_per_unit > 0:
                    previous = snap
                    break
            
            if not previous or previous.price_per_unit == 0:
                continue
            
            # Calculate increase
            if latest.price_per_unit > previous.price_per_unit:
                percentage_increase = (
                    (latest.price_per_unit - previous.price_per_unit) / previous.price_per_unit
                ) * 100
                
                if percentage_increase >= threshold_percentage:
                    absolute_increase = latest.price_per_unit - previous.price_per_unit
                    days_diff = (latest_time - datetime.fromisoformat(previous.timestamp.replace('Z', '+00:00'))).days
                    
                    # Determine severity
                    if percentage_increase >= 50:
                        severity = "critical"
                    elif percentage_increase >= 25:
                        severity = "high"
                    elif percentage_increase >= 15:
                        severity = "medium"
                    else:
                        severity = "low"
                    
                    spike = PriceSpike(
                        timestamp=latest.timestamp,
                        service=svc,
                        sku_id=sku,
                        sku_description=latest.sku_description,
                        price_type=ptype,
                        previous_price=previous.price_per_unit,
                        current_price=latest.price_per_unit,
                        percentage_increase=round(percentage_increase, 2),
                        absolute_increase=round(absolute_increase, 6),
                        severity=severity,
                        days_since_last_check=days_diff
                    )
                    spikes.append(spike)
        
        return sorted(spikes, key=lambda x: x.percentage_increase, reverse=True)
    
    def get_price_trend(
        self,
        service: str,
        sku_id: str,
        price_type: str,
        days: int = 30
    ) -> Dict[str, any]:
        """Get price trend analysis for a specific SKU."""
        history = self.get_price_history(
            service=service,
            sku_id=sku_id,
            price_type=price_type,
            days=days
        )
        
        if len(history) < 2:
            return {
                "service": service,
                "sku_id": sku_id,
                "price_type": price_type,
                "data_points": len(history),
                "trend": "insufficient_data"
            }
        
        prices = [s.price_per_unit for s in history]
        first_price = prices[0]
        last_price = prices[-1]
        
        if first_price == 0:
            return {
                "service": service,
                "sku_id": sku_id,
                "price_type": price_type,
                "data_points": len(history),
                "trend": "insufficient_data"
            }
        
        percentage_change = ((last_price - first_price) / first_price) * 100
        avg_price = sum(prices) / len(prices)
        max_price = max(prices)
        min_price = min(prices)
        
        return {
            "service": service,
            "sku_id": sku_id,
            "price_type": price_type,
            "data_points": len(history),
            "first_price": first_price,
            "last_price": last_price,
            "average_price": round(avg_price, 6),
            "max_price": max_price,
            "min_price": min_price,
            "percentage_change": round(percentage_change, 2),
            "trend": "increasing" if percentage_change > 0 else "decreasing" if percentage_change < 0 else "stable",
            "timeline": [
                {
                    "timestamp": s.timestamp,
                    "price": s.price_per_unit
                }
                for s in history
            ]
        }
    
    def import_from_csv(self, csv_path: str):
        """Import pricing data from CSV file."""
        import csv
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                service = row.get('Google service', '').strip()
                service_desc = row.get('Service description', '').strip()
                sku_id = row.get('SKU ID', '').strip()
                sku_desc = row.get('SKU description', '').strip()
                contract_price = row.get('Contract price ($)', '').strip()
                unit_desc = row.get('Unit description', '').strip()
                tier_start = row.get('Tiered usage start', '').strip()
                
                if not service or not sku_id or not contract_price:
                    continue
                
                try:
                    price = float(contract_price)
                    tier = float(tier_start) if tier_start else None
                    
                    # Determine price type from SKU description
                    price_type = "unknown"
                    if "input" in sku_desc.lower():
                        price_type = "input"
                    elif "output" in sku_desc.lower():
                        price_type = "output"
                    elif "storage" in sku_desc.lower():
                        price_type = "storage"
                    elif "egress" in sku_desc.lower() or "transfer" in sku_desc.lower():
                        price_type = "egress"
                    elif "operations" in sku_desc.lower() or "ops" in sku_desc.lower():
                        price_type = "operations"
                    elif "generation" in sku_desc.lower():
                        price_type = "generation"
                    elif "cpu" in sku_desc.lower():
                        price_type = "cpu"
                    elif "memory" in sku_desc.lower() or "ram" in sku_desc.lower():
                        price_type = "memory"
                    
                    self.record_price(
                        service=service,
                        sku_id=sku_id,
                        sku_description=sku_desc,
                        price_type=price_type,
                        price_per_unit=price,
                        unit=unit_desc,
                        tier_start=tier,
                        metadata={
                            "service_description": service_desc,
                            "source": "csv_import"
                        }
                    )
                except ValueError:
                    continue
        
        print(f"Imported {len([s for s in self.history if s.metadata.get('source') == 'csv_import'])} price records from CSV")


# Global tracker instance
_tracker_instance: Optional[PriceTracker] = None


def get_tracker() -> PriceTracker:
    """Get or create global price tracker instance."""
    global _tracker_instance
    if _tracker_instance is None:
        storage_path = os.environ.get("PRICE_HISTORY_PATH", "data/price_history.json")
        _tracker_instance = PriceTracker(storage_path=storage_path)
    return _tracker_instance
