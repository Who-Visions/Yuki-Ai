"""
Anime News Network (ANN) Encyclopedia API Client
Handles fetching anime details and reports from ANN.
Reference: https://www.animenewsnetwork.com/encyclopedia/api.php

Features:
- Rate limiting (1 request/second)
- XML parsing
- Batch details fetching
- Report generation
"""

import asyncio
import aiohttp
import logging
import time
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ANNAnime:
    id: int
    gid: Optional[int]
    type: str
    name: str
    precision: str
    generated_on: Optional[str] = None

class ANNClient:
    BASE_URL = "https://cdn.animenewsnetwork.com/encyclopedia"
    API_URL = f"{BASE_URL}/api.xml"
    REPORTS_URL = f"{BASE_URL}/reports.xml"
    
    def __init__(self):
        self._last_request_time = 0
        self._lock = asyncio.Lock()

    async def _enforce_rate_limit(self):
        """Ensure at least 1 second between requests."""
        async with self._lock:
            now = time.time()
            elapsed = now - self._last_request_time
            if elapsed < 1.1: # Buffer slightly over 1s
                wait_time = 1.1 - elapsed
                logger.debug(f"Rate limit: waiting {wait_time:.2f}s")
                await asyncio.sleep(wait_time)
            self._last_request_time = time.time()

    async def get_details(self, ids: Union[int, List[int]], type: str = "anime") -> str:
        """
        Get details for one or more titles.
        Args:
            ids: Single ID or list of IDs (max 50 for batch)
            type: 'anime', 'manga', or 'title'
        Returns:
            Raw XML string (parsing can be complex depending on needs)
        """
        await self._enforce_rate_limit()
        
        if isinstance(ids, list):
            if len(ids) > 50:
                raise ValueError("Max 50 IDs per batch")
            id_param = "/".join(map(str, ids))
        else:
            id_param = str(ids)
            
        params = {type: id_param}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.API_URL, params=params) as response:
                if response.status != 200:
                    raise RuntimeError(f"ANN API Error {response.status}")
                return await response.text()

    async def search_by_name(self, name: str) -> str:
        """Search for a title by name (approximate match)."""
        await self._enforce_rate_limit()
        params = {"title": f"~{name}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.API_URL, params=params) as response:
                if response.status != 200:
                    raise RuntimeError(f"ANN API Error {response.status}")
                return await response.text()

    async def get_reports(self, report_id: int = 155, type: str = "anime", nlist: Union[int, str] = 50, nskip: int = 0) -> List[ANNAnime]:
        """
        Fetch a list of titles from reports.
        Default report 155 is 'Anime' sorted by name.
        """
        await self._enforce_rate_limit()
        
        params = {
            "id": report_id,
            "type": type,
            "nlist": nlist,
            "nskip": nskip
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.REPORTS_URL, params=params) as response:
                if response.status != 200:
                    raise RuntimeError(f"ANN Reports Error {response.status}")
                content = await response.text()
                
        return self._parse_report(content)

    def _parse_report(self, xml_content: str) -> List[ANNAnime]:
        """Parse the XML report."""
        root = ET.fromstring(xml_content)
        results = []
        
        for item in root.findall(".//item"):
            try:
                anime = ANNAnime(
                    id=int(item.find("id").text),
                    gid=int(item.find("gid").text) if item.find("gid") is not None else None,
                    type=item.find("type").text,
                    name=item.find("name").text,
                    precision=item.find("precision").text
                )
                results.append(anime)
            except Exception as e:
                logger.warning(f"Failed to parse item: {e}")
                
        return results

# Example Usage
if __name__ == "__main__":
    async def main():
        client = ANNClient()
        
        print("Fetching report...")
        # Get first 5 anime
        anime_list = await client.get_reports(nlist=5)
        for a in anime_list:
            print(f"[{a.id}] {a.name} ({a.type})")
            
        if anime_list:
            print(f"\nFetching details for ID {anime_list[0].id}...")
            details = await client.get_details(anime_list[0].id)
            print(f"Details length: {len(details)} chars")

    asyncio.run(main())
