"""
⚡ SNOW TEST - OPTION 3 FACE MATH ⚡
10 Female Anime Characters | Facial IP Extraction + Generation
75s buffer | 250s mega-buffer every 4 | Canon R6 Mark II @ f/2.0, 4K
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
from rich.live import Live
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

# 10 Female Anime Characters
CHARACTERS = [
    {
        "name": "Yoruichi_Shihouin",
        "show": "Bleach",
        "description": """
        Yoruichi Shihouin from Bleach.
        
        APPEARANCE:
        - Dark brown/tan skin
        - GOLDEN/AMBER cat-like eyes (distinctive)
        - Long PURPLE hair (usually in ponytail or flowing)
        - Athletic, muscular but feminine build
        - Confident, playful smirk
        
        COSTUME OPTIONS:
        - Black stealth suit (skin-tight combat outfit)
        - OR casual orange tracksuit/jacket
        - Barefoot or simple sandals
        
        STYLE: Feline grace, athletic, stealth ninja queen
        EXPRESSION: Confident, teasing, slightly mischievous
        """,
        "scene": "Dark rooftops at night, moonlight, ninja stealth atmosphere"
    },
    {
        "name": "Nana_Osaki",
        "show": "Nana",
        "description": """
        Nana Osaki from Nana.
        
        APPEARANCE:
        - Pale skin with punk aesthetic
        - Short, spiky BLACK hair
        - Heavy eye makeup (dark eyeliner, smoky eyes)
        - Multiple piercings (ears, possibly lip or nose)
        - Slim, tall figure
        
        COSTUME:
        - Black leather jacket
        - Band t-shirt or corset top
        - Choker necklace
        - Cigarette optional (punk aesthetic)
        - Studded accessories
        
        STYLE: Punk rock goddess, moody, intense
        EXPRESSION: Brooding, melancholic, fierce
        """,
        "scene": "Moody bar or stage with dramatic single spotlight, smoke atmosphere"
    },
    {
        "name": "Mikasa_Ackerman",
        "show": "Attack on Titan",
        "description": """
        Mikasa Ackerman from Attack on Titan.
        
        APPEARANCE:
        - Pale skin with East Asian features
        - Short black hair (chin-length bob)
        - Intense, sharp gaze
        - Athletic, muscular build
        - Serious, stoic expression
        
        COSTUME:
        - Survey Corps military jacket (tan/brown with wings of freedom patch)
        - White pants
        - ODM gear harness (straps)
        - RED SCARF around neck (ESSENTIAL)
        
        STYLE: Elite soldier, deadly calm, protective
        EXPRESSION: Serious, determined, slightly sad
        """,
        "scene": "Wall Maria backdrop or battlefield, stormy sky, dramatic wind"
    },
    {
        "name": "Faye_Valentine",
        "show": "Cowboy Bebop",
        "description": """
        Faye Valentine from Cowboy Bebop.
        
        APPEARANCE:
        - Pale/fair skin
        - Short, shaggy purple/dark violet hair
        - Green eyes
        - Curvy, athletic figure
        - Confident, seductive expression
        
        COSTUME:
        - YELLOW crop top/bandeau
        - YELLOW hot pants/shorts
        - White thigh-high stockings
        - Red jacket/shrug (sometimes)
        - Suspenders
        
        STYLE: Retro sci-fi femme fatale, confident, dangerous
        EXPRESSION: Playful smirk, knowing look, slightly cocky
        """,
        "scene": "Bebop ship interior or casino, neon lights, noir atmosphere"
    },
    {
        "name": "Nico_Robin",
        "show": "One Piece",
        "description": """
        Nico Robin from One Piece.
        
        APPEARANCE:
        - Tan/olive skin
        - Long, straight black hair
        - Blue eyes
        - Tall, elegant, slim figure
        - Calm, mature expression
        
        COSTUME OPTIONS:
        - Long elegant dress (purple or dark)
        - OR casual crop top and long skirt
        - Sunglasses on head optional
        - Minimal jewelry
        
        STYLE: Elegant archaeologist, intellectual, mysterious
        EXPRESSION: Calm, slight mysterious smile, knowing
        """,
        "scene": "Library or ancient ruins, warm golden light, scholarly atmosphere"
    },
    {
        "name": "Rukia_Kuchiki",
        "show": "Bleach",
        "description": """
        Rukia Kuchiki from Bleach.
        
        APPEARANCE:
        - Pale/fair skin
        - Short black hair (chin-length, one strand between eyes)
        - Violet/purple eyes
        - Petite, small frame
        - Serious but soft expression
        
        COSTUME:
        - Black Shinigami shihakusho (kimono robes)
        - White obi sash
        - Zanpakuto at hip optional
        
        STYLE: Noble soul reaper, dignified but warm
        EXPRESSION: Serious, determined, hint of kindness
        """,
        "scene": "Soul Society gardens or moonlit scene, serene atmosphere"
    },
    {
        "name": "Bulma",
        "show": "Dragon Ball",
        "description": """
        Bulma from Dragon Ball series.
        
        APPEARANCE:
        - Fair skin
        - BRIGHT BLUE hair (short bob or styled)
        - Blue eyes
        - Slim, fashionable figure
        - Confident, sassy expression
        
        COSTUME (style changes often):
        - Casual outfit (jeans, t-shirt, jacket)
        - OR lab coat scientist look
        - OR stylish dress
        - Always fashionable
        
        STYLE: Genius inventor, fashion-forward, confident
        EXPRESSION: Sassy, smart, slightly exasperated
        """,
        "scene": "Capsule Corp lab or futuristic city, bright clean aesthetic"
    },
    {
        "name": "Android_18",
        "show": "Dragon Ball Z",
        "description": """
        Android 18 from Dragon Ball Z.
        
        APPEARANCE:
        - Fair/pale skin
        - Blonde hair (shoulder-length bob, side-swept bangs)
        - Blue eyes
        - Athletic, toned figure
        - Cold, stoic expression
        
        COSTUME:
        - Blue/teal denim vest
        - Black undershirt or crop top
        - Blue jeans or black leggings
        - Black and white striped long sleeves
        
        STYLE: Cool android, emotionally reserved, subtly human
        EXPRESSION: Cold stare with subtle softness, neutral
        """,
        "scene": "Rocky battlefield or modern city, harsh lighting"
    },
    {
        "name": "Sailor_Mars",
        "show": "Sailor Moon",
        "description": """
        Rei Hino / Sailor Mars from Sailor Moon.
        
        APPEARANCE:
        - Fair skin with slight warmth
        - Long, straight BLACK hair (very long, past waist)
        - Violet/purple eyes
        - Slim, elegant figure
        - Intense, spiritual expression
        
        COSTUME OPTIONS:
        - Sailor Mars uniform (red skirt, white bodysuit, red bow)
        - OR Shinto shrine maiden outfit (red hakama, white haori)
        - Red high heels (Sailor form)
        
        STYLE: Fire priestess, spiritual warrior, passionate
        EXPRESSION: Intense, fierce, elegant
        """,
        "scene": "Shinto shrine at sunset or magical fire background"
    },
    {
        "name": "Sailor_Jupiter",
        "show": "Sailor Moon",
        "description": """
        Makoto Kino / Sailor Jupiter from Sailor Moon.
        
        APPEARANCE:
        - Fair skin
        - Brown/auburn hair in HIGH PONYTAIL (curly at ends)
        - Green eyes
        - Tall, athletic, strong build (tallest Sailor Scout)
        - Kind yet tough expression
        
        COSTUME:
        - Sailor Jupiter uniform (green skirt, white bodysuit, pink bow)
        - Rose earrings
        - Green high heels
        - Lightning tiara
        
        STYLE: Thunder warrior, tough girl with sweet heart
        EXPRESSION: Determined, friendly, protective
        """,
        "scene": "Storm clouds with lightning or flower garden contrast"
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
    
    console.print("\n[bold magenta]🔬 EXTRACTING FACIAL IP PROFILE...[/bold magenta]")
    
    prompt = """Analyze ALL photos of this female subject. Create comprehensive facial geometry JSON.
Output ONLY raw JSON (no markdown, no backticks). Start with { end with }.

{
  "profile": {
    "name": "Snow",
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
    ║   ❄️  SNOW TEST - OPTION 3 FACE MATH  ❄️                                 ║
    ║                                                                           ║
    ║   10 Female Anime Characters with Facial IP Lock                         ║
    ║                                                                           ║
    ║   Yoruichi • Nana • Mikasa • Faye • Robin                                ║
    ║   Rukia • Bulma • Android 18 • Mars • Jupiter                            ║
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
    
    # Setup paths
    input_dir = Path("c:/Yuki_Local/snow test")
    output_dir = Path("c:/Yuki_Local/snow_test_opt3_results")
    output_dir.mkdir(exist_ok=True)
    
    # Load photos
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    console.print(f"\n[cyan]📸 Loading {len(input_images)} reference photos...[/cyan]")
    
    image_parts = []
    image_files = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        image_files.append(img.name)
        console.print(f"   [dim]✓ {img.name}[/dim]")
    
    best_photo = image_parts[0]
    console.print(f"[green]✅ Loaded {len(image_parts)} photos[/green]")
    
    # Extract Facial IP
    facial_ip = await extract_facial_ip(client, image_parts, image_files)
    
    # Save facial IP
    ip_path = output_dir / "snow_facial_ip.json"
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
    
    summary = Table(title="❄️ SNOW TEST OPT3 RESULTS", box=box.DOUBLE_EDGE)
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
    
    console.print("\n[bold green]✨ SNOW TEST OPTION 3 COMPLETE! ✨[/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
