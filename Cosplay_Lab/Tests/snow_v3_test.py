"""
⚡ SNOW V3 TEST - 4 Characters ⚡
Using V3 Facial IP (gemini-3-pro-preview extracted)
Foxxy Love • Aggretsuko • Vecna • Daphne
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

CAMERA_SPEC = """
CAMERA: Canon EOS R6 Mark II
LENS: RF 85mm f/1.2L USM @ f/2.0
RESOLUTION: 4K (9:16 vertical portrait)
LIGHTING: Professional cinematic lighting
QUALITY: Magazine cover, natural skin texture
"""

CHARACTERS = [
    {
        "name": "Foxxy_Love",
        "show": "Drawn Together",
        "description": """
        Foxxy Love from Drawn Together.
        
        APPEARANCE:
        - Dark brown/black skin
        - Long, flowing orange/auburn hair
        - Fox ears on head (orange/brown)
        - Fox tail (orange with white tip)
        - Curvy, athletic figure
        - Confident, sassy expression
        
        COSTUME:
        - Orange halter top/crop top
        - Orange shorts or skirt
        - Mystery-solving detective aesthetic
        - Seventies blaxploitation style
        
        STYLE: Foxy mystery solver, sassy and confident
        EXPRESSION: Knowing smile, one eyebrow raised
        """,
        "scene": "Groovy 70s backdrop with disco lighting"
    },
    {
        "name": "Aggretsuko",
        "show": "Aggretsuko (Sanrio)",
        "description": """
        Aggretsuko (Retsuko) from Aggretsuko anime.
        
        APPEARANCE:
        - Red panda aesthetic (human cosplay version)
        - Red/orange face paint or makeup accents
        - Round, cute face
        - Reddish-brown hair styled simply
        - Office worker look
        
        COSTUME:
        - Simple office blouse (white or light color)
        - Office skirt
        - Red panda ear headband
        - Cute but tired office worker vibe
        - Optional: microphone (death metal moment)
        
        STYLE: Cute office worker who rages with death metal
        EXPRESSION: Either sweet/tired OR screaming rage mode
        """,
        "scene": "Japanese office cubicle OR karaoke room with neon lights"
    },
    {
        "name": "Vecna",
        "show": "Stranger Things",
        "description": """
        Vecna (Henry Creel/One) from Stranger Things.
        
        APPEARANCE:
        - Pale, grayish skin with visible veins
        - No hair (bald head)
        - Elongated, monstrous features
        - Vine-like tendrils across body
        - Glowing eyes (optional)
        - Tall, imposing figure
        
        COSTUME:
        - Dark, organic-looking body
        - Root/vine textures covering skin
        - No traditional clothing
        - Horror monster aesthetic
        - Clawed hands
        
        STYLE: Eldritch horror villain, nightmare fuel
        EXPRESSION: Cold, calculating menace, slight smile
        """,
        "scene": "Upside Down realm, red lightning, floating particles"
    },
    {
        "name": "Daphne_Blake",
        "show": "Scooby-Doo",
        "description": """
        Daphne Blake from Scooby-Doo.
        
        APPEARANCE:
        - Fair skin
        - Long, flowing RED/ORANGE hair (signature look)
        - Purple eyes (in some versions) or blue
        - Slim, fashionable figure
        - Pretty, classic beauty
        
        COSTUME:
        - PURPLE dress (knee-length, classic style)
        - Purple headband in hair
        - Green scarf around neck
        - Purple heels
        - Pink stockings optional
        
        STYLE: Danger-prone fashionista, brave mystery solver
        EXPRESSION: Curious, slightly worried, but brave
        """,
        "scene": "Spooky mansion hallway with candles, mystery atmosphere"
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

def build_prompt(character: dict, geometry: str) -> str:
    return f"""
═══════════════════════════════════════════════════════════════════════════════
PROFESSIONAL COSPLAY - {character['name'].replace('_', ' ')} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

TRANSFORM this person into {character['name'].replace('_', ' ')}.

═══════════════════════════════════════════════════════════════════════════════
🔒 FACIAL IDENTITY LOCK (V3 - Gemini 3 Pro Verified) 🔒
═══════════════════════════════════════════════════════════════════════════════

{geometry}

⚠️ Use MUST_PRESERVE fields as absolute constraints.
The face must be INSTANTLY recognizable as the reference person.
Preserve: nose shape, lip fullness, skin tone, eye shape.

═══════════════════════════════════════════════════════════════════════════════
CHARACTER: {character['name'].replace('_', ' ')} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

{character['description']}

═══════════════════════════════════════════════════════════════════════════════
📷 {CAMERA_SPEC}
═══════════════════════════════════════════════════════════════════════════════

SCENE: {character['scene']}
COMPOSITION: 9:16 vertical portrait

Generate ONE photo where the person is INSTANTLY recognizable in character costume.
═══════════════════════════════════════════════════════════════════════════════
"""

async def main():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   ❄️  SNOW V3 TEST - 4 CHARACTERS  ❄️                                   ║
    ║                                                                           ║
    ║   Using V3 Facial IP (gemini-3-pro-preview extracted)                    ║
    ║                                                                           ║
    ║   Foxxy Love • Aggretsuko • Vecna • Daphne                               ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", box=box.DOUBLE_EDGE))
    
    with console.status("[bold cyan]⚡ Initializing...", spinner="dots12"):
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    console.print("[green]✅ Client ready![/green]")
    
    # Load V3 facial IP
    ip_path = Path("c:/Yuki_Local/snow_test2_enhanced_results/snow2_v3_facial_ip.json")
    with open(ip_path) as f:
        facial_ip = json.load(f)
    geometry_text = json.dumps(facial_ip, indent=2)
    console.print(f"[green]✅ V3 Facial IP loaded ({len(geometry_text)} chars)[/green]")
    
    # Load best photo
    input_dir = Path("c:/Yuki_Local/snow test 2")
    input_images = sorted(input_dir.glob("*.jpg"))[:1]
    with open(input_images[0], "rb") as f:
        best_photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    console.print(f"[green]✅ Reference photo loaded[/green]")
    
    output_dir = Path("c:/Yuki_Local/snow_v3_test_results")
    output_dir.mkdir(exist_ok=True)
    
    results = []
    start = time.time()
    
    for i, char in enumerate(CHARACTERS, 1):
        console.print("\n" + "═" * 70)
        console.print(f"[bold magenta]🎭 [{i}/4] {char['name'].replace('_', ' ')} ({char['show']})[/bold magenta]")
        console.print("═" * 70)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with Progress(
            SpinnerColumn("dots12"),
            TextColumn("[cyan]{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            console=console
        ) as prog:
            task = prog.add_task("⚡ Generating with V3 Face Math...", total=100)
            prog.update(task, advance=10)
            
            try:
                prompt = build_prompt(char, geometry_text)
                path = output_dir / f"V3_{char['name']}_{ts}.png"
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
            await animated_countdown(BUFFER_SECONDS, "Cooling down...")
    
    elapsed = time.time() - start
    console.print("\n" + "═" * 70)
    
    summary = Table(title="❄️ SNOW V3 TEST RESULTS", box=box.DOUBLE_EDGE)
    summary.add_column("#", style="dim")
    summary.add_column("Character", style="magenta")
    summary.add_column("File", style="white")
    summary.add_column("Size", style="green")
    
    for idx, (char, path, size) in enumerate(results, 1):
        summary.add_row(str(idx), char, path.name[:35], f"{size:.0f} KB")
    
    console.print(summary)
    console.print(f"\n[cyan]⏱️ Total: {elapsed/60:.1f} min | Generated: {len(results)}/4[/cyan]")
    console.print(f"[green]📂 Output: {output_dir}[/green]")
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    console.print("\n[bold green]✨ V3 TEST COMPLETE! ✨[/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
