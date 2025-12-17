# 🩵 Yuki Character Database RAG Setup Guide

**For:** Any LLM Agent assisting with Yuki project  
**Author:** Cyan 🩵  
**Date:** December 11, 2025  

---

## Overview

This guide walks through setting up a **Dual RAG System** for the Yuki cosplay generation platform:
1. **Vertex AI RAG Engine** - For semantic document retrieval
2. **BigQuery Embeddings** - For vector similarity search

Both systems query the same 1000+ male character database for redundancy.

---

## Prerequisites

### GCP Project
- **Project ID:** `gifted-cooler-479623-r7`
- **Display Name:** "Yuki-Ai"
- **Region:** `us-central1`

### Local Environment
- **Workspace:** `c:\Yuki_Local`
- **Python venv:** `c:\Yuki_Local\venv`
- **Character Data:** `c:\Yuki_Local\Cosplay_Lab\Brain\male_character_bank_1k.py`

### Required APIs (Enable in GCP Console)
1. Vertex AI API
2. Cloud Storage API
3. BigQuery API

---

## Step 1: Enable RAG Engine in GCP Console

> [!IMPORTANT]
> This MUST be done manually in GCP Console before running any scripts.

1. Go to: https://console.cloud.google.com/vertex-ai/rag
2. Select project: `gifted-cooler-479623-r7`
3. Select region: `us-central1 (Iowa)`
4. Click **"Configure RAG Engine"**
5. Select **"Basic tier"** (cost-effective for small data)
6. Click **Save**
7. Wait ~1 minute for provisioning

**Verification:** The RAG Engine page should no longer show the "Configure" prompt.

---

## Step 2: Export Character Data to JSON

Run this Python code to export the 1038 characters:

```python
import json
from pathlib import Path
import sys
sys.path.insert(0, "c:/Yuki_Local")
from Cosplay_Lab.Brain.male_character_bank_1k import MALE_CHARACTER_BANK

OUTPUT_DIR = Path("c:/Yuki_Local/data")
OUTPUT_DIR.mkdir(exist_ok=True)

characters = []
for i, name in enumerate(MALE_CHARACTER_BANK):
    characters.append({
        "id": f"char_{i:04d}",
        "name": name,
        "content": f"{name} - character for cosplay generation"
    })

# JSON format
with open(OUTPUT_DIR / "character_data.json", "w") as f:
    json.dump(characters, f, indent=2)

# JSONL format for RAG import
with open(OUTPUT_DIR / "character_data.jsonl", "w") as f:
    for char in characters:
        doc = {"text": f"{char['name']}\n\n{char['content']}"}
        f.write(json.dumps(doc) + "\n")

print(f"Exported {len(characters)} characters")
```

**Output files:**
- `c:\Yuki_Local\data\character_data.json`
- `c:\Yuki_Local\data\character_data.jsonl`

---

## Step 3: Upload to Google Cloud Storage

```bash
# Create bucket (run once)
gcloud storage buckets create gs://yuki-character-db --project=gifted-cooler-479623-r7 --location=us-central1

# Upload JSONL file
gcloud storage cp c:\Yuki_Local\data\character_data.jsonl gs://yuki-character-db/
```

**Verify:** `gcloud storage ls gs://yuki-character-db/`

---

## Step 4: Create RAG Corpus

```python
import vertexai
from vertexai import rag

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Create corpus
corpus = rag.create_corpus(
    display_name="yuki-character-db",
    description="1000+ male characters for Yuki cosplay generation"
)
print(f"Created corpus: {corpus.name}")

# Import data from GCS
response = rag.import_files(
    corpus_name=corpus.name,
    paths=["gs://yuki-character-db/character_data.jsonl"],
    timeout=600
)
print(f"Imported {response.imported_rag_files_count} files")
```

**Expected output:**
```
Created corpus: projects/gifted-cooler-479623-r7/locations/us-central1/ragCorpora/XXXXXX
Imported 1 files
```

---

## Step 5: Test RAG Retrieval

```python
from vertexai import rag

corpus_name = "projects/gifted-cooler-479623-r7/locations/us-central1/ragCorpora/XXXXXX"

response = rag.retrieval_query(
    text="Goku dragon ball",
    rag_corpora=[corpus_name],
    similarity_top_k=5
)

for ctx in response.contexts.contexts:
    print(ctx.text[:100])
```

---

## Step 6: Setup BigQuery Embeddings Table

```sql
-- Run in BigQuery Console
CREATE TABLE IF NOT EXISTS `gifted-cooler-479623-r7.yuki_memory.character_embeddings` (
    character_id STRING NOT NULL,
    name STRING NOT NULL,
    full_name STRING,
    category STRING,
    content_text STRING,
    embedding ARRAY<FLOAT64>,
    created_at TIMESTAMP
);
```

---

## Step 7: Generate Embeddings

```python
from google import genai
from google.cloud import bigquery
import json

PROJECT_ID = "gifted-cooler-479623-r7"
EMBEDDING_MODEL = "text-embedding-005"

# Load characters
with open("c:/Yuki_Local/data/character_data.json") as f:
    characters = json.load(f)

# Initialize clients
genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
bq_client = bigquery.Client(project=PROJECT_ID)

# Generate embeddings in batches of 20
for i in range(0, len(characters), 20):
    batch = characters[i:i+20]
    
    rows = []
    for char in batch:
        # Get embedding
        response = genai_client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=char["content"]
        )
        embedding = list(response.embeddings[0].values)
        
        rows.append({
            "character_id": char["id"],
            "name": char["name"],
            "full_name": char["name"],
            "category": "unknown",
            "content_text": char["content"],
            "embedding": embedding
        })
    
    # Insert to BigQuery
    table_ref = f"{PROJECT_ID}.yuki_memory.character_embeddings"
    bq_client.insert_rows_json(table_ref, rows)
    print(f"Inserted batch {i//20 + 1}")
```

> [!WARNING]
> Rate limits apply! Add `time.sleep(2)` between batches.

---

## Step 8: Test Vector Search

```python
from google import genai
from google.cloud import bigquery

PROJECT_ID = "gifted-cooler-479623-r7"

# Get query embedding
client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
response = client.models.embed_content(model="text-embedding-005", contents="anime swordsman")
query_vec = list(response.embeddings[0].values)

# Cosine similarity search
bq = bigquery.Client(project=PROJECT_ID)
sql = f"""
SELECT name, 
       (SELECT SUM(a*b)/(SQRT(SUM(a*a))*SQRT(SUM(b*b)))
        FROM UNNEST(embedding) a WITH OFFSET i
        JOIN UNNEST({query_vec}) b WITH OFFSET j ON i=j) AS score
FROM `{PROJECT_ID}.yuki_memory.character_embeddings`
ORDER BY score DESC
LIMIT 5
"""
for row in bq.query(sql).result():
    print(f"{row.name}: {row.score:.4f}")
```

---

## Step 9: Use the Unified Service

The file `c:\Yuki_Local\character_rag_service.py` provides a unified interface:

```python
from character_rag_service import CharacterRAGService

service = CharacterRAGService()
results = service.search_sync("Goku", top_k=5)

for r in results:
    print(f"{r.full_name} ({r.source}) - {r.score:.3f}")
```

---

## Troubleshooting

### "RAG Engine not onboarded"
→ Go to GCP Console → Vertex AI → RAG Engine → Configure → Select Basic tier → Save

### "Unknown project"
→ Ensure you're using `gifted-cooler-479623-r7` (not the display name "Yuki-Ai")

### "429 Rate Limit"
→ Add delays between API calls: `time.sleep(2)` or increase to 5s

### "Bucket already exists"
→ That's fine, continue with upload step

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `setup_character_rag.py` | Full automated setup script |
| `setup_bq_embeddings.py` | BigQuery embedding generation |
| `character_rag_service.py` | Unified dual retrieval service |
| `Cosplay_Lab/Brain/male_character_bank_1k.py` | Source character list (1038 chars) |
| `data/character_data.jsonl` | Exported data for RAG import |

---

## Summary

After completing all steps:

- ✅ RAG Engine enabled in `gifted-cooler-479623-r7`
- ✅ RAG corpus `yuki-character-db` with 1038 characters
- ✅ GCS bucket `gs://yuki-character-db/` with source data
- ✅ BigQuery table `yuki_memory.character_embeddings` with vectors
- ✅ `CharacterRAGService` for dual retrieval

**Signed:** Cyan 🩵 (Infrastructure Architect)
