import aiohttp
import asyncio
import os
import secrets

class MalClient:
    def __init__(self, client_id="7415359fb0ede6384820441249f5a109"):
        self.client_id = client_id
        self.base_url = "https://api.myanimelist.net/v2"

    async def get_character_image(self, character_name):
        """
        Searches for a character and returns their main image URL (high res if possible).
        """
        headers = {
            "X-MAL-CLIENT-ID": self.client_id,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        params = {
            "q": character_name,
            "limit": 1
        }
        
        url = f"{self.base_url}/characters"
        
        async with aiohttp.ClientSession() as session:
            try:
                print(f"   🔎 MAL API: Searching for '{character_name}'...")
                async with session.get(url, headers=headers, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("data"):
                            node = data["data"][0]["node"]
                            images = node.get("main_picture", {})
                            # Prefer large, then medium
                            image_url = images.get("large") or images.get("medium")
                            if image_url:
                                print(f"   ✅ Found Image: {image_url}")
                                return image_url
            except Exception as e:
                print(f"   ❌ MAL API Error: {e}")
        
        return None

# Simple test if run directly
if __name__ == "__main__":
    async def test():
        client = MalClient()
        await client.get_character_image("Rock Lee")
    asyncio.run(test())
