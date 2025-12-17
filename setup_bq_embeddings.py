"""
🩵 CYAN'S BIGQUERY EMBEDDINGS SETUP
Phase 2: Generate text embeddings for character database
"""
import json
import time
from pathlib import Path
from typing import List, Dict
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

# === CONFIGURATION ===
PROJECT_ID = "gifted-cooler-479623-r7"  # BigQuery project
DATASET_ID = "yuki_memory"
TABLE_ID = "character_embeddings"
EMBEDDING_MODEL = "text-embedding-005"
BATCH_SIZE = 5  # Smaller batches to avoid rate limits
DELAY_BETWEEN_BATCHES = 5  # seconds between batches


def load_characters() -> List[Dict]:
    """Load characters from exported JSON"""
    json_path = Path("c:/Yuki_Local/data/character_data.json")
    
    if not json_path.exists():
        console.print("[red]❌ character_data.json not found. Run setup_character_rag.py first![/red]")
        return []
    
    with open(json_path, "r", encoding="utf-8") as f:
        characters = json.load(f)
    
    console.print(f"[green]✅ Loaded {len(characters)} characters[/green]")
    return characters


def ensure_bq_table():
    """Create embeddings table if not exists"""
    from google.cloud import bigquery
    
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    schema = [
        bigquery.SchemaField("character_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("full_name", "STRING"),
        bigquery.SchemaField("category", "STRING"),
        bigquery.SchemaField("content_text", "STRING"),
        bigquery.SchemaField("embedding", "FLOAT64", mode="REPEATED"),  # 768-dim vector
        bigquery.SchemaField("created_at", "TIMESTAMP"),
    ]
    
    try:
        client.get_table(table_ref)
        console.print(f"[cyan]   Table {TABLE_ID} exists[/cyan]")
    except Exception:
        console.print(f"[yellow]   Creating table {TABLE_ID}...[/yellow]")
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        console.print(f"[green]   ✅ Created table {TABLE_ID}[/green]")
    
    return table_ref


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings using Vertex AI text-embedding-005"""
    from google import genai
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
    
    embeddings = []
    for text in texts:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )
        # Extract embedding vector
        if response.embeddings:
            embeddings.append(list(response.embeddings[0].values))
        else:
            embeddings.append([0.0] * 768)  # Fallback empty vector
    
    return embeddings


def batch_insert_embeddings(table_ref: str, rows: List[Dict]):
    """Insert embedding rows into BigQuery"""
    from google.cloud import bigquery
    import datetime
    
    client = bigquery.Client(project=PROJECT_ID)
    
    # Add timestamp
    for row in rows:
        row["created_at"] = datetime.datetime.utcnow().isoformat()
    
    errors = client.insert_rows_json(table_ref, rows)
    if errors:
        console.print(f"[red]   ❌ Insert errors: {errors}[/red]")
        return False
    return True


def main():
    console.print("\n[bold cyan]" + "=" * 60 + "[/bold cyan]")
    console.print("[bold cyan]🩵 CYAN'S DUAL RAG SETUP - Phase 2: BigQuery Embeddings[/bold cyan]")
    console.print("[bold cyan]" + "=" * 60 + "[/bold cyan]\n")
    
    # Load characters
    characters = load_characters()
    if not characters:
        return
    
    # Ensure table exists
    table_ref = ensure_bq_table()
    
    # Process in batches
    total_batches = (len(characters) + BATCH_SIZE - 1) // BATCH_SIZE
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Generating embeddings...", total=len(characters))
        
        for batch_idx in range(total_batches):
            start_idx = batch_idx * BATCH_SIZE
            end_idx = min(start_idx + BATCH_SIZE, len(characters))
            batch = characters[start_idx:end_idx]
            
            # Prepare texts for embedding
            texts = [
                f"{char['full_name']} - {char['category']} character for cosplay. {char['content']}"
                for char in batch
            ]
            
            try:
                # Generate embeddings
                embeddings = generate_embeddings(texts)
                
                # Prepare rows for BQ
                rows = []
                for i, char in enumerate(batch):
                    rows.append({
                        "character_id": char["id"],
                        "name": char["name"],
                        "full_name": char["full_name"],
                        "category": char["category"],
                        "content_text": texts[i],
                        "embedding": embeddings[i]
                    })
                
                # Insert to BigQuery
                batch_insert_embeddings(table_ref, rows)
                
                progress.update(task, advance=len(batch))
                
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    console.print(f"[yellow]   ⚠️ Rate limited. Waiting 30s...[/yellow]")
                    time.sleep(30)
                    batch_idx -= 1  # Retry this batch
                else:
                    console.print(f"[red]   ❌ Error on batch {batch_idx}: {e}[/red]")
            
            # Delay between batches
            if batch_idx < total_batches - 1:
                time.sleep(DELAY_BETWEEN_BATCHES)
    
    console.print(f"\n[green]✅ Phase 2 Complete! Generated embeddings for {len(characters)} characters.[/green]")
    console.print(f"[cyan]   Table: {table_ref}[/cyan]")


def test_semantic_search(query: str, top_k: int = 5):
    """Test semantic search using BigQuery vector search"""
    from google.cloud import bigquery
    from google import genai
    
    console.print(f"\n[bold]🔍 Testing semantic search: '{query}'[/bold]")
    
    # Generate query embedding
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
    response = client.models.embed_content(model=EMBEDDING_MODEL, contents=query)
    query_embedding = list(response.embeddings[0].values)
    
    # BigQuery cosine similarity search
    bq_client = bigquery.Client(project=PROJECT_ID)
    
    # Create a SQL query using COSINE_DISTANCE (available in BQ)
    # Note: This is a simplified approach. For production, use Vector Search.
    sql = f"""
    WITH query_embedding AS (
        SELECT {query_embedding} AS embedding
    )
    SELECT 
        c.character_id,
        c.name,
        c.full_name,
        c.category,
        -- Manual cosine similarity calculation
        (
            SELECT SUM(a * b) / (SQRT(SUM(a * a)) * SQRT(SUM(b * b)))
            FROM UNNEST(c.embedding) a WITH OFFSET pos
            JOIN UNNEST((SELECT embedding FROM query_embedding)) b WITH OFFSET pos2
            ON pos = pos2
        ) AS similarity
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` c
    ORDER BY similarity DESC
    LIMIT {top_k}
    """
    
    try:
        results = bq_client.query(sql).result()
        for row in results:
            console.print(f"   → {row.full_name} ({row.category}) - similarity: {row.similarity:.4f}")
    except Exception as e:
        console.print(f"[red]   ❌ Query error: {e}[/red]")


if __name__ == "__main__":
    main()
    
    # Optional: Test search
    console.print("\n" + "=" * 60)
    test_semantic_search("dragon ball character")
    test_semantic_search("dark gothic anime swordsman")
    test_semantic_search("video game hero sword magic")
