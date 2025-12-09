"""
AniDB HTTP API Client
Handles real-time data retrieval from AniDB's HTTP API.
Reference: https://wiki.anidb.net/w/HTTP_API_Definition

Features:
- Real-time anime details (AID lookup)
- Random recommendations and similar anime
- Hot anime retrieval
- Strict rate limiting (2s delay) and caching support
- Gzip handling and XML parsing
"""

import asyncio
import aiohttp
import logging
import time
import gzip
import xml.etree.ElementTree as ET
from typing import Dict, Optional, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AniDBHTTPClient:
    BASE_URL = "http://api.anidb.net:9001/httpapi"
    CLIENT_NAME = "yukiclient"  # Must be registered if used in prod
    CLIENT_VER = 1
    PROTO_VER = 1
    
    def __init__(self):
        self._last_request_time = 0.0
        self._lock = asyncio.Lock()
        self.RATE_LIMIT_DELAY = 2.1  # Strict 2s delay + buffer

    async def _enforce_rate_limit(self):
        async with self._lock:
            now = time.time()
            elapsed = now - self._last_request_time
            if elapsed < self.RATE_LIMIT_DELAY:
                wait_time = self.RATE_LIMIT_DELAY - elapsed
                logger.debug(f"Rate limit: waiting {wait_time:.2f}s")
                await asyncio.sleep(wait_time)
            self._last_request_time = time.time()

    async def _request(self, params: Dict[str, Any]) -> Optional[str]:
        await self._enforce_rate_limit()
        
        # Add required protocol params
        params.update({
            "client": self.CLIENT_NAME,
            "clientver": self.CLIENT_VER,
            "protover": self.PROTO_VER
        })
        
        headers = {"Accept-Encoding": "gzip"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params, headers=headers) as response:
                if response.status == 403:
                    logger.error("AniDB API: Banned (403). Check rate limits.")
                    return None
                if response.status == 503:
                    logger.warning("AniDB API: Service Unavailable (503). Retrying...")
                    await asyncio.sleep(5)
                    return await self._request(params)
                
                content = await response.read()
                
                # Handle gzip if needed (aiohttp usually handles this, but API docs mention manual need)
                # However, aiohttp with auto_decompress=True (default) handles standard gzip headers.
                # We'll rely on aiohttp but have a fallback check.
                try:
                    text = content.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        text = gzip.decompress(content).decode('utf-8')
                    except:
                        text = content.decode('latin-1') # Fallback
                        
                return text

    async def get_anime(self, aid: int) -> Optional[Dict[str, Any]]:
        """Get details for a specific anime by AID."""
        xml_data = await self._request({"request": "anime", "aid": aid})
        if not xml_data:
            return None
            
        return self._parse_anime_xml(xml_data)

    async def get_hot_anime(self) -> str:
        """Get list of currently popular anime."""
        return await self._request({"request": "hotanime"})

    async def get_random_recommendation(self) -> str:
        """Get a random recommendation."""
        return await self._request({"request": "randomrecommendation"})

    def _parse_anime_xml(self, xml_content: str) -> Dict[str, Any]:
        """Parse the raw XML into a dictionary."""
        try:
            root = ET.fromstring(xml_content)
            if root.tag == "error":
                logger.error(f"AniDB Error: {root.text}")
                return {}
                
            data = {
                "id": root.get("id"),
                "type": root.findtext("type"),
                "episode_count": root.findtext("episodecount"),
                "start_date": root.findtext("startdate"),
                "end_date": root.findtext("enddate"),
                "titles": [],
                "description": root.findtext("description"),
                "rating": root.find("ratings/permanent").text if root.find("ratings/permanent") is not None else "N/A"
            }
            
            for title in root.findall("titles/title"):
                data["titles"].append({
                    "text": title.text,
                    "lang": title.get("{http://www.w3.org/XML/1998/namespace}lang"),
                    "type": title.get("type")
                })
                
            return data
        except Exception as e:
            logger.error(f"Failed to parse XML: {e}")
            return {}

# Example Usage
if __name__ == "__main__":
    async def main():
        client = AniDBHTTPClient()
        
        print("Fetching info for 'Crest of the Stars' (AID=1)...")
        anime = await client.get_anime(1)
        if anime:
            print(f"Title: {anime.get('titles')[0]['text']}")
            print(f"Episodes: {anime.get('episode_count')}")
            print(f"Rating: {anime.get('rating')}")
            
        print("\nFetching Hot Anime...")
        hot = await client.get_hot_anime()
        print(f"Hot Anime XML length: {len(hot) if hot else 0}")

    asyncio.run(main())
