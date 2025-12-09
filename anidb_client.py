"""
AniDB API Client & Title Parser
Handles downloading and parsing the AniDB Anime Titles Dump.
Reference: https://wiki.anidb.net/w/API

Features:
- Automatic download and decompression of animetitles.xml.gz
- Efficient XML parsing to extract titles by language and type
- Local caching to avoid repeated large downloads
"""

import gzip
import xml.etree.ElementTree as ET
import aiohttp
import asyncio
import logging
import os
import time
from pathlib import Path
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AniDBTitle:
    aid: int
    titles: Dict[str, str]  # type -> title (e.g., 'main': 'Title', 'official_en': 'Title')
    primary_title: str

class AniDBClient:
    DUMP_URL = "http://anidb.net/api/anime-titles.xml.gz"
    CACHE_FILE = Path("c:/Yuki_Local/cache/animetitles.xml")
    
    def __init__(self):
        self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        self._titles_cache: Dict[int, AniDBTitle] = {}

    async def download_titles_dump(self, force: bool = False):
        """
        Download and decompress the AniDB titles dump.
        Enforces 24-hour cache validity to respect API rules.
        """
        if self.CACHE_FILE.exists() and not force:
            # Check file age
            mtime = self.CACHE_FILE.stat().st_mtime
            age_hours = (time.time() - mtime) / 3600
            
            if age_hours < 24:
                logger.info(f"Using cached AniDB dump ({age_hours:.1f}h old).")
                return
            else:
                logger.info(f"Cache expired ({age_hours:.1f}h old). Downloading new dump...")

        logger.info(f"Downloading AniDB dump from {self.DUMP_URL}...")
        
        headers = {
            "User-Agent": "YukiClient/1.0 (http://yuki.local; yuki@localhost)",
            "Accept-Encoding": "gzip"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.DUMP_URL, headers=headers) as response:
                if response.status != 200:
                    raise RuntimeError(f"Failed to download AniDB dump: {response.status}")
                
                content = await response.read()
                
                # Decompress if gzipped (AniDB usually sends gzip)
                try:
                    xml_content = gzip.decompress(content)
                except gzip.BadGzipFile:
                    # Fallback if it's already decompressed
                    xml_content = content
                
                # Save to cache
                self.CACHE_FILE.write_bytes(xml_content)
                logger.info(f"Saved AniDB dump to {self.CACHE_FILE}")

    def parse_titles(self) -> List[AniDBTitle]:
        """Parse the locally cached XML file."""
        if not self.CACHE_FILE.exists():
            raise FileNotFoundError("AniDB dump not found. Call download_titles_dump() first.")

        logger.info("Parsing AniDB XML...")
        tree = ET.parse(self.CACHE_FILE)
        root = tree.getroot()
        
        results = []
        # XML Namespace handling usually not needed for simple parsing if we ignore xmlns
        # Structure: <anime aid="1"> <title type="main" xml:lang="x-jat">...</title> ... </anime>
        
        for anime in root.findall('anime'):
            aid = int(anime.get('aid'))
            titles_map = {}
            primary = "Unknown"
            
            for title in anime.findall('title'):
                t_type = title.get('type')
                lang = title.get('{http://www.w3.org/XML/1998/namespace}lang') # Handle xml:lang
                text = title.text
                
                key = f"{t_type}_{lang}" if lang else t_type
                titles_map[key] = text
                
                # Determine primary title for display
                if t_type == 'main':
                    primary = text
                elif t_type == 'official' and lang == 'en' and primary == "Unknown":
                    primary = text
            
            # Fallback for primary if main not found (rare)
            if primary == "Unknown" and titles_map:
                primary = list(titles_map.values())[0]

            obj = AniDBTitle(aid=aid, titles=titles_map, primary_title=primary)
            results.append(obj)
            self._titles_cache[aid] = obj
            
        logger.info(f"Parsed {len(results)} anime titles.")
        return results

    async def search_anime(self, query: str, limit: int = 10) -> List[AniDBTitle]:
        """Search for anime by title (case-insensitive substring)."""
        if not self._titles_cache:
            await self.download_titles_dump()
            self.parse_titles()
            
        query = query.lower()
        matches = []
        
        for anime in self._titles_cache.values():
            # Search across all titles for this anime
            if any(query in t.lower() for t in anime.titles.values()):
                matches.append(anime)
                if len(matches) >= limit:
                    break
        
        return matches

    async def get_random_anime(self, count: int = 5) -> List[AniDBTitle]:
        """Get random anime titles (useful for stress testing)."""
        if not self._titles_cache:
            await self.download_titles_dump()
            self.parse_titles()
            
        import random
        return random.sample(list(self._titles_cache.values()), min(count, len(self._titles_cache)))

# Example Usage
if __name__ == "__main__":
    async def main():
        client = AniDBClient()
        await client.download_titles_dump()
        
        # Parse
        titles = client.parse_titles()
        print(f"Total Anime: {len(titles)}")
        
        # Search Example
        print("\nSearching for 'Crest of the Stars'...")
        results = await client.search_anime("Crest of the Stars")
        for res in results:
            print(f"[{res.aid}] {res.primary_title}")
            
    asyncio.run(main())
