"""
⚡ SNOW TEST - MULTI-CHARACTER COSPLAY GENERATOR ⚡
Rich CLI with animations, progress bars, spinners
Characters: Foxxy Love, Aggretsuko, Nezuko, Vecna
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich import box
from rich.layout import Layout
from rich.align import Align
import subprocess
import time

console = Console()

# Configuration - Gemini 3 Pro Image ONLY
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"  # Required for gemini-3-pro-image-preview
MODEL = "gemini-3-pro-image-preview"  # TRUE Gemini 3 - NO 2.0 EVER
BUFFER_SECONDS = 100  # 100 second buffer between generations

# Character definitions
CHARACTERS = [
    {
        "name": "Foxxy_Love",
        "show": "Drawn Together",
        "description": """
        Foxxy Love from the adult animated series Drawn Together.
        
        COSTUME & APPEARANCE:
        - Sexy purple/magenta halter top with cutout details
        - Purple/magenta short skirt or hot pants
        - Long flowing black hair, voluminous and curly
        - Purple headband or hair accessory
        - Hoop earrings
        - Confident, sassy expression
        - 70s funk/disco vibes
        
        STYLE: Stylized cartoon-inspired but photorealistic cosplay
        MOOD: Sassy, confident, fun, flirty attitude
        """,
        "scene": "Colorful disco/party background with neon lights"
    },
    {
        "name": "Aggretsuko",
        "show": "Aggretsuko (Sanrio)",
        "description": """
        Retsuko from Aggretsuko - the death metal singing red panda.
        
        COSTUME & APPEARANCE:
        - Office lady outfit: White button-up blouse
        - Navy blue pencil skirt
        - Red panda-inspired makeup with reddish tones
        - Red panda ear headband (cute plush ears)
        - Cute but slightly frustrated expression
        - Office worker aesthetic
        
        OPTIONAL: Microphone as prop for death metal mode
        
        STYLE: Cute Japanese office worker cosplay with kawaii elements
        MOOD: Cute on surface, hidden rage underneath, relatable
        """,
        "scene": "Modern office environment or karaoke room setting"
    },
    {
        "name": "Nezuko",
        "show": "Demon Slayer",
        "description": """
        Nezuko Kamado from Demon Slayer (Kimetsu no Yaiba).
        
        COSTUME & APPEARANCE:
        - Pink kimono with hemp leaf (asanoha) pattern
        - Black haori (jacket) over the kimono
        - Pink obi sash
        - Bamboo muzzle/gag in mouth (iconic accessory)
        - Long black hair with orange/red tips
        - Pink ribbon/bow in hair
        - Demon slayer aesthetic with slight demon features
        - Innocent but powerful expression
        
        STYLE: Traditional Japanese with supernatural elements
        MOOD: Protective, innocent, fierce when needed
        """,
        "scene": "Traditional Japanese forest at twilight with soft lighting"
    },
    {
        "name": "Vecna",
        "show": "Stranger Things",
        "description": """
        Vecna (Henry Creel/One) from Stranger Things Season 4.
        
        COSTUME & APPEARANCE:
        - Heavily textured skin prosthetics/makeup (vine-like patterns)
        - Exposed muscle and tendon appearance
        - Dark, decaying flesh tones (grays, browns, reds)
        - No nose, sunken features
        - Glowing reddish eyes or intense stare
        - Bald head with textured scalp
        - Long, claw-like fingers
        - Dark, flowing tattered robes or tendrils
        
        MAKEUP: Full SFX horror makeup transformation
        STYLE: High-end horror prosthetics and practical effects
        MOOD: Menacing, otherworldly, terrifying presence
        """,
        "scene": "Dark Upside Down environment with floating particles and red lightning"
    }
]

def create_banner():
    """Create animated banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║   ❄️  S N O W   T E S T   -   M U L T I   C H A R A C T E R  ❄️    ║
    ║                                                                      ║
    ║   🦊 Foxxy Love  •  🐼 Aggretsuko  •  👘 Nezuko  •  👹 Vecna        ║
    ║                                                                      ║
    ║   Model: gemini-3-pro-image-preview | Location: global              ║
    ║   Buffer: 100s | Aspect: 9:16 | DNA-Locked                          ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
    return Panel(
        Text(banner, style="bold cyan", justify="center"),
        box=box.DOUBLE_EDGE,
        border_style="bright_magenta"
    )

def build_prompt(character: dict) -> str:
    """Build enhanced prompt with facial DNA lock + photography specs + 9:16"""
    return f"""
═══════════════════════════════════════════════════════════════════════════════
PROFESSIONAL COSPLAY PHOTOGRAPHY - {character['name'].upper()} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

You are creating a PROFESSIONAL PHOTOGRAPH of this person in {character['name']} cosplay.
This must look like it was shot by a professional photographer with a high-end camera.

═══════════════════════════════════════════════════════════════════════════════
🔒 FACIAL DNA LOCK - MULTI-REFERENCE MAPPING (14 PHOTOS) 🔒
═══════════════════════════════════════════════════════════════════════════════

You have been provided with 14 reference photos of the SAME PERSON from different angles.
Use ALL of these photos to build a comprehensive understanding of their facial structure.

ANALYZE ACROSS ALL 14 REFERENCES:

BONE STRUCTURE:
- Their exact face shape and bone structure
- Their exact jawline contour
- Their exact cheekbone placement and height
- Their exact chin shape and size

SKIN:
- Their exact skin tone and complexion
- Their skin texture and natural characteristics
- Preserve any natural beauty marks or features

FEATURES - COPY PRECISELY:
- Their exact nose shape, bridge, and tip
- Their exact lip shape, fullness, and proportions
- Their exact eye shape, size, and spacing
- Their exact eyebrow shape and arch
- Any piercings or distinctive features - KEEP THEM

THE FINAL FACE MUST BE RECOGNIZABLE AS THE SAME PERSON.
If their own family looked at the photo, they would immediately recognize them.

═══════════════════════════════════════════════════════════════════════════════
CHARACTER: {character['name']} - {character['show']}
═══════════════════════════════════════════════════════════════════════════════

{character['description']}

═══════════════════════════════════════════════════════════════════════════════
📷 PROFESSIONAL PHOTOGRAPHY SPECIFICATIONS
═══════════════════════════════════════════════════════════════════════════════

CAMERA & LENS:
- Shot on Sony A7R V or Canon EOS R5
- 85mm f/1.4 portrait lens
- Shallow depth of field, f/1.8-2.8
- Sharp focus on eyes and face
- Natural bokeh in background

LIGHTING:
- Professional 3-point lighting setup
- Key light: Soft, diffused from 45 degrees
- Fill light: Subtle, reducing harsh shadows
- Rim/hair light: Creating separation from background
- Catch lights visible in eyes

IMAGE QUALITY:
- 8K resolution, ultra-sharp details
- Professional color grading
- Natural skin tones, no over-smoothing
- Visible skin texture (realistic)
- No artificial HDR or over-processing

COMPOSITION:
- ASPECT RATIO: 9:16 vertical portrait (1080x1920)
- Full body shot showing head to feet or mid-thigh
- Subject centered, using rule of thirds
- {character['scene']}

REALISM REQUIREMENTS:
- This must look like a REAL photograph, not AI-generated
- Natural fabric wrinkles and texture in costume
- Realistic hair physics and individual strands visible
- Natural shadowing on face and body
- Professional magazine or portfolio quality

═══════════════════════════════════════════════════════════════════════════════
OUTPUT: Generate ONE ultra-realistic professional cosplay photograph in 9:16
═══════════════════════════════════════════════════════════════════════════════
"""

async def countdown_timer(seconds: int, description: str):
    """Animated countdown timer"""
    with Progress(
        SpinnerColumn("dots12"),
        TextColumn("[bold yellow]{task.description}"),
        BarColumn(bar_width=50, complete_style="cyan", finished_style="green"),
        TextColumn("[bold cyan]{task.fields[remaining]}s remaining"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task(description, total=seconds, remaining=seconds)
        for i in range(seconds, 0, -1):
            progress.update(task, advance=1, remaining=i-1)
            await asyncio.sleep(1)

async def generate_all_characters():
    """Generate all character transformations with rich output"""
    
    console.print(create_banner())
    console.print()
    
    # Initialize client
    with console.status("[bold cyan]⚡ Initializing Gemini 3 Pro Image...", spinner="dots12"):
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
        await asyncio.sleep(1)
    console.print("[bold green]✅ Gemini 3 Pro Image client ready!")
    console.print()
    
    # Setup paths
    input_dir = Path("c:/Yuki_Local/snow test")
    output_dir = Path("c:/Yuki_Local/snow_test_results")
    output_dir.mkdir(exist_ok=True)
    
    # Get first image for testing
    input_images = list(input_dir.glob("*.jpg"))
    if not input_images:
        console.print("[bold red]❌ No images found in snow test folder!")
        return
    
    input_path = input_images[0]  # Use first image
    
    # Status table
    status_table = Table(box=box.ROUNDED, border_style="cyan")
    status_table.add_column("Setting", style="bold yellow")
    status_table.add_column("Value", style="green")
    status_table.add_row("🎯 Model", MODEL)
    status_table.add_row("🌍 Location", LOCATION)
    status_table.add_row("📁 Input", str(input_path.name))
    status_table.add_row("📂 Output", str(output_dir))
    status_table.add_row("⏱️ Buffer", f"{BUFFER_SECONDS}s between generations")
    status_table.add_row("📐 Aspect", "9:16 vertical")
    console.print(status_table)
    console.print()
    
    # Load ALL images for multi-reference facial mapping (up to 14)
    input_images = sorted(input_dir.glob("*.jpg"))[:14]  # Max 14 references
    
    with console.status(f"[bold cyan]📸 Loading {len(input_images)} reference photos for facial DNA mapping...", spinner="arc"):
        image_parts = []
        for img_path in input_images:
            with open(img_path, "rb") as f:
                img_data = f.read()
            image_parts.append(types.Part.from_bytes(data=img_data, mime_type="image/jpeg"))
        await asyncio.sleep(0.5)
    
    console.print(f"[bold green]✅ Loaded {len(image_parts)} reference photos for comprehensive facial bone mapping!")
    for img in input_images:
        console.print(f"   [dim]📷 {img.name}[/dim]")
    console.print()
    
    results = []
    start_time = time.time()
    
    for i, character in enumerate(CHARACTERS, 1):
        # Character header
        char_panel = Panel(
            f"[bold magenta]🎭 [{i}/4] {character['name']}[/bold magenta]\n"
            f"[dim]From: {character['show']}[/dim]",
            box=box.ROUNDED,
            border_style="magenta"
        )
        console.print(char_panel)
        
        prompt = build_prompt(character)
        
        # Generation progress
        with Progress(
            SpinnerColumn("dots12"),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task(f"⚡ Generating {character['name']}...", total=100)
            
            try:
                progress.update(task, advance=10, description=f"⚡ Sending to Gemini 3...")
                
                response = await client.aio.models.generate_content(
                    model=MODEL,
                    contents=[prompt] + image_parts,  # Prompt + all 14 reference images
                    config=types.GenerateContentConfig(
                        temperature=1.0,
                        top_p=0.95,
                        top_k=40,
                        response_modalities=["IMAGE", "TEXT"],
                        safety_settings=[
                            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
                            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
                            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_ONLY_HIGH"),
                            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
                        ]
                    )
                )
                
                progress.update(task, advance=60, description="🎨 Processing response...")
                
                # Extract and save
                saved = False
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        progress.update(task, advance=20, description="💾 Saving image...")
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{character['name']}_{timestamp}.png"
                        save_path = output_dir / filename
                        
                        with open(save_path, "wb") as f:
                            f.write(part.inline_data.data)
                        
                        progress.update(task, advance=10, description="✅ Complete!")
                        
                        size_kb = save_path.stat().st_size / 1024
                        results.append({
                            "character": character['name'],
                            "show": character['show'],
                            "path": save_path,
                            "size": size_kb
                        })
                        
                        # Success output
                        console.print()
                        success_table = Table(box=box.ROUNDED, border_style="green")
                        success_table.add_column("✅ SUCCESS", style="bold green")
                        success_table.add_column("Details", style="white")
                        success_table.add_row("📁 File", filename)
                        success_table.add_row("📐 Size", f"{size_kb:.1f} KB")
                        console.print(success_table)
                        saved = True
                        break
                
                if not saved:
                    console.print("[yellow]   ⚠️ No image in response (text response only)[/yellow]")
                    
            except Exception as e:
                error_msg = str(e)[:100]
                console.print(f"[bold red]   ❌ Error: {error_msg}...[/bold red]")
                results.append({
                    "character": character['name'],
                    "show": character['show'],
                    "error": error_msg
                })
        
        # Buffer countdown (if not last)
        if i < len(CHARACTERS):
            console.print()
            await countdown_timer(BUFFER_SECONDS, f"⏳ Cooling down before next generation...")
            console.print()
    
    # Final summary
    elapsed = time.time() - start_time
    console.print()
    console.print("=" * 70)
    
    summary_table = Table(title="⚡ GENERATION COMPLETE ⚡", box=box.DOUBLE_EDGE, border_style="bright_yellow")
    summary_table.add_column("Character", style="magenta")
    summary_table.add_column("Show", style="cyan")
    summary_table.add_column("Status", style="green")
    summary_table.add_column("Size", style="white")
    
    for r in results:
        if "path" in r:
            summary_table.add_row(r['character'], r['show'], "✅ Success", f"{r['size']:.0f} KB")
        else:
            summary_table.add_row(r['character'], r['show'], "❌ Failed", "-")
    
    console.print(summary_table)
    console.print()
    console.print(f"[bold cyan]⏱️ Total time: {elapsed/60:.1f} minutes[/bold cyan]")
    console.print(f"[bold green]📂 Output: {output_dir}[/bold green]")
    console.print()
    
    # Auto-open folder
    console.print("[bold green]📂 Opening output folder...[/bold green]")
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    
    return results

if __name__ == "__main__":
    asyncio.run(generate_all_characters())
