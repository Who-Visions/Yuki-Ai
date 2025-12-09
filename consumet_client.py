"""
Consumet API Client
Async client for Consumet API (https://github.com/consumet/api.consumet.org).
Default Base URL: https://api.consumet.org (Public instance)

Features:
- Search anime (Gogoanime provider)
- Get anime details
- Get streaming links
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsumetClient:
    # Note: Public instance may be unstable. Users often self-host.
    BASE_URL = "https://api.consumet.org" 

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")

    async def search_anime(self, query: str, page: int = 1) -> Optional[Dict[str, Any]]:
        """Search using Gogoanime provider."""
        url = f"{self.base_url}/anime/gogoanime/{query}"
        params = {"page": page}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        logger.error(f"Consumet API Error {response.status}")
                        return None
                    return await response.json()
            except Exception as e:
                logger.error(f"Failed to connect to Consumet: {e}")
                return None

    async def get_anime_info(self, id: str) -> Optional[Dict[str, Any]]:
        """Get details by ID (e.g., 'frieren-beyond-journeys-end')."""
        url = f"{self.base_url}/anime/gogoanime/info/{id}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        logger.error(f"Consumet API Error {response.status}")
                        return None
                    return await response.json()
            except Exception as e:
                logger.error(f"Failed to connect to Consumet: {e}")
                return None

# Example Usage
if __name__ == "__main__":
    async def main():
        client = ConsumetClient()
        print("🔍 Searching for 'Frieren' on Consumet (Gogoanime)...")
        results = await client.search_anime("Frieren")
        
        if results and "results" in results:
            first = results["results"][0]
            print(f"Found: {first.get('title')} (ID: {first.get('id')})")
            
            print(f"\nFetching details for {first.get('id')}...")
            details = await client.get_anime_info(first.get('id'))
            if details:
                print(f"Episodes: {len(details.get('episodes', []))}")
                print(f"Description: {details.get('description')[:100]}...")

    asyncio.run(main())
