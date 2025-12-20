"""
Danbooru API Client
Async client for interacting with Danbooru (https://danbooru.donmai.us).
Reference: https://danbooru.donmai.us/wiki_pages/help:api

Features:
- Async/Await support via aiohttp
- Rate limiting (10 req/s global read limit)
- Authentication support (Basic Auth or Query Params)
- Robust error handling for Danbooru specific codes
"""

import asyncio
import aiohttp
import logging
import time
import base64
from typing import List, Dict, Optional, Union, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DanbooruPost:
    id: int
    file_url: Optional[str]
    large_file_url: Optional[str]
    preview_file_url: Optional[str]
    tag_string: str
    rating: str
    score: int
    width: int
    height: int
    created_at: str

class DanbooruClient:
    BASE_URL = "https://danbooru.donmai.us"
    
    def __init__(self, username: Optional[str] = None, api_key: Optional[str] = None):
        self.username = username
        self.api_key = api_key
        self._last_request_time = 0.0
        self._lock = asyncio.Lock()
        
        # 10 requests per second = 0.1s delay between requests
        self.RATE_LIMIT_DELAY = 0.15  # Slightly conservative

    def _get_auth_header(self) -> Optional[Dict[str, str]]:
        if self.username and self.api_key:
            auth_str = f"{self.username}:{self.api_key}"
            b64_auth = base64.b64encode(auth_str.encode()).decode()
            return {"Authorization": f"Basic {b64_auth}"}
        return None

    async def _enforce_rate_limit(self):
        async with self._lock:
            now = time.time()
            elapsed = now - self._last_request_time
            if elapsed < self.RATE_LIMIT_DELAY:
                wait_time = self.RATE_LIMIT_DELAY - elapsed
                await asyncio.sleep(wait_time)
            self._last_request_time = time.time()

    async def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Any:
        await self._enforce_rate_limit()
        
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "User-Agent": "YukiClient/1.0 (yuki@localhost)",
            "Content-Type": "application/json"
        }
        
        auth_header = self._get_auth_header()
        if auth_header:
            headers.update(auth_header)

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, params=params, json=json_data, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    logger.warning("Danbooru Rate Limit Exceeded (429). Retrying after delay...")
                    await asyncio.sleep(2)
                    return await self._request(method, endpoint, params, json_data) # Simple retry
                elif response.status == 403:
                    raise PermissionError("Access Denied (403). Check API Key permissions.")
                elif response.status == 404:
                    return None # Not found
                else:
                    text = await response.text()
                    raise RuntimeError(f"Danbooru API Error {response.status}: {text}")

    async def get_posts(self, tags: str, limit: int = 20, page: int = 1) -> List[DanbooruPost]:
        """
        Search for posts.
        Args:
            tags: Space separated tags (e.g. "frieren 1girl")
            limit: Max 200
            page: Page number
        """
        params = {
            "tags": tags,
            "limit": limit,
            "page": page
        }
        
        data = await self._request("GET", "/posts.json", params=params)
        if not data:
            return []
            
        results = []
        for item in data:
            try:
                # Some posts might be deleted or restricted and lack file_url
                if "file_url" not in item and "large_file_url" not in item:
                    continue
                    
                results.append(DanbooruPost(
                    id=item.get("id"),
                    file_url=item.get("file_url"),
                    large_file_url=item.get("large_file_url"),
                    preview_file_url=item.get("preview_file_url"),
                    tag_string=item.get("tag_string", ""),
                    rating=item.get("rating"),
                    score=item.get("score", 0),
                    width=item.get("image_width", 0),
                    height=item.get("image_height", 0),
                    created_at=item.get("created_at")
                ))
            except Exception as e:
                logger.warning(f"Failed to parse post {item.get('id')}: {e}")
                
        return results

    async def get_post(self, post_id: int) -> Optional[DanbooruPost]:
        """Get a single post by ID."""
        data = await self._request("GET", f"/posts/{post_id}.json")
        if not data:
            return None
            
        return DanbooruPost(
            id=data.get("id"),
            file_url=data.get("file_url"),
            large_file_url=data.get("large_file_url"),
            preview_file_url=data.get("preview_file_url"),
            tag_string=data.get("tag_string", ""),
            rating=data.get("rating"),
            score=data.get("score", 0),
            width=data.get("image_width", 0),
            height=data.get("image_height", 0),
            created_at=data.get("created_at")
        )

# Example Usage
if __name__ == "__main__":
    async def main():
        client = DanbooruClient()
        
        print("🔍 Searching for 'frieren'...")
        posts = await client.get_posts("frieren rating:g", limit=5)
        
        for post in posts:
            print(f"[{post.id}] Score: {post.score} - {post.large_file_url}")
            
    asyncio.run(main())
