import os
import json
import requests
import time
from pathlib import Path
from typing import List, Dict
from anime_database import AnimeDatabase, Anime, Character, AnimeRanking
from google import genai
from google.genai import types

class AnimeCharacterScraper:
    """
    Intelligent anime character scraper with rate limiting and storage
    """
    
    def __init__(self, db: AnimeDatabase):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.image_dir = Path("c:/Yuki_Local/character_images")
        self.image_dir.mkdir(exist_ok=True)
    
    def scrape_myanimelist_top(self, limit: int = 50):
        """Scrape top anime from MyAnimeList"""
        print(f"\n[📥 SCRAPING MAL] Fetching top {limit} anime...")
        
        # This is a simplified example - real implementation would use MAL API or BeautifulSoup
        # For now, we'll add the manually collected data from earlier
        
        top_anime_data = [
            {
                "title_english": "Frieren: Beyond Journey's End",
                "title_romaji": "Sousou no Frieren",
                "year": 2023,
                "type": "TV",
                "genres": ["Adventure", "Drama", "Fantasy"],
                "mal_rank": 1
            },
            {
                "title_english": "Fullmetal Alchemist: Brotherhood",
                "title_romaji": "Hagane no Renkinjutsushi",
                "year": 2009,
                "type": "TV",
                "genres": ["Action", "Adventure", "Drama", "Fantasy"],
                "mal_rank": 2
            },
            {
                "title_english": "Steins;Gate",
                "title_romaji": "Steins;Gate",
                "year": 2011,
                "type": "TV",
                "genres": ["Sci-Fi", "Thriller"],
                "mal_rank": 3
            },
            # Add more as needed
        ]
        
        for data in top_anime_data[:limit]:
            anime = Anime(
                id="",
                title_english=data["title_english"],
                title_romaji=data.get("title_romaji"),
                title_native=None,
                year=data.get("year"),
                type=data["type"],
                episodes=None,
                status="Finished",
                genres=data["genres"],
                studio=None,
                rankings=AnimeRanking(
                    myanimelist={"rank": data["mal_rank"]}
                ),
                character_ids=[]
            )
            self.db.add_anime(anime)
            print(f"  ✓ Added: {anime.title_english}")
        
        self.db.save()
        print(f"✅ Scraped {len(top_anime_data[:limit])} anime from MAL")
    
    def download_character_image(self, url: str, character_id: str) -> str:
        """Download character reference image"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                ext = url.split('.')[-1].split('?')[0]
                filename = f"{character_id}.{ext}"
                filepath = self.image_dir / filename
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"    📥 Downloaded image: {filename}")
                return str(filepath)
            else:
                print(f"    ⚠️ Failed to download: {url}")
                return None
        except Exception as e:
            print(f"    ❌ Error downloading {url}: {e}")
            return None
    
    def add_manual_character(self, anime_title: str, character_data: Dict):
        """Manually add a character with data"""
        anime = self.db.search_anime(anime_title)
        if not anime:
            print(f"⚠️ Anime '{anime_title}' not found in database")
            return
        
        character = Character(
            id="",
            name_full=character_data["name_full"],
            name_given=character_data.get("name_given", ""),
            name_family=character_data.get("name_family", ""),
            aliases=character_data.get("aliases", []),
            anime_id=anime.id,
            role=character_data.get("role", "Main"),
            gender=character_data.get("gender"),
            age=character_data.get("age"),
            hair_color=character_data.get("hair_color"),
            eye_color=character_data.get("eye_color")
        )
        
        char_id = self.db.add_character(character)
        
        # Download reference images if URLs provided
        if "image_urls" in character_data:
            for url in character_data["image_urls"]:
                image_path = self.download_character_image(url, char_id)
                if image_path:
                    character.reference_images.append(image_path)
        
        self.db.save()
        print(f"✅ Added character: {character.name_full}")
        return char_id

class TrainingDataOrganizer:
    """
    Organizes character images into Face Math training structure
    """
    
    def __init__(self, db: AnimeDatabase):
        self.db = db
        self.training_dir = Path("c:/Yuki_Local/training")
        self.training_dir.mkdir(exist_ok=True)
    
    def organize_character_for_training(self, character_id: str):
        """
        Organize a character's images into the training directory structure:
        training/
            character_name/
                image_1.png
                image_2.png
                ...
        """
        character = self.db.characters.get(character_id)
        if not character:
            print(f"⚠️ Character {character_id} not found")
            return
        
        # Create character directory
        char_dir = self.training_dir / character.name_full.replace(" ", "_")
        char_dir.mkdir(exist_ok=True)
        
        # Copy reference images to training directory
        for i, img_path in enumerate(character.reference_images):
            if os.path.exists(img_path):
                ext = Path(img_path).suffix
                dest = char_dir / f"ref_{i+1}{ext}"
                
                # Copy file
                import shutil
                shutil.copy2(img_path, dest)
                print(f"  ✓ Organized: {dest}")
        
        print(f"✅ Organized {len(character.reference_images)} images for {character.name_full}")
        return str(char_dir)
    
    def organize_all_characters(self):
        """Organize all characters in database for training"""
        print(f"\n[📁 ORGANIZING TRAINING DATA]")
        
        organized_count = 0
        for char_id in self.db.characters.keys():
            char_dir = self.organize_character_for_training(char_id)
            if char_dir:
                organized_count += 1
        
        print(f"\n✅ Organized {organized_count} characters for training")
        return organized_count
    
    def generate_training_manifest(self) -> str:
        """Generate a JSON manifest of all training data"""
        manifest = {
            "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_characters": 0,
            "characters": []
        }
        
        for character in self.db.characters.values():
            char_dir = self.training_dir / character.name_full.replace(" ", "_")
            if char_dir.exists():
                images = list(char_dir.glob("*.*"))
                manifest["characters"].append({
                    "id": character.id,
                    "name": character.name_full,
                    "anime": self.db.anime.get(character.anime_id).title_english if character.anime_id in self.db.anime else "Unknown",
                    "directory": str(char_dir),
                    "image_count": len(images),
                    "images": [str(img) for img in images]
                })
                manifest["total_characters"] += 1
        
        manifest_path = self.training_dir / "training_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"✅ Training manifest saved: {manifest_path}")
        return str(manifest_path)

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Initialize
    db = AnimeDatabase()
    scraper = AnimeCharacterScraper(db)
    organizer = TrainingDataOrganizer(db)
    
    # Scrape anime data
    scraper.scrape_myanimelist_top(limit=10)
    
    # Example: Add a character manually
    edward_data = {
        "name_full": "Edward Elric",
        "name_given": "Edward",
        "name_family": "Elric",
        "aliases": ["Fullmetal Alchemist", "Ed"],
        "role": "Main",
        "gender": "Male",
        "age": 15,
        "hair_color": "Blonde",
        "eye_color": "Gold",
        "image_urls": [
            # Add real URLs here when available
        ]
    }
    
    # scraper.add_manual_character("Fullmetal Alchemist: Brotherhood", edward_data)
    
    # Organize for training
    # organizer.organize_all_characters()
    # organizer.generate_training_manifest()
    
    print("\n✅ Scraper and Organizer ready!")
