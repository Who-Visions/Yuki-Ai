"""
⚡ JORDAN V6 TEST - 8 RANDOM FROM 1K BANK ⚡
Using V6 15+ Zone Deep Map
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
BUFFER = 90
MEGA_BUFFER = 240

# 8 RANDOM PICKS from the 1K banks (2 from each)
RANDOM_8 = [
    # From DC Universe Bank
    {"name": "Starfire", "source": "DC Comics/Teen Titans", 
     "desc": "Alien princess, orange skin, long flowing red hair, purple crop top and skirt, starbolts, green glowing eyes",
     "scene": "Titans Tower, starry night sky"},
    
    # From Anime Bank
    {"name": "Yor_Forger", "source": "Spy x Family",
     "desc": "Elegant assassin, long black hair, red eyes, black form-fitting dress, gold rose accessories, deadly grace",
     "scene": "Dark ballroom, moonlight through windows"},
    
    # From Movie Characters Bank
    {"name": "The_Bride_Beatrix_Kiddo", "source": "Kill Bill",
     "desc": "Yellow and black Bruce Lee style tracksuit, blonde hair in ponytail, Hattori Hanzo katana sword, determined revenge look",
     "scene": "Snowy Japanese garden, blood on snow"},
    
    # From Movie Stars Bank (as character inspiration)
    {"name": "Zendaya_Chani_Inspired", "source": "Dune",
     "desc": "Fremen stillsuit (dark blue-grey desert survival suit), blue-within-blue eyes, desert warrior, hood down",
     "scene": "Arrakis desert, golden sand dunes at sunset"},
    
    # From DC Universe Bank
    {"name": "Zatanna", "source": "DC Comics",
     "desc": "Stage magician look, black tailcoat tuxedo jacket, white corset, bow tie, fishnet stockings, top hat, wand",
     "scene": "Magic stage, spotlights, mystical smoke"},
    
    # From Anime Bank  
    {"name": "Mitsuri_Kanroji", "source": "Demon Slayer",
     "desc": "Love Hashira, pink and green gradient long braided hair, demon slayer corps uniform with modified chest area, love breathing sword",
     "scene": "Cherry blossom forest, dramatic wind"},
    
    # From Movie Characters Bank
    {"name": "Furiosa", "source": "Mad Max Fury Road",
     "desc": "Post-apocalyptic warrior, shaved head or very short hair, black grease war paint on forehead, mechanical prosthetic arm, dusty leather gear",
     "scene": "Desert wasteland, war rig in background"},
    
    # From Movie Characters Bank
    {"name": "Leeloo", "source": "The Fifth Element",
     "desc": "Supreme being, bright orange hair in bob/pixie, white bandage outfit wraps, futuristic look, multipass",
     "scene": "Futuristic New York, neon lights"}
]

def get_lite_map_v6(full_map: dict) -> str:
    """Extract essential zones from V6 map"""
    return json.dumps({
        "face_calibration": full_map.get("face_calibration", {}),
        "zone_2_eyes": full_map.get("zone_2_eyes", {}),
        "zone_4_nose": full_map.get("zone_4_nose", {}),
        "zone_10_lips": full_map.get("zone_10_lips", {}),
        "zone_6_cheeks": full_map.get("zone_6_cheeks", {}),
        "zone_8_chin": full_map.get("zone_8_chin", {}),
        "zone_14_jaw": full_map.get("zone_14_jaw", {}),
        "zone_16_skin_surface": full_map.get("zone_16_skin_surface", {}),
        "critical_identity_lock": full_map.get("critical_identity_lock", {})
    }, indent=2)

async def main():
    console.print("[bold cyan]🎲 JORDAN V6 TEST - 8 RANDOM FROM 1K BANK[/bold cyan]")
    console.print("[cyan]   Using V6 15+ Zone Deep Map[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    
    # Load V6 Jordan map
    with open("c:/Yuki_Local/jordan_test_results/jordan_v6_full_zones.json") as f:
        full_map = json.load(f)
    lite_map = get_lite_map_v6(full_map)
    console.print(f"[green]✅ Jordan V6 Map loaded ({len(lite_map)} chars)[/green]")
    
    # Load photo
    photos = sorted(Path("c:/Yuki_Local/jordan test").glob("*.jpg"))
    with open(photos[0], "rb") as f:
        photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    output = Path("c:/Yuki_Local/jordan_v6_random8_results")
    output.mkdir(exist_ok=True)
    
    for i, c in enumerate(RANDOM_8, 1):
        console.print(f"\n[magenta]🎲 [{i}/8] {c['name'].replace('_', ' ')} ({c['source']})[/magenta]")
        
        prompt = f"""
📷 REAL PHOTOGRAPH - Canon EOS R6 Mark II, RF 85mm f/1.2L @ f/2.0, 4K 9:16 vertical portrait
⚠️ REAL COSPLAY PHOTOSHOOT (not anime, not illustration, not CGI)

🔒 FACIAL IDENTITY (V6 - 15+ ZONE DEEP MAP):
{lite_map}

CRITICAL: This is a forensic-level facial map. Preserve EVERY zone exactly.
The person must be INSTANTLY recognizable. Face = locked. Costume = character.

🎭 CHARACTER: {c['name'].replace('_', ' ')}
SOURCE: {c['source']}

COSTUME & APPEARANCE:
{c['desc']}

SCENE: {c['scene']}

Generate ONE REAL cosplay photograph shot TODAY on a professional set.
"""
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = output / f"V6_{c['name']}_{ts}.png"
        
        with console.status(f"[cyan]⚡ Generating...", spinner="dots12"):
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
                        break
            except Exception as e:
                console.print(f"[red]❌ {str(e)[:60]}[/red]")
        
        if i < len(RANDOM_8):
            if i % 4 == 0:
                console.print(f"[yellow]🔥 MEGA-BUFFER {MEGA_BUFFER}s[/yellow]")
                await asyncio.sleep(MEGA_BUFFER)
            else:
                console.print(f"[cyan]⏳ {BUFFER}s cooldown[/cyan]")
                await asyncio.sleep(BUFFER)
    
    subprocess.Popen(f'explorer "{output}"', shell=True)
    console.print("\n[bold green]✨ V6 RANDOM 8 TEST COMPLETE![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
