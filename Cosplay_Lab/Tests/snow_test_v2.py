"""
⚡ SNOW TEST V2 - SINGLE PHOTO REFERENCE (PROVEN APPROACH) ⚡
Rich CLI with animations + Google Search grounded character details
Characters: Foxxy Love, Aggretsuko, Nezuko, Vecna
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
import subprocess
import time

console = Console()

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
MODEL = "gemini-3-pro-image-preview"
BUFFER_SECONDS = 100

# CORRECTED character definitions (researched from wikis)
CHARACTERS = [
    {
        "name": "Foxxy_Love",
        "show": "Drawn Together",
        "description": """
        Foxxy Love from the adult animated series Drawn Together.
        
        ACCURATE COSTUME (from official wiki):
        - ORANGE one-shoulder crop top (very short, no bra)
        - ORANGE short shorts
        - Black thong underneath
        - ORANGE hat with two FOX EARS on top
        - Dark orange furry bracelets on wrists
        - Tall high-heel calf-length ORANGE boots
        - FOX TAIL (she is half-fox hybrid)
        
        HAIR & FEATURES:
        - Dark brown hair in low ponytail
        - Yellow hair tie
        - Dark complexion (Black woman)
        - Tall and slim body
        - Confident, sassy expression
        
        COLOR SCHEME: All ORANGE themed outfit with fox accessories
        STYLE: Stylized cartoon-inspired but photorealistic cosplay
        MOOD: Sassy, confident, mystery-solving musician vibes
        """,
        "scene": "Colorful 70s funk/disco environment with warm lighting"
    },
    {
        "name": "Aggretsuko",
        "show": "Aggretsuko (Sanrio)",
        "description": """
        Retsuko from Aggretsuko - the death metal singing red panda office worker.
        
        COSTUME & APPEARANCE:
        - Professional office attire: White button-up blouse
        - Navy blue pencil skirt
        - Simple office heels
        - Red panda ear headband (cute plush ears - reddish-brown with white inside)
        - Red panda inspired subtle makeup (reddish cheeks)
        - Cute but slightly stressed/frustrated expression
        
        OPTIONAL PROP: Microphone (for death metal mode)
        
        STYLE: Cute Japanese office worker (OL) cosplay with kawaii Sanrio elements
        MOOD: Cute on surface, relatable office worker stress, hidden rage
        """,
        "scene": "Modern Japanese office cubicle environment"
    },
    {
        "name": "Nezuko",
        "show": "Demon Slayer (Kimetsu no Yaiba)",
        "description": """
        Nezuko Kamado from Demon Slayer.
        
        COSTUME & APPEARANCE:
        - Pink kimono with hemp leaf (asanoha) geometric pattern
        - Black haori (short jacket) worn over the kimono
        - Pink obi sash tied at waist
        - BAMBOO MUZZLE/GAG in mouth (this is ESSENTIAL - iconic accessory)
        - Long black hair with gradient to orange/brownish-red at the tips
        - Pink ribbon/bow in hair
        - Bare feet or traditional sandals
        - Innocent but fierce expression in eyes
        
        DEMON FEATURES (subtle):
        - Pink eyes with slit pupils
        - Small fangs (visible if mouth shown)
        
        STYLE: Traditional Japanese with supernatural demon slayer aesthetic
        MOOD: Protective, innocent, powerful when needed
        """,
        "scene": "Traditional Japanese forest at twilight, soft ethereal lighting"
    },
    {
        "name": "Vecna",
        "show": "Stranger Things (Season 4)",
        "description": """
        Vecna (Henry Creel/One) from Stranger Things Season 4.
        
        FULL SFX MAKEUP TRANSFORMATION:
        - Heavily textured skin with vine-like patterns covering entire face and body
        - Exposed muscle and tendon appearance
        - Dark decaying flesh tones (grays, dark browns, deep reds)
        - Sunken features, no visible nose (just holes)
        - Bald head with textured, veiny scalp
        - Deep-set eyes with intense, menacing stare
        - Long claw-like fingers with dark nails
        - Tall, imposing figure
        
        COSTUME:
        - Tattered dark robes or organic tendrils wrapping body
        - Vine-like appendages
        
        MAKEUP STYLE: High-end Hollywood practical SFX prosthetics
        This should look like professional movie-quality makeup
        
        MOOD: Terrifying, otherworldly, Upside Down horror villain
        """,
        "scene": "Dark Upside Down environment with floating red particles, red lightning, apocalyptic atmosphere"
    }
]

def create_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   ❄️  SNOW TEST V2 - SINGLE PHOTO REFERENCE ❄️                  ║
    ║                                                                   ║
    ║   🦊 Foxxy  •  🐼 Aggretsuko  •  👘 Nezuko  •  👹 Vecna          ║
    ║                                                                   ║
    ║   Model: gemini-3-pro-image-preview | 1 Photo Reference          ║
    ║   Buffer: 100s | Aspect: 9:16 | DNA-Locked                       ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    return Panel(Text(banner, style="bold cyan", justify="center"), box=box.DOUBLE_EDGE, border_style="bright_magenta")

def build_prompt(character: dict) -> str:
    return f"""
═══════════════════════════════════════════════════════════════════════════════
PROFESSIONAL COSPLAY PHOTOGRAPHY - {character['name'].upper()} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

Create a PROFESSIONAL PHOTOGRAPH of this person in {character['name']} cosplay.
Shot by professional photographer with high-end camera.

═══════════════════════════════════════════════════════════════════════════════
🔒 FACIAL DNA LOCK - SINGLE REFERENCE - PRESERVE EXACTLY 🔒
═══════════════════════════════════════════════════════════════════════════════

Study this ONE photo carefully and PRESERVE:

BONE STRUCTURE: Their exact face shape, jawline, cheekbones, chin
SKIN: Their exact skin tone, texture, complexion
NOSE: Their exact nose shape, bridge, tip - KEEP ANY PIERCINGS
LIPS: Their exact lip shape, fullness, proportions  
EYES: Their exact eye shape, size, spacing, color
EYEBROWS: Their exact eyebrow shape and arch

THE FINAL FACE MUST BE IMMEDIATELY RECOGNIZABLE AS THIS PERSON.

═══════════════════════════════════════════════════════════════════════════════
CHARACTER: {character['name']} - {character['show']}
═══════════════════════════════════════════════════════════════════════════════

{character['description']}

═══════════════════════════════════════════════════════════════════════════════
📷 PROFESSIONAL PHOTOGRAPHY SPECIFICATIONS
═══════════════════════════════════════════════════════════════════════════════

CAMERA: Sony A7R V, 85mm f/1.4, shallow DOF f/1.8-2.8
LIGHTING: 3-point setup (key, fill, rim), catch lights in eyes
QUALITY: 8K, natural skin texture, no over-processing
COMPOSITION: 9:16 vertical portrait (1080x1920), full body or 3/4 shot
SCENE: {character['scene']}

REALISM: Must look like a REAL photo, not AI-generated
- Natural fabric texture and wrinkles
- Visible hair strands and realistic physics
- Professional magazine/portfolio quality

═══════════════════════════════════════════════════════════════════════════════
OUTPUT: Generate ONE ultra-realistic 9:16 professional cosplay photograph
═══════════════════════════════════════════════════════════════════════════════
"""

async def countdown(seconds: int, desc: str):
    with Progress(SpinnerColumn("dots12"), TextColumn(f"[yellow]{desc}"), BarColumn(bar_width=50), 
                  TextColumn("[cyan]{task.fields[r]}s"), console=console, transient=True) as p:
        t = p.add_task("", total=seconds, r=seconds)
        for i in range(seconds, 0, -1):
            p.update(t, advance=1, r=i-1)
            await asyncio.sleep(1)

async def main():
    console.print(create_banner())
    console.print()
    
    with console.status("[bold cyan]⚡ Initializing Gemini 3 Pro Image...", spinner="dots12"):
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
        await asyncio.sleep(1)
    console.print("[bold green]✅ Client ready!")
    
    input_dir = Path("c:/Yuki_Local/snow test")
    output_dir = Path("c:/Yuki_Local/snow_test_results_v2")
    output_dir.mkdir(exist_ok=True)
    
    # Use SINGLE best photo (first one)
    input_path = sorted(input_dir.glob("*.jpg"))[0]
    
    with console.status("[bold cyan]📸 Loading single reference photo...", spinner="arc"):
        with open(input_path, "rb") as f:
            image_data = f.read()
        image_part = types.Part.from_bytes(data=image_data, mime_type="image/jpeg")
    
    console.print(f"[bold green]✅ Loaded: {input_path.name} ({len(image_data)/1024:.1f} KB)")
    console.print("[dim]   Using SINGLE photo reference (proven more accurate than multi-ref)[/dim]")
    console.print()
    
    results = []
    start = time.time()
    
    for i, char in enumerate(CHARACTERS, 1):
        console.print(Panel(f"[bold magenta]🎭 [{i}/4] {char['name']}[/bold magenta]\n[dim]{char['show']}[/dim]",
                           box=box.ROUNDED, border_style="magenta"))
        
        with Progress(SpinnerColumn("dots12"), TextColumn("[cyan]{task.description}"), 
                      BarColumn(bar_width=40), TimeElapsedColumn(), console=console) as prog:
            task = prog.add_task(f"⚡ Generating {char['name']}...", total=100)
            
            try:
                prog.update(task, advance=10, description="⚡ Sending to Gemini 3...")
                
                response = await client.aio.models.generate_content(
                    model=MODEL,
                    contents=[build_prompt(char), image_part],  # Single image reference
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
                
                prog.update(task, advance=60, description="🎨 Processing...")
                
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        prog.update(task, advance=20, description="💾 Saving...")
                        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                        fn = f"{char['name']}_{ts}.png"
                        sp = output_dir / fn
                        with open(sp, "wb") as f:
                            f.write(part.inline_data.data)
                        prog.update(task, advance=10, description="✅ Done!")
                        sz = sp.stat().st_size / 1024
                        results.append({"char": char['name'], "path": sp, "size": sz})
                        console.print()
                        console.print(f"   [green]✅ {fn} ({sz:.0f} KB)[/green]")
                        break
                else:
                    console.print("   [yellow]⚠️ No image generated[/yellow]")
                    
            except Exception as e:
                console.print(f"   [red]❌ {str(e)[:80]}...[/red]")
        
        if i < len(CHARACTERS):
            console.print()
            await countdown(BUFFER_SECONDS, "⏳ Cooling down...")
            console.print()
    
    elapsed = time.time() - start
    console.print()
    console.print(Panel(f"[bold green]✅ Complete! {len(results)}/4 generated in {elapsed/60:.1f} min[/bold green]",
                        border_style="green"))
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)

if __name__ == "__main__":
    asyncio.run(main())
