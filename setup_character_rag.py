"""
🩵 CYAN'S CHARACTER RAG SETUP
Dual RAG System: Vertex AI RAG Engine + BigQuery Embeddings
"""
import json
import os
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from Cosplay_Lab.Brain.male_character_bank_1k import MALE_CHARACTER_BANK

# === CONFIGURATION ===
PROJECT_ID = "gifted-cooler-479623-r7"  # Main Yuki project
LOCATION = "us-central1"
GCS_BUCKET = "yuki-character-db"
OUTPUT_DIR = Path("c:/Yuki_Local/data")
OUTPUT_DIR.mkdir(exist_ok=True)




def categorize_character(name: str) -> dict:
    """Categorize a character based on name patterns"""
    name_lower = name.lower()
    
    # Categories based on known franchises
    categories = {
        "dc": ["batman", "superman", "joker", "flash", "aquaman", "darkseid", "nightwing", "robin", "lex", "sinestro", "cyborg", "shazam", "constantine", "swamp thing", "green lantern", "wonder"],
        "marvel": ["iron man", "spider", "thor", "hulk", "wolverine", "deadpool", "captain america", "thanos", "loki", "venom", "magneto", "x-men", "avenger", "panther", "strange"],
        "anime_shonen": ["goku", "vegeta", "naruto", "sasuke", "luffy", "zoro", "ichigo", "deku", "tanjiro", "gojo", "sukuna", "eren", "levi", "saitama", "mob", "asta", "natsu", "meliodas"],
        "anime_seinen": ["guts", "griffith", "spike", "vicious", "light", "l ", "kenshiro", "baki", "johan"],
        "anime_isekai": ["rimuru", "ainz", "subaru", "kazuma", "rudeus", "kirito", "naofumi", "anos"],
        "games": ["master chief", "kratos", "snake", "cloud", "sephiroth", "link", "mario", "sonic", "dante", "vergil", "leon", "chris", "geralt", "joel", "nathan drake"],
        "movies": ["luke skywalker", "darth vader", "neo", "morpheus", "john wick", "bond", "indiana jones", "harry potter", "gandalf", "aragorn", "jack sparrow", "mad max"],
        "horror": ["freddy", "jason", "michael myers", "pinhead", "pennywise", "chucky", "ghostface", "ash williams", "dracula"]
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in name_lower:
                return {"category": category, "subcategory": "main"}
    
    return {"category": "other", "subcategory": "unknown"}


def export_characters_to_json():
    """Export male character bank to JSON for RAG import"""
    print(f"🩵 CYAN: Exporting {len(MALE_CHARACTER_BANK)} characters to JSON...")
    
    characters = []
    for i, char_name in enumerate(MALE_CHARACTER_BANK):
        # Parse character name for source info
        if "(" in char_name and ")" in char_name:
            # Format: "Batman (Bruce Wayne)" -> name="Batman", real_name="Bruce Wayne"
            parts = char_name.split("(")
            name = parts[0].strip()
            extra = parts[1].replace(")", "").strip()
        else:
            name = char_name.strip()
            extra = ""
        
        category_info = categorize_character(char_name)
        
        char_doc = {
            "id": f"char_{i:04d}",
            "name": name,
            "full_name": char_name,
            "real_name_or_variant": extra,
            "category": category_info["category"],
            "content": f"{char_name} is a {category_info['category']} character suitable for cosplay generation. "
                      f"Key features and costume details should be researched for accurate representation.",
            "tags": [category_info["category"], "male", "cosplay"],
            "source_bank": "male_character_bank_1k"
        }
        characters.append(char_doc)
    
    # Save to JSON
    output_path = OUTPUT_DIR / "character_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(characters, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported {len(characters)} characters to {output_path}")
    
    # Also create JSONL format for RAG import (one doc per line)
    jsonl_path = OUTPUT_DIR / "character_data.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for char in characters:
            # RAG expects a "text" field for content
            rag_doc = {
                "text": f"{char['full_name']}\n\nCategory: {char['category']}\n\n{char['content']}",
                "metadata": {
                    "id": char["id"],
                    "name": char["name"],
                    "category": char["category"],
                    "tags": char["tags"]
                }
            }
            f.write(json.dumps(rag_doc, ensure_ascii=False) + "\n")
    
    print(f"✅ Exported JSONL for RAG import to {jsonl_path}")
    
    return output_path, jsonl_path


def upload_to_gcs(local_path: Path):
    """Upload file to GCS bucket"""
    from google.cloud import storage
    
    print(f"☁️ Uploading {local_path.name} to gs://{GCS_BUCKET}/...")
    
    client = storage.Client(project=PROJECT_ID)
    
    # Create bucket if not exists
    try:
        bucket = client.get_bucket(GCS_BUCKET)
    except Exception:
        print(f"   Creating bucket {GCS_BUCKET}...")
        bucket = client.create_bucket(GCS_BUCKET, location=LOCATION)
    
    blob = bucket.blob(local_path.name)
    blob.upload_from_filename(str(local_path))
    
    gcs_uri = f"gs://{GCS_BUCKET}/{local_path.name}"
    print(f"✅ Uploaded to {gcs_uri}")
    return gcs_uri


def create_rag_corpus(gcs_uri: str):
    """Create Vertex AI RAG corpus and import data"""
    import vertexai
    from vertexai import rag
    
    print(f"🧠 Creating RAG corpus in {PROJECT_ID}/{LOCATION}...")
    
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    # Check if corpus already exists
    existing_corpora = list(rag.list_corpora())
    for corpus in existing_corpora:
        if corpus.display_name == "yuki-character-db":
            print(f"   Found existing corpus: {corpus.name}")
            return corpus
    
    # Create new corpus
    corpus = rag.create_corpus(
        display_name="yuki-character-db",
        description="1000+ male characters for Yuki cosplay generation. Dual RAG system by Cyan."
    )
    print(f"✅ Created corpus: {corpus.name}")
    
    # Import files from GCS
    print(f"📥 Importing data from {gcs_uri}...")
    response = rag.import_files(
        corpus_name=corpus.name,
        paths=[gcs_uri],
        timeout=600
    )
    print(f"✅ Imported {response.imported_rag_files_count} files")
    
    return corpus


def test_rag_query(corpus_name: str):
    """Test RAG retrieval"""
    from vertexai import rag
    
    print("\n🔍 Testing RAG retrieval...")
    
    test_queries = ["Goku", "Batman", "Levi Ackerman", "Cloud Strife"]
    
    for query in test_queries:
        print(f"\n   Query: '{query}'")
        response = rag.retrieval_query(
            text=query,
            rag_corpora=[corpus_name],
            similarity_top_k=3
        )
        
        if response.contexts.contexts:
            for ctx in response.contexts.contexts[:2]:
                print(f"   → {ctx.text[:100]}...")
        else:
            print("   → No results found")


if __name__ == "__main__":
    print("=" * 60)
    print("🩵 CYAN'S DUAL RAG SETUP - Phase 1: Vertex AI RAG Engine")
    print("=" * 60)
    
    # Step 1: Export characters to JSON
    json_path, jsonl_path = export_characters_to_json()
    
    # Step 2: Upload to GCS
    gcs_uri = upload_to_gcs(jsonl_path)
    
    # Step 3: Create RAG corpus and import
    corpus = create_rag_corpus(gcs_uri)
    
    # Step 4: Test retrieval
    test_rag_query(corpus.name)
    
    print("\n" + "=" * 60)
    print("✅ Phase 1 Complete! RAG corpus ready.")
    print(f"   Corpus: {corpus.name}")
    print("=" * 60)
