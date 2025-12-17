"""
🧠 YUKI BRAIN - KNOWLEDGE ENRICHMENT AGENT 🧠
"The Researcher"
Iterates through incomplete characters in SQLite and fills in costume/hair/props data using Gemini.
"""
import sqlite3
import json
import asyncio
from rich.console import Console
from rich.progress import track
from google import genai
from google.genai import types

console = Console()
DB_PATH = "c:/Yuki_Local/yuki_memory.db"
PROJECT_ID = "gifted-cooler-479623-r7"
MODEL = "gemini-3-pro-preview"

# Limit batch size to avoid rate limits
BATCH_SIZE = 5

async def research_character(client, char_name, char_source):
    """Asks Gemini to research the character's visual details."""
    prompt = f"""
    You are a Cosplay Costume Researcher.
    Character: "{char_name}"
    Source/Franchise: "{char_source}"

    Provide a VISUAL DESCRIPTION for a cosplayer.
    Return JSON ONLY:
    {{
      "description": "Detailed description of iconic costume (colors, materials, fit).",
      "hair_style": "Specific hair color and style description.",
      "key_items": "List of iconic props or accessories (e.g. swords, hats, jewelry).",
      "anti_drift_rules": "Specific instructions to AVOID generating the original actor or wrong art style (e.g. 'Do not generate Robert Downey Jr', 'Do not use anime eyes')."
    }}
    """
    try:
        response = await client.aio.models.generate_content(
            model=MODEL, contents=[prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        console.print(f"[red]❌ Failed to research {char_name}: {e}[/red]")
        return None

async def main():
    console.print("[bold cyan]📚 YUKI KNOWLEDGE ENRICHMENT STARTING...[/bold cyan]")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check column existence (migration handling)
    try:
        c.execute("SELECT hair_style FROM characters LIMIT 1")
    except sqlite3.OperationalError:
        console.print("[yellow]⚠️ Adding new columns for detailed metadata...[/yellow]")
        c.execute("ALTER TABLE characters ADD COLUMN hair_style TEXT")
        c.execute("ALTER TABLE characters ADD COLUMN key_items TEXT")
        conn.commit()

    # Find un-researched characters (where description is NULL)
    c.execute("SELECT id, name, source_franchise FROM characters WHERE description IS NULL LIMIT ?", (BATCH_SIZE,))
    batch = c.fetchall()
    
    if not batch:
        console.print("[green]✅ No un-researched characters found in this batch! (Run again if DB is huge)[/green]")
        return

    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    
    console.print(f"[cyan]🔍 Researching batch of {len(batch)} characters...[/cyan]")
    
    tasks = []
    for char in batch:
        tasks.append(research_character(client, char[1], char[2]))
        
    results = await asyncio.gather(*tasks)
    
    updates = 0
    for i, res in enumerate(results):
        if res:
            char_id = batch[i][0]
            name = batch[i][1]
            
            # Formulate rich description
            full_desc = f"{res['description']} Hair: {res['hair_style']}."
            if res['key_items']:
                full_desc += f" Items: {res['key_items']}."
            
            c.execute("""
                UPDATE characters 
                SET description = ?, 
                    hair_style = ?, 
                    key_items = ?, 
                    anti_drift_rules = ? 
                WHERE id = ?
            """, (full_desc, res['hair_style'], str(res.get('key_items','')), res['anti_drift_rules'], char_id))
            updates += 1
            console.print(f"   ✨ Enriched: [bold]{name}[/bold]")
            
    conn.commit()
    conn.close()
    console.print(f"[bold green]✅ Batch Complete! Enriched {updates}/{len(batch)} characters.[/bold green]")
    console.print("[grey50]Run this script in a loop to populate the full 1,000+ database.[/grey50]")

if __name__ == "__main__":
    asyncio.run(main())
