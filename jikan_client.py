"""
Jikan API Client - Production Grade
Cloud-native client for MyAnimeList (Jikan) API with enterprise features:
- Rate limiting and retry logic
- Caching support
- Comprehensive error handling
- Request/response validation
- Monitoring hooks
"""

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from urllib.parse import urljoin

import aiohttp
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnimeType(Enum):
    """Anime types supported by Jikan API"""
    TV = "tv"
    MOVIE = "movie"
    OVA = "ova"
    SPECIAL = "special"
    ONA = "ona"
    MUSIC = "music"


class AnimeStatus(Enum):
    """Anime airing status"""
    AIRING = "airing"
    COMPLETE = "complete"
    UPCOMING = "upcoming"


class RateLimitError(Exception):
    """Raised when API rate limit is exceeded"""
    pass


class JikanAPIError(Exception):
    """Base exception for Jikan API errors"""
    pass


@dataclass
class AnimeData:
    """Structured anime data from Jikan API"""
    mal_id: int
    title: str
    title_english: Optional[str]
    title_japanese: Optional[str]
    type: str
    source: str
    episodes: Optional[int]
    status: str
    airing: bool
    aired_from: Optional[str]
    aired_to: Optional[str]
    duration: Optional[str]
    rating: Optional[str]
    score: Optional[float]
    scored_by: Optional[int]
    rank: Optional[int]
    popularity: Optional[int]
    members: Optional[int]
    favorites: Optional[int]
    synopsis: Optional[str]
    background: Optional[str]
    season: Optional[str]
    year: Optional[int]
    broadcast: Optional[Dict[str, Any]]
    producers: List[Dict[str, Any]]
    studios: List[Dict[str, Any]]
    genres: List[Dict[str, Any]]
    themes: List[Dict[str, Any]]
    demographics: List[Dict[str, Any]]
    images: Dict[str, Any]
    trailer: Optional[Dict[str, Any]]
    url: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def cache_key(self) -> str:
        """Generate cache key for this anime"""
        return f"anime:{self.mal_id}"


class JikanClient:
    """
    Production-grade Jikan API client
    
    Features:
    - Automatic rate limiting (3 req/sec, 60 req/min per Jikan v4 limits)
    - Exponential backoff retry logic
    - Response caching support
    - Request validation
    - Comprehensive error handling
    - Metrics collection hooks
    """
    
    BASE_URL = "https://api.jikan.moe/v4"
    RATE_LIMIT_PER_SECOND = 2  # Reduced from 3 to be safe
    RATE_LIMIT_PER_MINUTE = 50 # Reduced from 60 to be safe
    CACHE_TTL_SECONDS = 3600  # 1 hour default
    
    def __init__(
        self,
        cache_backend: Optional[Any] = None,
        metrics_callback: Optional[Callable] = None,
        session: Optional[aiohttp.ClientSession] = None
    ):
        """
        Initialize Jikan client
        
        Args:
            cache_backend: Optional cache backend (Redis, etc.)
            metrics_callback: Callback for metrics collection
            session: Optional aiohttp session (will create if None)
        """
        self._session = session
        self._cache = cache_backend
        self._metrics = metrics_callback
        self._request_times: List[float] = []
        self._lock = asyncio.Lock()
        
    async def __aenter__(self):
        """Async context manager entry"""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self._session:
            await self._session.close()
    
    async def _enforce_rate_limit(self):
        """Enforce API rate limits"""
        async with self._lock:
            now = time.time()
            # Remove requests older than 1 minute
            self._request_times = [t for t in self._request_times if now - t < 60]
            
            # Check per-minute limit
            if len(self._request_times) >= self.RATE_LIMIT_PER_MINUTE:
                wait_time = 60 - (now - self._request_times[0]) + 1 # Add buffer
                logger.info(f"Rate limit (minute) reached, waiting {wait_time:.2f}s")
                await asyncio.sleep(wait_time)
                # Re-check time after sleep to remove old entries
                now = time.time()
                self._request_times = [t for t in self._request_times if now - t < 60]
            
            # Check per-second limit
            recent_requests = [t for t in self._request_times if now - t < 1]
            if len(recent_requests) >= self.RATE_LIMIT_PER_SECOND:
                logger.debug("Rate limit (second) reached, small sleep")
                await asyncio.sleep(1.2) # Sleep slightly more than 1s
            
            self._request_times.append(time.time()) # Append NEW time
    
    def _cache_key(self, endpoint: str, params: Optional[Dict] = None) -> str:
        """Generate cache key for request"""
        key_parts = [endpoint]
        if params:
            key_parts.append(json.dumps(params, sort_keys=True))
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    async def _get_cached(self, cache_key: str) -> Optional[Dict]:
        """Get data from cache"""
        if not self._cache:
            return None
        
        try:
            cached_data = await self._cache.get(cache_key)
            if cached_data:
                logger.debug(f"Cache hit: {cache_key}")
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
        
        return None
    
    async def _set_cached(self, cache_key: str, data: Dict, ttl: int = None):
        """Set data in cache"""
        if not self._cache:
            return
        
        try:
            ttl = ttl or self.CACHE_TTL_SECONDS
            await self._cache.setex(
                cache_key,
                ttl,
                json.dumps(data)
            )
            logger.debug(f"Cache set: {cache_key} (TTL: {ttl}s)")
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
    
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=4, max=20),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError))
    )
    async def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Jikan API with retry logic
        
        Args:
            endpoint: API endpoint (e.g., '/seasons/2022/summer')
            params: Query parameters
            
        Returns:
            API response data
            
        Raises:
            JikanAPIError: On API errors
            RateLimitError: On rate limit exceeded
        """
        # Check cache first
        cache_key = self._cache_key(endpoint, params)
        cached = await self._get_cached(cache_key)
        if cached:
            return cached
        
        # Enforce rate limiting
        await self._enforce_rate_limit()
        
        # Make request
        # Ensure proper URL joining (handle leading slashes)
        base = self.BASE_URL.rstrip('/')
        path = endpoint.lstrip('/')
        url = f"{base}/{path}"
        
        start_time = time.time()
        
        try:
            if not self._session:
                raise RuntimeError("Client session not initialized. Use 'async with' context manager.")
            
            async with self._session.get(url, params=params) as response:
                elapsed = time.time() - start_time
                
                # Collect metrics
                if self._metrics:
                    await self._metrics({
                        'endpoint': endpoint,
                        'status': response.status,
                        'elapsed': elapsed
                    })
                
                # Handle rate limiting
                if response.status == 429:
                    raise RateLimitError("API rate limit exceeded")
                
                # Handle errors
                if response.status >= 400:
                    error_text = await response.text()
                    raise JikanAPIError(
                        f"API error {response.status}: {error_text}"
                    )
                
                data = await response.json()
                logger.info(f"GET {endpoint} - {response.status} - {elapsed:.2f}s")
                
                # Cache successful response
                await self._set_cached(cache_key, data)
                
                return data
                
        except aiohttp.ClientError as e:
            logger.error(f"Request failed: {e}")
            raise
    
    async def get_seasonal_anime(
        self,
        year: int,
        season: str,
        sfw: bool = True,
        page: int = 1
    ) -> List[AnimeData]:
        """
        Get anime for a specific season
        
        Args:
            year: Year (e.g., 2022)
            season: Season (winter, spring, summer, fall)
            sfw: Safe for work filter
            page: Page number (25 items per page)
            
        Returns:
            List of anime data
        """
        endpoint = f"/seasons/{year}/{season}"
        params = {"sfw": "true" if sfw else "false", "page": page}
        
        response = await self._make_request(endpoint, params)
        
        anime_list = []
        for item in response.get("data", []):
            try:
                anime = self._parse_anime(item)
                anime_list.append(anime)
            except Exception as e:
                logger.warning(f"Failed to parse anime {item.get('mal_id')}: {e}")
        
        return anime_list
    
    async def get_anime_by_id(self, mal_id: int) -> AnimeData:
        """
        Get anime by MyAnimeList ID
        
        Args:
            mal_id: MyAnimeList ID
            
        Returns:
            Anime data
        """
        endpoint = f"/anime/{mal_id}"
        response = await self._make_request(endpoint)
        return self._parse_anime(response.get("data", {}))
    
    async def search_anime(
        self,
        query: str,
        type: Optional[AnimeType] = None,
        status: Optional[AnimeStatus] = None,
        limit: int = 25
    ) -> List[AnimeData]:
        """
        Search for anime
        
        Args:
            query: Search query
            type: Filter by type
            status: Filter by status
            limit: Result limit
            
        Returns:
            List of anime data
        """
        endpoint = "/anime"
        params = {"q": query, "limit": limit}
        
        if type:
            params["type"] = type.value
        if status:
            params["status"] = status.value
        
        response = await self._make_request(endpoint, params)
        
        anime_list = []
        for item in response.get("data", []):
            try:
                anime = self._parse_anime(item)
                anime_list.append(anime)
            except Exception as e:
                logger.warning(f"Failed to parse anime {item.get('mal_id')}: {e}")
        
        return anime_list
    
    async def get_top_anime(
        self,
        type: Optional[AnimeType] = None,
        limit: int = 25,
        page: int = 1
    ) -> List[AnimeData]:
        """
        Get top-rated anime
        
        Args:
            type: Filter by type
            limit: Result limit
            page: Page number
            
        Returns:
            List of top anime
        """
        endpoint = "/top/anime"
        params = {"limit": limit, "page": page}
        
        if type:
            params["type"] = type.value
        
        response = await self._make_request(endpoint, params)
        
        anime_list = []
        for item in response.get("data", []):
            try:
                anime = self._parse_anime(item)
                anime_list.append(anime)
            except Exception as e:
                logger.warning(f"Failed to parse anime {item.get('mal_id')}: {e}")
        
        return anime_list
    
    async def get_anime_characters(self, mal_id: int) -> List[Dict[str, Any]]:
        """
        Get characters for an anime
        
        Args:
            mal_id: MyAnimeList ID
            
        Returns:
            List of character data
        """
        endpoint = f"/anime/{mal_id}/characters"
        response = await self._make_request(endpoint)
        return response.get("data", [])
    
    def _parse_anime(self, data: Dict[str, Any]) -> AnimeData:
        """Parse raw API response into AnimeData"""
        return AnimeData(
            mal_id=data.get("mal_id"),
            title=data.get("title", ""),
            title_english=data.get("title_english"),
            title_japanese=data.get("title_japanese"),
            type=data.get("type", ""),
            source=data.get("source", ""),
            episodes=data.get("episodes"),
            status=data.get("status", ""),
            airing=data.get("airing", False),
            aired_from=data.get("aired", {}).get("from"),
            aired_to=data.get("aired", {}).get("to"),
            duration=data.get("duration"),
            rating=data.get("rating"),
            score=data.get("score"),
            scored_by=data.get("scored_by"),
            rank=data.get("rank"),
            popularity=data.get("popularity"),
            members=data.get("members"),
            favorites=data.get("favorites"),
            synopsis=data.get("synopsis"),
            background=data.get("background"),
            season=data.get("season"),
            year=data.get("year"),
            broadcast=data.get("broadcast"),
            producers=data.get("producers", []),
            studios=data.get("studios", []),
            genres=data.get("genres", []),
            themes=data.get("themes", []),
            demographics=data.get("demographics", []),
            images=data.get("images", {}),
            trailer=data.get("trailer"),
            url=data.get("url", "")
        )


# Example usage
if __name__ == "__main__":
    async def main():
        async with JikanClient() as client:
            # Get Summer 2022 anime
            anime_list = await client.get_seasonal_anime(2022, "summer")
            print(f"Found {len(anime_list)} anime in Summer 2022")
            
            for anime in anime_list[:5]:
                print(f"- {anime.title} (Score: {anime.score})")
    
    asyncio.run(main())
