"""
Yuki Knowledge Graph Populator
Fetches data from APIs and populates the local SQLite database.
Demonstrates "Enhanced" character breakdown logic.
"""

import asyncio
import logging
from sqlalchemy.orm import sessionmaker
from schema import init_db, Series, Character, AppearanceVariant, GenderEnum, RoleEnum
import sys
import os
# Add parent dir to path to find anilist_client
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from anilist_client import AniListClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YukiPopulator:
    def __init__(self):
        self.engine = init_db()
        self.Session = sessionmaker(bind=self.engine)
        self.anilist = AniListClient()

    async def populate_series_by_name(self, name: str):
        """Fetch series and main characters, then populate DB."""
        session = self.Session()
        try:
            # 1. Fetch Series Data
            logger.info(f"Searching for '{name}'...")
            search_res = await self.anilist.search_anime(name, limit=1)
            if not search_res or not search_res.get("Page", {}).get("media"):
                logger.error("Series not found.")
                return

            anime_data = search_res["Page"]["media"][0]
            anime_id = anime_data["id"]
            
            # Check if exists
            existing = session.query(Series).filter_by(anilist_id=anime_id).first()
            if existing:
                logger.info(f"Series '{existing.title_english}' already exists.")
                series = existing
            else:
                # Create Series
                series = Series(
                    title_romaji=anime_data["title"]["romaji"],
                    title_english=anime_data["title"]["english"] or anime_data["title"]["romaji"],
                    title_native=anime_data["title"]["native"],
                    description=anime_data["description"],
                    format="TV", # Simplified for demo
                    anilist_id=anime_id
                )
                session.add(series)
                session.commit()
                logger.info(f"Added series: {series.title_english}")

            # 2. Fetch Detailed Info (including characters)
            # Note: The basic client search didn't fetch characters. 
            # We need a more complex query or just use the ID to fetch characters now.
            # For this demo, I'll implement a character fetch method inside this script 
            # or extend the client. I'll extend the client logic here ad-hoc for speed.
            
            logger.info(f"Fetching characters for series ID {anime_id}...")
            # Custom query to get characters
            char_query = """
            query ($id: Int) {
              Media(id: $id) {
                characters(sort: ROLE, perPage: 5) {
                  edges {
                    role
                    node {
                      id
                      name {
                        full
                        native
                      }
                      gender
                      description
                      image {
                        large
                      }
                    }
                  }
                }
              }
            }
            """
            char_data = await self.anilist._query(char_query, {"id": anime_id})
            if not char_data:
                return

            characters = char_data["Media"]["characters"]["edges"]
            
            for char_edge in characters:
                c_node = char_edge["node"]
                role_str = char_edge["role"]
                
                # Check existence
                existing_char = session.query(Character).filter_by(anilist_id=c_node["id"]).first()
                if existing_char:
                    continue
                
                # Parse Gender
                gender_map = {"Female": GenderEnum.FEMALE, "Male": GenderEnum.MALE}
                gender_enum = gender_map.get(c_node["gender"], GenderEnum.UNKNOWN)
                
                # Parse Role
                role_enum = RoleEnum.MAIN if role_str == "MAIN" else RoleEnum.SUPPORTING

                # Create Character
                new_char = Character(
                    series_id=series.id,
                    name_romaji=c_node["name"]["full"],
                    name_native=c_node["name"]["native"],
                    gender=gender_enum,
                    description=c_node["description"],
                    role=role_enum,
                    anilist_id=c_node["id"]
                )
                session.add(new_char)
                session.commit() # Commit to get ID
                
                # 3. Create Default Appearance Variant (The "Enhancement")
                # In a real system, we'd use NLP or Vision AI to extract this.
                # Here, we'll use heuristics based on the name for demonstration.
                
                variant = AppearanceVariant(
                    character_id=new_char.id,
                    name="Default",
                    is_default=True,
                    prompt_tags=f"solo, {new_char.name_romaji}, anime style"
                )
                
                # Manual "Enhancement" for Frieren (Demo)
                if "Frieren" in new_char.name_romaji:
                    variant.hair_color = "Silver"
                    variant.hair_style = "Twin-tails"
                    variant.eye_color = "Green"
                    variant.outfit_structure = {
                        "upper": ["white capelet", "black collar", "striped shirt"],
                        "lower": ["white skirt"],
                        "accessories": ["red earrings", "staff"]
                    }
                    variant.prompt_tags += ", white capelet, striped shirt, twin tails, holding staff"
                
                elif "Fern" in new_char.name_romaji:
                    variant.hair_color = "Purple"
                    variant.hair_style = "Long straight"
                    variant.eye_color = "Purple"
                    variant.outfit_structure = {
                        "upper": ["white robe", "black coat"],
                    }
                    variant.prompt_tags += ", long purple hair, white robe"

                session.add(variant)
                logger.info(f"Added character: {new_char.name_romaji} with Default variant.")
            
            session.commit()
            logger.info("Population complete.")

        except Exception as e:
            logger.error(f"Population failed: {e}")
            session.rollback()
        finally:
            session.close()

if __name__ == "__main__":
    populator = YukiPopulator()
    asyncio.run(populator.populate_series_by_name("Frieren"))
