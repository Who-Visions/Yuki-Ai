"""
🩵 EXPORT MASTER BANK AND GENERATE EMBEDDINGS
"""
import json
import hashlib
from pathlib import Path
from google.cloud import bigquery
from rich.console import Console

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
DATASET_ID = "yuki_memory"


def categorize(name: str) -> str:
    """Simple category detection from character name"""
    name_lower = name.lower()
    
    # Winter/Christmas
    if any(x in name_lower for x in ["christmas", "winter", "snow", "ice", "frost", "frozen", "santa", "elf", "grinch", "scrooge"]):
        return "Winter/Christmas"
    
    # Games
    if any(x in name_lower for x in ["genshin", "honkai", "pokemon", "overwatch", "mortal kombat"]):
        return "Video Games"
    
    # Anime detection by common series markers
    anime_names = ["kamado", "uzumaki", "uchiha", "kurosaki", "forger", "ackerman", "joestar", 
                   "fullbuster", "zodiac", "senshi", "sailor", "kocho", "tomioka", "todoroki"]
    if any(x in name_lower for x in anime_names):
        return "Anime"
    
    # Marvel/DC
    if any(x in name_lower for x in ["spider", "batman", "superman", "avenger", "x-men", "marvel", "dc"]):
        return "Comics"
    
    # Star Wars
    if any(x in name_lower for x in ["skywalker", "vader", "jedi", "sith", "mandalorian"]):
        return "Star Wars"
    
    # Default
    return "Cosplay Character"


def main():
    console.print("\n[bold cyan]🩵 MASTER CHARACTER BANK EXPORT & EMBED[/bold cyan]\n")
    
    # Import master bank
    from Cosplay_Lab.Brain.master_character_bank import MASTER_CHARACTER_BANK
    console.print(f"✅ Loaded {len(MASTER_CHARACTER_BANK)} characters")
    
    # Build JSON data
    characters = []
    for name in MASTER_CHARACTER_BANK:
        char_id = hashlib.md5(name.encode()).hexdigest()[:12]
        category = categorize(name)
        content = f"{name} is a {category} character popular for cosplay."
        
        characters.append({
            "id": char_id,
            "name": name.split("(")[0].strip(),  # Remove parenthetical
            "full_name": name,
            "category": category,
            "content": content
        })
    
    # Save JSON
    json_path = Path("c:/Yuki_Local/data/master_character_data.json")
    json_path.parent.mkdir(exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(characters, f, indent=2, ensure_ascii=False)
    console.print(f"✅ Exported to {json_path}")
    
    # Create staging table
    console.print("\n[cyan]Creating staging table...[/cyan]")
    client = bigquery.Client(project=PROJECT_ID)
    
    staging = f"{PROJECT_ID}.{DATASET_ID}.master_char_staging"
    
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
    
    # Write JSONL
    jsonl_path = Path("c:/Yuki_Local/data/master_staging.jsonl")
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for char in characters:
            row = {
                "character_id": char["id"],
                "name": char["name"],
                "full_name": char["full_name"],
                "category": char["category"],
                "content": f"{char['full_name']} - {char['category']} character for cosplay. {char['content']}"
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    
    # Load to BQ
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )
    with open(jsonl_path, "rb") as f:
        job = client.load_table_from_file(f, staging, job_config=job_config)
    job.result()
    
    count = list(client.query(f"SELECT COUNT(*) c FROM `{staging}`").result())[0].c
    console.print(f"✅ Loaded {count} rows to staging")
    
    # Generate embeddings
    console.print("\n[cyan]Generating embeddings via BigQuery ML (2-5 min)...[/cyan]")
    
    embeddings_table = f"{PROJECT_ID}.{DATASET_ID}.master_character_embeddings"
    
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
    console.print(f"\n[green]✅ SUCCESS! {count} master embeddings created[/green]")
    console.print(f"[cyan]   Table: {embeddings_table}[/cyan]")
    
    # Cleanup
    client.delete_table(staging, not_found_ok=True)
    jsonl_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
