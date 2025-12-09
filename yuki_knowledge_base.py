"""
Yuki Knowledge Base - RAG System with File Search
Intelligent character and cosplay knowledge retrieval

Features:
- Anime character database indexing
- Cosplay construction guides
- Prompt templates library
- Character reference materials
- Semantic search across all knowledge
"""

import asyncio
import logging
import time
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from enum import Enum

from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeCategory(Enum):
    """Knowledge base categories"""
    ANIME_CHARACTERS = "anime_characters"
    COSPLAY_GUIDES = "cosplay_guides"
    PROMPT_TEMPLATES = "prompt_templates"
    CHARACTER_REFERENCES = "character_references"
    COSTUME_CONSTRUCTION = "costume_construction"
    PHOTOGRAPHY_TECHNIQUES = "photography_techniques"


@dataclass
class KnowledgeDocument:
    """Single knowledge document"""
    doc_id: str
    title: str
    category: KnowledgeCategory
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    file_path: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class YukiKnowledgeBase:
    """
    RAG-powered knowledge base using Gemini File Search
    
    Features:
    - Semantic search across anime character data
    - Document chunking and embedding
    - Metadata filtering (character, anime, category)
    - Citation tracking
    - Free storage and query-time embeddings
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize knowledge base"""
        self.client = genai.Client(api_key=api_key)
        self.file_search_stores: Dict[str, Any] = {}
        self.document_index: Dict[str, KnowledgeDocument] = {}
        
        logger.info("Initialized Yuki Knowledge Base")
    
    def create_knowledge_store(
        self,
        store_name: str,
        category: KnowledgeCategory
    ) -> str:
        """
        Create a File Search store for a knowledge category
        
        Args:
            store_name: Display name for store
            category: Knowledge category
            
        Returns:
            Store name (resource ID)
        """
        logger.info(f"Creating File Search store: {store_name}")
        
        file_search_store = self.client.file_search_stores.create(
            config={'display_name': store_name}
        )
        
        self.file_search_stores[category.value] = {
            'name': file_search_store.name,
            'display_name': store_name,
            'category': category,
            'created_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Created store: {file_search_store.name}")
        return file_search_store.name
    
    async def index_character_data(
        self,
        character_data: Dict[str, Any],
        anime_data: Dict[str, Any],
        store_name: Optional[str] = None
    ) -> str:
        """
        Index anime character data into knowledge base
        
        Args:
            character_data: Character info from Jikan API
            anime_data: Anime info from Jikan API
            store_name: Optional specific store name
            
        Returns:
            Operation name
        """
        # Create document content
        content = self._format_character_document(character_data, anime_data)
        
        # Save to temp file
        doc_id = f"char_{character_data['mal_id']}"
        filepath = Path(f"./temp/{doc_id}.txt")
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Get or create character store
        if not store_name:
            category = KnowledgeCategory.ANIME_CHARACTERS
            if category.value not in self.file_search_stores:
                store_name = self.create_knowledge_store(
                    "Anime Characters Database",
                    category
                )
            else:
                store_name = self.file_search_stores[category.value]['name']
        
        # Upload and import
        logger.info(f"Indexing character: {character_data['name']}")
        
        operation = self.client.file_search_stores.upload_to_file_search_store(
            file=str(filepath),
            file_search_store_name=store_name,
            config={
                'display_name': f"{character_data['name']} ({anime_data['title']})",
                'chunking_config': {
                    'white_space_config': {
                        'max_tokens_per_chunk': 300,
                        'max_overlap_tokens': 50
                    }
                }
            },
            custom_metadata=[
                {"key": "character_name", "string_value": character_data['name']},
                {"key": "anime_title", "string_value": anime_data['title']},
                {"key": "mal_id", "numeric_value": character_data['mal_id']},
                {"key": "anime_id", "numeric_value": anime_data['mal_id']},
                {"key": "role", "string_value": character_data.get('role', 'Unknown')},
                {"key": "category", "string_value": "anime_character"}
            ]
        )
        
        # Wait for completion
        while not operation.done:
            await asyncio.sleep(2)
            operation = self.client.operations.get(operation)
        
        # Index document
        doc = KnowledgeDocument(
            doc_id=doc_id,
            title=f"{character_data['name']} from {anime_data['title']}",
            category=KnowledgeCategory.ANIME_CHARACTERS,
            content=content,
            metadata={
                'character_name': character_data['name'],
                'anime_title': anime_data['title'],
                'mal_id': character_data['mal_id'],
                'anime_id': anime_data['mal_id']
            },
            file_path=str(filepath)
        )
        
        self.document_index[doc_id] = doc
        
        logger.info(f"✅ Indexed: {character_data['name']}")
        return operation.name
    
    def _format_character_document(
        self,
        character: Dict[str, Any],
        anime: Dict[str, Any]
    ) -> str:
        """Format character data as searchable document"""
        doc = f"""
        CHARACTER PROFILE
        
        Name: {character['name']}
        Anime: {anime['title']}
        Role: {character.get('role', 'Unknown')}
        
        ANIME INFORMATION
        Title: {anime['title']}
        Genre: {', '.join([g.get('name', '') for g in anime.get('genres', [])])}
        Studios: {', '.join([s.get('name', '') for s in anime.get('studios', [])])}
        Score: {anime.get('score', 'N/A')}
        
        CHARACTER DESCRIPTION
        {character.get('about', 'No description available.')}
        
        VISUAL CHARACTERISTICS
        """
        
        # Add inferred visual details if available
        if 'about' in character and character['about']:
            about_text = character['about'].lower()
            
            # Simple keyword extraction
            if 'hair' in about_text:
                doc += "\n- Hair details mentioned in description"
            if 'eye' in about_text:
                doc += "\n- Eye details mentioned in description"
            if 'outfit' in about_text or 'costume' in about_text or 'wear' in about_text:
                doc += "\n- Costume details mentioned in description"
        
        doc += f"""
        
        POPULARITY
        Favorites: {character.get('favorites', 0)}
        
        COSPLAY SUITABILITY
        This character from {anime['title']} is a popular cosplay choice.
        The character's distinctive features and costume make them recognizable.
        
        SEARCH KEYWORDS
        {character['name']}, {anime['title']}, {character.get('role', '')}, 
        anime characters, cosplay ideas, {', '.join([g.get('name', '') for g in anime.get('genres', [])])}
        """
        
        return doc.strip()
    
    async def index_cosplay_guide(
        self,
        character_name: str,
        anime_title: str,
        guide_content: str,
        construction_notes: Optional[str] = None,
        materials_list: Optional[List[str]] = None,
        difficulty_level: str = "intermediate"
    ) -> str:
        """
        Index a cosplay construction guide
        
        Args:
            character_name: Character name
            anime_title: Source anime
            guide_content: Guide text
            construction_notes: Optional construction details
            materials_list: List of materials needed
            difficulty_level: easy/intermediate/advanced
            
        Returns:
            Operation name
        """
        # Format guide document
        content = f"""
        COSPLAY CONSTRUCTION GUIDE
        
        Character: {character_name}
        Anime: {anime_title}
        Difficulty: {difficulty_level}
        
        GUIDE CONTENT
        {guide_content}
        """
        
        if construction_notes:
            content += f"\n\nCONSTRUCTION NOTES\n{construction_notes}"
        
        if materials_list:
            content += f"\n\nMATERIALS LIST\n" + "\n".join(f"- {m}" for m in materials_list)
        
        # Save to file
        doc_id = f"guide_{character_name.replace(' ', '_').lower()}"
        filepath = Path(f"./temp/{doc_id}.txt")
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Get or create cosplay guides store
        category = KnowledgeCategory.COSPLAY_GUIDES
        if category.value not in self.file_search_stores:
            store_name = self.create_knowledge_store(
                "Cosplay Construction Guides",
                category
            )
        else:
            store_name = self.file_search_stores[category.value]['name']
        
        # Upload and import
        operation = self.client.file_search_stores.upload_to_file_search_store(
            file=str(filepath),
            file_search_store_name=store_name,
            config={
                'display_name': f"Cosplay Guide: {character_name}",
                'chunking_config': {
                    'white_space_config': {
                        'max_tokens_per_chunk': 400,
                        'max_overlap_tokens': 60
                    }
                }
            },
            custom_metadata=[
                {"key": "character_name", "string_value": character_name},
                {"key": "anime_title", "string_value": anime_title},
                {"key": "difficulty", "string_value": difficulty_level},
                {"key": "category", "string_value": "cosplay_guide"}
            ]
        )
        
        while not operation.done:
            await asyncio.sleep(2)
            operation = self.client.operations.get(operation)
        
        logger.info(f"✅ Indexed cosplay guide: {character_name}")
        return operation.name
    
    async def search_character_knowledge(
        self,
        query: str,
        character_filter: Optional[str] = None,
        anime_filter: Optional[str] = None,
        category_filter: Optional[KnowledgeCategory] = None
    ) -> Dict[str, Any]:
        """
        Search knowledge base with semantic understanding
        
        Args:
            query: Natural language query
            character_filter: Optional character name filter
            anime_filter: Optional anime title filter
            category_filter: Optional category filter
            
        Returns:
            Response with results and citations
        """
        # Determine which stores to search
        store_names = []
        
        if category_filter:
            if category_filter.value in self.file_search_stores:
                store_names.append(self.file_search_stores[category_filter.value]['name'])
        else:
            # Search all stores
            store_names = [s['name'] for s in self.file_search_stores.values()]
        
        if not store_names:
            return {"error": "No knowledge stores available"}
        
        # Build metadata filter
        metadata_filter = None
        if character_filter:
            metadata_filter = f"character_name={character_filter}"
        elif anime_filter:
            metadata_filter = f"anime_title={anime_filter}"
        
        # Configure File Search tool
        file_search_config = types.FileSearch(
            file_search_store_names=store_names
        )
        
        if metadata_filter:
            file_search_config.metadata_filter = metadata_filter
        
        # Query
        logger.info(f"Searching knowledge base: {query[:50]}...")
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(file_search=file_search_config)
                ]
            )
        )
        
        # Extract results with citations
        result = {
            "answer": response.text,
            "citations": [],
            "grounding_metadata": None
        }
        
        # Get citations
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if hasattr(candidate, 'grounding_metadata'):
                result["grounding_metadata"] = candidate.grounding_metadata
                
                # Extract citations
                if candidate.grounding_metadata and hasattr(candidate.grounding_metadata, 'grounding_chunks'):
                    for chunk in candidate.grounding_metadata.grounding_chunks:
                        result["citations"].append({
                            "source": getattr(chunk, 'document_name', 'Unknown'),
                            "content": getattr(chunk, 'text', '')[:200]
                        })
        
        return result
    
    async def get_character_cosplay_advice(
        self,
        character_name: str,
        anime_title: str
    ) -> str:
        """
        Get comprehensive cosplay advice for a character
        
        Args:
            character_name: Character to cosplay
            anime_title: Source anime
            
        Returns:
            Detailed advice with citations
        """
        query = f"""
        Provide comprehensive cosplay advice for {character_name} from {anime_title}.
        Include:
        1. Character visual characteristics (hair, eyes, distinctive features)
        2. Costume/outfit details
        3. Accessories and props needed
        4. Makeup and styling tips
        5. Pose and expression suggestions
        6. Difficulty level and construction tips if available
        """
        
        result = await self.search_character_knowledge(
            query=query,
            character_filter=character_name
        )
        
        return result["answer"]
    
    def list_stores(self) -> List[Dict[str, Any]]:
        """List all knowledge stores"""
        return list(self.file_search_stores.values())
    
    def export_index(self, filepath: str):
        """Export document index to JSON"""
        index_data = {
            doc_id: {
                "title": doc.title,
                "category": doc.category.value,
                "metadata": doc.metadata,
                "created_at": doc.created_at
            }
            for doc_id, doc in self.document_index.items()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)
        
        logger.info(f"Exported index: {len(index_data)} documents to {filepath}")


# Example usage
async def demo():
    """Demonstrate knowledge base capabilities"""
    print("🦊 Yuki Knowledge Base Demo\n")
    
    kb = YukiKnowledgeBase()
    
    # Create knowledge stores
    print("1. Creating knowledge stores...")
    kb.create_knowledge_store(
        "Anime Characters Database",
        KnowledgeCategory.ANIME_CHARACTERS
    )
    kb.create_knowledge_store(
        "Cosplay Construction Guides",
        KnowledgeCategory.COSPLAY_GUIDES
    )
    print(f"   ✅ Created {len(kb.file_search_stores)} stores\n")
    
    # Index sample character
    print("2. Indexing sample character...")
    sample_char = {
        "mal_id": 123456,
        "name": "Makima",
        "role": "Main",
        "about": "A mysterious woman with yellow ringed eyes and light red-pink hair. She wears a white shirt with black tie and dark suit. Known for her commanding presence and enigmatic smile."
    }
    sample_anime = {
        "mal_id": 44511,
        "title": "Chainsaw Man",
        "genres": [{"name": "Action"}, {"name": "Horror"}],
        "studios": [{"name": "MAPPA"}],
        "score": 8.62
    }
    
    await kb.index_character_data(sample_char, sample_anime)
    print("   ✅ Character indexed\n")
    
    # Index cosplay guide
    print("3. Indexing cosplay guide...")
    await kb.index_cosplay_guide(
        character_name="Makima",
        anime_title="Chainsaw Man",
        guide_content="""
        Makima cosplay requires attention to detail for her distinctive appearance.
        
        Hair: Long light red-pink hair, straight and flowing. Use a high-quality wig.
        Eyes: Yellow ringed eyes are the signature feature. Use colored contacts.
        Outfit: White dress shirt, black tie, dark suit pants, professional appearance.
        Accessories: Multiple earrings on right ear.
        Makeup: Subtle, professional look with emphasis on eyes.
        Expression: Mysterious, enigmatic smile. Practice in mirror.
        """,
        materials_list=[
            "Light pink/red wig (long, straight)",
            "Yellow ringed contact lenses",
            "White dress shirt",
            "Black slim tie",
            "Dark suit pants",
            "Black dress shoes",
            "Ear cuffs or earrings",
            "Professional makeup kit"
        ],
        difficulty_level="intermediate"
    )
    print("   ✅ Guide indexed\n")
    
    # Search knowledge base
    print("4. Searching knowledge base...")
    result = await kb.search_character_knowledge(
        query="What are the key visual features for cosplaying Makima?"
    )
    print(f"   Answer: {result['answer'][:200]}...")
    print(f"   Citations: {len(result['citations'])} sources\n")
    
    # Get comprehensive advice
    print("5. Getting comprehensive cosplay advice...")
    advice = await kb.get_character_cosplay_advice("Makima", "Chainsaw Man")
    print(f"   {advice[:300]}...\n")
    
    # Export index
    print("6. Exporting document index...")
    kb.export_index("knowledge_index.json")
    print("   ✅ Index exported\n")
    
    print("🎉 Knowledge Base demo complete!")


if __name__ == "__main__":
    asyncio.run(demo())
