"""
Instant Anime Database Seeder
Seeds database from static JSON for instant startup (no API calls needed)
"""

import json
import logging
from pathlib import Path
from anime_db import AnimeDatabase

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("InstantSeed")

def seed_from_json(json_path: str = "anime_seed_data.json"):
    """Seed database from static JSON file"""
    logger.info("\n=== ⚡ INSTANT DATABASE SEED ===")
    
    # Load JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        anime_data = json.load(f)
    
    logger.info(f"   📦 Loaded {len(anime_data)} anime from {json_path}")
    
    # Connect to database
    db = AnimeDatabase()
    db.connect()
    
    # Quick insert (minimal data for now)
    cursor = db.conn.cursor()
    
    inserted = 0
    for anime in anime_data:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO anime (
                    mal_id, title, score, rank, popularity, year, type, episodes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                anime.get('mal_id'),
                anime.get('title'),
                anime.get('score'),
                anime.get('rank'),
                anime.get('popularity'),
                anime.get('year'),
                anime.get('type'),
                anime.get('episodes')
            ))
            inserted += 1
        except Exception as e:
            logger.warning(f"   ⚠️ Failed to insert {anime.get('title')}: {e}")
    
    db.conn.commit()
    
    stats = db.get_stats()
    logger.info(f"\n=== ✨ SEED COMPLETE ===")
    logger.info(f"   ✅ Inserted: {inserted}/{len(anime_data)}")
    logger.info(f"   📊 Total in DB: {stats['total_anime']}")
    
    # Show top 10
    top = db.get_top_anime(10)
    logger.info(f"\n   🏆 Top 10 Anime:")
    for anime in top:
        logger.info(f"      {anime['rank']}. {anime['title']} (Score: {anime['score']})")
    
    db.close()
    logger.info(f"\n   🚀 Database ready for instant queries!")

if __name__ == "__main__":
    seed_from_json()
