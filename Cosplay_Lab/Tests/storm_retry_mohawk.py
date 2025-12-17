"""
⚡ STORM MOHAWK RETRY - Rich Animated CLI ⚡
Sugar-rich visuals with progress animations
"""

import asyncio
import base64
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich import box
import subprocess
import os
import time

console = Console()

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"  # gemini-3-pro-image-preview requires global endpoint
MODEL = "gemini-3-pro-image-preview"  # TRUE Gemini 3 Pro Image

MOHAWK_STORM = {
    "name": "Mohawk_Punk_Storm",
    "description": """
    Storm in her iconic 80s PUNK/MOHAWK era look.
    
    COSTUME DETAILS:
    - Black leather punk jacket with silver studs
    - Black leather pants or leggings
    - Silver chains and punk accessories
    - Combat boots with buckles
    - Fishnet elements under leather
    
    STORM'S SIGNATURE:
    - Dramatic WHITE MOHAWK hairstyle, shaved sides
    - Intense eyes with dark dramatic makeup
    - Confident, rebellious expression
    - Lightning crackling around her
    
    SETTING: Urban rooftop at night, neon city lights below,
    storm clouds gathering above. Gritty, punk aesthetic.
    
    MOOD: Rebellious, fierce, "don't mess with me" energy, punk goddess
    """
}

def create_banner():
    """Create animated banner"""
    banner_text = """
    ⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡
    
         🌩️  S T O R M   C O S P L A Y   G E N E R A T O R  🌩️
         
              ⚡ MOHAWK PUNK EDITION - 4K ULTRA ⚡
    
    ⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡
    """
    return Panel(
        Text(banner_text, style="bold cyan", justify="center"),
        box=box.DOUBLE_EDGE,
        border_style="bright_yellow"
    )

async def generate_mohawk():
    """Generate Mohawk Storm with rich visuals"""
    
    console.print(create_banner())
    console.print()
    
    # Status table
    status_table = Table(box=box.ROUNDED, border_style="cyan")
    status_table.add_column("Setting", style="bold yellow")
    status_table.add_column("Value", style="green")
    status_table.add_row("🎯 Model", MODEL)
    status_table.add_row("📁 Project", PROJECT_ID)
    status_table.add_row("🌍 Region", LOCATION)
    status_table.add_row("⚡ Version", "Mohawk Punk Storm")
    console.print(status_table)
    console.print()
    
    # Initialize client with spinner
    with console.status("[bold cyan]⚡ Initializing Gemini 3 Pro Image...", spinner="dots12"):
        client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=LOCATION
        )
        await asyncio.sleep(1)
    console.print("[bold green]✅ Gemini client initialized!")
    
    # Load image with spinner
    input_path = Path("c:/Yuki_Local/storm_input.png")
    output_dir = Path("c:/Yuki_Local/storm_results")
    
    with console.status("[bold cyan]📸 Loading your photo...", spinner="arc"):
        with open(input_path, "rb") as f:
            image_data = f.read()
        image_part = types.Part.from_bytes(data=image_data, mime_type="image/png")
        await asyncio.sleep(0.5)
    
    size_kb = len(image_data) / 1024
    console.print(f"[bold green]✅ Photo loaded! [dim]({size_kb:.1f} KB)[/dim]")
    console.print()
    
    # Build the prompt
    prompt = f"""
    TASK: Transform this person into Storm from Marvel X-Men.
    
    ═══════════════════════════════════════════════════════════════
    ⚠️ CRITICAL IDENTITY PRESERVATION (DNA-AUTHENTIC) ⚠️
    ═══════════════════════════════════════════════════════════════
    
    PRESERVE EXACTLY (DO NOT CHANGE):
    - Her EXACT face shape, bone structure, and facial proportions
    - Her beautiful dark brown/black skin tone (Fitzpatrick Type V-VI)
    - Her exact nose shape and nose ring/septum piercing
    - Her exact lip shape and size
    - Her exact eye shape and warm brown eye color
    - Her exact eyebrow shape and arch
    - Her makeup style (dark lips, lashes)
    - Her natural beauty and elegance
    
    ═══════════════════════════════════════════════════════════════
    CHARACTER TRANSFORMATION: STORM - MOHAWK PUNK ERA
    ═══════════════════════════════════════════════════════════════
    
    {MOHAWK_STORM['description']}
    
    ═══════════════════════════════════════════════════════════════
    TECHNICAL REQUIREMENTS
    ═══════════════════════════════════════════════════════════════
    
    - Resolution: 4K ultra-high definition
    - Style: Photorealistic professional cosplay photography
    - Lighting: Dramatic cinematic lighting with storm effects
    - Camera: Full body or 3/4 shot, heroic angle
    - Quality: Cover of Marvel Comics or movie poster quality
    - Aspect Ratio: Portrait orientation
    
    CREATE AN EPIC, POWERFUL IMAGE OF HER AS PUNK STORM!
    """
    
    # Generation with animated progress
    console.print(Panel(
        "[bold magenta]🌩️ GENERATING: Mohawk Punk Storm[/bold magenta]\n\n"
        "[dim]Leather jacket • White mohawk • Punk goddess energy[/dim]",
        box=box.ROUNDED,
        border_style="magenta"
    ))
    
    with Progress(
        SpinnerColumn("dots12"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=40),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task = progress.add_task("⚡ Calling Gemini 3 Pro Image...", total=100)
        
        try:
            # Simulate progress while waiting for API
            progress.update(task, advance=10, description="⚡ Sending to AI...")
            
            response = await client.aio.models.generate_content(
                model=MODEL,
                contents=[prompt, image_part],
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
            
            # Extract and save image
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    progress.update(task, advance=20, description="💾 Saving 4K image...")
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"Storm_Mohawk_Punk_{timestamp}.png"
                    save_path = output_dir / filename
                    
                    image_bytes = part.inline_data.data
                    with open(save_path, "wb") as f:
                        f.write(image_bytes)
                    
                    progress.update(task, advance=10, description="✅ Complete!")
                    await asyncio.sleep(0.5)
                    
                    # Success output
                    console.print()
                    result_table = Table(box=box.DOUBLE_EDGE, border_style="green")
                    result_table.add_column("🎉 SUCCESS", style="bold green")
                    result_table.add_column("Details", style="white")
                    result_table.add_row("📁 File", filename)
                    result_table.add_row("📐 Size", f"{save_path.stat().st_size / 1024:.1f} KB")
                    result_table.add_row("📍 Path", str(save_path))
                    console.print(result_table)
                    
                    return save_path
                    
        except Exception as e:
            progress.update(task, description=f"[red]❌ Error![/red]")
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
            return None
    
    console.print("[yellow]⚠️ No image in response[/yellow]")
    return None

async def main():
    """Main entry with final summary"""
    start_time = time.time()
    
    result = await generate_mohawk()
    
    elapsed = time.time() - start_time
    
    console.print()
    console.print(Panel(
        f"[bold cyan]⚡ Generation Complete in {elapsed:.1f}s ⚡[/bold cyan]\n\n"
        f"[green]📁 Check: c:\\Yuki_Local\\storm_results\\[/green]",
        box=box.DOUBLE_EDGE,
        border_style="bright_yellow"
    ))
    
    # List all Storm images
    console.print()
    console.print("[bold yellow]🌩️ All Storm Versions Generated:[/bold yellow]")
    output_dir = Path("c:/Yuki_Local/storm_results")
    for f in output_dir.glob("Storm_*.png"):
        console.print(f"   [cyan]⚡[/cyan] {f.name} [dim]({f.stat().st_size/1024:.0f}KB)[/dim]")
    
    # Auto-open folder in Windows Explorer
    console.print()
    console.print("[bold green]📂 Opening output folder...[/bold green]")
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)

if __name__ == "__main__":
    asyncio.run(main())

