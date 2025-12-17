"""
⚡ SNOW V5-LITE TEST - CONDENSED NODES + PHOTOREALISM ⚡
V5 map trimmed to ESSENTIAL nodes only (~3k chars vs 8k)
Faster generation, same identity lock

12 Characters - Set 31-42
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from rich import box
import subprocess
import time
import json

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
MODEL = "gemini-3-pro-image-preview"
BUFFER_SECONDS = 90
MEGA_BUFFER_SECONDS = 240
MEGA_BUFFER_EVERY = 4

# CONDENSED V5-LITE MAP - essential nodes only
def get_lite_map(full_map: dict) -> str:
    """Extract only essential identity-locking info from full V5 map"""
    lite = {
        "face_calibration": full_map.get("face_calibration", {}),
        "eye_nodes": {
            "shape": full_map.get("eye_nodes", {}).get("eye_shape", ""),
            "size": full_map.get("eye_nodes", {}).get("eye_size", ""),
            "color": full_map.get("eye_nodes", {}).get("eye_color", ""),
            "spacing": full_map.get("eye_nodes", {}).get("eye_spacing", ""),
        },
        "nose_nodes": {
            "bridge": full_map.get("nose_nodes", {}).get("bridge_shape", ""),
            "tip": full_map.get("nose_nodes", {}).get("tip_shape", ""),
            "width": full_map.get("nose_nodes", {}).get("nose_width_ratio", ""),
            "piercings": full_map.get("nose_nodes", {}).get("piercings", "")
        },
        "lip_nodes": {
            "fullness": full_map.get("lip_nodes", {}).get("upper_lip_fullness", "") + "/" + full_map.get("lip_nodes", {}).get("lower_lip_fullness", ""),
            "cupids_bow": full_map.get("lip_nodes", {}).get("cupids_bow_definition", ""),
            "width": full_map.get("lip_nodes", {}).get("lip_width", "")
        },
        "jaw_chin": {
            "jaw_shape": full_map.get("jaw_chin_nodes", {}).get("jaw_shape", ""),
            "chin_shape": full_map.get("jaw_chin_nodes", {}).get("chin_shape", "")
        },
        "skin": {
            "fitzpatrick": full_map.get("skin_surface", {}).get("fitzpatrick", ""),
            "tone": full_map.get("skin_surface", {}).get("tone_description", ""),
            "undertone": full_map.get("skin_surface", {}).get("undertone", "")
        },
        "critical_identity_lock": full_map.get("critical_identity_lock", {})
    }
    return json.dumps(lite, indent=2)

CAMERA_SPEC = """
📷 REAL PHOTOGRAPH - Canon EOS R6 Mark II, RF 85mm f/1.2L @ f/2.0, 4K 9:16

⚠️ OUTPUT: REAL COSPLAY PHOTO with natural skin texture, real fabric, real hair
⚠️ NOT: anime, illustration, CGI, cartoon, digital art, cell shading
"""

CHARACTERS = [
    {"name": "Tenten", "show": "Naruto Shippuden", "description": "Brown hair in TWO BUNS, Chinese-inspired outfit, weapons specialist", "scene": "Training ground, morning light"},
    {"name": "Tsunade", "show": "Naruto", "description": "Blonde pigtails, DIAMOND MARK on forehead, green coat over low-cut top, mature strong woman", "scene": "Hokage office"},
    {"name": "Rangiku_Matsumoto", "show": "Bleach", "description": "Long ORANGE wavy hair, black shinigami robes open front, curvy, flirty smile", "scene": "Soul Society gardens"},
    {"name": "Soi_Fon", "show": "Bleach", "description": "Short dark hair with braids, backless assassin uniform, athletic sharp intense", "scene": "Dark rooftop, moonlight"},
    {"name": "Yor_Forger", "show": "Spy x Family", "description": "Long BLACK hair, RED eyes, black assassin dress with gold accents, elegant deadly", "scene": "Dark ballroom, red lighting"},
    {"name": "Mirko", "show": "My Hero Academia", "description": "BROWN SKIN, white hair, rabbit ears, muscular legs, white leotard hero suit, fierce grin", "scene": "Destroyed city, action pose"},
    {"name": "Midnight_Nemuri", "show": "My Hero Academia", "description": "Long dark purple hair, bodysuit hero costume, mask up, expressive flirty eyes", "scene": "Stage, purple lighting"},
    {"name": "Rukia_Royal", "show": "Bleach TYBW", "description": "Short black hair, violet eyes, captain haori, ice-themed regal cloak", "scene": "Seireitei, ice crystals"},
    {"name": "Yoruichi_Street", "show": "Bleach", "description": "DARK BROWN skin, purple hair, golden eyes, MODERN streetwear jacket leggings sneakers", "scene": "Urban street, graffiti"},
    {"name": "Robin_Dressrosa", "show": "One Piece", "description": "Long black hair, tight dress, sunglasses on head, elegant intellectual", "scene": "Spanish plaza, warm light"},
    {"name": "Boa_Hancock", "show": "One Piece", "description": "Very long BLACK hair, revealing royal robes, serpent theme, haughty looking down", "scene": "Throne room, red gold"},
    {"name": "Nami_PostTS", "show": "One Piece", "description": "Long ORANGE hair, pinwheel tattoo on shoulder, bikini top, jean shorts, confident smirk", "scene": "Beach, golden hour"}
]

async def countdown(seconds: int, desc: str, mega: bool = False):
    color = "bold yellow" if mega else "cyan"
    with Progress(SpinnerColumn("dots12"), TextColumn(f"[{color}]{desc}"), BarColumn(bar_width=40), TextColumn("{task.fields[r]}s"), console=console, transient=True) as p:
        t = p.add_task("", total=seconds, r=seconds)
        for i in range(seconds, 0, -1):
            p.update(t, advance=1, r=i-1)
            await asyncio.sleep(1)

async def generate(client, prompt: str, photo, path: Path) -> bool:
    r = await client.aio.models.generate_content(model=MODEL, contents=[prompt, photo], config=types.GenerateContentConfig(
        temperature=1.0, response_modalities=["IMAGE", "TEXT"],
        safety_settings=[types.SafetySetting(category=c, threshold="BLOCK_ONLY_HIGH") for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]))
    for p in r.candidates[0].content.parts:
        if hasattr(p, 'inline_data') and p.inline_data:
            with open(path, "wb") as f: f.write(p.inline_data.data)
            return True
    return False

def build_prompt(char: dict, lite_map: str) -> str:
    return f"""{CAMERA_SPEC}

🔒 FACIAL IDENTITY (V5-LITE):
{lite_map}

PRESERVE: Face shape, nose, eyes, lips, skin tone EXACTLY. This person must be INSTANTLY recognizable.

📷 COSPLAY: {char['name'].replace('_', ' ')} from {char['show']}
{char['description']}
SCENE: {char['scene']}

Generate ONE REAL cosplay photograph. NOT anime. Real person in costume."""

async def main():
    console.print(Panel("📷 SNOW V5-LITE - 12 CHARACTERS (FAST + PHOTOREALISM)", style="bold cyan", box=box.DOUBLE_EDGE))
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    console.print("[green]✅ Client ready[/green]")
    
    with open("c:/Yuki_Local/snow_v5_deep_nodes.json") as f: full_map = json.load(f)
    lite_map = get_lite_map(full_map)
    console.print(f"[green]✅ V5-Lite map: {len(lite_map)} chars (vs {len(json.dumps(full_map))} full)[/green]")
    
    with open(sorted(Path("c:/Yuki_Local/snow test 2").glob("*.jpg"))[0], "rb") as f:
        photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    output = Path("c:/Yuki_Local/snow_v5lite_results")
    output.mkdir(exist_ok=True)
    
    results = []
    start = time.time()
    
    for i, c in enumerate(CHARACTERS, 1):
        console.print(f"\n[bold magenta]📷 [{i}/12] {c['name']} ({c['show']})[/bold magenta]")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = output / f"V5L_{c['name']}_{ts}.png"
        
        with console.status(f"[cyan]⚡ Generating {c['name']}...", spinner="dots12"):
            try:
                if await generate(client, build_prompt(c, lite_map), photo, path):
                    kb = path.stat().st_size / 1024
                    console.print(f"[green]✅ {path.name} ({kb:.0f} KB)[/green]")
                    results.append((c['name'], kb))
                else:
                    console.print("[yellow]⚠️ No image[/yellow]")
            except Exception as e:
                console.print(f"[red]❌ {str(e)[:60]}[/red]")
        
        if i < len(CHARACTERS):
            if i % MEGA_BUFFER_EVERY == 0:
                console.print(f"[yellow]🔥 MEGA-BUFFER {MEGA_BUFFER_SECONDS}s[/yellow]")
                await countdown(MEGA_BUFFER_SECONDS, "MEGA-BUFFER", True)
            else:
                await countdown(BUFFER_SECONDS, "Cooldown")
    
    console.print(f"\n[cyan]⏱️ {(time.time()-start)/60:.1f} min | {len(results)}/12 generated[/cyan]")
    subprocess.Popen(f'explorer "{output}"', shell=True)
    console.print("[bold green]✨ V5-LITE COMPLETE![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
