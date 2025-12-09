"""
Anime Database - Cloud-Native Version
Local-first with automatic GCS backup
"""

import os
import json
import datetime
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from google.cloud import storage

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ID = "gifted-cooler-479623-r7"
GCS_BUCKET_NAME = "yuki-anime-database"
GCS_BACKUP_PATH = "database/anime_database.json"

# ============================================================================
# HELPER FUNCTIONS (Same as before)
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
# DATABASE SCHEMA (Same as before)
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
# CLOUD-NATIVE ANIME DATABASE
# ============================================================================

class CloudAnimeDatabase:
    """
    Cloud-native anime database
    Local-first with automatic GCS backup
    """
    
    def __init__(
        self, 
        local_path: str = "c:/Yuki_Local/anime_database.json",
        enable_cloud_backup: bool = True,
        bucket_name: str = GCS_BUCKET_NAME
    ):
        self.local_path = Path(local_path)
        self.enable_cloud_backup = enable_cloud_backup
        self.bucket_name = bucket_name
        
        # Initialize GCS client if cloud backup enabled
        self.storage_client = None
        self.bucket = None
        if self.enable_cloud_backup:
            try:
                self.storage_client = storage.Client(project=PROJECT_ID)
                self.bucket = self.storage_client.bucket(bucket_name)
                print(f"☁️  Cloud backup enabled: gs://{bucket_name}")
            except Exception as e:
                print(f"⚠️  Cloud backup disabled: {e}")
                self.enable_cloud_backup = False
        
        # Database state
        self.anime: Dict[str, Anime] = {}
        self.characters: Dict[str, Character] = {}
        self.indices = {
            "anime_by_title": {},
            "characters_by_name": {},
            "characters_by_anime": {},
            "top_ranked_anime": []
        }
        
        # Load (preferably from cloud, fallback to local)
        self.load()
    
    def _ensure_bucket_exists(self):
        """Ensure GCS bucket exists, create if not"""
        if not self.enable_cloud_backup:
            return
        
        try:
            if not self.bucket.exists():
                print(f"Creating GCS bucket: {self.bucket_name}")
                self.bucket = self.storage_client.create_bucket(
                    self.bucket_name,
                    location="us-central1"
                )
                print(f"✓ Bucket created: gs://{self.bucket_name}")
        except Exception as e:
            print(f"⚠️  Could not create bucket: {e}")
    
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
    
    def save(self, cloud_backup: bool = True):
        """
        Save database (local-first, then cloud backup)
        """
        try:
            # Prepare data
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
                },
                "cloud_backup_enabled": self.enable_cloud_backup
            }
            
            # Save locally first (fast)
            with open(self.local_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved locally: {self.local_path}")
            
            # Backup to GCS (if enabled)
            if self.enable_cloud_backup and cloud_backup:
                self._upload_to_gcs(data)
            
        except Exception as e:
            print(f"❌ Error saving database: {e}")
    
    def _upload_to_gcs(self, data: Dict):
        """Upload database to GCS"""
        try:
            self._ensure_bucket_exists()
            
            blob = self.bucket.blob(GCS_BACKUP_PATH)
            blob.upload_from_string(
                json.dumps(data, indent=2, ensure_ascii=False),
                content_type='application/json'
            )
            print(f"☁️  Backed up to: gs://{self.bucket_name}/{GCS_BACKUP_PATH}")
        except Exception as e:
            print(f"⚠️  Cloud backup failed: {e}")
    
    def load(self):
        """
        Load database (cloud-first if available, fallback to local)
        """
        data = None
        
        # Try cloud first
        if self.enable_cloud_backup:
            data = self._load_from_gcs()
        
        # Fallback to local
        if not data:
            data = self._load_from_local()
        
        if not data:
            print("No existing database found. Starting fresh.")
            return
        
        # Parse data
        try:
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
            
            source = "cloud" if data.get("cloud_backup_enabled") else "local"
            print(f"✓ Loaded from {source}: {len(self.anime)} anime, {len(self.characters)} characters")
        except Exception as e:
            print(f"❌ Error loading database: {e}")
    
    def _load_from_gcs(self) -> Optional[Dict]:
        """Load database from GCS"""
        try:
            blob = self.bucket.blob(GCS_BACKUP_PATH)
            if blob.exists():
                data_str = blob.download_as_string()
                print(f"☁️  Loading from cloud: gs://{self.bucket_name}/{GCS_BACKUP_PATH}")
                return json.loads(data_str)
        except Exception as e:
            print(f"⚠️  Could not load from cloud: {e}")
        return None
    
    def _load_from_local(self) -> Optional[Dict]:
        """Load database from local file"""
        try:
            if self.local_path.exists():
                with open(self.local_path, 'r', encoding='utf-8') as f:
                    print(f"💾 Loading from local: {self.local_path}")
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load from local: {e}")
        return None
    
    def restore_from_cloud(self):
        """Force restore from cloud backup"""
        if not self.enable_cloud_backup:
            print("Cloud backup not enabled")
            return False
        
        data = self._load_from_gcs()
        if data:
            # Save to local
            with open(self.local_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Restored from cloud to {self.local_path}")
            return True
        return False

# For backwards compatibility
AnimeDatabase = CloudAnimeDatabase

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Initialize with cloud backup
    db = CloudAnimeDatabase(enable_cloud_backup=True)
    
    # Add sample data
    fma = Anime(
        title_english="Fullmetal Alchemist: Brotherhood",
        title_romaji="Hagane no Renkinjutsushi",
        year=2009,
        type="TV",
        status="Finished",
        genres=["Action", "Adventure"],
        rankings=AnimeRanking(
            myanimelist={"rank": 1, "score": 9.1}
        )
    )
    
    anime_id = db.add_anime(fma)
    
    edward = Character(
        name_full="Edward Elric",
        anime_id=anime_id,
        role="Main"
    )
    
    db.add_character(edward)
    
    # Save (automatically backs up to cloud)
    db.save()
    
    print("\n✅ Cloud-native database test complete!")
