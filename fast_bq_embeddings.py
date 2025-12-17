"""
🩵 FAST BQ ML EMBEDDINGS v3
Uses load_table_from_json for reliable data upload
"""
from google.cloud import bigquery
from rich.console import Console
import json
from pathlib import Path
from datetime import datetime

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
DATASET_ID = "yuki_memory"


def run():
    console.print("\n[bold cyan]🩵 FAST BQ ML EMBEDDINGS v3[/bold cyan]\n")
    
    client = bigquery.Client(project=PROJECT_ID)
    
    # Step 1: Load characters
    console.print("[cyan]Step 1: Loading characters...[/cyan]")
    json_path = Path("c:/Yuki_Local/data/character_data.json")
    with open(json_path) as f:
        characters = json.load(f)
    console.print(f"   ✅ {len(characters)} characters")
    
    # Step 2: Create staging table and load via JSON
    console.print("[cyan]Step 2: Creating staging table...[/cyan]")
    
    staging = f"{PROJECT_ID}.{DATASET_ID}.char_staging"
    
    schema = [
        bigquery.SchemaField("character_id", "STRING"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("full_name", "STRING"),
        bigquery.SchemaField("category", "STRING"),
        bigquery.SchemaField("content", "STRING"),
    ]
    
    # Create table
    table = bigquery.Table(staging, schema=schema)
    client.delete_table(staging, not_found_ok=True)
    client.create_table(table)
    
    # Prepare rows
    rows = []
    for c in characters:
        content = f"{c['full_name']} - {c['category']} character for cosplay. {c['content']}"
        rows.append({
            "character_id": c['id'],
            "name": c['name'],
            "full_name": c['full_name'],
            "category": c['category'],
            "content": content
        })
    
    # Load from JSON (more reliable than streaming)
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )
    
    # Write to temp file
    temp_path = Path("c:/Yuki_Local/data/staging.jsonl")
    with open(temp_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    with open(temp_path, "rb") as f:
        job = client.load_table_from_file(f, staging, job_config=job_config)
    job.result()
    
    count = list(client.query(f"SELECT COUNT(*) c FROM `{staging}`").result())[0].c
    console.print(f"   ✅ Loaded {count} rows")
    
    # Step 3: Generate embeddings
    console.print("[cyan]Step 3: Generating embeddings (2-5 min)...[/cyan]")
    
    embeddings_table = f"{PROJECT_ID}.{DATASET_ID}.character_embeddings_v2"
    
    embed_sql = f"""
    CREATE OR REPLACE TABLE `{embeddings_table}` AS
    SELECT 
        character_id,
        name,
        full_name,
        category,
        content,
        text_embedding AS embedding,
        CURRENT_TIMESTAMP() AS created_at
    FROM ML.GENERATE_TEXT_EMBEDDING(
        MODEL `{PROJECT_ID}.{DATASET_ID}.text_embedding_model`,
        TABLE `{staging}`
    )
    """
    
    try:
        job = client.query(embed_sql)
        console.print("   ⏳ Running ML.GENERATE_TEXT_EMBEDDING...")
        job.result()
        console.print("   ✅ Done!")
    except Exception as e:
        console.print(f"[red]   ❌ Error: {e}[/red]")
        return
    
    # Verify
    count = list(client.query(f"SELECT COUNT(*) c FROM `{embeddings_table}`").result())[0].c
    console.print(f"\n[green]✅ SUCCESS! {count} embeddings created[/green]")
    console.print(f"[cyan]   Table: {embeddings_table}[/cyan]")
    
    # Cleanup
    client.delete_table(staging, not_found_ok=True)
    temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    run()
