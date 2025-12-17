"""
Yuki Rate Limiter Service
Implements Token Bucket algorithm for API rate limiting.
Designed to be used as a FastAPI dependency or middleware.
"""

import time
import asyncio
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class RateLimitConfig:
    """Configuration for rate limits"""
    rate: int        # Requests per period
    period: int      # Period in seconds
    burst: int       # Maximum burst size

# Default Limits
TIER_LIMITS = {
    "free": RateLimitConfig(rate=5, period=60, burst=10),     # 5 req/min
    "pro": RateLimitConfig(rate=50, period=60, burst=60),     # 50 req/min
    "studio": RateLimitConfig(rate=1000, period=60, burst=2000), # High limit
}

class TokenBucket:
    """Token bucket implementation for a single client"""
    def __init__(self, config: RateLimitConfig):
        self.rate = config.rate
        self.period = config.period
        self.capacity = config.burst
        self.tokens = config.burst
        self.last_update = time.time()
        self.lock = asyncio.Lock()

    async def consume(self, tokens: int = 1) -> bool:
        """Attempt to consume tokens"""
        async with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            
            # Refill tokens
            refill = elapsed * (self.rate / self.period)
            self.tokens = min(self.capacity, self.tokens + refill)
            self.last_update = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

class RateLimiter:
    """Global Rate Limiter Service"""
    
    def __init__(self):
        # Map user_id/ip -> TokenBucket
        self._buckets: Dict[str, TokenBucket] = {}
        self._clean_lock = asyncio.Lock()
        
    def _get_bucket(self, key: str, tier: str = "free") -> TokenBucket:
        if key not in self._buckets:
            config = TIER_LIMITS.get(tier, TIER_LIMITS["free"])
            self._buckets[key] = TokenBucket(config)
        return self._buckets[key]

    async def check_limit(self, key: str, tier: str = "free", cost: int = 1) -> bool:
        """
        Check if request is allowed.
        key: User ID or IP
        tier: User tier (free, pro, studio)
        cost: Cost of the operation (default 1)
        """
        bucket = self._get_bucket(key, tier)
        return await bucket.consume(cost)

    async def cleanup(self):
        """Remove old buckets to prevent memory leaks"""
        async with self._clean_lock:
            now = time.time()
            # Remove buckets not accessed in 1 hour
            keys_to_remove = [
                k for k, b in self._buckets.items() 
                if now - b.last_update > 3600
            ]
            for k in keys_to_remove:
                del self._buckets[k]

# Global Instance
limiter = RateLimiter()
