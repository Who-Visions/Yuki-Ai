"""
Anime Database - Refactored & Enhanced
Complete error handling, validation, and proper serialization
"""

import os
import json
import datetime
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def dataclass_to_dict(obj: Any) -> Any:
    """Recursively convert dataclass to dict"""
    if hasattr(obj, '__dataclass_fields__'):
        return {
            key: dataclass_to_dict(value)
            for key, value in obj.__dict__.items()
        }
    elif isinstance(obj, list):
        return [dataclass_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: dataclass_to_dict(value) for key, value in obj.items()}
    else:
        return obj

def dict_to_dataclass(cls, data: Dict) -> Any:
    """Recursively convert dict to dataclass"""
    if not isinstance(data, dict):
        return data
    
    field_types = {f.name: f.type for f in cls.__dataclass_fields__.values()}
    kwargs = {}
    
    for key, value in data.items():
        if key not in field_types:
            kwargs[key] = value
            continue
        
        field_type = field_types[key]
        
        # Handle Optional types
        if hasattr(field_type, '__origin__') and field_type.__origin__ is type(None) or type(Optional):
            if value is None:
                kwargs[key] = None
                continue
            # Get the actual type from Optional[Type]
            if hasattr(field_type, '__args__'):
                field_type = field_type.__args__[0] if field_type.__args__ else field_type
        
        # Handle nested dataclasses
        if hasattr(field_type, '__dataclass_fields__'):
            kwargs[key] = dict_to_dataclass(field_type, value)
        # Handle lists
        elif hasattr(field_type, '__origin__') and field_type.__origin__ is list:
            if isinstance(value, list) and value and hasattr(field_type.__args__[0], '__dataclass_fields__'):
                kwargs[key] = [dict_to_dataclass(field_type.__args__[0], item) for item in value]
            else:
                kwargs[key] = value
        else:
            kwargs[key] = value
    
    try:
        return cls(**kwargs)
    except Exception as e:
        print(f"Error creating {cls.__name__}: {e}")
        return None

# ============================================================================
# DATABASE SCHEMA
# ============================================================================

@dataclass
class CharacterFaceSchema:
    """Face math schema for a character"""
    extracted: bool = False
    extraction_date: Optional[str] = None
    model_used: Optional[str] = None
    schema_data: Optional[Dict[str, Any]] = None
    reference_image_hashes: List[str] = field(default_factory=list)

@dataclass
class CosplayGeneration:
    """Record of a cosplay generation"""
    generation_id: str = ""
    timestamp: str = ""
    model_used: str = ""
    prompt: str = ""
    output_path: str = ""
    source_image_hash: str = ""
    quality_score: Optional[float] = None

@dataclass
class Character:
    """Anime character entity"""
    id: str = ""
    name_full: str = ""
    name_given: str = ""
    name_family: str = ""
    anime_id: str = ""
    role: str = "Main"
    aliases: List[str] = field(default_factory=list)
    gender: Optional[str] = None
    age: Optional[int] = None
    hair_color: Optional[str] = None
    eye_color: Optional[str] = None
    popularity_rank: Optional[int] = None
    favorites_count: Optional[int] = None
    face_schema: CharacterFaceSchema = field(default_factory=CharacterFaceSchema)
    cosplay_generations: List[CosplayGeneration] = field(default_factory=list)
    reference_images: List[str] = field(default_factory=list)

@dataclass
class AnimeRanking:
    """Rankings from various sources"""
    myanimelist: Optional[Dict[str, Any]] = None
    animenewsnetwork: Optional[Dict[str, Any]] = None
    imdb: Optional[Dict[str, Any]] = None
    
    def get_average_rank(self) -> float:
        """Calculate weighted average rank"""
        ranks = []
        if self.myanimelist and 'rank' in self.myanimelist:
            ranks.append(self.myanimelist['rank'])
        if self.animenewsnetwork and 'rank' in self.animenewsnetwork:
            ranks.append(self.animenewsnetwork['rank'])
        if self.imdb and 'rank' in self.imdb:
            ranks.append(self.imdb['rank'])
        return sum(ranks) / len(ranks) if ranks else 999999

@dataclass
class Anime:
    """Anime series/movie entity"""
    id: str = ""
    title_english: str = ""
    type: str = "TV"
    status: str = "Unknown"
    title_romaji: Optional[str] = None
    title_native: Optional[str] = None
    year: Optional[int] = None
    episodes: Optional[int] = None
    genres: List[str] = field(default_factory=list)
    studio: Optional[str] = None
    rankings: AnimeRanking = field(default_factory=AnimeRanking)
    character_ids: List[str] = field(default_factory=list)
    poster_url: Optional[str] = None

# ============================================================================
# ANIME DATABASE
# ============================================================================

class AnimeDatabase:
    """
    Smart, structured anime database with indexing, search, and Face Math integration
    """
    
    def __init__(self, db_path: str = "c:/Yuki_Local/anime_database.json"):
        self.db_path = Path(db_path)
        self.anime: Dict[str, Anime] = {}
        self.characters: Dict[str, Character] = {}
        self.indices = {
            "anime_by_title": {},
            "characters_by_name": {},
            "characters_by_anime": {},
            "top_ranked_anime": []
        }
        self.load()
    
    def generate_id(self, text: str) -> str:
        """Generate a unique ID from text"""
        return hashlib.md5(text.encode()).hexdigest()[:12]
    
    def add_anime(self, anime: Anime) -> str:
        """Add anime and update indices"""
        try:
            if not anime.id:
                anime.id = self.generate_id(anime.title_english)
            self.anime[anime.id] = anime
            self._update_anime_indices(anime)
            return anime.id
        except Exception as e:
            print(f"Error adding anime: {e}")
            return ""
    
    def add_character(self, character: Character) -> str:
        """Add character and update indices"""
        try:
            if not character.id:
                character.id = self.generate_id(f"{character.anime_id}_{character.name_full}")
            self.characters[character.id] = character
            self._update_character_indices(character)
            return character.id
        except Exception as e:
            print(f"Error adding character: {e}")
            return ""
    
    def _update_anime_indices(self, anime: Anime):
        """Update search indices for anime"""
        try:
            self.indices["anime_by_title"][anime.title_english.lower()] = anime.id
            if anime.title_romaji:
                self.indices["anime_by_title"][anime.title_romaji.lower()] = anime.id
        except Exception as e:
            print(f"Error updating anime indices: {e}")
    
    def _update_character_indices(self, character: Character):
        """Update search indices for character"""
        try:
            self.indices["characters_by_name"][character.name_full.lower()] = character.id
            if character.anime_id not in self.indices["characters_by_anime"]:
                self.indices["characters_by_anime"][character.anime_id] = []
            if character.id not in self.indices["characters_by_anime"][character.anime_id]:
                self.indices["characters_by_anime"][character.anime_id].append(character.id)
        except Exception as e:
            print(f"Error updating character indices: {e}")
    
    def rebuild_indices(self):
        """Rebuild all search indices"""
        try:
            self.indices = {
                "anime_by_title": {},
                "characters_by_name": {},
                "characters_by_anime": {},
                "top_ranked_anime": []
            }
            for anime in self.anime.values():
                self._update_anime_indices(anime)
            for character in self.characters.values():
                self._update_character_indices(character)
            self._rebuild_top_ranked()
        except Exception as e:
            print(f"Error rebuilding indices: {e}")
    
    def _rebuild_top_ranked(self):
        """Rebuild top ranked anime list"""
        try:
            ranked = [(a.id, a.rankings.get_average_rank()) for a in self.anime.values() if a.rankings]
            ranked.sort(key=lambda x: x[1])
            self.indices["top_ranked_anime"] = [aid for aid, _ in ranked[:100]]
        except Exception as e:
            print(f"Error rebuilding top ranked: {e}")
    
    def search_anime(self, title: str) -> Optional[Anime]:
        """Search for anime by title"""
        try:
            aid = self.indices["anime_by_title"].get(title.lower())
            return self.anime.get(aid) if aid else None
        except Exception as e:
            print(f"Error searching anime: {e}")
            return None
    
    def search_character(self, name: str) -> Optional[Character]:
        """Search for character by name"""
        try:
            cid = self.indices["characters_by_name"].get(name.lower())
            return self.characters.get(cid) if cid else None
        except Exception as e:
            print(f"Error searching character: {e}")
            return None
    
    def get_characters_for_anime(self, anime_id: str) -> List[Character]:
        """Get all characters for an anime"""
        try:
            char_ids = self.indices["characters_by_anime"].get(anime_id, [])
            return [self.characters[cid] for cid in char_ids if cid in self.characters]
        except Exception as e:
            print(f"Error getting characters: {e}")
            return []
    
    def get_top_anime(self, limit: int = 50) -> List[Anime]:
        """Get top ranked anime"""
        try:
            return [self.anime[aid] for aid in self.indices["top_ranked_anime"][:limit] if aid in self.anime]
        except Exception as e:
            print(f"Error getting top anime: {e}")
            return []
    
    def save(self):
        """Save database to JSON"""
        try:
            data = {
                "schema_version": "1.0",
                "last_updated": datetime.datetime.now().isoformat(),
                "anime": {aid: dataclass_to_dict(a) for aid, a in self.anime.items()},
                "characters": {cid: dataclass_to_dict(c) for cid, c in self.characters.items()},
                "indices": self.indices,
                "stats": {
                    "total_anime": len(self.anime),
                    "total_characters": len(self.characters),
                    "characters_with_face_schemas": sum(1 for c in self.characters.values() if c.face_schema.extracted)
                }
            }
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Database saved to {self.db_path}")
        except Exception as e:
            print(f"❌ Error saving database: {e}")
    
    def load(self):
        """Load database from JSON"""
        try:
            if not self.db_path.exists():
                print("No existing database found. Starting fresh.")
                return
            
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load anime
            for aid, anime_dict in data.get("anime", {}).items():
                anime = dict_to_dataclass(Anime, anime_dict)
                if anime:
                    self.anime[aid] = anime
            
            # Load characters
            for cid, char_dict in data.get("characters", {}).items():
                char = dict_to_dataclass(Character, char_dict)
                if char:
                    self.characters[cid] = char
            
            self.indices = data.get("indices", self.indices)
            print(f"✓ Loaded database with {len(self.anime)} anime and {len(self.characters)} characters")
        except Exception as e:
            print(f"❌ Error loading database: {e}")

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    db = AnimeDatabase()
    
    # Add sample data
    fma = Anime(
        title_english="Fullmetal Alchemist: Brotherhood",
        title_romaji="Hagane no Renkinjutsushi: Fullmetal Alchemist",
        title_native="鋼の錬金術師 FULLMETAL ALCHEMIST",
        year=2009,
        type="TV",
        episodes=64,
        status="Finished",
        genres=["Action", "Adventure", "Drama", "Fantasy"],
        studio="Bones",
        rankings=AnimeRanking(
            myanimelist={"rank": 1, "score": 9.1, "popularity": 3}
        )
    )
    
    anime_id = db.add_anime(fma)
    
    edward = Character(
        name_full="Edward Elric",
        name_given="Edward",
        name_family="Elric",
        aliases=["Fullmetal Alchemist", "Ed"],
        anime_id=anime_id,
        role="Main",
        gender="Male",
        age=15,
        hair_color="Blonde",
        eye_color="Gold"
    )
    
    db.add_character(edward)
    db.save()
    
    print("\n✅ Sample database created successfully!")
