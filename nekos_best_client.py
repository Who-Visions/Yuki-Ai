"""
Nekos.Best API Client
Async client for retrieving high-quality anime images and GIFs.
Documentation: https://nekos.best/api/v2/
"""

import aiohttp
import asyncio
import logging
from typing import List, Dict, Optional, Union, Literal
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NekoResult:
    url: str
    artist_name: Optional[str] = None
    artist_href: Optional[str] = None
    source_url: Optional[str] = None
    anime_name: Optional[str] = None

class NekosBestClient:
    BASE_URL = "https://nekos.best/api/v2"
    
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        self._own_session = False

    async def __aenter__(self):
        if not self._session:
            self._session = aiohttp.ClientSession()
            self._own_session = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._own_session and self._session:
            await self._session.close()

    async def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Internal GET helper"""
        url = f"{self.BASE_URL}{endpoint}"
        
        # Ensure session exists if used outside context manager
        if not self._session:
            self._session = aiohttp.ClientSession()
            self._own_session = True
            
        async with self._session.get(url, params=params) as response:
            if response.status != 200:
                text = await response.text()
                raise RuntimeError(f"Nekos.Best API Error {response.status}: {text}")
            return await response.json()

    async def get_endpoints(self) -> Dict[str, Dict[str, str]]:
        """Lists all available categories and their formats."""
        return await self._get("/endpoints")

    async def get_image(self, category: str, amount: int = 1) -> List[NekoResult]:
        """
        Get random images/GIFs from a category.
        
        Args:
            category: e.g., 'neko', 'kitsune', 'hug', 'pat'
            amount: 1-20
        """
        if not 1 <= amount <= 20:
            raise ValueError("Amount must be between 1 and 20")
            
        data = await self._get(f"/{category}", params={"amount": amount})
        return self._parse_results(data)

    async def search(self, query: str, type: int = 1, category: Optional[str] = None, amount: int = 1) -> List[NekoResult]:
        """
        Search for specific images/GIFs.
        
        Args:
            query: Search term (e.g., character name)
            type: 1 for images, 2 for GIFs
            category: Optional category filter
            amount: Number of results
        """
        params = {
            "query": query,
            "type": type,
            "amount": amount
        }
        if category:
            params["category"] = category
            
        data = await self._get("/search", params=params)
        return self._parse_results(data)

    def _parse_results(self, data: Dict) -> List[NekoResult]:
        results = []
        for item in data.get("results", []):
            results.append(NekoResult(
                url=item.get("url"),
                artist_name=item.get("artist_name"),
                artist_href=item.get("artist_href"),
                source_url=item.get("source_url"),
                anime_name=item.get("anime_name")
            ))
        return results

    async def download_image(self, url: str, save_path: str):
        """Helper to download an image to disk"""
        if not self._session:
            self._session = aiohttp.ClientSession()
            self._own_session = True
            
        async with self._session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                with open(save_path, 'wb') as f:
                    f.write(content)
                logger.info(f"Downloaded {url} to {save_path}")
            else:
                logger.error(f"Failed to download {url}")

# Example Usage
if __name__ == "__main__":
    async def main():
        async with NekosBestClient() as client:
            # Test endpoints
            endpoints = await client.get_endpoints()
            print(f"Available endpoints: {list(endpoints.keys())[:5]}...")
            
            # Test random image
            results = await client.get_image("neko", amount=1)
            if results:
                print(f"Random Neko: {results[0].url} by {results[0].artist_name}")
                
            # Test search
            search_res = await client.search("Senko", type=2, category="pat", amount=1)
            if search_res:
                print(f"Found Senko: {search_res[0].url} from {search_res[0].anime_name}")

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
