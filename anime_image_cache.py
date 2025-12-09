"""
Image Cache Manager for Anime Database
Downloads and caches anime cover images locally.
"""

import asyncio
import aiohttp
import hashlib
import logging
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("ImageCache")

class ImageCache:
    """Local image cache for anime covers"""
    
    def __init__(self, cache_dir: str = "anime_images"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def _get_cache_path(self, url: str, size: str = "normal") -> Path:
        """Generate cache filepath from URL"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return self.cache_dir / f"{url_hash}_{size}.jpg"
    
    def is_cached(self, url: str, size: str = "normal") -> bool:
        """Check if image is already cached"""
        return self._get_cache_path(url, size).exists()
    
    def get_cached_path(self, url: str, size: str = "normal") -> Optional[Path]:
        """Get path to cached image if it exists"""
        cache_path = self._get_cache_path(url, size)
        return cache_path if cache_path.exists() else None
    
    async def download_and_cache(self, url: str, size: str = "normal") -> Optional[Path]:
        """Download image and cache it locally"""
        if not url:
            return None
            
        # Check if already cached
        cache_path = self._get_cache_path(url, size)
        if cache_path.exists():
            return cache_path
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        with open(cache_path, 'wb') as f:
                            f.write(image_data)
                        logger.debug(f"✅ Cached: {url} -> {cache_path.name}")
                        return cache_path
                    else:
                        logger.warning(f"❌ Failed to download {url}: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"❌ Error downloading {url}: {e}")
            return None
    
    async def cache_batch(self, urls: list[str], max_concurrent: int = 5):
        """Download and cache multiple images concurrently"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def download_with_limit(url):
            async with semaphore:
                return await self.download_and_cache(url)
        
        tasks = [download_with_limit(url) for url in urls if url]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in results if isinstance(r, Path))
        logger.info(f"✅ Cached {success_count}/{len(urls)} images")
        return results
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        cached_files = list(self.cache_dir.glob("*.jpg"))
        total_size = sum(f.stat().st_size for f in cached_files)
        
        return {
            'total_images': len(cached_files),
            'total_size_mb': total_size / (1024 * 1024)
        }


async def cache_all_anime_images():
    """Download and cache images for all anime in database"""
    from anime_db import AnimeDatabase
    
    logger.info("\n=== 🖼️ CACHING ANIME IMAGES ===")
    
    db = AnimeDatabase()
    db.connect()
    
    # Get all anime with images
    cursor = db.conn.cursor()
    cursor.execute("""
        SELECT mal_id, title, image_url, image_large_url 
        FROM anime 
        WHERE image_url IS NOT NULL
    """)
    
    anime_list = cursor.fetchall()
    logger.info(f"   📊 Found {len(anime_list)} anime with images")
    
    cache = ImageCache()
    
    # Extract all image URLs
    normal_urls = [row['image_url'] for row in anime_list if row['image_url']]
    large_urls = [row['image_large_url'] for row in anime_list if row['image_large_url']]
    
    logger.info(f"   ⬇️ Downloading {len(normal_urls)} normal images...")
    await cache.cache_batch(normal_urls, max_concurrent=10)
    
    logger.info(f"   ⬇️ Downloading {len(large_urls)} large images...")
    await cache.cache_batch(large_urls, max_concurrent=10)
    
    stats = cache.get_stats()
    logger.info(f"\n=== ✨ CACHING COMPLETE ===")
    logger.info(f"   📁 Total Images: {stats['total_images']}")
    logger.info(f"   💾 Total Size: {stats['total_size_mb']:.2f} MB")
    
    db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "cache":
        # Cache all images
        asyncio.run(cache_all_anime_images())
    else:
        # Show stats
        cache = ImageCache()
        stats = cache.get_stats()
        print(f"Image Cache Stats:")
        print(f"  Total Images: {stats['total_images']}")
        print(f"  Total Size: {stats['total_size_mb']:.2f} MB")
