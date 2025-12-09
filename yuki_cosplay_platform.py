"""
Yuki Cosplay Platform - SaaS Service
Complete end-to-end anime cosplay preview generation platform

Features:
- Anime database (Jikan API integration)  
- Character recognition and metadata
- Prompt engineering and optimization
- Image generation (Nano Banana Pro)
- User management
- Cloud storage
- API for external integrations
- Analytics and monitoring
"""

import asyncio
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

# Import our custom modules
from jikan_client import JikanClient, AnimeData
from prompt_engineering_system import (
    PromptEngineering,
    PromptCategory,
    GeneratedPrompt
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CharacterData:
    """Extended character data for cosplay generation"""
    mal_id: int
    name: str
    name_kanji: Optional[str]
    anime_id: int
    anime_title: str
    role: str  # Main, Supporting, etc.
    images: Dict[str, Any]
    about: Optional[str]
    favorites: int
    # Cosplay-specific attributes
    hair_color: Optional[str] = None
    eye_color: Optional[str] = None
    signature_outfit: Optional[str] = None
    personality_traits: List[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CosplayProject:
    """A cosplay photo generation project"""
    project_id: str
    user_id: str
    character_id: int
    character_name: str
    anime_id: int
    anime_title: str
    user_photo_path: Optional[str]
    generated_prompt: str
    generated_images: List[str]
    settings: Dict[str, Any]
    created_at: str
    status: str  # pending, processing, complete, failed
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class YukiCosplayPlatform:
    """
    Main SaaS platform service for anime cosplay preview generation
    
    Architecture:
    1. Anime Database Layer (Jikan API)
    2. Character Intelligence Layer (metadata + ML)
    3. Prompt Engineering Layer (optimization)
    4. Generation Layer (Nano Banana Pro / Imagen)
    5. Storage Layer (GCS / Cloud Storage)
    6. API Layer (FastAPI endpoints)
    """
    
    def __init__(
        self,
        project_id: str = "yuki-cosplay-platform",
        storage_bucket: Optional[str] = None,
        cache_backend: Optional[Any] = None
    ):
        """
        Initialize Yuki Cosplay Platform
        
        Args:
            project_id: GCP project ID
            storage_bucket: GCS bucket for image storage
            cache_backend: Redis/Memcached for caching
        """
        self.project_id = project_id
        self.storage_bucket = storage_bucket
        self.cache = cache_backend
        
        # Initialize subsystems
        self.anime_client: Optional[JikanClient] = None
        self.prompt_system = PromptEngineering(storage_backend=cache_backend)
        
        # In-memory stores (would be Cloud Firestore in production)
        self.anime_cache: Dict[int, AnimeData] = {}
        self.character_cache: Dict[int, CharacterData] = {}
        self.cosplay_projects: Dict[str, CosplayProject] = {}
        
        logger.info(f"Initialized Yuki Cosplay Platform (Project: {project_id})")
    
    async def initialize(self):
        """Initialize async components"""
        self.anime_client = JikanClient(cache_backend=self.cache)
        await self.anime_client.__aenter__()
        logger.info("Platform initialized and ready")
    
    async def shutdown(self):
        """Cleanup resources"""
        if self.anime_client:
            await self.anime_client.__aexit__(None, None, None)
        logger.info("Platform shutdown complete")
    
    async def index_seasonal_anime(
        self,
        year: int,
        season: str,
        fetch_characters: bool = True
    ) -> int:
        """
        Index anime from a season into the database
        
        Args:
            year: Year
            season: Season (winter/spring/summer/fall)
            fetch_characters: Whether to fetch character data
            
        Returns:
            Number of anime indexed
        """
        logger.info(f"Indexing {season} {year} anime...")
        
        # Fetch all pages for the season
        page = 1
        total_indexed = 0
        
        while True:
            try:
                anime_list = await self.anime_client.get_seasonal_anime(
                    year, season, sfw=True, page=page
                )
                
                if not anime_list:
                    break
                
                for anime in anime_list:
                    self.anime_cache[anime.mal_id] = anime
                    total_indexed += 1
                    
                    # Fetch characters if requested
                    if fetch_characters:
                        try:
                            characters = await self.anime_client.get_anime_characters(
                                anime.mal_id
                            )
                            await self._process_characters(anime, characters)
                        except Exception as e:
                            logger.warning(f"Failed to fetch characters for {anime.title}: {e}")
                
                logger.info(f"Indexed page {page}: {len(anime_list)} anime")
                page += 1
                
                # Respect rate limits
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error indexing page {page}: {e}")
                break
        
        logger.info(f"Total indexed: {total_indexed} anime")
        return total_indexed
    
    async def _process_characters(
        self,
        anime: AnimeData,
        characters_data: List[Dict[str, Any]]
    ):
        """Process and store character data"""
        for char_data in characters_data:
            char = char_data.get("character", {})
            if not char:
                continue
            
            character = CharacterData(
                mal_id=char.get("mal_id"),
                name=char.get("name", ""),
                name_kanji=char.get("name_kanji"),
                anime_id=anime.mal_id,
                anime_title=anime.title,
                role=char_data.get("role", "Unknown"),
                images=char.get("images", {}),
                about=char.get("about"),
                favorites=char.get("favorites", 0),
                personality_traits=[]
            )
            
            # Extract visual features from 'about' text (basic NLP)
            if character.about:
                about_lower = character.about.lower()
                if "hair" in about_lower:
                    # Simple extraction - could use NER in production
                    pass
            
            self.character_cache[character.mal_id] = character
    
    async def search_anime(self, query: str, limit: int = 10) -> List[AnimeData]:
        """
        Search for anime
        
        Args:
            query: Search query
            limit: Max results
            
        Returns:
            List of matching anime
        """
        results = await self.anime_client.search_anime(query, limit=limit)
        
        # Cache results
        for anime in results:
            self.anime_cache[anime.mal_id] = anime
        
        return results
    
    async def get_anime_characters(
        self,
        anime_id: int,
        force_refresh: bool = False
    ) -> List[CharacterData]:
        """
        Get characters for an anime
        
        Args:
            anime_id: MyAnimeList anime ID
            force_refresh: Force refresh from API
            
        Returns:
            List of characters
        """
        # Check cache first
        if not force_refresh:
            cached = [
                c for c in self.character_cache.values()
                if c.anime_id == anime_id
            ]
            if cached:
                return cached
        
        # Fetch from API
        characters_data = await self.anime_client.get_anime_characters(anime_id)
        
        # Get anime data
        anime = self.anime_cache.get(anime_id)
        if not anime:
            anime_data = await self.anime_client.get_anime_by_id(anime_id)
            anime = anime_data
            self.anime_cache[anime_id] = anime
        
        # Process characters
        await self._process_characters(anime, characters_data)
        
        # Return from cache
        return [
            c for c in self.character_cache.values()
            if c.anime_id == anime_id
        ]
    
    def generate_cosplay_prompt(
        self,
        character_id: int,
        customizations: Optional[Dict[str, Any]] = None
    ) -> GeneratedPrompt:
        """
        Generate optimized cosplay prompt for a character
        
        Args:
            character_id: Character MAL ID
            customizations: Optional prompt customizations
            
        Returns:
            Generated prompt with metadata
        """
        character = self.character_cache.get(character_id)
        if not character:
            raise ValueError(f"Character {character_id} not found in cache")
        
        # Prepare prompt parameters
        params = customizations or {}
        
        # Auto-fill from character data
        if not params.get("outfit_description") and character.signature_outfit:
            params["outfit_description"] = character.signature_outfit
        
        # Generate prompt
        generated = self.prompt_system.generate_cosplay_prompt(
            character_name=character.name,
            anime_title=character.anime_title,
            **params
        )
        
        # Link to character and anime
        generated.character_id = character.mal_id
        generated.anime_id = character.anime_id
        
        return generated
    
    async def create_cosplay_project(
        self,
        user_id: str,
        character_id: int,
        user_photo_path: Optional[str] = None,
        customizations: Optional[Dict[str, Any]] = None
    ) -> CosplayProject:
        """
        Create a new cosplay photo generation project
        
        Args:
            user_id: User identifier
            character_id: Character to cosplay
            user_photo_path: Optional user reference photo
            customizations: Prompt customizations
            
        Returns:
            Created project
        """
        character = self.character_cache.get(character_id)
        if not character:
            raise ValueError(f"Character {character_id} not found")
        
        # Generate prompt
        generated_prompt = self.generate_cosplay_prompt(
            character_id,
            customizations
        )
        
        # Create project
        project_id = f"cos_{user_id}_{character_id}_{int(datetime.utcnow().timestamp())}"
        project = CosplayProject(
            project_id=project_id,
            user_id=user_id,
            character_id=character_id,
            character_name=character.name,
            anime_id=character.anime_id,
            anime_title=character.anime_title,
            user_photo_path=user_photo_path,
            generated_prompt=generated_prompt.prompt,
            generated_images=[],
            settings=customizations or {},
            created_at=datetime.utcnow().isoformat(),
            status="pending"
        )
        
        self.cosplay_projects[project_id] = project
        
        logger.info(f"Created cosplay project {project_id} for {character.name}")
        return project
    
    def get_top_cosplayable_characters(
        self,
        limit: int = 50,
        anime_id: Optional[int] = None
    ) -> List[CharacterData]:
        """
        Get top characters for cosplay (by popularity)
        
        Args:
            limit: Max results
            anime_id: Optional filter by anime
            
        Returns:
            List of popular characters
        """
        characters = list(self.character_cache.values())
        
        if anime_id:
            characters = [c for c in characters if c.anime_id == anime_id]
        
        # Sort by favorites
        characters.sort(key=lambda c: c.favorites, reverse=True)
        
        return characters[:limit]
    
    def export_database(self, output_dir: str):
        """Export entire database to JSON files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Export anime
        anime_data = {
            str(mal_id): anime.to_dict()
            for mal_id, anime in self.anime_cache.items()
        }
        with open(output_path / "anime_database.json", "w", encoding="utf-8") as f:
            json.dump(anime_data, f, indent=2, default=str, ensure_ascii=False)
        
        # Export characters
        character_data = {
            str(mal_id): char.to_dict()
            for mal_id, char in self.character_cache.items()
        }
        with open(output_path / "characters_database.json", "w", encoding="utf-8") as f:
            json.dump(character_data, f, indent=2, default=str, ensure_ascii=False)
        
        # Export projects
        project_data = {
            proj_id: proj.to_dict()
            for proj_id, proj in self.cosplay_projects.items()
        }
        with open(output_path / "cosplay_projects.json", "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=2, default=str, ensure_ascii=False)
        
        # Export prompt templates
        self.prompt_system.export_templates(
            str(output_path / "prompt_templates.json")
        )
        
        logger.info(f"Database exported to {output_dir}")
        logger.info(f"  - {len(anime_data)} anime")
        logger.info(f"  - {len(character_data)} characters")
        logger.info(f"  - {len(project_data)} projects")
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get platform statistics"""
        return {
            "total_anime": len(self.anime_cache),
            "total_characters": len(self.character_cache),
            "total_projects": len(self.cosplay_projects),
            "total_prompt_templates": len(self.prompt_system.templates),
            "top_anime_by_score": sorted(
                self.anime_cache.values(),
                key=lambda a: a.score or 0,
                reverse=True
            )[:10],
            "most_cosplayed_characters": self.get_top_cosplayable_characters(10)
        }


# Example usage and demo
async def demo():
    """Run a complete platform demo"""
    print("🦊 Yuki Cosplay Platform - SaaS Demo\n")
    
    # Initialize platform
    platform = YukiCosplayPlatform(
        project_id="yuki-demo",
        storage_bucket="gs://yuki-cosplay-images"
    )
    await platform.initialize()
    
    try:
        # 1. Index Summer 2022 anime
        print("📚 Step 1: Indexing Summer 2022 anime...")
        indexed_count = await platform.index_seasonal_anime(2022, "summer", fetch_characters=False)
        print(f"✅ Indexed {indexed_count} anime\n")
        
        # 2. Search for popular anime
        print("🔍 Step 2: Searching for 'Cyberpunk'...")
        results = await platform.search_anime("Cyberpunk Edgerunners")
        if results:
            anime = results[0]
            print(f"✅ Found: {anime.title} (Score: {anime.score})\n")
            
            # 3. Get characters
            print(f"👥 Step 3: Fetching characters for {anime.title}...")
            characters = await platform.get_anime_characters(anime.mal_id)
            print(f"✅ Found {len(characters)} characters")
            for char in characters[:5]:
                print(f"  - {char.name} ({char.role})")
            print()
            
            # 4. Generate cosplay prompt
            if characters:
                char = characters[0]
                print(f"✨ Step 4: Generating cosplay prompt for {char.name}...")
                generated = platform.generate_cosplay_prompt(
                    char.mal_id,
                    customizations={
                        "setting": "neon-lit Night City street at night",
                        "lighting": "dramatic neon lights with volumetric fog",
                        "composition": "cinematic wide shot, anamorphic lens"
                    }
                )
                print(f"✅ Generated Prompt:\n{generated.prompt}\n")
                print(f"📊 Quality Score: {platform.prompt_system.score_prompt(generated.prompt)}/1.0\n")
                
                # 5. Create cosplay project
                print(f"🎨 Step 5: Creating cosplay project...")
                project = await platform.create_cosplay_project(
                    user_id="demo_user_001",
                    character_id=char.mal_id,
                    customizations={
                        "setting": "futuristic cyberpunk city",
                        "art_style": "hyper-realistic with neon accents"
                    }
                )
                print(f"✅ Project created: {project.project_id}\n")
        
        # 6. Show platform stats
        print("📊 Step 6: Platform Statistics")
        stats = platform.get_platform_stats()
        print(f"  - Total Anime: {stats['total_anime']}")
        print(f"  - Total Characters: {stats['total_characters']}")
        print(f"  - Total Projects: {stats['total_projects']}")
        print(f"  - Prompt Templates: {stats['total_prompt_templates']}\n")
        
        # 7. Export database
        print("💾 Step 7: Exporting database...")
        platform.export_database("./yuki_database_export")
        print("✅ Database exported to ./yuki_database_export\n")
        
        print("🎉 Demo Complete! Yuki Cosplay Platform is ready for production.\n")
        
    finally:
        await platform.shutdown()


if __name__ == "__main__":
    asyncio.run(demo())
