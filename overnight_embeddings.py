"""
🩵 OVERNIGHT EMBEDDING GENERATOR
Slow and steady - 60s between batches to avoid rate limits
Run this overnight: python overnight_embeddings.py
"""
import json
import time
from pathlib import Path
from datetime import datetime
from google.cloud import bigquery
from google import genai

PROJECT_ID = "gifted-cooler-479623-r7"
DATASET_ID = "yuki_memory"
TABLE_ID = "character_embeddings"
EMBEDDING_MODEL = "text-embedding-005"
BATCH_SIZE = 3  # Very small batches
DELAY_SECONDS = 60  # 1 minute between batches

def run():
    print(f"\n🩵 OVERNIGHT EMBEDDING GENERATOR")
    print(f"   Started: {datetime.now()}")
    print(f"   Batch size: {BATCH_SIZE}, Delay: {DELAY_SECONDS}s")
    print("=" * 50)
    
    # Load characters
    json_path = Path("c:/Yuki_Local/data/character_data.json")
    with open(json_path) as f:
        characters = json.load(f)
    print(f"📦 Loaded {len(characters)} characters")
    
    # Init clients
    bq_client = bigquery.Client(project=PROJECT_ID)
    genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
    
    # Check existing count
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    try:
        result = list(bq_client.query(f"SELECT COUNT(*) as c FROM `{table_ref}`").result())[0]
        start_idx = result.c
        print(f"📊 Already have {start_idx} embeddings, resuming...")
    except:
        start_idx = 0
        print("📊 Starting fresh...")
    
    # Process
    total = len(characters)
    processed = start_idx
    
    for i in range(start_idx, total, BATCH_SIZE):
        batch = characters[i:i+BATCH_SIZE]
        
        try:
            rows = []
            for char in batch:
                text = f"{char['full_name']} - {char['category']} character for cosplay. {char['content']}"
                
                # Get embedding
                response = genai_client.models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=text
                )
                embedding = list(response.embeddings[0].values)
                
                rows.append({
                    "character_id": char["id"],
                    "name": char["name"],
                    "full_name": char["full_name"],
                    "category": char["category"],
                    "content_text": text,
                    "embedding": embedding,
                    "created_at": datetime.utcnow().isoformat()
                })
            
            # Insert to BQ
            errors = bq_client.insert_rows_json(table_ref, rows)
            if errors:
                print(f"❌ Insert error: {errors}")
            else:
                processed += len(batch)
                pct = (processed / total) * 100
                eta_min = ((total - processed) / BATCH_SIZE) * DELAY_SECONDS / 60
                print(f"✅ {processed}/{total} ({pct:.1f}%) - ETA: {eta_min:.0f} min")
        
        except Exception as e:
            if "429" in str(e) or "RESOURCE" in str(e):
                print(f"⚠️ Rate limited, waiting 120s...")
                time.sleep(120)
                continue
            else:
                print(f"❌ Error: {e}")
                time.sleep(30)
                continue
        
        # Delay
        if i + BATCH_SIZE < total:
            time.sleep(DELAY_SECONDS)
    
    print(f"\n✅ DONE! {processed} embeddings generated")
    print(f"   Finished: {datetime.now()}")

if __name__ == "__main__":
    run()
