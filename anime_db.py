"""
Anime Local Database - SQLite Cache Layer
Fast local access to 300+ top anime with incremental updates.
"""

import asyncio
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from jikan_client import JikanClient, AnimeData

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("AnimeDB")

class AnimeDatabase:
    """Local SQLite database for anime data"""
    
    def __init__(self, db_path: str = "anime_cache.db"):
        self.db_path = Path(db_path)
        self.conn = None
        
    def connect(self):
        """Connect and initialize database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            
    def _create_tables(self):
        """Create database schema"""
        cursor = self.conn.cursor()
        
        # Main anime table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anime (
                mal_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                title_english TEXT,
                title_japanese TEXT,
                type TEXT,
                source TEXT,
                episodes INTEGER,
                status TEXT,
                airing BOOLEAN,
                aired_from TEXT,
                aired_to TEXT,
                duration TEXT,
                rating TEXT,
                score REAL,
                scored_by INTEGER,
                rank INTEGER,
                popularity INTEGER,
                members INTEGER,
                favorites INTEGER,
                synopsis TEXT,
                background TEXT,
                season TEXT,
                year INTEGER,
                url TEXT,
                image_url TEXT,
                image_large_url TEXT,
                trailer_url TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Genres/Tags table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anime_genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mal_id INTEGER,
                genre_id INTEGER,
                genre_name TEXT,
                genre_type TEXT,
                FOREIGN KEY (mal_id) REFERENCES anime(mal_id)
            )
        """)
        
        # Studios table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anime_studios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mal_id INTEGER,
                studio_id INTEGER,
                studio_name TEXT,
                FOREIGN KEY (mal_id) REFERENCES anime(mal_id)
            )
        """)
        
        # Characters table (for future use)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anime_characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mal_id INTEGER,
                character_id INTEGER,
                character_name TEXT,
                role TEXT,
                image_url TEXT,
                FOREIGN KEY (mal_id) REFERENCES anime(mal_id)
            )
        """)
        
        # Create indexes for fast lookups
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON anime(title)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rank ON anime(rank)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_popularity ON anime(popularity)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_score ON anime(score)")
        
        self.conn.commit()
        logger.info("✅ Database schema initialized")
        
    def insert_anime(self, anime: AnimeData):
        """Insert or update anime data"""
        cursor = self.conn.cursor()
        
        # Extract image URLs
        image_url = anime.images.get('jpg', {}).get('image_url')
        image_large_url = anime.images.get('jpg', {}).get('large_image_url')
        trailer_url = anime.trailer.get('url') if anime.trailer else None
        
        cursor.execute("""
            INSERT OR REPLACE INTO anime (
                mal_id, title, title_english, title_japanese, type, source,
                episodes, status, airing, aired_from, aired_to, duration,
                rating, score, scored_by, rank, popularity, members, favorites,
                synopsis, background, season, year, url, image_url, image_large_url,
                trailer_url, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            anime.mal_id, anime.title, anime.title_english, anime.title_japanese,
            anime.type, anime.source, anime.episodes, anime.status, anime.airing,
            anime.aired_from, anime.aired_to, anime.duration, anime.rating,
            anime.score, anime.scored_by, anime.rank, anime.popularity,
            anime.members, anime.favorites, anime.synopsis, anime.background,
            anime.season, anime.year, anime.url, image_url, image_large_url, trailer_url
        ))
        
        # Insert genres
        cursor.execute("DELETE FROM anime_genres WHERE mal_id = ?", (anime.mal_id,))
        for genre in anime.genres:
            cursor.execute("""
                INSERT INTO anime_genres (mal_id, genre_id, genre_name, genre_type)
                VALUES (?, ?, ?, 'genre')
            """, (anime.mal_id, genre.get('mal_id'), genre.get('name')))
        
        for theme in anime.themes:
            cursor.execute("""
                INSERT INTO anime_genres (mal_id, genre_id, genre_name, genre_type)
                VALUES (?, ?, ?, 'theme')
            """, (anime.mal_id, theme.get('mal_id'), theme.get('name')))
        
        # Insert studios
        cursor.execute("DELETE FROM anime_studios WHERE mal_id = ?", (anime.mal_id,))
        for studio in anime.studios:
            cursor.execute("""
                INSERT INTO anime_studios (mal_id, studio_id, studio_name)
                VALUES (?, ?, ?)
            """, (anime.mal_id, studio.get('mal_id'), studio.get('name')))
        
        self.conn.commit()
        
    def get_anime_by_id(self, mal_id: int) -> Optional[Dict]:
        """Get anime by MAL ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM anime WHERE mal_id = ?", (mal_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def search_anime(self, query: str, limit: int = 25) -> List[Dict]:
        """Search anime by title"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM anime 
            WHERE title LIKE ? OR title_english LIKE ? OR title_japanese LIKE ?
            ORDER BY score DESC
            LIMIT ?
        """, (f'%{query}%', f'%{query}%', f'%{query}%', limit))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_top_anime(self, limit: int = 300) -> List[Dict]:
        """Get top anime by rank"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM anime 
            WHERE rank IS NOT NULL
            ORDER BY rank ASC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_popular_anime(self, limit: int = 100) -> List[Dict]:
        """Get most popular anime"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM anime 
            WHERE popularity IS NOT NULL
            ORDER BY popularity ASC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM anime")
        anime_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM anime WHERE airing = 1")
        airing_count = cursor.fetchone()['count']
        
        return {
            'total_anime': anime_count,
            'airing_anime': airing_count
        }


async def seed_database(target_count: int = 300):
    """
    Seed database with seasonal anime from recent years
    """
    logger.info(f"\n=== 📊 SEEDING ANIME DATABASE (Target: {target_count}) ===")
    
    db = AnimeDatabase()
    db.connect()
    
    async with JikanClient() as client:
        total_fetched = 0
        
        # Fetch from multiple recent seasons
        from datetime import datetime
        current_year = datetime.now().year
        seasons = ['winter', 'spring', 'summer', 'fall']
        
        # Go back 3 years
        for year in range(current_year, current_year - 3, -1):
            for season in seasons:
                if total_fetched >= target_count:
                    break
                    
                try:
                    logger.info(f"   📥 Fetching {season} {year}...")
                    
                    # Fetch multiple pages per season
                    for page in range(1, 5):  # Up to 4 pages per season
                        anime_list = await client.get_seasonal_anime(year, season, page=page)
                        
                        if not anime_list:
                            break
                        
                        for anime in anime_list:
                            try:
                                db.insert_anime(anime)
                                total_fetched += 1
                                
                                if total_fetched % 50 == 0:
                                    logger.info(f"   ✅ Inserted {total_fetched}/{target_count} anime...")
                                
                                if total_fetched >= target_count:
                                    break
                            except Exception as e:
                                logger.warning(f"   ⚠️ Failed to insert anime: {e}")
                        
                        if total_fetched >= target_count:
                            break
                        
                        # Small delay between pages
                        await asyncio.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"   ❌ Error fetching {season} {year}: {e}")
                
                if total_fetched >= target_count:
                    break
    
    stats = db.get_stats()
    logger.info(f"\n=== ✨ SEEDING COMPLETE ===")
    logger.info(f"   📊 Total Anime: {stats['total_anime']}")
    logger.info(f"   📡 Currently Airing: {stats['airing_anime']}")
    
    db.close()


async def update_database():
    """
    Incrementally update database with latest anime
    """
    logger.info("\n=== 🔄 UPDATING ANIME DATABASE ===")
    
    db = AnimeDatabase()
    db.connect()
    
    # Get current season anime (incremental update)
    now = datetime.now()
    current_year = now.year
    season_map = {1: 'winter', 4: 'spring', 7: 'summer', 10: 'fall'}
    current_season = season_map[((now.month - 1) // 3) * 3 + 1]
    
    async with JikanClient() as client:
        logger.info(f"   📅 Fetching {current_season} {current_year} anime...")
        anime_list = await client.get_seasonal_anime(current_year, current_season)
        
        new_count = 0
        updated_count = 0
        
        for anime in anime_list:
            existing = db.get_anime_by_id(anime.mal_id)
            if existing:
                updated_count += 1
            else:
                new_count += 1
            db.insert_anime(anime)
        
        logger.info(f"   ✅ New: {new_count}, Updated: {updated_count}")
    
    stats = db.get_stats()
    logger.info(f"   📊 Total Anime: {stats['total_anime']}")
    db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "seed":
        # Seed database
        asyncio.run(seed_database(300))
    elif len(sys.argv) > 1 and sys.argv[1] == "update":
        # Incremental update
        asyncio.run(update_database())
    else:
        # Demo: Show stats
        db = AnimeDatabase()
        db.connect()
        stats = db.get_stats()
        print(f"Database Stats: {stats}")
        
        # Show top 10
        top = db.get_top_anime(10)
        print(f"\nTop 10 Anime:")
        for anime in top:
            print(f"  {anime['rank']}. {anime['title']} (Score: {anime['score']})")
        
        db.close()
