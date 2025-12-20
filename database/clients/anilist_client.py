"""
AniList GraphQL Client
Handles data retrieval from AniList API.
Reference: https://github.com/AniList/docs

Features:
- GraphQL query support
- Search anime by name
- Get anime details by ID
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AniListClient:
    URL = "https://graphql.anilist.co"

    async def _query(self, query: str, variables: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.URL, json={"query": query, "variables": variables}) as response:
                if response.status != 200:
                    logger.error(f"AniList API Error {response.status}: {await response.text()}")
                    return None
                
                data = await response.json()
                if "errors" in data:
                    logger.error(f"AniList GraphQL Errors: {data['errors']}")
                    return None
                    
                return data.get("data")

    async def search_anime(self, search: str, limit: int = 5) -> Optional[Dict[str, Any]]:
        query = """
        query ($search: String, $perPage: Int) {
          Page(perPage: $perPage) {
            media(search: $search, type: ANIME) {
              id
              title {
                romaji
                english
                native
              }
              description
              averageScore
              episodes
              coverImage {
                large
              }
            }
          }
        }
        """
        variables = {"search": search, "perPage": limit}
        return await self._query(query, variables)

    async def get_anime_details(self, id: int) -> Optional[Dict[str, Any]]:
        query = """
        query ($id: Int) {
          Media(id: $id, type: ANIME) {
            id
            title {
              romaji
              english
              native
            }
            description
            averageScore
            episodes
            genres
            studios {
              nodes {
                name
              }
            }
            coverImage {
              extraLarge
            }
          }
        }
        """
        variables = {"id": id}
        return await self._query(query, variables)

# Example Usage
if __name__ == "__main__":
    async def main():
        client = AniListClient()
        print("🔍 Searching for 'Frieren' on AniList...")
        results = await client.search_anime("Frieren")
        
        if results and results.get("Page", {}).get("media"):
            first_anime = results["Page"]["media"][0]
            print(f"Found: {first_anime['title']['english'] or first_anime['title']['romaji']} (ID: {first_anime['id']})")
            print(f"Score: {first_anime['averageScore']}")
            
            print(f"\nFetching details for ID {first_anime['id']}...")
            details = await client.get_anime_details(first_anime['id'])
            if details:
                media = details["Media"]
                print(f"Genres: {', '.join(media['genres'])}")
                studios = [s['name'] for s in media['studios']['nodes']]
                print(f"Studios: {', '.join(studios)}")

    asyncio.run(main())
