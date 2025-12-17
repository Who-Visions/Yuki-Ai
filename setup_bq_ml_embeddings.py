"""
🩵 CYAN'S BIGQUERY ML EMBEDDINGS
Uses BigQuery's built-in ML.GENERATE_TEXT_EMBEDDING - no API rate limits!
"""
import json
from pathlib import Path
from google.cloud import bigquery
from rich.console import Console

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
DATASET_ID = "yuki_memory"
LOCATION = "us-central1"  # Must match your BQ dataset location


def setup_bq_ml_embeddings():
    """Generate embeddings using BigQuery ML (no API rate limits)"""
    
    console.print("\n[bold cyan]🩵 CYAN'S BIGQUERY ML EMBEDDINGS[/bold cyan]")
    console.print("[dim]Using ML.GENERATE_TEXT_EMBEDDING - bypasses API rate limits[/dim]\n")
    
    client = bigquery.Client(project=PROJECT_ID)
    
    # Step 1: Load character data
    console.print("[cyan]Step 1: Loading character data...[/cyan]")
    json_path = Path("c:/Yuki_Local/data/character_data.json")
    
    if not json_path.exists():
        console.print("[red]❌ Run setup_character_rag.py first to export data![/red]")
        return
    
    with open(json_path, "r", encoding="utf-8") as f:
        characters = json.load(f)
    
    console.print(f"   ✅ Loaded {len(characters)} characters")
    
    # Step 2: Create staging table with character text
    console.print("[cyan]Step 2: Creating staging table...[/cyan]")
    
    staging_table = f"{PROJECT_ID}.{DATASET_ID}.character_staging"
    
    # Drop if exists
    client.query(f"DROP TABLE IF EXISTS `{staging_table}`").result()
    
    # Create staging table
    create_staging_sql = f"""
    CREATE TABLE `{staging_table}` (
        character_id STRING,
        name STRING,
        full_name STRING,
        category STRING,
        content_text STRING
    )
    """
    client.query(create_staging_sql).result()
    console.print("   ✅ Created staging table")
    
    # Insert character data
    console.print("[cyan]Step 3: Inserting character data...[/cyan]")
    
    rows = []
    for char in characters:
        rows.append({
            "character_id": char["id"],
            "name": char["name"],
            "full_name": char["full_name"],
            "category": char["category"],
            "content_text": f"{char['full_name']} - {char['category']} character for cosplay. {char['content']}"
        })
    
    # Insert in chunks of 500
    for i in range(0, len(rows), 500):
        chunk = rows[i:i+500]
        errors = client.insert_rows_json(staging_table, chunk)
        if errors:
            console.print(f"[red]   ❌ Insert errors: {errors}[/red]")
            return
    
    console.print(f"   ✅ Inserted {len(rows)} rows")
    
    # Step 3: Create embeddings table using ML.GENERATE_TEXT_EMBEDDING
    console.print("[cyan]Step 4: Generating embeddings via BigQuery ML...[/cyan]")
    console.print("   [dim]This runs inside BigQuery - no API rate limits![/dim]")
    
    embeddings_table = f"{PROJECT_ID}.{DATASET_ID}.character_embeddings_ml"
    
    # Drop if exists
    client.query(f"DROP TABLE IF EXISTS `{embeddings_table}`").result()
    
    # Generate embeddings using BQ ML
    # Note: This requires a Vertex AI connection in BigQuery
    generate_embeddings_sql = f"""
    CREATE TABLE `{embeddings_table}` AS
    SELECT 
        character_id,
        name,
        full_name,
        category,
        content_text,
        ml_generate_text_embedding_result.text_embedding AS embedding,
        CURRENT_TIMESTAMP() AS created_at
    FROM ML.GENERATE_TEXT_EMBEDDING(
        MODEL `bqml.text_embedding_005`,
        (SELECT * FROM `{staging_table}`),
        STRUCT('content_text' AS content_column, TRUE AS flatten_json_output)
    )
    """
    
    try:
        job = client.query(generate_embeddings_sql)
        job.result()  # Wait for completion
        console.print("   ✅ Embeddings generated!")
    except Exception as e:
        if "not found" in str(e).lower() or "model" in str(e).lower():
            console.print("[yellow]   ⚠️ Need to create the embedding model first...[/yellow]")
            create_model_and_retry(client, staging_table, embeddings_table)
        else:
            console.print(f"[red]   ❌ Error: {e}[/red]")
            return
    
    # Step 5: Verify
    console.print("[cyan]Step 5: Verifying results...[/cyan]")
    
    count_sql = f"SELECT COUNT(*) as cnt FROM `{embeddings_table}`"
    result = list(client.query(count_sql).result())[0]
    
    console.print(f"\n[green]✅ SUCCESS! Created {result.cnt} character embeddings[/green]")
    console.print(f"[cyan]   Table: {embeddings_table}[/cyan]")


def create_model_and_retry(client, staging_table, embeddings_table):
    """Create the text embedding model using remote connection"""
    
    console.print("[cyan]   Creating Vertex AI connection and model...[/cyan]")
    
    # First, create a connection to Vertex AI
    connection_id = "vertex-ai-connection"
    
    # Check if connection exists, if not provide instructions
    console.print(f"""
[yellow]To use BigQuery ML embeddings, you need to:[/yellow]

1. Go to BigQuery Console
2. Click '+ ADD' → 'Connections to external data sources'
3. Select 'Vertex AI remote models'
4. Connection ID: {connection_id}
5. Location: {LOCATION}

Or run this in Cloud Shell:
[dim]bq mk --connection --location={LOCATION} --project_id={PROJECT_ID} \\
    --connection_type=CLOUD_RESOURCE {connection_id}[/dim]

Then grant the service account 'Vertex AI User' role.

After that, run this SQL in BigQuery Console:

[dim]CREATE OR REPLACE MODEL `{PROJECT_ID}.bqml.text_embedding_005`
REMOTE WITH CONNECTION `{PROJECT_ID}.{LOCATION}.{connection_id}`
OPTIONS (ENDPOINT = 'text-embedding-005');[/dim]

Then re-run this script!
""")


def test_search(query: str = "anime swordsman"):
    """Test vector similarity search"""
    
    console.print(f"\n[bold]🔍 Testing search: '{query}'[/bold]")
    
    client = bigquery.Client(project=PROJECT_ID)
    embeddings_table = f"{PROJECT_ID}.{DATASET_ID}.character_embeddings_ml"
    
    # First get query embedding
    query_embedding_sql = f"""
    SELECT ml_generate_text_embedding_result.text_embedding AS embedding
    FROM ML.GENERATE_TEXT_EMBEDDING(
        MODEL `bqml.text_embedding_005`,
        (SELECT '{query}' AS content_text),
        STRUCT('content_text' AS content_column, TRUE AS flatten_json_output)
    )
    """
    
    try:
        query_result = list(client.query(query_embedding_sql).result())[0]
        query_vec = list(query_result.embedding)
        
        # Now search
        search_sql = f"""
        SELECT 
            name,
            full_name,
            category,
            (SELECT SUM(a*b)/(SQRT(SUM(a*a))*SQRT(SUM(b*b)))
             FROM UNNEST(embedding) a WITH OFFSET i
             JOIN UNNEST({query_vec}) b WITH OFFSET j ON i=j) AS similarity
        FROM `{embeddings_table}`
        ORDER BY similarity DESC
        LIMIT 5
        """
        
        for row in client.query(search_sql).result():
            console.print(f"   → {row.full_name} ({row.category}): {row.similarity:.4f}")
            
    except Exception as e:
        console.print(f"[red]   ❌ Search error: {e}[/red]")


if __name__ == "__main__":
    setup_bq_ml_embeddings()
    
    console.print("\n" + "=" * 60)
    test_search("dragon ball fighter")
    test_search("dark gothic anime")
