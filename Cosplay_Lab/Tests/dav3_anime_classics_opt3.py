"""
⚡ DAV3 ANIME CLASSICS TEST - 11 CHARACTERS (OPTION 3 ONLY) ⚡
Face Math approach for comparison with Option 1 synergy test
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
import json

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

# 11 Anime Characters for Option 3 testing
CHARACTERS = [
    {
        "name": "Yusuke_Urameshi",
        "show": "Yu Yu Hakusho",
        "description": """
        Yusuke Urameshi from Yu Yu Hakusho.
        
        APPEARANCE:
        - Black slicked-back hair (delinquent style)
        - Intense, confident expression
        - Athletic, lean muscular build
        - Young face (teenager)
        
        COSTUME:
        - Green school uniform jacket
        - White undershirt
        - Green pants
        - School uniform style
        
        STYLE: Delinquent hero, street fighter turned spirit detective
        POSE: Confident stance, maybe fists ready
        """,
        "scene": "City street at night, street lamp lighting, urban atmosphere"
    },
    {
        "name": "Kazuma_Kuwabara",
        "show": "Yu Yu Hakusho",
        "description": """
        Kazuma Kuwabara from Yu Yu Hakusho.
        
        APPEARANCE:
        - Orange/red slicked-back pompadour hairstyle
        - Strong jaw, somewhat blocky face
        - Tall, muscular build
        - Determined, honorable expression
        
        COSTUME:
        - Blue school uniform jacket
        - White undershirt
        - Blue pants
        
        STYLE: Loud, honorable brawler with a heart of gold
        EXPRESSION: Fierce determination or comedic intensity
        """,
        "scene": "School rooftop, dramatic afternoon lighting"
    },
    {
        "name": "Ichigo_Kurosaki",
        "show": "Bleach",
        "description": """
        Ichigo Kurosaki from Bleach (Shinigami form).
        
        APPEARANCE:
        - Bright orange spiky hair (signature look)
        - Intense, scowling expression (permanent frown)
        - Athletic, tall build
        - Brown eyes
        
        COSTUME:
        - Black Shinigami shihakusho (kimono robe)
        - White obi sash
        - Zangetsu (large cleaver sword) on back or in hand
        
        STYLE: Substitute Soul Reaper, protective hero
        EXPRESSION: Serious scowl, ready for battle
        """,
        "scene": "Soul Society rooftops, dramatic sky, wind blowing robes"
    },
    {
        "name": "Toji_Fushiguro",
        "show": "Jujutsu Kaisen",
        "description": """
        Toji Fushiguro from Jujutsu Kaisen.
        
        APPEARANCE:
        - Short dark/black hair
        - Scar on corner of mouth
        - Extremely muscular, imposing physique
        - Cold, calculating expression
        - Sharp, predatory eyes
        
        COSTUME:
        - Tight black shirt (showing muscle definition)
        - Dark pants
        - Minimal accessories
        - Sorcerer Killer aesthetic
        
        STYLE: Assassin dad, physically imposing with no cursed energy
        EXPRESSION: Menacing smirk or cold stare
        """,
        "scene": "Dark underground arena, harsh single-source lighting"
    },
    {
        "name": "Kento_Nanami",
        "show": "Jujutsu Kaisen",
        "description": """
        Kento Nanami from Jujutsu Kaisen.
        
        APPEARANCE:
        - Blonde/light brown hair (slicked back professionally)
        - Rectangular glasses (dark frames)
        - Mature, professional look
        - Athletic but lean build
        - Tired, over-it expression
        
        COSTUME:
        - Professional tan/beige suit
        - White dress shirt
        - Dark tie (loosened)
        - Dress shoes
        - Blunt sword wrapped in cloth (optional)
        
        STYLE: Salaryman sorcerer, professional jujutsu consultant
        EXPRESSION: Mild annoyance, professional detachment
        """,
        "scene": "Modern Tokyo office building exterior, golden hour"
    },
    {
        "name": "Shikamaru_Nara",
        "show": "Naruto Shippuden",
        "description": """
        Shikamaru Nara from Naruto Shippuden (adult/Shippuden era).
        
        APPEARANCE:
        - Black hair in high ponytail (spiky pineapple style)
        - Lazy, bored expression
        - Lean build (not overly muscular)
        - Ear piercings (studs)
        
        COSTUME:
        - Konoha flak jacket/vest (green)
        - Black long-sleeve undershirt
        - Black pants
        - Ninja sandals
        - Konoha headband on arm or forehead
        
        STYLE: Genius strategist who wishes he was a cloud
        EXPRESSION: "This is troublesome" tired face
        """,
        "scene": "Konoha village rooftops, clouds in sky, peaceful"
    },
    {
        "name": "Naruto_Hokage",
        "show": "Boruto: Naruto Next Generations",
        "description": """
        Naruto Uzumaki as Hokage from Boruto era.
        
        APPEARANCE:
        - Short spiky blonde hair (shorter than young Naruto)
        - Whisker marks on cheeks (3 lines each side)
        - Blue eyes
        - Mature, confident expression
        - Athletic build
        
        COSTUME:
        - Orange/red Hokage cloak with flames
        - Black and orange outfit underneath
        - Konoha headband
        - Warm, fatherly presence
        
        STYLE: Leader of the village, achieved his dream
        EXPRESSION: Warm smile, big grin
        """,
        "scene": "Hokage office or village overlook at sunset"
    },
    {
        "name": "Inuyasha",
        "show": "Inuyasha",
        "description": """
        Inuyasha from Inuyasha.
        
        APPEARANCE:
        - Long silver/white hair
        - Dog ears on top of head (fluffy, pointed)
        - Golden/amber eyes
        - Fangs visible when speaking
        - Claws on hands
        - Athletic, lean build
        
        COSTUME:
        - Red fire-rat robe (traditional Japanese)
        - Red hakama pants
        - Beads of Subjugation necklace (purple/white beads)
        - Barefoot or simple footwear
        - Tessaiga sword at hip
        
        STYLE: Half-demon, brash but protective
        EXPRESSION: Cocky smirk or determined scowl
        """,
        "scene": "Feudal Japan forest, mystical atmosphere"
    },
    {
        "name": "Kenshin_Himura",
        "show": "Rurouni Kenshin",
        "description": """
        Kenshin Himura from Rurouni Kenshin.
        
        APPEARANCE:
        - Long red hair in ponytail
        - X-shaped scar on left cheek (iconic)
        - Soft, gentle expression (hiding deadly past)
        - Lean, slender build
        - Violet/purple eyes
        
        COSTUME:
        - Red/magenta gi (kimono top)
        - White hakama pants
        - Reverse-blade sword (sakabato) at hip
        - Simple sandals
        
        STYLE: Wandering swordsman with peaceful heart
        EXPRESSION: Gentle smile with hint of melancholy
        """,
        "scene": "Traditional Japanese dojo, soft natural lighting"
    },
    {
        "name": "Coach_Ukai",
        "show": "Haikyuu",
        "description": """
        Keishin Ukai (Coach Ukai) from Haikyuu.
        
        APPEARANCE:
        - Blonde/dyed spiky hair with dark roots
        - Stubble/light beard
        - Laid-back but sharp expression
        - Athletic build (former player)
        - Usually has a cigarette or whistle
        
        COSTUME:
        - Casual track jacket (Karasuno colors - black/orange)
        - Regular pants or track pants
        - Whistle around neck
        - Sneakers
        
        STYLE: Volleyball coach, tough love mentor
        EXPRESSION: Analyzing players, slight smirk
        """,
        "scene": "Gymnasium, fluorescent lighting, volleyball court"
    },
    {
        "name": "Mori_Jin",
        "show": "The God of High School",
        "description": """
        Mori Jin from The God of High School.
        
        APPEARANCE:
        - Spiky brown/dark hair
        - Headband (red or white)
        - Open, energetic expression
        - Athletic, martial artist build
        - Young face
        
        COSTUME:
        - Simple t-shirt or martial arts gi
        - Loose pants for mobility
        - Fighting wraps on hands optional
        - Minimal accessories
        
        STYLE: Energetic martial artist, Monkey King descendant
        POSE: Dynamic fighting stance or mid-action
        """,
        "scene": "Martial arts tournament arena, dramatic spotlights"
    }
]

async def countdown(seconds: int, desc: str):
    with Progress(SpinnerColumn("dots12"), TextColumn(f"[yellow]{desc}"), BarColumn(bar_width=50), 
                  TextColumn("[cyan]{task.fields[r]}s"), console=console, transient=True) as p:
        t = p.add_task("", total=seconds, r=seconds)
        for i in range(seconds, 0, -1):
            p.update(t, advance=1, r=i-1)
            await asyncio.sleep(1)

async def extract_face_math(client, image_parts: list) -> dict:
    """Extract geometric facial measurements"""
    
    math_prompt = """
    Extract PRECISE GEOMETRIC facial measurements as JSON:
    {
        "face_proportions": {"width_to_height": "", "eye_spacing": ""},
        "bone_structure": {"face_shape": "", "jawline": "", "cheekbones": "", "chin": ""},
        "nose": {"bridge": "", "tip": "", "width": ""},
        "lips": {"upper": "", "lower": "", "width": ""},
        "eyes": {"shape": "", "size": "", "spacing": "", "color": ""},
        "eyebrows": {"shape": "", "thickness": ""},
        "skin": {"fitzpatrick": "I-VI", "undertone": ""},
        "distinctive_features": []
    }
    Be precise. Output valid JSON only.
    """
    
    response = await client.aio.models.generate_content(
        model=TEXT_MODEL,
        contents=[math_prompt] + image_parts,
        config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=2000)
    )
    
    text = response.text
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end]) if start >= 0 else {"raw": text}
    except:
        return {"raw": text}

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
🔒 FACIAL GEOMETRY PROFILE (FACE MATH FROM 14 PHOTOS) 🔒
═══════════════════════════════════════════════════════════════════════════════

{geometry}

USE THESE GEOMETRIC RATIOS for accurate facial reproduction.
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
    ║   🎌 DAV3 ANIME CLASSICS - 11 CHARACTERS (OPTION 3 FACE MATH) 🎌         ║
    ║                                                                           ║
    ║   Yusuke • Kuwabara • Ichigo • Toji • Nanami • Shikamaru                 ║
    ║   Naruto • Inuyasha • Kenshin • Coach Ukai • Mori Jin                    ║
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
    output_dir = Path("c:/Yuki_Local/dav3_anime_classics_opt3")
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
    
    # Pre-analyze with Face Math
    console.print("\n[bold magenta]🔬 Extracting Face Math Geometry...[/bold magenta]")
    with console.status("[cyan]   Computing geometric ratios...", spinner="dots12"):
        geometry = await extract_face_math(client, image_parts)
    geometry_text = json.dumps(geometry, indent=2) if isinstance(geometry, dict) else str(geometry)
    console.print(f"[green]   ✅ Geometry: {len(geometry_text)} chars[/green]")
    
    with open(output_dir / "face_geometry.json", "w") as f:
        json.dump(geometry, f, indent=2)
    
    results = []
    start = time.time()
    
    for i, char in enumerate(CHARACTERS, 1):
        console.print("\n" + "═" * 70)
        console.print(f"[bold magenta]🎭 [{i}/11] {char['name'].replace('_', ' ')} ({char['show']})[/bold magenta]")
        console.print("═" * 70)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with Progress(SpinnerColumn("dots12"), TextColumn("[cyan]{task.description}"), 
                      BarColumn(bar_width=40), TimeElapsedColumn(), console=console) as prog:
            task = prog.add_task("⚡ Generating with Face Math...", total=100)
            prog.update(task, advance=10)
            
            try:
                prompt = build_prompt(char, geometry_text)
                path = output_dir / f"OPT3_{char['name']}_{ts}.png"
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
            # Mega-buffer every 5 generations (300s) + normal buffer (100s)
            if i % 5 == 0:
                console.print("[bold yellow]🔥 MEGA-BUFFER: 300s cooldown after 5 generations...[/bold yellow]")
                await countdown(300, "🔥 MEGA-BUFFER (5 gens complete)...")
            else:
                await countdown(BUFFER_SECONDS, "⏳ Cooling down...")
    
    # Summary
    elapsed = time.time() - start
    console.print("\n" + "═" * 70)
    
    summary = Table(title="🎌 ANIME CLASSICS (OPT3) RESULTS", box=box.DOUBLE_EDGE)
    summary.add_column("Character", style="magenta")
    summary.add_column("File", style="white")
    summary.add_column("Size", style="green")
    
    for char, path in results:
        summary.add_row(char, path.name[:40], f"{path.stat().st_size/1024:.0f} KB")
    
    console.print(summary)
    console.print(f"\n[cyan]⏱️ Total: {elapsed/60:.1f} min | Generated: {len(results)}/11[/cyan]")
    console.print(f"[green]📂 Output: {output_dir}[/green]")
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)

if __name__ == "__main__":
    asyncio.run(main())
