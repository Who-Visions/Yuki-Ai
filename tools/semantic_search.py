"""
Semantic Search Module for Yuki App
Uses Gemini Embeddings (gemini-embedding-001) for vector-based similarity search.
"""

import os
import json
import sqlite3
import hashlib
import numpy as np
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types

# Configuration
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSIONS = 768  # Good balance of quality vs storage
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "yuki_knowledge.db")

# GCP Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"

# Initialize Gemini client with Vertex AI
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)


def get_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
    """
    Generate embedding for a single text using Gemini Embeddings API.
    
    Args:
        text: The text to embed
        task_type: One of RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, SEMANTIC_SIMILARITY
    
    Returns:
        List of floats representing the embedding vector
    """
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=EMBEDDING_DIMENSIONS
        )
    )
    return result.embeddings[0].values


def get_query_embedding(query: str) -> List[float]:
    """Generate embedding optimized for search queries."""
    return get_embedding(query, task_type="RETRIEVAL_QUERY")


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def text_hash(text: str) -> str:
    """Generate SHA256 hash of text for cache invalidation."""
    return hashlib.sha256(text.encode()).hexdigest()


def init_embeddings_table(db_path: str = DB_PATH):
    """Create embeddings table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_type TEXT NOT NULL,
            entity_id INTEGER NOT NULL,
            text_hash TEXT NOT NULL,
            embedding TEXT NOT NULL,
            created_at INTEGER DEFAULT (strftime('%s', 'now')),
            UNIQUE(entity_type, entity_id)
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_type ON embeddings(entity_type)")
    conn.commit()
    conn.close()


def store_embedding(entity_type: str, entity_id: int, text: str, embedding: List[float], db_path: str = DB_PATH):
    """Store an embedding in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO embeddings (entity_type, entity_id, text_hash, embedding)
        VALUES (?, ?, ?, ?)
    """, (entity_type, entity_id, text_hash(text), json.dumps(embedding)))
    conn.commit()
    conn.close()


def get_all_embeddings(entity_type: str, db_path: str = DB_PATH) -> List[Dict]:
    """Get all embeddings of a given type."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT entity_id, embedding FROM embeddings WHERE entity_type = ?
    """, (entity_type,))
    results = []
    for row in cursor.fetchall():
        results.append({
            "entity_id": row[0],
            "embedding": json.loads(row[1])
        })
    conn.close()
    return results


def search_characters(query: str, top_k: int = 10, db_path: str = DB_PATH) -> List[Dict]:
    """
    Semantic search across characters.
    
    Returns list of {id, name, series, score} sorted by relevance.
    """
    query_embedding = get_query_embedding(query)
    embeddings = get_all_embeddings("character", db_path)
    
    if not embeddings:
        return []
    
    # Calculate similarities
    scored = []
    for emb in embeddings:
        score = cosine_similarity(query_embedding, emb["embedding"])
        scored.append({"entity_id": emb["entity_id"], "score": score})
    
    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)
    top_results = scored[:top_k]
    
    # Fetch character details
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    results = []
    for item in top_results:
        cursor.execute("""
            SELECT c.id, c.name_romaji, c.description, s.title_romaji
            FROM characters c
            LEFT JOIN series s ON c.series_id = s.id
            WHERE c.id = ?
        """, (item["entity_id"],))
        row = cursor.fetchone()
        if row:
            results.append({
                "id": row[0],
                "name": row[1],
                "description": row[2][:200] if row[2] else None,
                "series": row[3],
                "score": round(item["score"], 4),
                "type": "character"
            })
    
    conn.close()
    return results


def search_series(query: str, top_k: int = 5, db_path: str = DB_PATH) -> List[Dict]:
    """
    Semantic search across series/anime.
    
    Returns list of {id, title, description, score} sorted by relevance.
    """
    query_embedding = get_query_embedding(query)
    embeddings = get_all_embeddings("series", db_path)
    
    if not embeddings:
        return []
    
    # Calculate similarities
    scored = []
    for emb in embeddings:
        score = cosine_similarity(query_embedding, emb["embedding"])
        scored.append({"entity_id": emb["entity_id"], "score": score})
    
    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)
    top_results = scored[:top_k]
    
    # Fetch series details
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    results = []
    for item in top_results:
        cursor.execute("""
            SELECT id, title_romaji, title_english, description
            FROM series WHERE id = ?
        """, (item["entity_id"],))
        row = cursor.fetchone()
        if row:
            results.append({
                "id": row[0],
                "title": row[1],
                "title_english": row[2],
                "description": row[3][:200] if row[3] else None,
                "score": round(item["score"], 4),
                "type": "series"
            })
    
    conn.close()
    return results


def hybrid_search(
    query: str,
    include_characters: bool = True,
    include_series: bool = True,
    top_k: int = 10,
    min_score: float = 0.3,
    db_path: str = DB_PATH
) -> Dict[str, Any]:
    """
    Combined semantic search across characters and series.
    
    Args:
        query: Search query text
        include_characters: Search characters
        include_series: Search series
        top_k: Max results per category
        min_score: Minimum similarity threshold (0-1)
    
    Returns:
        Dict with characters, series, and total count
    """
    results = {
        "query": query,
        "characters": [],
        "series": [],
        "total": 0
    }
    
    if include_characters:
        chars = search_characters(query, top_k, db_path)
        results["characters"] = [c for c in chars if c["score"] >= min_score]
    
    if include_series:
        series = search_series(query, top_k, db_path)
        results["series"] = [s for s in series if s["score"] >= min_score]
    
    results["total"] = len(results["characters"]) + len(results["series"])
    
    return results


# Initialize on import
init_embeddings_table()
