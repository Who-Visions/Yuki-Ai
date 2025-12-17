"""
🚀 YUKI ULTIMATE TEST: THE LONG WALK 🚀
100 Generations. 4K Resolution. V7 DNA-Lock.
Scans all subjects, builds profiles, generates Solo & Group cosplay.
"""
import asyncio
import os
import random
import json
import sqlite3
import time
import subprocess
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from google import genai
from google.genai import types

# --- CONFIGURATION ---
PROJECT_ID = "gifted-cooler-479623-r7"
MODEL_GEN = "gemini-3-pro-image-preview"
MODEL_VISION = "gemini-3-pro-preview"
TOTAL_GENS = 100
ROOT_DIR = Path("c:/Yuki_Local/Cosplay_Lab")
SUBJECTS_DIR = ROOT_DIR / "Subjects"
RENDERS_DIR = ROOT_DIR / "Renders/Ultimate_Walk_100"
DB_PATH = ROOT_DIR / "Brain/yuki_memory.db"
COST_PER_IMG = 0.04 # Est
COST_PER_EXTRACT = 0.12 # Est

console = Console()
RENDERS_DIR.mkdir(parents=True, exist_ok=True)

# --- V7 EXTRACTOR (Embedded for adaptability) ---
async def extract_identity(client, name, images):
    console.print(f"[yellow]🔍 Extracting V7 DNA for {name}...[/yellow]")
    prompt = f"""
    Forensic Analysis of SUBJECT: {name}.
    Analyze these {len(images)} photos.
    Create a V7 FACIAL TOPOLOGY JSON with 18 Zones (Neck, Jaw, Eyes, Math).
    Output JSON ONLY.
    """
    try:
        # Load max 5 images to save tokens
        parts = [types.Part.from_bytes(data=open(img, "rb").read(), mime_type="image/jpeg") for img in images[:5]]
        
        response = await client.aio.models.generate_content(
            model=MODEL_VISION,
            contents=[prompt] + parts,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        data = json.loads(response.text)
        # Simplify for prompt injection
        dna_summary = json.dumps(data)
        
        # Save to DB
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO subjects (name, v7_map_json, last_updated) VALUES (?, ?, CURRENT_TIMESTAMP)", 
                  (name, dna_summary))
        conn.commit()
        conn.close()
        console.print(f"[green]✅ DNA Locked for {name}[/green]")
        return dna_summary
    except Exception as e:
        console.print(f"[red]❌ Extraction Failed: {e}[/red]")
        return None

# --- MAIN ENGINE ---
async def main():
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    
    console.print(Panel.fit("[bold magenta]🚀 YUKI ULTIMATE TEST: THE LONG WALK[/bold magenta]\n[cyan]100 Generations | Group & Solo | V7 Parsing[/cyan]"))

    # 1. DISCOVER SUBJECTS
    subjects = {} # name -> [image_paths]
    for item in SUBJECTS_DIR.iterdir():
        if item.is_dir():
             imgs = list(item.glob("*.jpg")) + list(item.glob("*.JPG")) + list(item.glob("*.png"))
             if imgs:
                 subjects[item.name] = imgs
    
    console.print(f"[green]Found {len(subjects)} Subject Groups: {list(subjects.keys())}[/green]")

    # 2. EXTRACT PROFILES (If needed)
    conn = sqlite3.connect(DB_PATH)
    active_dna = {} # name -> json_string
    
    for name, images in subjects.items():
        # Skip "group test" from individual extraction usually, but if requested we try.
        # User said "find matching faces"... let's treat every folder as a subject for now.
        
        # Check DB first
        cursor = conn.cursor()
        cursor.execute("SELECT v7_map_json FROM subjects WHERE name=?", (name,))
        row = cursor.fetchone()
        
        if row:
            active_dna[name] = row[0]
            console.print(f"   🧬 Loaded DNA: {name}")
        else:
            # Extract
            dna = await extract_identity(client, name, images)
            if dna: 
                active_dna[name] = dna
                console.print("[yellow]💤 Cooling down 45s after extraction...[/yellow]")
                time.sleep(45) # Heavy buffer between extractions

    conn.close()

    # 3. THE 100 GENERATION LOOP
    total_cost = 0.0
    buffer_time = 240 # STRICTER: Start with 4 mins
    STATE_FILE = ROOT_DIR / "Brain/ultimate_state.json"
    
    start_index = 1
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f: 
                state = json.load(f)
                start_index = state.get("last_index", 0) + 1
                console.print(f"[bold yellow]🔄 Resuming from Generation {start_index}...[/bold yellow]")
        except: pass
    
    for i in range(start_index, TOTAL_GENS + 1):
        try:
            is_group = (i % 5 == 0) and (len(active_dna) >= 2) # Every 5th is a Group Shot (Winter Squad)
            
            # --- PICK CHARACTERS (Winter Priority) ---
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            # Pick 'Winter' / 'New' chars first (High IDs)
            c.execute("SELECT name, description, source_franchise FROM characters WHERE description IS NOT NULL ORDER BY id DESC LIMIT 100")
            candidate_chars = c.fetchall()
            conn.close()
            
            # --- GENERATION ---
            ts = datetime.now().strftime("%H%M%S")
            prompt = ""
            ref_images = []
            filename = ""
            
            if is_group:
                # TEAM SHOT (WINTER SQUAD)
                team_size = min(3, len(active_dna))
                team_subjects = random.sample(list(active_dna.keys()), team_size)
                # Pick adjacent characters from list to keep themes similar (e.g. frozen chars together)
                start_idx = random.randint(0, len(candidate_chars)-team_size)
                team_chars = candidate_chars[start_idx : start_idx+team_size]
                
                prompt = "📷 GROUP COSPLAY PHOTOSHOOT. WINTER HOLIDAY SQUAD. 4K.\nTheme: Ice, Snow, Festive.\n"
                filename = f"{i:03d}_GROUP_"
                
                for idx, sub_name in enumerate(team_subjects):
                    char = team_chars[idx]
                    prompt += f"\n[SUBJECT {idx+1}: {sub_name}] as [{char[0]} from {char[2]}]. \nCosplay: {char[1]}.\nIdentity Lock: Use V7 DNA tokens.\n"
                    ref_images.append(subjects[sub_name][0]) # Add 1 ref per person
                    filename += f"{sub_name}_{char[0]}_"
                
                filename += f"{ts}.png"
                console.print(f"\n[bold yellow]❄️👥 [{i}/100] WINTER SQUAD: {team_subjects}[/bold yellow]")
                
            else:
                # SOLO SHOT
                sub_name = random.choice(list(active_dna.keys()))
                char = random.choice(candidate_chars)
                dna = active_dna[sub_name]
                
                # Pick specific reference
                ref_img_path = subjects[sub_name][0]
                ref_name_clean = ref_img_path.stem # Get filename without extension
                
                prompt = f"""
📷 REAL PHOTOGRAPH. 85mm Portrait. 4K resolution.
SUBJECT: {sub_name} matches V7 DNA.
CHARACTER: {char[0]} ({char[2]})
COSTUME: {char[1]}

INSTRUCTIONS:
- Generate a DNA-Authentic cosplay portrait.
- {sub_name}'s face must be precise.
- Apply high-end cosplay materials (leather, armor, fabric).
- Winter/Holiday themes preferred if applicable.
"""
                ref_images = [ref_img_path] 
                # Filename: ID_Folder_SourceFile_Character_Time
                filename = f"{i:03d}_{sub_name}_{ref_name_clean}_{char[0].replace(' ','_')}_{ts}.png"
                console.print(f"\n[bold magenta]🎭 [{i}/100] {sub_name} ({ref_name_clean}) as {char[0]}[/bold magenta]")

            # --- API CALL ---
            out_path = RENDERS_DIR / filename
            
            request_parts = [prompt]
            for img_path in ref_images:
                 request_parts.append(types.Part.from_bytes(data=open(img_path, "rb").read(), mime_type="image/jpeg"))

            with console.status("[cyan]⚡ Generating (High Res)...[/cyan]"):
                # Configuring for Image Generation
                # Note: valid params depend on SDK version. Defaulting to minimal safe config.
                r = await client.aio.models.generate_content(
                    model=MODEL_GEN,
                    contents=request_parts,
                    config=types.GenerateContentConfig(
                        temperature=0.9, 
                        response_modalities=["IMAGE"]
                    )
                )
                
                if r.candidates[0].content.parts[0].inline_data:
                    with open(out_path, "wb") as f: f.write(r.candidates[0].content.parts[0].inline_data.data)
                    console.print(f"[green]   ✅ Saved: {filename}[/green]")
                    total_cost += COST_PER_IMG
                    
                    # CLOUD SYNC
                    try:
                        gcs_path = f"gs://{PROJECT_ID}-yuki-output/Ultimate_Walk/{filename}"
                        cmd = f'gcloud storage cp "{str(out_path)}" {gcs_path}'
                        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        console.print(f"[blue]   ☁️ Synced[/blue]")
                    except:
                        pass
                        
                    # SAVE STATE
                    with open(STATE_FILE, "w") as f:
                        json.dump({"last_index": i}, f)
                
                # ADAPTIVE BUFFER
                # If success, slight reduce.
                buffer_time = max(30, buffer_time - 5)
                
        except Exception as e:
            console.print(f"[red]⚠️ ERROR: {e}[/red]")
            if "429" in str(e) or "quota" in str(e).lower():
                buffer_time = 1200 # 20 MINUTES PENALTY
                console.print(f"[red]🛑 Rate Limit! NUCLEAR Protocol: Cooling down for {buffer_time}s...[/red]")
        
        # SLEEP
        console.print(f"[dim]💰 Est. Cost: ${total_cost:.2f} | 💤 Sleeping {buffer_time}s...[/dim]")
        await asyncio.sleep(buffer_time)

    console.print("[bold green]🏁 THE LONG WALK COMPLETE![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
