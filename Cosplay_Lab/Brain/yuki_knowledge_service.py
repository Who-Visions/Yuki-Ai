"""
♾️ YUKI KNOWLEDGE SERVICE (INFINITE LOOP) ♾️
Continuously enriches the character database towards 50,000 entries.
Features:
- Adaptive Rate Limiting (Auto-Buffer)
- Self-Expansion (Generates new character names when queue is empty)
"""
import sqlite3
import json
import asyncio
import time
import subprocess
from rich.console import Console
from google import genai
from google.genai import types

console = Console()
DB_PATH = "c:/Yuki_Local/Cosplay_Lab/Brain/yuki_memory.db"
PROJECT_ID = "gifted-cooler-479623-r7"
MODEL = "gemini-3-pro-preview"

TARGET_DB_SIZE = 50000
BATCH_SIZE = 5
BASE_BUFFER = 10  # Seconds between batches

async def suggest_new_characters(client, count=20):
    """Asks Gemini to invent/retrieve more characters to expand the DB."""
    console.print(f"[yellow]⚠️ DB Queue Empty! Expansion Mode: Fetching {count} new characters...[/yellow]")
    
    # Get existing count to seed diversity
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM characters")
    current_count = c.fetchone()[0]
    conn.close()

    prompt = f"""
    We are building a database of {TARGET_DB_SIZE} fictional characters for cosplay.
    Current Count: {current_count}
    
    List {count} UNIQUE, famous (or cult classic) characters from Anime, Comics, Movies, or Games.
    Do NOT repeat common ones like Batman/Naruto. Dig deeper or find new franchises.
    
    RETURN JSON ONLY:
    [
      {{"name": "Character Name", "source_franchise": "Franchise Name"}},
      ...
    ]
    """
    try:
        response = await client.aio.models.generate_content(
            model=MODEL, contents=[prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        console.print(f"[red]❌ Expansion Failed: {e}[/red]")
        return []

async def research_character(client, char_name, char_source):
    """Enriches a single character with model fallback."""
    prompt = f"""
    Cosplay Research: query details for "{char_name}" from "{char_source}".
    JSON Response:
    {{
      "description": "Visual costume description.",
      "hair_style": "Hair color/style.",
      "key_items": "Props/Accessories.",
      "anti_drift_rules": "Anti-hallucination rules."
    }}
    """
    models = ["gemini-3-pro-preview", "gemini-2.5-flash"]
    
    for model in models:
        try:
            response = await client.aio.models.generate_content(
                model=model, contents=[prompt],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            return json.loads(response.text)
        except Exception as e:
            if "429" in str(e) and model != models[-1]:
                #console.print(f"[yellow]⚠️ 429 on {model}, falling back...[/yellow]")
                continue # Try next model
            if "429" in str(e):
                return "429" # All models exhausted
            return None

async def main():
    console.print(f"[bold magenta]♾️ YUKI INFINITE KNOWLEDGE SERVICE[/bold magenta]")
    console.print(f"[cyan]   Target: {TARGET_DB_SIZE} Characters | Mode: Continuous Enrichment[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    buffer = BASE_BUFFER
    BatchCounter = 0
    
    while True:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # 1. CHECK QUEUE (Find un-researched, Newest First)
        c.execute("SELECT id, name, source_franchise FROM characters WHERE description IS NULL ORDER BY id DESC LIMIT ?", (BATCH_SIZE,))
        batch = c.fetchall()
        
        # 2. EXPANSION (If queue empty)
        if not batch:
            new_chars = await suggest_new_characters(client, count=50) # Fetch 50 at a time
            if new_chars:
                for nc in new_chars:
                    c.execute("INSERT OR IGNORE INTO characters (name, source_franchise) VALUES (?, ?)", 
                              (nc['name'], nc['source_franchise']))
                conn.commit()
                console.print(f"[green]🌱 Planted {len(new_chars)} new seeds in the DB.[/green]")
                conn.close()
                continue # Restart loop to pick them up
            else:
                conn.close()
                console.print("[red]❌ Failed to expand. Sleeping 60s...[/red]")
                time.sleep(60)
                continue

        # 3. RESEARCH BATCH
        console.print(f"\n[cyan]🔍 Researching batch of {len(batch)}... (Buffer: {buffer}s)[/cyan]")
        tasks = [research_character(client, row[1], row[2]) for row in batch]
        results = await asyncio.gather(*tasks)
        
        success_count = 0
        hit_rate_limit = False
        
        for i, res in enumerate(results):
            if res == "429":
                hit_rate_limit = True
                console.print(f"   ⚠️ Rate Limit on {batch[i][1]}")
                continue
            
            if isinstance(res, list):
                if len(res) > 0 and isinstance(res[0], dict):
                    res = res[0] # Take first item if list
                else:
                    console.print(f"[red]⚠️ Unexpected list format for {batch[i][1]}[/red]")
                    continue

            if res and isinstance(res, dict):
                char_id = batch[i][0]
                full_desc = f"{res.get('description','')} Hair: {res.get('hair_style','')}."
                
                c.execute("""
                    UPDATE characters 
                    SET description = ?, hair_style = ?, key_items = ?, anti_drift_rules = ? 
                    WHERE id = ?
                """, (full_desc, res.get('hair_style'), str(res.get('key_items')), res.get('anti_drift_rules'), char_id))
                success_count += 1
                console.print(f"   ✅ Learned: {batch[i][1]}")

        conn.commit()
        conn.close()
        
        # 4. CLOUD SYNC (Every 5 batches)
        if BatchCounter % 5 == 0:
            console.print("[blue]☁️ Syncing Memory DB to Cloud...[/blue]")
            try:
                gcs_path = f"gs://{PROJECT_ID}-yuki-output/memory_backup/yuki_memory.db"
                # Using gcloud storage cp for robustness
                cmd = f'gcloud storage cp "{str(DB_PATH)}" {gcs_path}'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    console.print(f"[blue]   ✅ Backup Complete: {gcs_path}[/blue]")
                else:
                    console.print(f"[red]   ☁️ Backup Failed: {result.stderr.strip()}[/red]")
            except Exception as e:
                console.print(f"[red]   ☁️ Backup Error: {e}[/red]")

        # 5. ADAPTIVE BUFFER LOGIC
        BatchCounter += 1
        if hit_rate_limit:
            buffer = min(buffer * 2, 120) # Max 2 mins wait
            console.print(f"[red]🛑 Rate Limited. Increasing buffer to {buffer}s[/red]")
        elif success_count == len(batch):
            buffer = max(buffer - 1, 2) # Min 2s wait (speed up if smooth)
        
        console.print(f"[grey50]Sleeping {buffer}s...[/grey50]")
        time.sleep(buffer)

if __name__ == "__main__":
    asyncio.run(main())
