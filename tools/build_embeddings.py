"""
Build Embeddings Script
Pre-computes and stores embeddings for all characters and series in the database.
Run this once to index, or periodically to update.
"""

import os
import sys
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from semantic_search import (
    get_embedding,
    store_embedding,
    init_embeddings_table,
    DB_PATH
)

# ANSI colors
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RED = "\033[91m"
    RESET = "\033[0m"


def build_character_embeddings(db_path: str = DB_PATH, dry_run: bool = False):
    """Generate and store embeddings for all characters."""
    print(f"\n{Colors.CYAN}📦 Building Character Embeddings...{Colors.RESET}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.id, c.name_romaji, c.description, c.base_prompt, s.title_romaji
        FROM characters c
        LEFT JOIN series s ON c.series_id = s.id
    """)
    
    characters = cursor.fetchall()
    conn.close()
    
    print(f"   Found {len(characters)} characters")
    
    indexed = 0
    for char_id, name, description, base_prompt, series in characters:
        # Build text to embed (combine all text fields)
        text_parts = [name]
        if series:
            text_parts.append(f"from {series}")
        if description:
            text_parts.append(description[:500])  # Limit to 500 chars
        if base_prompt:
            text_parts.append(base_prompt[:300])
        
        embed_text = " | ".join(text_parts)
        
        if dry_run:
            print(f"   [DRY RUN] Would embed: {name} ({len(embed_text)} chars)")
        else:
            try:
                embedding = get_embedding(embed_text)
                store_embedding("character", char_id, embed_text, embedding, db_path)
                indexed += 1
                print(f"   {Colors.GREEN}✓{Colors.RESET} {name}")
            except Exception as e:
                print(f"   {Colors.RED}✗{Colors.RESET} {name}: {e}")
    
    print(f"\n   {Colors.GREEN}Indexed {indexed}/{len(characters)} characters{Colors.RESET}")
    return indexed


def build_series_embeddings(db_path: str = DB_PATH, dry_run: bool = False):
    """Generate and store embeddings for all series."""
    print(f"\n{Colors.CYAN}📦 Building Series Embeddings...{Colors.RESET}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title_romaji, title_english, description
        FROM series
    """)
    
    series_list = cursor.fetchall()
    conn.close()
    
    print(f"   Found {len(series_list)} series")
    
    indexed = 0
    for series_id, title_romaji, title_english, description in series_list:
        # Build text to embed
        text_parts = [title_romaji]
        if title_english and title_english != title_romaji:
            text_parts.append(f"({title_english})")
        if description:
            text_parts.append(description[:800])
        
        embed_text = " | ".join(text_parts)
        
        if dry_run:
            print(f"   [DRY RUN] Would embed: {title_romaji} ({len(embed_text)} chars)")
        else:
            try:
                embedding = get_embedding(embed_text)
                store_embedding("series", series_id, embed_text, embedding, db_path)
                indexed += 1
                print(f"   {Colors.GREEN}✓{Colors.RESET} {title_romaji}")
            except Exception as e:
                print(f"   {Colors.RED}✗{Colors.RESET} {title_romaji}: {e}")
    
    print(f"\n   {Colors.GREEN}Indexed {indexed}/{len(series_list)} series{Colors.RESET}")
    return indexed


def main():
    parser = argparse.ArgumentParser(description="Build embeddings for Yuki semantic search")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be indexed without calling API")
    parser.add_argument("--characters-only", action="store_true", help="Only index characters")
    parser.add_argument("--series-only", action="store_true", help="Only index series")
    parser.add_argument("--db", default=DB_PATH, help="Path to database")
    args = parser.parse_args()
    
    print(f"\n{Colors.YELLOW}🦊 Yuki Semantic Search - Embedding Builder{Colors.RESET}")
    print(f"   Database: {args.db}")
    
    if args.dry_run:
        print(f"   {Colors.YELLOW}Mode: DRY RUN (no API calls){Colors.RESET}")
    
    # Ensure table exists
    init_embeddings_table(args.db)
    
    char_count = 0
    series_count = 0
    
    if not args.series_only:
        char_count = build_character_embeddings(args.db, args.dry_run)
    
    if not args.characters_only:
        series_count = build_series_embeddings(args.db, args.dry_run)
    
    print(f"\n{Colors.GREEN}✅ Complete!{Colors.RESET}")
    print(f"   Characters indexed: {char_count}")
    print(f"   Series indexed: {series_count}")
    print(f"   Total: {char_count + series_count}")


if __name__ == "__main__":
    main()
