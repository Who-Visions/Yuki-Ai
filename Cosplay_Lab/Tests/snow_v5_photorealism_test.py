"""
⚡ SNOW V5 TEST - 12 CHARACTERS (SET 31-42) ⚡
Using V5 Deep Node Map + EXPLICIT PHOTOREALISM (no anime rendering)

Characters:
1. Tenten (Naruto Shippuden)
2. Tsunade (Naruto)
3. Rangiku Matsumoto (Bleach)
4. Soi Fon (Bleach)
5. Yor Forger (Spy x Family) - assassin version
6. Mirko (My Hero Academia)
7. Midnight (My Hero Academia)
8. Rukia Royal Cloak (Bleach TYBW)
9. Yoruichi Streetwear (Bleach)
10. Nico Robin Dressrosa (One Piece)
11. Boa Hancock (One Piece)
12. Nami Post-Timeskip (One Piece)

KEY FIX: Explicit "REAL COSPLAY PHOTOGRAPHY" not anime/illustration
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

# EXPLICIT PHOTOREALISM CAMERA SPEC
CAMERA_SPEC = """
═══════════════════════════════════════════════════════════════════════════════
📷 CRITICAL: THIS IS A REAL PHOTOGRAPH, NOT ANIME OR ILLUSTRATION
═══════════════════════════════════════════════════════════════════════════════

CAMERA: Canon EOS R6 Mark II (actual camera, not simulated)
LENS: RF 85mm f/1.2L USM shooting at f/2.0
RESOLUTION: 4K resolution, 9:16 vertical portrait
LIGHTING: Professional 3-point studio lighting OR cinematic location lighting

OUTPUT REQUIREMENTS:
- REAL HUMAN SKIN with natural pores, texture, imperfections
- REAL FABRIC with actual material properties (leather, cotton, silk)
- REAL HAIR with individual strands visible
- Magazine cover quality photoshoot
- This is a COSPLAY PHOTOSHOOT - a real person dressed as a character
- Shot TODAY in a professional studio

⚠️ DO NOT GENERATE:
- Anime style
- Cartoon style
- CGI/3D render style
- Illustration style
- Cell shading
- Smooth digital art skin
- ANY stylization beyond realistic photography

The output must look like a photograph from a Canon R6 Mark II camera.
═══════════════════════════════════════════════════════════════════════════════
"""

CHARACTERS = [
    {
        "name": "Tenten",
        "show": "Naruto Shippuden",
        "description": """
        Tenten from Naruto Shippuden - REAL COSPLAY.
        
        HAIR: Brown hair in two BUNS on sides of head (signature look)
        OUTFIT: Chinese-inspired top with pants, weapons scroll on back
        ACCESSORIES: Ninja headband, possibly weapons
        
        STYLE: Clean, underrated, weapons specialist
        EXPRESSION: Confident, ready for battle
        """,
        "scene": "Weapons training ground, wooden targets, morning light"
    },
    {
        "name": "Tsunade",
        "show": "Naruto",
        "description": """
        Tsunade from Naruto - REAL COSPLAY.
        
        HAIR: Long blonde hair in two loose pigtails
        FACE: Purple/blue DIAMOND MARK on forehead (essential!)
        BODY: Mature, strong build
        
        OUTFIT:
        - Green haori/coat (open)
        - Low-cut grey/white top underneath
        - Necklace (crystal)
        
        EXPRESSION: Strong, confident, "gamble aunt" energy
        """,
        "scene": "Hokage office or casino setting, warm lighting"
    },
    {
        "name": "Rangiku_Matsumoto",
        "show": "Bleach",
        "description": """
        Rangiku Matsumoto from Bleach - REAL COSPLAY.
        
        HAIR: Long ORANGE/strawberry blonde wavy hair
        BODY: Curvy figure
        
        OUTFIT:
        - Black Shinigami shihakusho (robes)
        - Open front showing cleavage (her signature style)
        - Lieutenant badge on arm
        - Pink scarf optional
        
        EXPRESSION: Flirty smile, playful yet dangerous
        """,
        "scene": "Soul Society gardens, soft ethereal lighting"
    },
    {
        "name": "Soi_Fon",
        "show": "Bleach",
        "description": """
        Soi Fon (Suì-Fēng) from Bleach - REAL COSPLAY.
        
        HAIR: Short dark hair with two long braids wrapped in cloth
        BUILD: Athletic, assassin build (lean, toned)
        
        OUTFIT:
        - Backless Onmitsukidō uniform (black)
        - Commander's haori
        - Ninja/assassin aesthetic
        
        EXPRESSION: Sharp, intense, cold efficiency
        """,
        "scene": "Dark rooftop at night, moonlight, stealth atmosphere"
    },
    {
        "name": "Yor_Forger_Assassin",
        "show": "Spy x Family",
        "description": """
        Yor Forger as Thorn Princess (assassin mode) - REAL COSPLAY.
        
        HAIR: Long BLACK hair
        EYES: Red/crimson (distinctive)
        
        OUTFIT:
        - Black form-fitting dress with high slit
        - Red accents
        - Thigh-high boots
        - Golden rose hairpiece/accessories
        
        EXPRESSION: Cold, deadly, elegant assassin
        """,
        "scene": "Dark ballroom or rooftop at night, dramatic red lighting"
    },
    {
        "name": "Mirko",
        "show": "My Hero Academia",
        "description": """
        Mirko (Rumi Usagiyama) from My Hero Academia - REAL COSPLAY.
        
        SKIN: BROWN/tan skin (essential - she is dark-skinned!)
        HAIR: White/silver long hair
        FEATURES: Rabbit ears (white, can be headband style for cosplay)
        BUILD: Very muscular, especially legs - athletic build
        
        OUTFIT:
        - White leotard hero suit
        - Thigh cutouts
        - Very athletic, revealing hero costume
        
        EXPRESSION: Fierce grin, battle-ready, confident
        """,
        "scene": "Destroyed city block, action pose, dramatic lighting"
    },
    {
        "name": "Midnight_Nemuri",
        "show": "My Hero Academia",
        "description": """
        Midnight (Nemuri Kayama) from My Hero Academia - REAL COSPLAY.
        
        HAIR: Long dark purple/black spiky hair
        BODY: Curvy, sensual build
        
        OUTFIT:
        - Dominatrix-inspired hero costume (toned down for photo)
        - Bodysuit with exposed areas
        - Mask can be pushed up or removed
        - White highlights
        
        EXPRESSION: Flirty, expressive eyes, playful
        """,
        "scene": "UA teacher's office or stage, dramatic purple lighting"
    },
    {
        "name": "Rukia_Royal_Cloak",
        "show": "Bleach Thousand Year Blood War",
        "description": """
        Rukia Kuchiki Royal Guard/Captain version - REAL COSPLAY.
        
        HAIR: Short black hair (her signature)
        EYES: Violet/purple
        
        OUTFIT:
        - Captain's haori (white with Squad 13 insignia)
        - Ice-themed additions
        - Slight armor elements
        - Regal cloak
        - Power upgrade aesthetic
        
        EXPRESSION: Regal, powerful, calm determination
        """,
        "scene": "Seireitei throne room, ice crystals, dramatic backlighting"
    },
    {
        "name": "Yoruichi_Streetwear",
        "show": "Bleach",
        "description": """
        Yoruichi Shihouin modern streetwear version - REAL COSPLAY.
        
        SKIN: Dark brown/tan skin
        HAIR: Long purple hair (can be in ponytail)
        EYES: Golden/amber
        
        OUTFIT - MODERN STREETWEAR:
        - Stylish modern jacket (orange or black)
        - Fitted leggings or joggers
        - Fresh sneakers
        - Urban/athletic wear
        - Street style, not traditional
        
        EXPRESSION: Cool, confident, casual
        """,
        "scene": "Urban city street, graffiti, modern atmosphere"
    },
    {
        "name": "Nico_Robin_Dressrosa",
        "show": "One Piece",
        "description": """
        Nico Robin Dressrosa arc outfit - REAL COSPLAY.
        
        SKIN: Slightly tan/olive
        HAIR: Long black hair
        EYES: Blue
        
        OUTFIT:
        - Tight-fitting dress (purple or dark)
        - Sunglasses on head
        - Elegant heels
        - Minimal jewelry
        
        EXPRESSION: Calm, mysterious smile, serious scholar charm
        """,
        "scene": "Spanish-style plaza, warm Mediterranean light"
    },
    {
        "name": "Boa_Hancock",
        "show": "One Piece",
        "description": """
        Boa Hancock from One Piece - REAL COSPLAY.
        
        HAIR: Long straight BLACK hair (very long, past waist)
        BODY: Tall, elegant, "most beautiful woman" aesthetic
        
        OUTFIT:
        - Revealing royal robes (red and gold)
        - Serpent/snake theme accessories
        - Qipao-inspired dress
        - High heels
        - Gold jewelry
        
        EXPRESSION: Haughty, looking down at camera, dangerous beauty
        """,
        "scene": "Amazon Lily throne room, red and gold drapery"
    },
    {
        "name": "Nami_PostTimeskip",
        "show": "One Piece",
        "description": """
        Nami post-timeskip from One Piece - REAL COSPLAY.
        
        HAIR: Long ORANGE hair
        BODY: Curvy, beach-ready
        TATTOO: Pinwheel/mikan tattoo on left shoulder (essential!)
        
        OUTFIT:
        - Bikini top (various colors)
        - Low-rise jeans or jean shorts
        - Clima-Tact staff optional
        
        EXPRESSION: Confident, money-loving smirk, fun
        """,
        "scene": "Beach, yacht, or tropical club setting, golden hour"
    }
]

async def animated_countdown(seconds: int, desc: str, mega: bool = False):
    color = "bold yellow" if mega else "cyan"
    emoji = "🔥" if mega else "⏳"
    
    with Progress(
        SpinnerColumn("dots12"),
        TextColumn(f"[{color}]{emoji} {desc}"),
        BarColumn(bar_width=50, complete_style="green" if not mega else "yellow"),
        TextColumn("[bold cyan]{task.fields[remaining]}s"),
        TimeElapsedColumn(),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("", total=seconds, remaining=seconds)
        for i in range(seconds, 0, -1):
            progress.update(task, advance=1, remaining=i-1)
            await asyncio.sleep(1)

async def generate_image(client, prompt: str, photo, output_path: Path) -> bool:
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=[prompt, photo],
        config=types.GenerateContentConfig(
            temperature=1.0, top_p=0.95, top_k=40,
            response_modalities=["IMAGE", "TEXT"],
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_ONLY_HIGH"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
            ]
        )
    )
    
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            with open(output_path, "wb") as f:
                f.write(part.inline_data.data)
            return True
    return False

def build_prompt(character: dict, node_map: str) -> str:
    return f"""
{CAMERA_SPEC}

═══════════════════════════════════════════════════════════════════════════════
🔒 V5 DEEP NODE FACIAL MAP - IDENTITY LOCK (100+ ANCHOR POINTS) 🔒
═══════════════════════════════════════════════════════════════════════════════

{node_map}

⚠️ USE ALL ANCHOR POINTS. The face topology is precisely mapped.
This person's face must be INSTANTLY recognizable in the final photo.
DO NOT stylize the face. Preserve EXACT proportions and features.

═══════════════════════════════════════════════════════════════════════════════
CHARACTER COSPLAY: {character['name'].replace('_', ' ')} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

This is a REAL COSPLAY PHOTOSHOOT - a real person wearing a costume.

{character['description']}

═══════════════════════════════════════════════════════════════════════════════
SCENE: {character['scene']}
═══════════════════════════════════════════════════════════════════════════════

GENERATE: One REAL PHOTOGRAPH. NOT anime. NOT illustration. NOT CGI.
A professional cosplay photo shot on Canon R6 Mark II today.
═══════════════════════════════════════════════════════════════════════════════
"""

async def main():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   📷  SNOW V5 TEST - 12 CHARACTERS (PHOTOREALISM FOCUS)  📷             ║
    ║                                                                           ║
    ║   Using V5 Deep Node Map + EXPLICIT ANTI-ANIME INSTRUCTIONS              ║
    ║                                                                           ║
    ║   Tenten • Tsunade • Rangiku • Soi Fon • Yor • Mirko                    ║
    ║   Midnight • Rukia TYBW • Yoruichi Street • Robin • Hancock • Nami       ║
    ║                                                                           ║
    ║   🎯 Goal: REAL COSPLAY PHOTOS, not anime renders                        ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", box=box.DOUBLE_EDGE))
    
    with console.status("[bold cyan]⚡ Initializing...", spinner="dots12"):
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    console.print("[green]✅ Client ready![/green]")
    
    # Load V5 facial map
    v5_path = Path("c:/Yuki_Local/snow_v5_deep_nodes.json")
    if not v5_path.exists():
        console.print("[red]❌ V5 map not found! Run facial_ip_extractor_v5.py first.[/red]")
        return
    
    with open(v5_path) as f:
        node_map = json.load(f)
    node_text = json.dumps(node_map, indent=2)
    console.print(f"[green]✅ V5 Deep Node Map loaded ({len(node_text)} chars)[/green]")
    
    # Load best photo
    input_dir = Path("c:/Yuki_Local/snow test 2")
    input_images = sorted(input_dir.glob("*.jpg"))[:1]
    with open(input_images[0], "rb") as f:
        best_photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    console.print(f"[green]✅ Reference photo loaded[/green]")
    
    output_dir = Path("c:/Yuki_Local/snow_v5_photorealism_results")
    output_dir.mkdir(exist_ok=True)
    
    results = []
    start = time.time()
    
    for i, char in enumerate(CHARACTERS, 1):
        console.print("\n" + "═" * 70)
        console.print(f"[bold magenta]📷 [{i}/12] {char['name'].replace('_', ' ')} ({char['show']})[/bold magenta]")
        console.print("═" * 70)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with Progress(
            SpinnerColumn("dots12"),
            TextColumn("[cyan]{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            console=console
        ) as prog:
            task = prog.add_task("📷 Generating REAL cosplay photo...", total=100)
            prog.update(task, advance=10)
            
            try:
                prompt = build_prompt(char, node_text)
                path = output_dir / f"V5_PHOTO_{char['name']}_{ts}.png"
                success = await generate_image(client, prompt, best_photo, path)
                
                prog.update(task, advance=90, description="✅ Complete!")
                if success:
                    size_kb = path.stat().st_size / 1024
                    console.print(f"   [green]✅ {path.name} ({size_kb:.0f} KB)[/green]")
                    results.append((char['name'], path, size_kb))
                else:
                    console.print("   [yellow]⚠️ No image returned[/yellow]")
            except Exception as e:
                console.print(f"   [red]❌ {str(e)[:80]}...[/red]")
        
        if i < len(CHARACTERS):
            if i % MEGA_BUFFER_EVERY == 0:
                console.print(f"\n[bold yellow]🔥 MEGA-BUFFER: {MEGA_BUFFER_SECONDS}s (4 min)[/bold yellow]")
                await animated_countdown(MEGA_BUFFER_SECONDS, f"MEGA-BUFFER ({i}/12 done)", mega=True)
            else:
                await animated_countdown(BUFFER_SECONDS, "Cooling down...")
    
    elapsed = time.time() - start
    console.print("\n" + "═" * 70)
    
    summary = Table(title="📷 SNOW V5 PHOTOREALISM RESULTS", box=box.DOUBLE_EDGE)
    summary.add_column("#", style="dim")
    summary.add_column("Character", style="magenta")
    summary.add_column("Show", style="cyan")
    summary.add_column("File", style="white")
    summary.add_column("Size", style="green")
    
    for idx, (char, path, size) in enumerate(results, 1):
        summary.add_row(str(idx), char[:18], CHARACTERS[idx-1]['show'][:15], path.name[:28], f"{size:.0f} KB")
    
    console.print(summary)
    console.print(f"\n[cyan]⏱️ Total: {elapsed/60:.1f} min | Generated: {len(results)}/12[/cyan]")
    console.print(f"[green]📂 Output: {output_dir}[/green]")
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    console.print("\n[bold green]✨ V5 PHOTOREALISM TEST COMPLETE! ✨[/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
