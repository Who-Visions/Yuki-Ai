"""
⚡ SNOW TEST 2 - OPTION 3 FACE MATH ⚡
10 Female Anime Characters (New Set) | Facial IP Extraction + Generation
75s buffer | 250s mega-buffer every 4 | Canon R6 Mark II @ f/2.0, 4K
References: C:\Yuki_Local\snow test 2
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
import re

console = Console()

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
MODEL = "gemini-3-pro-image-preview"
TEXT_MODEL = "gemini-2.5-flash"
BUFFER_SECONDS = 75
MEGA_BUFFER_SECONDS = 250
MEGA_BUFFER_EVERY = 4

CAMERA_SPEC = """
CAMERA: Canon EOS R6 Mark II
LENS: RF 85mm f/1.2L USM @ f/2.0
RESOLUTION: 4K (9:16 vertical portrait)
LIGHTING: Professional cinematic lighting with dramatic shadows
QUALITY: Magazine cover quality, natural skin texture, no smoothing
"""

# 10 New Female Anime Characters
CHARACTERS = [
    {
        "name": "Nobara_Kugisaki",
        "show": "Jujutsu Kaisen",
        "description": """
        Nobara Kugisaki from Jujutsu Kaisen.
        
        APPEARANCE:
        - Short brown/orange-brown hair (bob cut, styled)
        - Sharp, confident eyes
        - Pretty face with fierce expression
        - Athletic, feminine build
        
        COSTUME:
        - Jujutsu High school uniform (dark blue/black)
        - Modified uniform jacket
        - Black boots
        - Hammer and nails as weapons (optional)
        
        STYLE: Pretty, lethal, petty in the best way
        EXPRESSION: Confident smirk, ready to fight
        """,
        "scene": "Urban Tokyo streets or cursed domain, dramatic lighting"
    },
    {
        "name": "Maki_Zenin",
        "show": "Jujutsu Kaisen",
        "description": """
        Maki Zenin from Jujutsu Kaisen.
        
        APPEARANCE:
        - Dark green/black hair in HIGH PONYTAIL
        - RED-framed glasses (ESSENTIAL)
        - Athletic, muscular build (fighter body)
        - Stoic, confident expression
        - Sharp features
        
        COSTUME:
        - Jujutsu High uniform
        - Sometimes modified for combat
        - Polearm weapon (cursed tool)
        
        STYLE: Confident, stoic, powerful
        EXPRESSION: Calm intensity, slight superiority
        """,
        "scene": "Training grounds or battlefield, focused lighting"
    },
    {
        "name": "Kallen_Stadtfeld",
        "show": "Code Geass",
        "description": """
        Kallen Stadtfeld/Kozuki from Code Geass.
        
        APPEARANCE:
        - Bright RED spiky hair (distinctive)
        - Blue eyes
        - Athletic, slim figure
        - Fierce, rebellious expression
        
        COSTUME OPTIONS:
        - Red/white pilot suit (Guren cockpit)
        - OR Ashford Academy school uniform (beige/brown)
        - OR Black Knights uniform
        
        STYLE: Rebellious fighter, passionate revolutionary
        EXPRESSION: Determined, fierce, ready for battle
        """,
        "scene": "Mecha cockpit or resistance headquarters, dramatic red/black lighting"
    },
    {
        "name": "Ryuko_Matoi",
        "show": "Kill la Kill",
        "description": """
        Ryuko Matoi from Kill la Kill.
        
        APPEARANCE:
        - Short, spiky dark blue/black hair
        - RED STREAK on left side (ESSENTIAL)
        - Blue eyes
        - Athletic, toned figure
        - Aggressive, defiant expression
        
        COSTUME:
        - Modified dark blue sailor uniform
        - Red scarf/accent
        - Scissor blade weapon (optional)
        - Senketsu aesthetic (red accents)
        
        STYLE: Delinquent hero, aggressive action vibes
        EXPRESSION: Fierce scowl, confrontational
        """,
        "scene": "Honnouji Academy or urban battleground, intense lighting"
    },
    {
        "name": "Satsuki_Kiryuin",
        "show": "Kill la Kill",
        "description": """
        Satsuki Kiryuin from Kill la Kill.
        
        APPEARANCE:
        - Very long, straight BLACK hair (extremely long)
        - Sharp blue eyes
        - Regal, commanding presence
        - Tall, elegant figure
        - Dominant, imperious expression
        
        COSTUME:
        - WHITE Honnouji Academy uniform (modified, regal)
        - Large eyebrows (thick, dramatic)
        - Bakuzan sword at side optional
        
        STYLE: Empress, dominant ruler, absolute authority
        EXPRESSION: Cold superiority, commanding stare
        """,
        "scene": "Top of Honnouji Academy stairs, dramatic upward angle, sunset"
    },
    {
        "name": "Winry_Rockbell",
        "show": "Fullmetal Alchemist",
        "description": """
        Winry Rockbell from Fullmetal Alchemist.
        
        APPEARANCE:
        - Long BLONDE hair in high ponytail
        - Blue eyes
        - Soft, kind face
        - Slim but strong build (mechanic's arms)
        - Warm, friendly expression
        
        COSTUME:
        - Mechanic outfit (tube top or tank top)
        - Work apron
        - Tool belt
        - Bandana in hair sometimes
        - Work gloves
        
        STYLE: Skilled automail mechanic, warm-hearted
        EXPRESSION: Friendly smile, or focused concentration
        """,
        "scene": "Rockbell automail workshop, warm golden light"
    },
    {
        "name": "Olivier_Armstrong",
        "show": "Fullmetal Alchemist Brotherhood",
        "description": """
        Olivier Mira Armstrong from Fullmetal Alchemist Brotherhood.
        
        APPEARANCE:
        - Long BLONDE hair (wavy, loose)
        - Icy blue eyes
        - Sharp, severe features
        - Tall, commanding build
        - Cold, intimidating expression
        
        COSTUME:
        - Amestris military uniform (blue)
        - Long military coat with fur collar
        - Sword at hip
        - General's rank insignia
        
        STYLE: Ice Queen commander, ruthless leader
        EXPRESSION: Icy stare, absolute authority
        """,
        "scene": "Briggs Fortress snow backdrop, cold blue lighting"
    },
    {
        "name": "Asuna_Yuuki",
        "show": "Sword Art Online",
        "description": """
        Asuna Yuuki from Sword Art Online.
        
        APPEARANCE:
        - Long chestnut/orange-brown hair
        - Amber/hazel eyes
        - Beautiful, elegant features
        - Slim, graceful figure
        - Gentle but determined expression
        
        COSTUME:
        - Knights of the Blood Oath uniform
        - White and red leather armor dress
        - Rapier sword at side
        - Red and white color scheme
        
        STYLE: Lightning Flash, gentle but battle-ready
        EXPRESSION: Kind smile, or focused determination
        """,
        "scene": "Aincrad floating castle, golden fantasy lighting"
    },
    {
        "name": "Sinon",
        "show": "Sword Art Online",
        "description": """
        Sinon (Shino Asada) from Sword Art Online.
        
        APPEARANCE:
        - Short AQUA/light blue hair (bob cut)
        - Teal/blue eyes
        - Slim, athletic figure
        - Calm, focused expression
        - Light accessories
        
        COSTUME:
        - GGO sniper outfit (futuristic)
        - Green/teal combat gear
        - Sniper rifle (Hecate II) optional
        - Tactical gear, light armor
        
        STYLE: Ice-cold sniper, precise and deadly
        EXPRESSION: Focused, calculating, calm
        """,
        "scene": "Futuristic battlefield, blue/teal sci-fi lighting"
    },
    {
        "name": "Revy",
        "show": "Black Lagoon",
        "description": """
        Revy (Rebecca Lee) from Black Lagoon.
        
        APPEARANCE:
        - TAN/brown skin (Chinese-American)
        - Long dark purple/maroon hair in ponytail
        - Brown eyes
        - Athletic, muscular build
        - Aggressive, wild expression
        
        COSTUME:
        - Black crop top/tank top (midriff showing)
        - Daisy duke shorts (cut-off jeans)
        - Combat boots
        - TWIN Beretta pistols in holsters
        - Tribal tattoo on right arm
        
        STYLE: Chaotic gunfighter, foul-mouthed mercenary
        EXPRESSION: Wild grin, dangerous, unhinged
        """,
        "scene": "Roanapur docks at night, neon signs, smoke atmosphere"
    }
]

async def animated_countdown(seconds: int, desc: str, mega: bool = False):
    """Animated countdown with rich visuals"""
    color = "bold yellow" if mega else "cyan"
    emoji = "🔥" if mega else "⏳"
    
    with Progress(
        SpinnerColumn("dots12"),
        TextColumn(f"[{color}]{emoji} {desc}"),
        BarColumn(bar_width=50, complete_style="green" if not mega else "yellow"),
        TextColumn("[bold cyan]{task.fields[remaining]}s remaining"),
        TimeElapsedColumn(),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("", total=seconds, remaining=seconds)
        for i in range(seconds, 0, -1):
            progress.update(task, advance=1, remaining=i-1)
            await asyncio.sleep(1)

async def extract_facial_ip(client, image_parts: list, image_files: list) -> dict:
    """Extract comprehensive facial geometry JSON"""
    
    console.print("\n[bold magenta]🔬 EXTRACTING FACIAL IP PROFILE (SNOW 2)...[/bold magenta]")
    
    prompt = """Analyze ALL photos of this female subject. Create comprehensive facial geometry JSON.
Output ONLY raw JSON (no markdown, no backticks). Start with { end with }.

{
  "profile": {
    "name": "Snow2",
    "role": "Reference Template",
    "platform": "Yuki DNA-Authentic Cosplay"
  },
  "demographics": {
    "ethnicity": "<observed>",
    "gender": "Female",
    "age_range": "<estimate>",
    "fitzpatrick": "<I-VI>",
    "undertone": "<warm/cool/neutral>"
  },
  "bone_structure": {
    "face_shape": "<shape>",
    "jawline": "<description>",
    "cheekbones": "<description>",
    "chin": "<description>",
    "forehead": "<description>"
  },
  "nose": {
    "bridge": "<description>",
    "tip": "<description>",
    "width": "<description>",
    "nostrils": "<description>",
    "piercings": "<any>"
  },
  "lips": {
    "fullness": "<level>",
    "upper": "<description>",
    "lower": "<description>",
    "width": "<relative>",
    "cupids_bow": "<defined/subtle/flat>"
  },
  "eyes": {
    "shape": "<shape>",
    "size": "<relative>",
    "spacing": "<close/average/wide>",
    "color": "<color>",
    "eyelids": "<type>"
  },
  "eyebrows": {
    "shape": "<shape>",
    "thickness": "<level>",
    "arch": "<position>"
  },
  "hair": {
    "texture": "<type>",
    "color": "<color>",
    "style": "<current>",
    "length": "<length>"
  },
  "skin": {
    "tone": "<description>",
    "texture": "<description>",
    "notable_marks": "<any>"
  },
  "distinctive_features": ["<list unique features>"],
  "identity_priorities": [
    "1. <most critical to preserve>",
    "2. <second>",
    "3. <third>",
    "4. <fourth>",
    "5. <fifth>"
  ],
  "generation_rules": {
    "must_preserve": ["<list>"],
    "can_modify": ["<list>"],
    "never_modify": ["<list>"]
  }
}

Be thorough and specific based on all photos."""

    with console.status("[cyan]   Analyzing facial geometry from all photos...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=TEXT_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=3000)
        )
    
    text = response.text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        profile = json.loads(text[start:end]) if start >= 0 else {"raw": text}
    except:
        profile = {"raw": text}
    
    profile["_metadata"] = {
        "created": datetime.now().isoformat(),
        "sources": image_files,
        "version": "1.0.0"
    }
    
    console.print(f"[green]   ✅ Facial IP extracted ({len(json.dumps(profile))} chars)[/green]")
    return profile

async def generate_image(client, prompt: str, photo, output_path: Path) -> bool:
    """Generate single image"""
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
PROFESSIONAL ANIME COSPLAY PHOTOGRAPHY - {character['name'].replace('_', ' ')} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

Create a PROFESSIONAL PHOTOGRAPH of this person as {character['name'].replace('_', ' ')}.

═══════════════════════════════════════════════════════════════════════════════
🔒 FACIAL GEOMETRY PROFILE (FACE MATH - IDENTITY LOCK) 🔒
═══════════════════════════════════════════════════════════════════════════════

{geometry}

USE THESE GEOMETRIC RATIOS. The face MUST be IMMEDIATELY RECOGNIZABLE as this person.
Preserve bone structure, skin tone, eye shape, nose shape, lip shape EXACTLY.

═══════════════════════════════════════════════════════════════════════════════
CHARACTER: {character['name'].replace('_', ' ')} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

{character['description']}

═══════════════════════════════════════════════════════════════════════════════
📷 CAMERA SPECIFICATIONS
═══════════════════════════════════════════════════════════════════════════════

{CAMERA_SPEC}

COMPOSITION: 9:16 vertical portrait, full body or 3/4 shot
SCENE: {character['scene']}

Generate ONE ultra-realistic professional cosplay photograph.
═══════════════════════════════════════════════════════════════════════════════
"""

async def main():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   ❄️  SNOW TEST 2 - OPTION 3 FACE MATH  ❄️                               ║
    ║                                                                           ║
    ║   10 Female Anime Characters (New Set) with Facial IP Lock              ║
    ║                                                                           ║
    ║   Nobara • Maki • Kallen • Ryuko • Satsuki                               ║
    ║   Winry • Olivier • Asuna • Sinon • Revy                                 ║
    ║                                                                           ║
    ║   Buffer: 75s | Mega-Buffer: 250s every 4                                ║
    ║   Camera: Canon R6 Mark II @ f/2.0, 4K                                   ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", box=box.DOUBLE_EDGE))
    
    # Initialize
    with console.status("[bold cyan]⚡ Initializing Gemini client...", spinner="dots12"):
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    console.print("[green]✅ Client ready![/green]")
    
    # Setup paths - SNOW TEST 2
    input_dir = Path("c:/Yuki_Local/snow test 2")
    output_dir = Path("c:/Yuki_Local/snow_test2_opt3_results")
    output_dir.mkdir(exist_ok=True)
    
    # Load photos
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    if not input_images:
        input_images = sorted(input_dir.glob("*.JPG"))[:14]
    if not input_images:
        input_images = sorted(input_dir.glob("*.png"))[:14]
    
    console.print(f"\n[cyan]📸 Loading {len(input_images)} reference photos from snow test 2...[/cyan]")
    
    image_parts = []
    image_files = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        image_files.append(img.name)
        console.print(f"   [dim]✓ {img.name}[/dim]")
    
    if not image_parts:
        console.print("[red]❌ No images found in snow test 2 folder![/red]")
        return
    
    best_photo = image_parts[0]
    console.print(f"[green]✅ Loaded {len(image_parts)} photos[/green]")
    
    # Extract Facial IP
    facial_ip = await extract_facial_ip(client, image_parts, image_files)
    
    # Save facial IP
    ip_path = output_dir / "snow2_facial_ip.json"
    with open(ip_path, "w", encoding="utf-8") as f:
        json.dump(facial_ip, f, indent=2, ensure_ascii=False)
    console.print(f"[green]💾 Facial IP saved: {ip_path.name}[/green]")
    
    geometry_text = json.dumps(facial_ip, indent=2)
    
    results = []
    start = time.time()
    
    # Generate for each character
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
            task = prog.add_task("⚡ Generating with Face Math...", total=100)
            prog.update(task, advance=10)
            
            try:
                prompt = build_prompt(char, geometry_text)
                path = output_dir / f"OPT3_{char['name']}_{ts}.png"
                success = await generate_image(client, prompt, best_photo, path)
                
                prog.update(task, advance=90, description="✅ Complete!")
                if success:
                    size_kb = path.stat().st_size / 1024
                    console.print(f"   [green]✅ {path.name} ({size_kb:.0f} KB)[/green]")
                    results.append((char['name'], path, size_kb))
                else:
                    console.print("   [yellow]⚠️ No image returned[/yellow]")
            except Exception as e:
                error_msg = str(e)[:80]
                console.print(f"   [red]❌ {error_msg}...[/red]")
        
        # Buffer logic
        if i < len(CHARACTERS):
            if i % MEGA_BUFFER_EVERY == 0:
                console.print(f"\n[bold yellow]🔥 MEGA-BUFFER: {MEGA_BUFFER_SECONDS}s cooldown ({i} generations complete)[/bold yellow]")
                await animated_countdown(MEGA_BUFFER_SECONDS, f"MEGA-BUFFER ({i}/{len(CHARACTERS)} done)", mega=True)
            else:
                await animated_countdown(BUFFER_SECONDS, "Cooling down...")
    
    # Summary
    elapsed = time.time() - start
    console.print("\n" + "═" * 70)
    
    summary = Table(title="❄️ SNOW TEST 2 OPT3 RESULTS", box=box.DOUBLE_EDGE)
    summary.add_column("#", style="dim")
    summary.add_column("Character", style="magenta")
    summary.add_column("File", style="white")
    summary.add_column("Size", style="green")
    
    for idx, (char, path, size) in enumerate(results, 1):
        summary.add_row(str(idx), char, path.name[:35], f"{size:.0f} KB")
    
    console.print(summary)
    console.print(f"\n[cyan]⏱️ Total time: {elapsed/60:.1f} min | Generated: {len(results)}/10[/cyan]")
    console.print(f"[green]📂 Output: {output_dir}[/green]")
    console.print(f"[green]🔐 Facial IP: {ip_path}[/green]")
    
    # Open folder
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    
    console.print("\n[bold green]✨ SNOW TEST 2 OPTION 3 COMPLETE! ✨[/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
