import os
import json
import datetime
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from google import genai
from google.genai import types

# ============================================================================
# DATABASE SCHEMA (Smart, Structured, Relational-Style)
# ============================================================================

@dataclass
class CharacterFaceSchema:
    """Face math schema for a character"""
    extracted: bool = False
    extraction_date: Optional[str] = None
    model_used: Optional[str] = None
    schema_data: Optional[Dict] = None
    reference_image_hashes: List[str] = None
    
    def __post_init__(self):
        if self.reference_image_hashes is None:
            self.reference_image_hashes = []

@dataclass
class CosplayGeneration:
    """Record of a cosplay generation"""
    generation_id: str
    timestamp: str
    model_used: str
    prompt: str
    output_path: str
    source_image_hash: str
    quality_score: Optional[float] = None

@dataclass
class Character:
    """Anime character entity"""
    id: str
    name_full: str
    name_given: str
    name_family: str
    aliases: List[str]
    anime_id: str
    role: str  # Main, Supporting, Background
    gender: Optional[str] = None
    age: Optional[int] = None
    hair_color: Optional[str] = None
    eye_color: Optional[str] = None
    popularity_rank: Optional[int] = None
    favorites_count: Optional[int] = None
    face_schema: Optional[CharacterFaceSchema] = None
    cosplay_generations: List[CosplayGeneration] = None
    reference_images: List[str] = None
    
    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []
        if self.cosplay_generations is None:
            self.cosplay_generations = []
        if self.reference_images is None:
            self.reference_images = []
        if self.face_schema is None:
            self.face_schema = CharacterFaceSchema()

@dataclass
class AnimeRanking:
    """Rankings from various sources"""
    myanimelist: Optional[Dict] = None
    animenewsnetwork: Optional[Dict] = None
    imdb: Optional[Dict] = None
    
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
    id: str
    title_english: str
    title_romaji: Optional[str]
    title_native: Optional[str]
    year: Optional[int]
    type: str  # TV, Movie, OVA, ONA
    episodes: Optional[int]
    status: str  # Airing, Finished, Upcoming
    genres: List[str]
    studio: Optional[str]
    rankings: Optional[AnimeRanking]
    character_ids: List[str]
    poster_url: Optional[str] = None
    
    def __post_init__(self):
        if self.genres is None:
            self.genres = []
        if self.character_ids is None:
            self.character_ids = []
        if self.rankings is None:
            self.rankings = AnimeRanking()

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
        if not anime.id:
            anime.id = self.generate_id(anime.title_english)
        self.anime[anime.id] = anime
        self._update_anime_indices(anime)
        return anime.id
    
    def add_character(self, character: Character) -> str:
        """Add character and update indices"""
        if not character.id:
            character.id = self.generate_id(f"{character.anime_id}_{character.name_full}")
        self.characters[character.id] = character
        self._update_character_indices(character)
        return character.id
    
    def _update_anime_indices(self, anime: Anime):
        """Update search indices for anime"""
        self.indices["anime_by_title"][anime.title_english.lower()] = anime.id
        if anime.title_romaji:
            self.indices["anime_by_title"][anime.title_romaji.lower()] = anime.id
    
    def _update_character_indices(self, character: Character):
        """Update search indices for character"""
        self.indices["characters_by_name"][character.name_full.lower()] = character.id
        if character.anime_id not in self.indices["characters_by_anime"]:
            self.indices["characters_by_anime"][character.anime_id] = []
        self.indices["characters_by_anime"][character.anime_id].append(character.id)
    
    def rebuild_indices(self):
        """Rebuild all search indices"""
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
    
    def _rebuild_top_ranked(self):
        """Rebuild top ranked anime list"""
        ranked = [(a.id, a.rankings.get_average_rank()) for a in self.anime.values() if a.rankings]
        ranked.sort(key=lambda x: x[1])
        self.indices["top_ranked_anime"] = [aid for aid, _ in ranked[:100]]
    
    def search_anime(self, title: str) -> Optional[Anime]:
        """Search for anime by title"""
        aid = self.indices["anime_by_title"].get(title.lower())
        return self.anime.get(aid) if aid else None
    
    def search_character(self, name: str) -> Optional[Character]:
        """Search for character by name"""
        cid = self.indices["characters_by_name"].get(name.lower())
        return self.characters.get(cid) if cid else None
    
    def get_characters_for_anime(self, anime_id: str) -> List[Character]:
        """Get all characters for an anime"""
        char_ids = self.indices["characters_by_anime"].get(anime_id, [])
        return [self.characters[cid] for cid in char_ids if cid in self.characters]
    
    def get_top_anime(self, limit: int = 50) -> List[Anime]:
        """Get top ranked anime"""
        return [self.anime[aid] for aid in self.indices["top_ranked_anime"][:limit]]
    
    def save(self):
        """Save database to JSON"""
        data = {
            "schema_version": "1.0",
            "last_updated": datetime.datetime.now().isoformat(),
            "anime": {aid: asdict(a) for aid, a in self.anime.items()},
            "characters": {cid: asdict(c) for cid, c in self.characters.items()},
            "indices": self.indices,
            "stats": {
                "total_anime": len(self.anime),
                "total_characters": len(self.characters),
                "characters_with_face_schemas": sum(1 for c in self.characters.values() if c.face_schema.extracted)
            }
        }
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Database saved to {self.db_path}")
    
    def load(self):
        """Load database from JSON"""
        if not self.db_path.exists():
            print("No existing database found. Starting fresh.")
            return
        
        with open(self.db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Load anime
        for aid, anime_dict in data.get("anime", {}).items():
            self.anime[aid] = Anime(**anime_dict)
        
        # Load characters
        for cid, char_dict in data.get("characters", {}).items():
            self.characters[cid] = Character(**char_dict)
        
        self.indices = data.get("indices", self.indices)
        print(f"Loaded database with {len(self.anime)} anime and {len(self.characters)} characters")

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    db = AnimeDatabase()
    
    # Add sample data
    fma = Anime(
        id="",
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
        ),
        character_ids=[]
    )
    
    anime_id = db.add_anime(fma)
    
    edward = Character(
        id="",
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
    print(f"Top anime: {db.get_top_anime(5)}")
