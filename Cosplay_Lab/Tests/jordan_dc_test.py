"""
⚡ JORDAN DC TEST - Using Primary Subject IP with DC Characters ⚡
"""
import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
import subprocess, time, json

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
MODEL = "gemini-3-pro-image-preview"
BUFFER = 90
MEGA_BUFFER = 240

# First 6 DC characters for test
DC_CHARS = [
    {"name": "Wonder_Woman", "costume": "Red corset armor with gold W emblem, blue skirt with stars, gold belt, bracers, red boots, lasso on hip", "hair": "Long black wavy hair, tiara on forehead", "scene": "Themyscira beach, golden hour"},
    {"name": "Supergirl", "costume": "Blue top with red/yellow S crest, red skirt, red cape, red boots", "hair": "Blonde, shoulder length or longer, straight, free flowing", "scene": "Metropolis skyline, sunset"},
    {"name": "Batgirl", "costume": "Purple and yellow suit, yellow bat symbol, utility belt, yellow boots. Cowl off", "hair": "Red/orange, long, ponytail or flowing", "scene": "Gotham rooftop at night"},
    {"name": "Catwoman", "costume": "Tight black catsuit, belt, cat ears or goggles. Cowl off for full face", "hair": "Short black bob or pixie", "scene": "Museum heist, moonlight through window"},
    {"name": "Harley_Quinn", "costume": "Shorts, bomber jacket, fishnets. Modern street look", "hair": "Blonde with twin tails, dyed tips red and blue", "scene": "Neon-lit club"},
    {"name": "Poison_Ivy", "costume": "Green leotard, vines on arms and legs, leafy accents", "hair": "Long red hair, big waves, leaves woven in", "scene": "Botanical garden, green lighting"}
]

def get_lite_map(full_map: dict) -> str:
    return json.dumps({
        "face_calibration": full_map.get("face_calibration", {}),
        "eye_nodes": full_map.get("eye_nodes", {}),
        "nose_nodes": full_map.get("nose_nodes", {}),
        "lip_nodes": full_map.get("lip_nodes", {}),
        "jaw_chin": full_map.get("jaw_chin", {}),
        "skin": full_map.get("skin", {}),
        "facial_hair": full_map.get("facial_hair", {}),
        "critical_identity_lock": full_map.get("critical_identity_lock", {})
    }, indent=2)

async def main():
    console.print("[bold cyan]🦇 JORDAN DC TEST - 6 DC Characters[/bold cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    
    # Load existing Jordan IP
    with open("c:/Yuki_Local/jordan_test_results/jordan_primary_subject_ip.json") as f:
        full_map = json.load(f)
    lite_map = get_lite_map(full_map)
    console.print(f"[green]✅ Jordan IP loaded ({len(lite_map)} chars)[/green]")
    
    # Load photo
    photos = sorted(Path("c:/Yuki_Local/jordan test").glob("*.jpg"))
    with open(photos[0], "rb") as f:
        photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    output = Path("c:/Yuki_Local/jordan_dc_results")
    output.mkdir(exist_ok=True)
    
    for i, c in enumerate(DC_CHARS, 1):
        console.print(f"\n[magenta]🦸 [{i}/6] {c['name']}[/magenta]")
        
        prompt = f"""
📷 REAL PHOTOGRAPH - Canon EOS R6 Mark II, RF 85mm f/1.2L @ f/2.0, 4K 9:16
⚠️ REAL COSPLAY PHOTO (not anime, not illustration, not CGI)

🔒 FACIAL IDENTITY (PRIMARY SUBJECT):
{lite_map}
PRESERVE: Face shape, nose, eyes, lips, skin tone EXACTLY. Must be INSTANTLY recognizable.

🦇 DC COSPLAY: {c['name'].replace('_', ' ')}
COSTUME: {c['costume']}
HAIR: {c['hair']}
SCENE: {c['scene']}

Generate ONE REAL cosplay photograph. Face = locked identity. Costume = DC character.
"""
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = output / f"JORDAN_DC_{c['name']}_{ts}.png"
        
        with console.status(f"[cyan]⚡ Generating {c['name']}...", spinner="dots12"):
            try:
                r = await client.aio.models.generate_content(model=MODEL, contents=[prompt, photo],
                    config=types.GenerateContentConfig(temperature=1.0, response_modalities=["IMAGE", "TEXT"],
                        safety_settings=[types.SafetySetting(category=cat, threshold="BLOCK_ONLY_HIGH") 
                            for cat in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                                        "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]))
                for p in r.candidates[0].content.parts:
                    if hasattr(p, 'inline_data') and p.inline_data:
                        with open(path, "wb") as f: f.write(p.inline_data.data)
                        console.print(f"[green]✅ {path.name} ({path.stat().st_size/1024:.0f} KB)[/green]")
                        break
            except Exception as e:
                console.print(f"[red]❌ {str(e)[:60]}[/red]")
        
        if i < len(DC_CHARS):
            if i % 4 == 0:
                console.print(f"[yellow]🔥 MEGA-BUFFER {MEGA_BUFFER}s[/yellow]")
                await asyncio.sleep(MEGA_BUFFER)
            else:
                console.print(f"[cyan]⏳ {BUFFER}s cooldown[/cyan]")
                await asyncio.sleep(BUFFER)
    
    subprocess.Popen(f'explorer "{output}"', shell=True)
    console.print("\n[bold green]✨ JORDAN DC TEST COMPLETE![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
