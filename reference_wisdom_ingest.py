"""
Universal Wisdom Ingestion Script for Dav1d
Generalizes DOAC ingestion to work with any YouTube video/transcript.
"""
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add project root to path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# NOTE: These imports might missing in Yuki environment, kept for reference
try:
    from tools.vector_store_bigquery import BigQueryVectorStore
    from config import PROJECT_ID, LOCATION, Colors
except ImportError:
    # Dummy mocks for analysis if run locally without full Dav1d stack
    PROJECT_ID = "mock-project"
    LOCATION = "us-central1"
    class Colors:
        NEON_RED = ""
        NEON_CYAN = ""
        NEON_YELLOW = ""
        NEON_GREEN = ""
        RESET = ""
    class BigQueryVectorStore:
        def __init__(self, project, location): pass
        def initialize_dataset(self): pass
        def add_memory(self, content, metadata): pass

# Paths
RESOURCES_DIR = PROJECT_ROOT / "resources"
TRANSCRIPTS_DIR = RESOURCES_DIR / "transcripts"

def format_chunk_for_ingestion(
    chunk: Dict, 
    video_title: str, 
    video_id: str,
    guest: str,
    source_name: str,
    categories: List[str],
    chunk_index: int
) -> Dict:
    """Format a transcript chunk for BigQuery ingestion."""
    
    # Create rich content with context
    content = f"""Source: {source_name}
Guest/Topic: {guest}
Episode: {video_title}
Timestamp: {int(chunk['start_time']//60)}:{int(chunk['start_time']%60):02d} - {int(chunk['end_time']//60)}:{int(chunk['end_time']%60):02d}
Categories: {', '.join(categories)}

{chunk['text'].strip()}"""
    
    metadata = {
        "source": source_name,
        "guest": guest,
        "video_id": video_id,
        "video_title": video_title,
        "chunk_index": chunk_index,
        "start_time": chunk['start_time'],
        "end_time": chunk['end_time'],
        "categories": categories
    }
    
    return {
        "content": content,
        "metadata": metadata
    }

def ingest_video(
    transcript_path: Path,
    source_name: str,
    default_category: str,
    dry_run: bool = False
) -> bool:
    """Ingest a single video transcript."""
    
    if not transcript_path.exists():
        print(f"{Colors.NEON_RED}❌ Transcript file not found: {transcript_path}{Colors.RESET}")
        return False
        
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = json.load(f)
            
        video_id = transcript.get('video_id', transcript_path.stem)
        title = transcript.get('title', 'Unknown Title')[:60]
        guest = transcript.get('guest', 'Unknown Guest')
        chunks = transcript.get('chunks', [])
        
        # Determine categories (use Guest if available, else default)
        categories = [default_category]
        if guest != 'Unknown Guest':
             categories.append(guest.lower().replace(" ", "-"))

        print(f"\n{Colors.NEON_CYAN}📥 Ingesting: {title}{Colors.RESET}")
        print(f"   Source: {source_name} | Guest: {guest}")
        print(f"   Chunks: {len(chunks)} | Categories: {categories}")

        if dry_run:
            print(f"{Colors.NEON_YELLOW}🔍 DRY RUN - Skipping BigQuery Write{Colors.RESET}")
            return True

        # Initialize BigQuery Store
        bq_location = "US" if LOCATION == "global" else LOCATION
        store = BigQueryVectorStore(PROJECT_ID, bq_location)
        store.initialize_dataset()
        
        for i, chunk in enumerate(chunks):
            formatted = format_chunk_for_ingestion(
                chunk=chunk,
                video_title=transcript.get('title', ''),
                video_id=video_id,
                guest=guest,
                source_name=source_name,
                categories=categories,
                chunk_index=i
            )
            store.add_memory(formatted['content'], formatted['metadata'])
            
        print(f"{Colors.NEON_GREEN}✅ Successfully ingested {len(chunks)} chunks!{Colors.RESET}")
        return True

    except Exception as e:
        print(f"{Colors.NEON_RED}❌ Ingestion Failed: {e}{Colors.RESET}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Wisdom Ingestion for Dav1d")
    parser.add_argument('--file', type=str, required=True, help="Path to transcript JSON file")
    parser.add_argument('--source', type=str, default="YouTube", help="Source name (e.g. 'The Diary Of A CEO')")
    parser.add_argument('--category', type=str, default="general", help="Default category")
    parser.add_argument('--dry-run', action='store_true', help="Preview without writing")
    
    args = parser.parse_args()
    
    ingest_video(
        transcript_path=Path(args.file),
        source_name=args.source,
        default_category=args.category,
        dry_run=args.dry_run
    )
