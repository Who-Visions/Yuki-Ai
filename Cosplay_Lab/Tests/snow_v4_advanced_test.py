"""
⚡ SNOW V4 VFX TEST - 10 Advanced Characters ⚡
Using V4 VFX Deep Map (face projection mapping inspired)
Includes: Fusions • Gender Swaps • Original Character

Characters:
1. Rukia-Kallen Fusion
2. Uraraka Ochaco
3. Kyoka Jiro
4. Nana Shimura
5. Tifa Lockhart (anime style)
6. Yoruichi Cat-Human
7. Megumi Fushiguro (gender swap)
8. Levi Ackerman (gender swap)
9. Afro Samurai (gender swap)
10. Original Black Sorceress (OC)
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

CAMERA_SPEC = """CAMERA: Canon EOS R6 Mark II | LENS: RF 85mm f/1.2L @ f/2.0 | 4K 9:16 | Professional lighting"""

CHARACTERS = [
    {
        "name": "Rukia_Kallen_Fusion",
        "show": "Bleach x Code Geass",
        "description": """
        CUSTOM FUSION: Rukia Kuchiki face + Kallen Stadtfeld styling
        
        FACE: Rukia's soft, serious expression with violet/purple eyes
        HAIR: Kallen's bright RED spiky hair (NOT Rukia's black hair)
        
        COSTUME:
        - Black Knights/rebel jacket (red and black accents)
        - Mix of Shinigami and pilot aesthetics
        - Confident stance
        
        STYLE: Soul Reaper rebel hybrid
        EXPRESSION: Fierce determination, rebel fire in eyes
        """,
        "scene": "Dark battlefield with red and purple energy swirling"
    },
    {
        "name": "Uraraka_Ochaco",
        "show": "My Hero Academia",
        "description": """
        Uraraka Ochaco from My Hero Academia.
        
        HAIR: Short brown bob with bangs
        EYES: Large, round brown eyes
        FACE: Soft, round cheeks with permanent blush
        
        COSTUME OPTIONS:
        - Pink and black hero suit (skin tight with braces at wrists)
        - OR UA school uniform (grey blazer, green skirt)
        
        EXPRESSION: Bright, optimistic smile, determined
        """,
        "scene": "UA High School rooftop, bright sunny day"
    },
    {
        "name": "Kyoka_Jiro",
        "show": "My Hero Academia",
        "description": """
        Kyoka Jiro from My Hero Academia.
        
        HAIR: Short dark purple/black bob, slightly punk
        EYES: Dark, slightly sleepy/bored look
        QUIRK FEATURE: Earphone jack cables (long cables from earlobes)
        
        COSTUME:
        - Punk rock aesthetic
        - Black leather jacket
        - Band tees
        - Headphones around neck
        
        EXPRESSION: Cool, slightly aloof but passionate about music
        """,
        "scene": "Dark concert stage with purple spotlights"
    },
    {
        "name": "Nana_Shimura",
        "show": "My Hero Academia",
        "description": """
        Nana Shimura from My Hero Academia (flashback appearance).
        
        HAIR: Short, dark hair (similar to Deku's style but feminine)
        EYES: Determined, heroic gaze
        FACE: Strong, warm smile - "symbol of hope" energy
        
        COSTUME:
        - White cape with high collar
        - Dark bodysuit underneath
        - Classic All Might predecessor look
        
        EXPRESSION: Heroic smile, confident, inspiring
        """,
        "scene": "Sunset skyline, heroic pose, wind in cape"
    },
    {
        "name": "Tifa_Lockhart_Anime",
        "show": "Final Fantasy VII (anime style)",
        "description": """
        Tifa Lockhart in anime art style.
        
        HAIR: Long, straight BLACK hair (very long, past waist)
        EYES: Brown/reddish-brown, warm and kind
        BODY: Athletic, martial artist build
        
        COSTUME:
        - White crop top/sports bra
        - Black mini skirt
        - Black leather suspenders
        - Red gloves (fighting gloves)
        - Long legs, combat boots
        
        EXPRESSION: Gentle smile with fighter's confidence
        """,
        "scene": "Seventh Heaven bar interior, warm lighting"
    },
    {
        "name": "Yoruichi_CatHuman",
        "show": "Bleach",
        "description": """
        Yoruichi Shihouin - human form with subtle cat features.
        
        SKIN: Dark brown/tan
        HAIR: Long purple hair, flowing
        EYES: GOLDEN/amber cat-like eyes (slightly slit pupils)
        
        CAT FEATURES (subtle):
        - Cat ear headband or real cat ears peeking through hair
        - Slightly feline facial features
        - Athletic, feline grace
        
        COSTUME:
        - Orange and black sporty athletic wear
        - OR stealth ninja outfit
        - Barefoot or minimal footwear
        
        EXPRESSION: Playful, mischievous, ready to pounce
        """,
        "scene": "Rooftop at night, parkour stance, moonlight"
    },
    {
        "name": "Megumi_Fushiguro_GenderSwap",
        "show": "Jujutsu Kaisen",
        "description": """
        ⚧️ GENDER SWAP: Megumi Fushiguro as female
        
        HAIR: Keep Megumi's signature spiky black hair
        FACE: Apply to feminine face structure while keeping stoic expression
        EYES: Dark, intense, slightly tired
        
        COSTUME:
        - Jujutsu High uniform (unmodified)
        - Dark blue/black
        - Slightly disheveled student look
        
        EXPRESSION: Stoic, serious, unbothered
        """,
        "scene": "Dark alley with summoned shadows (shikigami energy)"
    },
    {
        "name": "Levi_Ackerman_GenderSwap",
        "show": "Attack on Titan",
        "description": """
        ⚧️ GENDER SWAP: Levi Ackerman as female
        
        HAIR: Short, black, undercut style (keep Levi's signature cut)
        FACE: Feminine structure but COLD EYES, sharp gaze
        EYES: Narrow, steel grey, intimidating
        
        COSTUME:
        - Survey Corps jacket (tan with Wings of Freedom)
        - ODM harness/straps
        - White pants, knee-high boots
        - White cravat at neck
        
        EXPRESSION: Cold, calculating, slightly disgusted look
        """,
        "scene": "Wall Maria, dramatic wind, Survey Corps setting"
    },
    {
        "name": "Afro_Samurai_GenderSwap",
        "show": "Afro Samurai",
        "description": """
        ⚧️ GENDER SWAP: Afro Samurai as female - TAILOR MADE FOR YOU
        
        HAIR: LARGE AFRO (the signature look!) - dark and voluminous
        HEADBAND: Number One or Number Two headband
        FACE: Feminine but warrior-fierce
        EYES: Intense, focused, warrior's gaze
        
        COSTUME:
        - White gi (traditional martial arts)
        - Open front showing athletic build
        - Katana sword at hip or on back
        - Minimal accessories
        
        EXPRESSION: Silent determination, hunter's focus
        """,
        "scene": "Mountain path, cherry blossoms and blood mist"
    },
    {
        "name": "OC_Black_Sorceress",
        "show": "ORIGINAL CHARACTER",
        "description": """
        🎨 ORIGINAL CHARACTER: Black Sorceress (Yoruichi x Robin fusion inspired)
        
        SKIN: Dark brown/black (preserve subject's actual skin tone)
        HAIR: Long, flowing VIOLET or PURE WHITE hair (mystical)
        EYES: Glowing purple or golden (magical)
        
        COSTUME:
        - Long dark coat/robe (elegant, flowing)
        - Arcane symbols/glyphs glowing on hands
        - Mystical jewelry (gold accents)
        - Dark bodysuit underneath
        
        MAGIC EFFECTS:
        - Glowing glyphs/runes around hands and floating nearby
        - Purple or gold magical energy
        - Ethereal mist
        
        EXPRESSION: Calm, powerful, ancient wisdom in young face
        VIBE: Elegant archaeologist meets battle mage
        
        This is your CUSTOM OC PRESET for future runs.
        """,
        "scene": "Ancient library with floating magical books, purple and gold energy"
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

def build_prompt(character: dict, vfx_map: str) -> str:
    return f"""
═══════════════════════════════════════════════════════════════════════════════
🎬 VFX-GRADE COSPLAY GENERATION - {character['name'].replace('_', ' ')}
═══════════════════════════════════════════════════════════════════════════════

TRANSFORM this person into {character['name'].replace('_', ' ')} from {character['show']}.

═══════════════════════════════════════════════════════════════════════════════
🔒 VFX FACIAL PROJECTION MAP (V4 - 3D Topology Locked) 🔒
═══════════════════════════════════════════════════════════════════════════════

{vfx_map}

⚠️ CRITICAL: This is a 3D facial topology map like VFX projection mapping.
- Use the bone_structure_zones as the foundation
- Respect the facial_anchor_points for feature placement
- Follow surface_characteristics for skin/lighting
- The face MUST be instantly recognizable as the reference person

═══════════════════════════════════════════════════════════════════════════════
CHARACTER COSTUME & STYLING:
═══════════════════════════════════════════════════════════════════════════════

{character['description']}

═══════════════════════════════════════════════════════════════════════════════
📷 {CAMERA_SPEC}
SCENE: {character['scene']}
═══════════════════════════════════════════════════════════════════════════════

Generate ONE photo. Face = locked identity. Everything else = character costume.
═══════════════════════════════════════════════════════════════════════════════
"""

async def main():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   🎬  SNOW V4 VFX TEST - 10 ADVANCED CHARACTERS  🎬                      ║
    ║                                                                           ║
    ║   Using V4 VFX Deep Map (face projection mapping inspired)               ║
    ║                                                                           ║
    ║   🔀 Rukia-Kallen Fusion                                                 ║
    ║   ⚧️ Gender Swaps: Megumi, Levi, Afro Samurai                            ║
    ║   🎨 OC: Black Sorceress (custom preset)                                 ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", box=box.DOUBLE_EDGE))
    
    with console.status("[bold cyan]⚡ Initializing...", spinner="dots12"):
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    console.print("[green]✅ Client ready![/green]")
    
    # Load V4 VFX facial map
    vfx_path = Path("c:/Yuki_Local/snow_v4_vfx_facial_map.json")
    with open(vfx_path) as f:
        vfx_map = json.load(f)
    vfx_text = json.dumps(vfx_map, indent=2)
    console.print(f"[green]✅ V4 VFX Map loaded ({len(vfx_text)} chars)[/green]")
    
    # Load best photo
    input_dir = Path("c:/Yuki_Local/snow test 2")
    input_images = sorted(input_dir.glob("*.jpg"))[:1]
    with open(input_images[0], "rb") as f:
        best_photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    console.print(f"[green]✅ Reference photo loaded[/green]")
    
    output_dir = Path("c:/Yuki_Local/snow_v4_advanced_results")
    output_dir.mkdir(exist_ok=True)
    
    results = []
    start = time.time()
    
    for i, char in enumerate(CHARACTERS, 1):
        console.print("\n" + "═" * 70)
        console.print(f"[bold magenta]🎭 [{i}/10] {char['name'].replace('_', ' ')} ({char['show']})[/bold magenta]")
        console.print("═" * 70)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with Progress(
            SpinnerColumn("dots12"),
            TextColumn("[cyan]{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            console=console
        ) as prog:
            task = prog.add_task("⚡ Generating with V4 VFX Map...", total=100)
            prog.update(task, advance=10)
            
            try:
                prompt = build_prompt(char, vfx_text)
                path = output_dir / f"V4_{char['name']}_{ts}.png"
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
                await animated_countdown(MEGA_BUFFER_SECONDS, f"MEGA-BUFFER ({i}/10 done)", mega=True)
            else:
                await animated_countdown(BUFFER_SECONDS, "Cooling down...")
    
    elapsed = time.time() - start
    console.print("\n" + "═" * 70)
    
    summary = Table(title="🎬 SNOW V4 VFX ADVANCED RESULTS", box=box.DOUBLE_EDGE)
    summary.add_column("#", style="dim")
    summary.add_column("Character", style="magenta")
    summary.add_column("Type", style="cyan")
    summary.add_column("File", style="white")
    summary.add_column("Size", style="green")
    
    char_types = {
        "Rukia_Kallen_Fusion": "🔀 Fusion",
        "Megumi_Fushiguro_GenderSwap": "⚧️ Swap",
        "Levi_Ackerman_GenderSwap": "⚧️ Swap",
        "Afro_Samurai_GenderSwap": "⚧️ Swap",
        "OC_Black_Sorceress": "🎨 OC"
    }
    
    for idx, (char, path, size) in enumerate(results, 1):
        char_type = char_types.get(char, "👤 Standard")
        summary.add_row(str(idx), char[:20], char_type, path.name[:30], f"{size:.0f} KB")
    
    console.print(summary)
    console.print(f"\n[cyan]⏱️ Total: {elapsed/60:.1f} min | Generated: {len(results)}/10[/cyan]")
    console.print(f"[green]📂 Output: {output_dir}[/green]")
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    console.print("\n[bold green]✨ V4 VFX ADVANCED TEST COMPLETE! ✨[/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
