"""
⚡ DAV3 ANIME SYNERGY TEST - 10 CHARACTERS (OPTION 1 ONLY) ⚡
Characters with natural synergy for dark skin and build
Canon R6 Mark II @ f/2.0, 4K | Buffer: 70s
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

console = Console()

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
MODEL = "gemini-3-pro-image-preview"
TEXT_MODEL = "gemini-2.5-flash"
BUFFER_SECONDS = 100

CAMERA_SPEC = """
CAMERA: Canon EOS R6 Mark II
LENS: RF 85mm f/1.2L USM @ f/2.0
RESOLUTION: 4K (9:16 vertical portrait)
LIGHTING: Professional cinematic lighting with dramatic shadows
QUALITY: Magazine cover quality, natural skin texture
"""

# 10 Anime Characters with natural synergy
CHARACTERS = [
    {
        "name": "Afro_Samurai",
        "show": "Afro Samurai",
        "description": """
        Afro from Afro Samurai.
        
        APPEARANCE:
        - Dark skin (Black man)
        - Large afro hairstyle (natural black hair)
        - Lean, muscular swordsman build
        - Intense, focused expression
        - Battle scars
        
        COSTUME:
        - Simple white cloth headband with #2 or #1 headband
        - Open traditional Japanese robe/gi (showing chest)
        - Loose hakama pants
        - Straw sandals
        - Katana sword on hip or in hand
        
        STYLE: Stylish samurai meets blaxploitation cool
        """,
        "scene": "Misty mountain path at sunset, cherry blossoms falling, cinematic wide shot"
    },
    {
        "name": "Mugen",
        "show": "Samurai Champloo",
        "description": """
        Mugen from Samurai Champloo.
        
        APPEARANCE:
        - Tan/brown skin
        - Wild, spiky dark hair (untamed)
        - Lean, athletic build
        - Cocky, wild expression
        - Tattoos on wrists (blue bands)
        
        COSTUME:
        - Red/maroon short-sleeved shirt (open or loose)
        - Gray/brown baggy shorts
        - Straw sandals (geta)
        - Sword with unique curved blade at hip
        
        STYLE: Chaotic street samurai, hip-hop meets Edo period
        POSE: Casual, loose stance with attitude
        """,
        "scene": "Dusty Japanese town street at golden hour, dynamic action pose"
    },
    {
        "name": "Jet_Black",
        "show": "Cowboy Bebop",
        "description": """
        Jet Black from Cowboy Bebop.
        
        APPEARANCE:
        - Dark/tan skin
        - Bald head (completely shaved)
        - Full dark beard (well-groomed)
        - Large, muscular frame (tank build)
        - Cybernetic left arm (metal prosthetic visible)
        - Mature, experienced look (40s)
        
        COSTUME:
        - Blue mechanic/pilot jumpsuit
        - Rolled up sleeves
        - Heavy boots
        - No accessories needed
        
        STYLE: Cyberpunk uncle, experienced bounty hunter
        EXPRESSION: Calm, wise, slightly tired
        """,
        "scene": "Bebop spaceship interior with warm lighting, noir atmosphere"
    },
    {
        "name": "Dutch",
        "show": "Black Lagoon",
        "description": """
        Dutch from Black Lagoon.
        
        APPEARANCE:
        - Dark skin (Black man)
        - Bald head
        - Muscular, imposing frame
        - Clean shaven face
        - Sunglasses (dark aviators)
        - Calm but menacing presence
        
        COSTUME:
        - Green military tactical vest
        - Dark t-shirt underneath
        - Military cargo pants
        - Combat boots
        - Dog tags optional
        
        STYLE: Calm mercenary leader, professional killer
        EXPRESSION: Cool, collected, intimidating
        """,
        "scene": "Roanapur docks at night, neon signs reflecting on water"
    },
    {
        "name": "Ogun_Montgomery",
        "show": "Fire Force",
        "description": """
        Ogun Montgomery from Fire Force (Enen no Shouboutai).
        
        APPEARANCE:
        - Dark skin
        - Short black hair (fade style)
        - Athletic, lean muscular build
        - Confident, friendly expression
        - Fire Force Company 4 member
        
        COSTUME:
        - Fire Force uniform (black with orange accents)
        - Fire-resistant coat/jacket
        - Combat boots
        - Bunker gear elements
        
        POWERS: Fire user (flames optional in image)
        STYLE: Modern firefighter meets anime action hero
        """,
        "scene": "Tokyo street with fire in background, heroic pose"
    },
    {
        "name": "Killer_Bee",
        "show": "Naruto Shippuden",
        "description": """
        Killer Bee from Naruto Shippuden.
        
        APPEARANCE:
        - Dark skin (muscular Black man)
        - White/platinum blonde hair (styled up)
        - Very muscular, bodybuilder physique
        - Dark sunglasses (oval shades)
        - Confident, playful rapper expression
        - Beard/goatee
        
        COSTUME:
        - White one-strap vest (showing muscles)
        - White baggy pants
        - Kumogakure headband (cloud symbol)
        - Seven swords on back (if visible)
        - Arm wraps/bandages
        
        STYLE: Rapper ninja with bijuu host energy
        POSE: Dynamic, possibly mid-rap gesture
        """,
        "scene": "Hidden Cloud Village mountains, dramatic lightning in sky"
    },
    {
        "name": "Kaname_Tosen",
        "show": "Bleach",
        "description": """
        Kaname Tosen from Bleach (pre-visor, early appearance).
        
        APPEARANCE:
        - Dark skin
        - Long dreadlocks/braids (dark purple-black)
        - Eyes visible (NOT wearing visor)
        - Calm, peaceful expression
        - Lean build
        
        COSTUME:
        - White Soul Reaper captain haori (coat)
        - Black shihakusho underneath
        - Captain of Squad 9
        - Zanpakuto at hip
        
        STYLE: Serene, philosophical warrior
        EXPRESSION: Calm, wise, slightly melancholic
        """,
        "scene": "Soul Society gardens, peaceful zen atmosphere"
    },
    {
        "name": "Yami_Sukehiro",
        "show": "Black Clover",
        "description": """
        Yami Sukehiro from Black Clover.
        
        APPEARANCE:
        - Tan/dark skin
        - Messy black spiky hair
        - Heavy stubble/5 o'clock shadow
        - Extremely muscular, tall build
        - Always looks tired/annoyed
        - Cigarette in mouth optional
        
        COSTUME:
        - Black sleeveless shirt (tight, showing muscles)
        - Black Bulls captain coat (hanging open)
        - Dark pants
        - Large katana (nodachi/odachi sword)
        
        STYLE: Tired swordsman captain with insane power
        EXPRESSION: Annoyed, "surpass your limits" energy
        """,
        "scene": "Black Bulls base, dark moody lighting with shadows"
    },
    {
        "name": "Trafalgar_Law",
        "show": "One Piece",
        "description": """
        Trafalgar D. Water Law from One Piece.
        
        APPEARANCE:
        - Tan skin
        - Dark sideburns and goatee
        - Dark circles under eyes
        - Lean, athletic build
        - DEATH tattoo on fingers
        - Jolly Roger tattoos on arms and chest
        
        COSTUME:
        - Spotted/leopard print hat (fuzzy white hat with spots)
        - Long black/yellow hoodie coat
        - Jeans
        - Nodachi sword (Kikoku) - very long
        
        STYLE: Surgeon of Death, cool pirate captain
        EXPRESSION: Calm, calculating, slightly smirking
        """,
        "scene": "Ship deck at night, moody blue lighting, sea in background"
    },
    {
        "name": "Shanks",
        "show": "One Piece",
        "description": """
        Red-Haired Shanks from One Piece.
        
        APPEARANCE:
        - Tan skin
        - BRIGHT RED hair (shoulder length, messy)
        - Three scars over left eye (from Blackbeard)
        - Missing left arm (sleeve hanging empty)
        - Strong, powerful build
        - Confident, king-like presence
        
        COSTUME:
        - White button-up shirt (open, showing chest)
        - Black cloak/cape draped over shoulders
        - Simple pants and sandals
        - Straw hat optionally in hand (Luffy's hat origin)
        
        STYLE: Pirate Emperor, absolute confidence
        EXPRESSION: Warm smile but radiating power
        """,
        "scene": "Pirate ship deck at sunset, crew silhouettes in background"
    }
]

async def countdown(seconds: int, desc: str):
    with Progress(SpinnerColumn("dots12"), TextColumn(f"[yellow]{desc}"), BarColumn(bar_width=50), 
                  TextColumn("[cyan]{task.fields[r]}s"), console=console, transient=True) as p:
        t = p.add_task("", total=seconds, r=seconds)
        for i in range(seconds, 0, -1):
            p.update(t, advance=1, r=i-1)
            await asyncio.sleep(1)

async def analyze_photos_to_schema(client, image_parts: list) -> str:
    """Analyze all photos and extract facial DNA as text"""
    
    analysis_prompt = """
    Analyze ALL these photos of the SAME PERSON and extract a comprehensive facial profile.
    Be SPECIFIC about: face shape, skin tone (Fitzpatrick), nose, lips, eyes, eyebrows, 
    distinctive features, bone structure.
    """
    
    response = await client.aio.models.generate_content(
        model=TEXT_MODEL,
        contents=[analysis_prompt] + image_parts,
        config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
    )
    return response.text

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

def build_prompt(character: dict, schema: str) -> str:
    return f"""
═══════════════════════════════════════════════════════════════════════════════
PROFESSIONAL ANIME COSPLAY PHOTOGRAPHY - {character['name'].replace('_', ' ')} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

Create a PROFESSIONAL PHOTOGRAPH of this person as {character['name'].replace('_', ' ')}.

═══════════════════════════════════════════════════════════════════════════════
🔒 FACIAL DNA PROFILE (TEXT SCHEMA FROM 14 PHOTOS) 🔒
═══════════════════════════════════════════════════════════════════════════════

{schema}

THE FINAL FACE MUST BE IMMEDIATELY RECOGNIZABLE AS THIS PERSON.

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
    ║   🔥 DAV3 ANIME SYNERGY TEST - 10 CHARACTERS 🔥                          ║
    ║                                                                           ║
    ║   Option 1 (Text Schema) Only - Natural Synergy Characters               ║
    ║                                                                           ║
    ║   Afro • Mugen • Jet • Dutch • Ogun • Bee • Tosen • Yami • Law • Shanks  ║
    ║                                                                           ║
    ║   Camera: Canon R6 Mark II @ f/2.0, 4K | Buffer: 70s                     ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", box=box.DOUBLE_EDGE))
    
    # Initialize
    with console.status("[bold cyan]⚡ Initializing...", spinner="dots12"):
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    console.print("[green]✅ Client ready![/green]")
    
    # Setup paths
    input_dir = Path("c:/Yuki_Local/Dav3 test")
    output_dir = Path("c:/Yuki_Local/dav3_anime_synergy_results")
    output_dir.mkdir(exist_ok=True)
    
    # Load photos
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    console.print(f"\n[cyan]📸 Loading {len(input_images)} photos...[/cyan]")
    
    image_parts = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
    
    best_photo = image_parts[0]
    console.print(f"[green]✅ Loaded {len(image_parts)} photos[/green]")
    
    # Pre-analyze
    console.print("\n[bold magenta]🔬 Extracting Facial DNA Schema...[/bold magenta]")
    with console.status("[cyan]   Analyzing 14 photos...", spinner="dots12"):
        schema = await analyze_photos_to_schema(client, image_parts)
    console.print(f"[green]   ✅ Schema: {len(schema)} chars[/green]")
    
    with open(output_dir / "facial_schema.txt", "w") as f:
        f.write(schema)
    
    results = []
    start = time.time()
    
    for i, char in enumerate(CHARACTERS, 1):
        console.print("\n" + "═" * 70)
        console.print(f"[bold magenta]🎭 [{i}/10] {char['name'].replace('_', ' ')} ({char['show']})[/bold magenta]")
        console.print("═" * 70)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with Progress(SpinnerColumn("dots12"), TextColumn("[cyan]{task.description}"), 
                      BarColumn(bar_width=40), TimeElapsedColumn(), console=console) as prog:
            task = prog.add_task("⚡ Generating...", total=100)
            prog.update(task, advance=10)
            
            try:
                prompt = build_prompt(char, schema)
                path = output_dir / f"{char['name']}_{ts}.png"
                success = await generate_image(client, prompt, best_photo, path)
                
                prog.update(task, advance=90, description="✅ Done!")
                if success:
                    console.print(f"   [green]✅ {path.name} ({path.stat().st_size/1024:.0f} KB)[/green]")
                    results.append((char['name'], path))
                else:
                    console.print("   [yellow]⚠️ No image[/yellow]")
            except Exception as e:
                console.print(f"   [red]❌ {str(e)[:60]}...[/red]")
        
        if i < len(CHARACTERS):
            await countdown(BUFFER_SECONDS, "⏳ Cooling down...")
    
    # Summary
    elapsed = time.time() - start
    console.print("\n" + "═" * 70)
    
    summary = Table(title="🔥 ANIME SYNERGY RESULTS", box=box.DOUBLE_EDGE)
    summary.add_column("Character", style="magenta")
    summary.add_column("File", style="white")
    summary.add_column("Size", style="green")
    
    for char, path in results:
        summary.add_row(char, path.name[:40], f"{path.stat().st_size/1024:.0f} KB")
    
    console.print(summary)
    console.print(f"\n[cyan]⏱️ Total: {elapsed/60:.1f} min | Generated: {len(results)}/10[/cyan]")
    console.print(f"[green]📂 Output: {output_dir}[/green]")
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)

if __name__ == "__main__":
    asyncio.run(main())
