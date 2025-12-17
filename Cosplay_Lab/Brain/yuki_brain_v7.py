"""
⚡ YUKI BRAIN V7 - REBOOTED & DB CONNECTED ⚡
Orchestrating adaptive cosplay generation with V7 Neck/Jaw logic.
Subjects: Snow, Dav3, Nadly, Jordan, Jesse
Memory: SQLite (yuki_memory.db)
"""
import asyncio
import random
import json
import sqlite3
import subprocess
import traceback
from pathlib import Path
from datetime import datetime
from rich.console import Console
from google import genai
from google.genai import types

# Import Character Banks
from dc_character_bank import DC_CHARACTER_BANK
from anime_character_bank import ANIME_CHARACTER_BANK
from movie_characters_bank import MOVIE_CHARACTERS_BANK
from facial_ip_extractor_v7 import extract_v7_complete

console = Console()
PROJECT_ID = "gifted-cooler-479623-r7"
MODEL = "gemini-3-pro-image-preview"

# SUBJECTS
SUBJECTS = {
    "Jordan": Path("c:/Yuki_Local/Cosplay_Lab/Subjects/jordan test"),
    "Snow": Path("c:/Yuki_Local/Cosplay_Lab/Subjects/snow test 2"),
    "Dav3": Path("c:/Yuki_Local/Cosplay_Lab/Subjects/Dav3 test"),
    "Nadly": Path("c:/Yuki_Local/Cosplay_Lab/Subjects/friends test/Nadley"),
    "Jesse": Path("c:/Yuki_Local/Cosplay_Lab/Subjects/jesse 1 pic test")
}

# DB CONNECTION
DB_PATH = Path("c:/Yuki_Local/Cosplay_Lab/Brain/yuki_memory.db")

def log_generation(subject, character, prompt, output_path, status, buffer):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO generation_log (subject_id, character_id, prompt_used, output_path, status, buffer_time)
            VALUES ((SELECT id FROM subjects WHERE name=?), 
                    (SELECT id FROM characters WHERE name=?), 
                    ?, ?, ?, ?)
        """, (subject, character, prompt, str(output_path), status, buffer))
        conn.commit()
        conn.close()
    except Exception as e:
        console.print(f"[red]DB Log Error: {e}[/red]")

# SELECT 24 RANDOM CHARACTERS
ALL_CHARS = DC_CHARACTER_BANK + ANIME_CHARACTER_BANK + MOVIE_CHARACTERS_BANK
random.shuffle(ALL_CHARS)
SELECTED_BATCH = ALL_CHARS[:24]

async def get_or_create_ip(subject, path):
    out_file = Path(f"c:/Yuki_Local/Cosplay_Lab/Brain/{subject.lower()}_v7_ip.json")
    if out_file.exists():
        with open(out_file) as f: return json.load(f)
    
    if not path.exists():
        console.print(f"[red]⚠️ Path not found: {path}[/red]")
        return None
        
    return await extract_v7_complete(path, out_file, subject)

async def main():
    console.print("[bold cyan]🧠 YUKI BRAIN V7 - REBOOTED (DB ACTIVE)[/bold cyan]")
    
    # Init Subjects
    ips = {}
    for name, path in SUBJECTS.items():
        console.print(f"   🔍 Checking {name}...")
        ip = await get_or_create_ip(name, path)
        if ip: ips[name] = ip
    
    valid_subjects = list(ips.keys())
    console.print(f"[green]✅ Active Subjects: {valid_subjects}[/green]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    output_dir = Path("c:/Yuki_Local/Cosplay_Lab/Renders/yuki_v7_yolo_results")
    output_dir.mkdir(exist_ok=True)
    
    for i, char_name in enumerate(SELECTED_BATCH, 1):
        try:
            subject_name = random.choice(valid_subjects)
            ip = ips[subject_name]
            
            console.print(f"\n[magenta]🎭 [{i}/24] {subject_name} as {char_name}[/magenta]")
            
            # Prepare V7 Data
            flattened_ip = json.dumps({k:v for k,v in ip.items() if "zone_" in k or "critical" in k}, indent=2)
            skin_tone = ip.get("zone_16_skin_surface", {}).get("tone", "natural")
            
            prompt = f"""
📷 REAL PHOTOGRAPH - Canon EOS R6 Mark II, RF 85mm f/1.2L @ f/2.0
⚠️ FORMAT: 9:16 VERTICAL PORTRAIT (Strict Aspect Ratio)
⚠️ CRITICAL: DNA-AUTHENTIC COSPLAY GENERATION

SUBJECT: {subject_name}
CHARACTER: {char_name}

⛔ ANTI-DRIFT PROTOCOL:
- Do NOT generate the original actor/actress.
- Do NOT change the Subject's race or bone structure.
- If character is anime, generate REALISTIC HUMAN COSPLAY, not 2D.
- Maintain Subject's exact skin tone: {skin_tone}.

🔒 FACIAL IDENTITY LOCK (V7 NECK/JAW ARCHITECTURE):
{flattened_ip}

INSTRUCTION:
Generate a photorealistic portrait. 
Use the V7 Map to construct the face, neck, and jawline exactly.
Apply the costume and styling of {char_name}.
"""
            
            # Determine Photo Source
            subject_path = SUBJECTS[subject_name]
            ref_photos = list(subject_path.glob("*.jpg")) + list(subject_path.glob("*.JPG"))
            if not ref_photos:
                console.print(f"[red]❌ No photos found for {subject_name}![/red]")
                continue
                
            img_part = types.Part.from_bytes(data=open(ref_photos[0], "rb").read(), mime_type="image/jpeg")

            ts = datetime.now().strftime("%H%M%S")
            filename = f"{i:02d}_{subject_name}_{char_name.replace(' ','_')}_{ts}.png"
            out_path = output_dir / filename
            
            with console.status(f"[cyan]⚡ Generating...[/cyan]", spinner="dots12"):
                r = await client.aio.models.generate_content(
                    model=MODEL, contents=[prompt, img_part],
                    config=types.GenerateContentConfig(temperature=1.0, response_modalities=["IMAGE", "TEXT"])
                )
                
                saved = False
                for p in r.candidates[0].content.parts:
                    if hasattr(p, 'inline_data') and p.inline_data:
                        with open(out_path, "wb") as f: f.write(p.inline_data.data)
                        kb = out_path.stat().st_size / 1024
                        console.print(f"[green]✅ Saved: {filename} ({kb:.0f} KB)[/green]")
                        
                        # CLOUD SYNC
                        try:
                            gcs_path = f"gs://{PROJECT_ID}-yuki-output/{filename}"
                            subprocess.run(f"gsutil cp \"{out_path}\" {gcs_path}", shell=True, check=True, stdout=subprocess.DEVNULL)
                            console.print(f"[blue]☁️ Synced to GCloud: {gcs_path}[/blue]")
                            log_generation(subject_name, char_name, prompt, gcs_path, "SUCCESS_SYNCED", 60)
                        except Exception as e:
                            console.print(f"[red]☁️ Cloud Sync Failed: {e}[/red]")
                            log_generation(subject_name, char_name, prompt, str(out_path), "SUCCESS_LOCAL_ONLY", 60)
                            
                        saved = True
                        break
                
                if not saved:
                    console.print("[red]❌ No image data received![/red]")
                    log_generation(subject_name, char_name, prompt, "NONE", "FAILED_NO_DATA", 0)

            # Wait Loop
            delay = 200 if i % 4 == 0 else 60
            console.print(f"[yellow]⏳ Cooling down {delay}s...[/yellow]")
            await asyncio.sleep(delay)
            
        except Exception as e:
            console.print(f"[red]❌ FATAL ERROR: {e}[/red]")
            traceback.print_exc()

    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    console.print("\n[bold green]🔥 YOLO BATCH COMPLETE![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
