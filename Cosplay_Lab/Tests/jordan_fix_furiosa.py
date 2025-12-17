"""
⚡ JORDAN V6 FIX - FURIOSA REINFORCED ⚡
Fixing the identity drift/race-swap issue with strong character associations.
"""
import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
import subprocess, json

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
MODEL = "gemini-3-pro-image-preview"

async def main():
    console.print("[bold red]🔧 FIXED FURIOSA GENERATION[/bold red]")
    console.print("[cyan]   Reinforcing Identity Lock to prevent race-swapping[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    
    # Load V6 Jordan map
    with open("c:/Yuki_Local/jordan_test_results/jordan_v6_full_zones.json") as f:
        full_map = json.load(f)
    
    # Extract specific V6 skin/face details for reinforcing
    skin_tone = full_map.get("zone_16_skin_surface", {}).get("tone_description", "deep warm brown")
    identifiers = full_map.get("critical_identity_lock", {}).get("top_7_unique_identifiers", [])
    
    lite_map_str = json.dumps({
        "face_calibration": full_map.get("face_calibration", {}),
        "zone_16_skin_surface": full_map.get("zone_16_skin_surface", {}),
        "zone_4_nose": full_map.get("zone_4_nose", {}),
        "zone_10_lips": full_map.get("zone_10_lips", {}),
        "critical_identity_lock": full_map.get("critical_identity_lock", {})
    }, indent=2)

    # Load photo
    photos = sorted(Path("c:/Yuki_Local/jordan test").glob("*.jpg"))
    with open(photos[0], "rb") as f:
        photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    output = Path("c:/Yuki_Local/jordan_v6_random8_results")
    
    # REINFORCED PROMPT
    prompt = f"""
📷 REAL PHOTOGRAPH - Canon EOS R6 Mark II, RF 85mm f/1.2L @ f/2.0, 4K 9:16 vertical portrait
⚠️ CRITICAL INSTRUCTION: DNA-AUTHENTIC COSPLAY

SUBJECT: The person in the reference photo (Jordan).
CHARACTER TO PLAY: Furiosa (Mad Max: Fury Road)

⛔ NEGATIVE CONSTRAINTS (DO NOT IGNORE):
- DO NOT GENERATE CHARLIZE THERON.
- DO NOT GENERATE ANYA TAYLOR-JOY.
- DO NOT CHANGE THE SUBJECT'S RACE OR SKIN TONE.
- If the output looks like a white woman, YOU HAVE FAILED.

🔒 FACIAL IDENTITY LOCK (V6 DATA):
- Skin Tone: {skin_tone} (MUST PRESERVE)
- Unique Features: {identifiers}
- JSON Map:
{lite_map_str}

COSTUME:
Post-apocalyptic warrior, shaved head/buzzcut (dark hair), black grease war paint on forehead (but do not obscure facial features), mechanical prosthetic arm, dusty leather gear.

SCENE:
Desert wasteland, war rig in background.

GENERATE:
A photorealistic image of JORDAN (the Black woman in the reference) cosplaying as Furiosa.
Her face, skin tone, and features must be 100% hers. Only the clothes and makeup style change.
"""
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output / f"V6_FIX_Furiosa_{ts}.png"
    
    with console.status(f"[cyan]⚡ Generating Fixed Furiosa...", spinner="dots12"):
        try:
            r = await client.aio.models.generate_content(model=MODEL, contents=[prompt, photo],
                config=types.GenerateContentConfig(temperature=1.0, response_modalities=["IMAGE", "TEXT"],
                    safety_settings=[types.SafetySetting(category=cat, threshold="BLOCK_ONLY_HIGH") 
                        for cat in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                                    "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]))
            for p in r.candidates[0].content.parts:
                if hasattr(p, 'inline_data') and p.inline_data:
                    with open(path, "wb") as f: f.write(p.inline_data.data)
                    kb = path.stat().st_size / 1024
                    console.print(f"[green]✅ {path.name} ({kb:.0f} KB)[/green]")
        except Exception as e:
            console.print(f"[red]❌ {str(e)[:60]}[/red]")
            
    subprocess.Popen(f'explorer "{output}"', shell=True)

if __name__ == "__main__":
    asyncio.run(main())
