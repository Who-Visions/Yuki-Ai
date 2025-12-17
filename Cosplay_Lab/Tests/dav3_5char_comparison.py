"""
⚡ DAV3 TEST - 5 CHARACTER COMPARISON ⚡
Option 1 (Text Schema) vs Option 3 (Face Math) for each character
Canon R6 Mark II, f/2.0, 4K | Buffer: 70s
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
BUFFER_SECONDS = 70

# Camera specs
CAMERA_SPEC = """
CAMERA: Canon EOS R6 Mark II
LENS: RF 85mm f/1.2L USM
APERTURE: f/2.0 (shallow depth of field, beautifully blurred background)
RESOLUTION: 4K (3840x2160 or 9:16 equivalent)
LIGHTING: Professional 3-point studio setup with dramatic accents
QUALITY: Magazine cover quality, natural skin texture, professional color grading
"""

# 5 Characters with researched accurate descriptions
CHARACTERS = [
    {
        "name": "Solid_Snake",
        "show": "Metal Gear Solid",
        "description": """
        Solid Snake from Metal Gear Solid video game series.
        
        APPEARANCE:
        - Dark tactical sneaking suit (skin-tight bodysuit, dark blue/gray)
        - Bandana wrapped around forehead (iconic signature)
        - 5 o'clock shadow / stubble beard
        - Mullet hairstyle (dark brown/black hair, longer in back)
        - Intense, focused expression
        - Muscular but lean build
        
        ACCESSORIES:
        - Codec earpiece (optional)
        - Cigarette (optional)
        - Tactical belt with pouches
        
        POSE: Crouched tactical stance or standing heroically
        """,
        "scene": "Dark military base corridor with dramatic shadows and blue-gray lighting"
    },
    {
        "name": "Superman",
        "show": "DC Comics",
        "description": """
        Superman / Clark Kent from DC Comics.
        
        COSTUME:
        - Iconic blue suit with red cape
        - Red boots
        - Red trunks/briefs over the suit (classic look)
        - Yellow belt
        - Large red and yellow 'S' shield on chest
        - Red cape flowing heroically
        
        HAIR:
        - Black hair with iconic 'S' curl on forehead
        - Clean-shaven, strong jaw
        
        PHYSIQUE:
        - Extremely muscular, heroic build
        - Confident, noble expression
        - Standing tall, heroic pose
        """,
        "scene": "Metropolis skyline at golden hour, cape billowing in wind, heroic low-angle shot"
    },
    {
        "name": "Knuckleduster",
        "show": "My Hero Academia Vigilantes",
        "description": """
        Knuckleduster (Iwao Oguro) from My Hero Academia Vigilantes.
        
        APPEARANCE (from official wiki):
        - Towering, heavily muscled man
        - Short dark hair
        - Thick visible eyebrows
        - Heavy stubble/5 o'clock shadow
        - Prominent SCAR running diagonally down left cheek
        
        COSTUME:
        - Black wrap-around mask tied over top of head
        - Tight-fitting black shirt
        - Khaki/tan jeans or cargo pants
        - Black boots
        - Long hunter GREEN trench coat
        - Dark gloves with SILVER KNUCKLEDUSTERS on hands (iconic)
        
        EXPRESSION: Intense, intimidating, vigilante demeanor
        POSE: Standing imposingly or in fighting stance
        """,
        "scene": "Dark urban alley at night, neon signs in background, gritty vigilante atmosphere"
    },
    {
        "name": "Master_Chief_Unmasked",
        "show": "Halo",
        "description": """
        Master Chief (John-117) from Halo - HELMET OFF revealing face.
        
        ARMOR (Mjolnir):
        - Iconic green Spartan armor (Mjolnir Mark VI or later)
        - Gold/bronze visor (but helmet is OFF, held under arm or nearby)
        - Chest armor, shoulder pauldrons, arm guards
        - Full body green power armor
        
        FACE (helmet removed):
        - Short cropped military haircut
        - Battle-worn, weathered face
        - Strong jaw, intense focused eyes
        - Some scars from combat
        - Pale skin from always wearing helmet
        
        EXPRESSION: Stoic, battle-hardened soldier
        POSE: Helmet tucked under arm, standing at attention or ready for battle
        """,
        "scene": "UNSC ship bridge or Halo ring landscape in background, military sci-fi atmosphere"
    },
    {
        "name": "L_DeathNote",
        "show": "Death Note",
        "description": """
        L Lawliet from Death Note anime/manga.
        
        APPEARANCE:
        - Wild, messy black hair (unkempt, sticking out in all directions)
        - Large, wide eyes with dark circles/bags underneath (sleep deprived look)
        - Pale skin
        - Thin, lanky build (not muscular)
        - Barefoot or simple shoes
        
        COSTUME:
        - Plain white long-sleeve shirt (loose fitting)
        - Blue jeans (also loose, casual)
        - No accessories - very minimal aesthetic
        
        SIGNATURE POSE:
        - Crouched/squatting position (how L sits in chairs)
        - Holding thumb to lips while thinking
        - Hunched posture
        
        EXPRESSION: Blank, analytical stare with slight curiosity
        """,
        "scene": "Dark room with computer monitors, dramatic single-source lighting from screens"
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
    
    Describe in PRECISE DETAIL:
    - Face shape, bone structure, jawline, cheekbones, chin
    - Skin tone (Fitzpatrick scale), undertones, texture
    - Nose shape (bridge, tip, width), any piercings
    - Lip shape, fullness, proportions
    - Eye shape, size, spacing, color
    - Eyebrow shape, thickness, arch
    - Distinctive features (scars, marks, etc.)
    
    Be SPECIFIC enough that this profile could recreate their face accurately.
    """
    
    response = await client.aio.models.generate_content(
        model=TEXT_MODEL,
        contents=[analysis_prompt] + image_parts,
        config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
    )
    return response.text

async def extract_face_math(client, image_parts: list) -> dict:
    """Extract geometric facial measurements"""
    
    math_prompt = """
    Extract PRECISE GEOMETRIC facial measurements as JSON:
    {
        "face_proportions": {"width_to_height": "ratio", "eye_spacing": "ratio"},
        "bone_structure": {"face_shape": "", "jawline": "", "cheekbones": "", "chin": ""},
        "nose": {"bridge": "", "tip": "", "width": "", "piercings": ""},
        "lips": {"upper": "", "lower": "", "width": ""},
        "eyes": {"shape": "", "size": "", "spacing": "", "color": ""},
        "eyebrows": {"shape": "", "thickness": ""},
        "skin": {"fitzpatrick": "I-VI", "undertone": ""},
        "distinctive_features": []
    }
    Output valid JSON only.
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

def build_prompt(character: dict, facial_data: str, method: str) -> str:
    return f"""
═══════════════════════════════════════════════════════════════════════════════
PROFESSIONAL COSPLAY PHOTOGRAPHY - {character['name'].replace('_', ' ')} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

Create a PROFESSIONAL PHOTOGRAPH of this person as {character['name'].replace('_', ' ')}.

═══════════════════════════════════════════════════════════════════════════════
🔒 FACIAL DNA PROFILE ({method}) 🔒
═══════════════════════════════════════════════════════════════════════════════

{facial_data}

THE FINAL FACE MUST BE IMMEDIATELY RECOGNIZABLE AS THIS PERSON.
Match their exact facial structure from the reference photo.

═══════════════════════════════════════════════════════════════════════════════
CHARACTER: {character['name'].replace('_', ' ')}
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
    ║   🎮 DAV3 TEST - 5 CHARACTER COMPARISON 🎮                               ║
    ║                                                                           ║
    ║   Option 1: Text Schema  vs  Option 3: Face Math                         ║
    ║                                                                           ║
    ║   Characters: Snake • Superman • Knuckleduster • Chief • L               ║
    ║   Camera: Canon R6 Mark II @ f/2.0, 4K                                   ║
    ║   Buffer: 70s | 10 total generations                                     ║
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
    output_dir = Path("c:/Yuki_Local/dav3_comparison_results")
    output_dir.mkdir(exist_ok=True)
    
    # Load photos
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    console.print(f"\n[cyan]📸 Loading {len(input_images)} photos...[/cyan]")
    
    image_parts = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
    console.print(f"[green]✅ Loaded {len(image_parts)} reference photos[/green]")
    
    best_photo = image_parts[0]
    
    # Pre-analyze ONCE for all characters
    console.print("\n" + "═" * 70)
    console.print("[bold magenta]🔬 PRE-ANALYSIS: Building facial profiles...[/bold magenta]")
    console.print("═" * 70)
    
    with console.status("[cyan]   Extracting Text Schema...", spinner="dots12"):
        schema = await analyze_photos_to_schema(client, image_parts)
    console.print(f"[green]   ✅ Text Schema: {len(schema)} chars[/green]")
    
    await asyncio.sleep(10)  # Brief pause
    
    with console.status("[cyan]   Extracting Face Math...", spinner="dots12"):
        geometry = await extract_face_math(client, image_parts)
    geometry_text = json.dumps(geometry, indent=2) if isinstance(geometry, dict) else str(geometry)
    console.print(f"[green]   ✅ Face Math: {len(geometry_text)} chars[/green]")
    
    # Save profiles
    with open(output_dir / "facial_schema.txt", "w") as f:
        f.write(schema)
    with open(output_dir / "face_geometry.json", "w") as f:
        json.dump(geometry, f, indent=2)
    
    results = []
    start = time.time()
    
    # Generate for each character
    for i, char in enumerate(CHARACTERS, 1):
        console.print("\n" + "═" * 70)
        console.print(f"[bold magenta]🎭 [{i}/5] {char['name'].replace('_', ' ')} ({char['show']})[/bold magenta]")
        console.print("═" * 70)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Option 1: Text Schema
        console.print("\n[cyan]   📝 Option 1: Text Schema...[/cyan]")
        with Progress(SpinnerColumn("dots12"), TextColumn("[cyan]{task.description}"), 
                      BarColumn(bar_width=40), TimeElapsedColumn(), console=console) as prog:
            task = prog.add_task("⚡ Generating...", total=100)
            prog.update(task, advance=10)
            
            try:
                prompt1 = build_prompt(char, schema, "TEXT SCHEMA FROM 14 PHOTOS")
                path1 = output_dir / f"OPT1_TextSchema_{char['name']}_{ts}.png"
                success1 = await generate_image(client, prompt1, best_photo, path1)
                
                prog.update(task, advance=90, description="✅ Done!")
                if success1:
                    console.print(f"      [green]✅ {path1.name} ({path1.stat().st_size/1024:.0f} KB)[/green]")
                    results.append(("Opt1", char['name'], path1))
                else:
                    console.print("      [yellow]⚠️ No image[/yellow]")
            except Exception as e:
                console.print(f"      [red]❌ {str(e)[:60]}...[/red]")
        
        # Buffer
        await countdown(BUFFER_SECONDS, "   ⏳ Cooling down...")
        
        # Option 3: Face Math
        console.print("\n[cyan]   📐 Option 3: Face Math...[/cyan]")
        with Progress(SpinnerColumn("dots12"), TextColumn("[cyan]{task.description}"), 
                      BarColumn(bar_width=40), TimeElapsedColumn(), console=console) as prog:
            task = prog.add_task("⚡ Generating...", total=100)
            prog.update(task, advance=10)
            
            try:
                prompt3 = build_prompt(char, geometry_text, "GEOMETRIC FACE MATH FROM 14 PHOTOS")
                path3 = output_dir / f"OPT3_FaceMath_{char['name']}_{ts}.png"
                success3 = await generate_image(client, prompt3, best_photo, path3)
                
                prog.update(task, advance=90, description="✅ Done!")
                if success3:
                    console.print(f"      [green]✅ {path3.name} ({path3.stat().st_size/1024:.0f} KB)[/green]")
                    results.append(("Opt3", char['name'], path3))
                else:
                    console.print("      [yellow]⚠️ No image[/yellow]")
            except Exception as e:
                console.print(f"      [red]❌ {str(e)[:60]}...[/red]")
        
        # Buffer between characters (not after last)
        if i < len(CHARACTERS):
            await countdown(BUFFER_SECONDS, "   ⏳ Cooling down before next character...")
    
    # Summary
    elapsed = time.time() - start
    console.print("\n" + "═" * 70)
    
    summary = Table(title="🎮 DAV3 COMPARISON RESULTS", box=box.DOUBLE_EDGE)
    summary.add_column("Method", style="magenta")
    summary.add_column("Character", style="cyan")
    summary.add_column("File", style="white")
    summary.add_column("Size", style="green")
    
    for method, char, path in results:
        summary.add_row(method, char, path.name[:40], f"{path.stat().st_size/1024:.0f} KB")
    
    console.print(summary)
    console.print(f"\n[cyan]⏱️ Total time: {elapsed/60:.1f} min[/cyan]")
    console.print(f"[green]📂 Output: {output_dir}[/green]")
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)

if __name__ == "__main__":
    asyncio.run(main())
