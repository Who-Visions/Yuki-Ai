"""
❄️ WINTER THEME INJECTION ❄️
Injects 100+ Winter/Holiday characters into the queue for immediate research.
"""
import sqlite3
import json
import asyncio
from rich.console import Console
from google import genai
from google.genai import types

console = Console()
DB_PATH = "c:/Yuki_Local/Cosplay_Lab/Brain/yuki_memory.db"
PROJECT_ID = "gifted-cooler-479623-r7"
MODEL = "gemini-3-pro-preview"

async def get_winter_chars():
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    prompt = """
    List 100 FICTIONAL CHARACTERS with a WINTER, ICE, SNOW, or HOLIDAY theme.
    Include diverse sources: Anime, Comics, Movies, Folklore, Games.
    Examples: Elsa, Sub-Zero, Jack Frost, Krampus, The Grinch, Mrs. Claus (Anime version), White Witch, Captain Cold.
    
    RETURN JSON ONLY:
    [
      {"name": "Name", "source_franchise": "Source"},
      ...
    ]
    """
    console.print("[cyan]❄️ Asking Gemini for the Ultimate Winter List...[/cyan]")
    response = await client.aio.models.generate_content(
        model=MODEL, contents=[prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    return json.loads(response.text)

def inject():
    chars = asyncio.run(get_winter_chars())
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    added = 0
    for char in chars:
        try:
            c.execute("INSERT OR IGNORE INTO characters (name, source_franchise) VALUES (?, ?)", 
                      (char['name'], char['source_franchise']))
            if c.rowcount > 0:
                added += 1
                console.print(f"   ❄️ Added: {char['name']}")
        except:
            pass
            
    conn.commit()
    conn.close()
    console.print(f"\n[bold green]✅ Injected {added} Winter Characters into the Queue![/bold green]")

if __name__ == "__main__":
    inject()
