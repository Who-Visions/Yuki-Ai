"""
⚡ SNOW TEST - MULTI-REFERENCE COMPARISON ⚡
Testing Option 1 (Pre-Analysis Text Schema) vs Option 3 (Face Math)
Buffer: 70 seconds | Both labeled for comparison
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
TEXT_MODEL = "gemini-2.5-flash"  # For analysis (fast, cheap)
BUFFER_SECONDS = 70

# Test character - Foxxy Love (face fully visible, just researched accurate details)
TEST_CHARACTER = {
    "name": "Foxxy_Love",
    "show": "Drawn Together",
    "description": """
    Foxxy Love from the adult animated series Drawn Together.
    
    ACCURATE COSTUME (from official Drawn Together wiki):
    - ORANGE one-shoulder crop top (very short)
    - ORANGE short shorts
    - ORANGE hat with two FOX EARS on top
    - Dark orange furry bracelets on wrists
    - Tall high-heel calf-length ORANGE boots
    - FOX TAIL (she is half-fox hybrid)
    
    HAIR & STYLE:
    - Dark brown/black hair in low ponytail
    - Yellow hair tie
    - Tall and slim body
    - Confident, sassy expression
    - 70s funk/mystery-solving musician vibes
    
    COLOR SCHEME: All ORANGE themed outfit with fox accessories
    Make sure her FULL FACE is clearly visible - no masks or coverings.
    """,
    "scene": "Colorful 70s disco/funk environment with warm orange and pink lighting"
}

async def countdown(seconds: int, desc: str):
    with Progress(SpinnerColumn("dots12"), TextColumn(f"[yellow]{desc}"), BarColumn(bar_width=50), 
                  TextColumn("[cyan]{task.fields[r]}s"), console=console, transient=True) as p:
        t = p.add_task("", total=seconds, r=seconds)
        for i in range(seconds, 0, -1):
            p.update(t, advance=1, r=i-1)
            await asyncio.sleep(1)

# ═══════════════════════════════════════════════════════════════════════
# OPTION 1: Pre-Analysis Text Schema
# ═══════════════════════════════════════════════════════════════════════

async def analyze_photos_to_schema(client, image_parts: list) -> str:
    """Analyze all 14 photos and extract comprehensive facial DNA as text"""
    
    console.print("[bold cyan]🔬 OPTION 1: Analyzing 14 photos to build text schema...[/bold cyan]")
    
    analysis_prompt = """
    You are a professional facial analysis expert. Study ALL these photos of the SAME PERSON carefully.
    
    Analyze from multiple angles and lighting conditions to build a COMPREHENSIVE facial profile.
    
    Extract and describe in PRECISE DETAIL:
    
    ## BONE STRUCTURE
    - Face shape (oval, round, square, heart, oblong?)
    - Jawline (sharp, soft, rounded, angular?)
    - Cheekbone placement (high, medium, low?) and prominence
    - Chin shape and size
    - Forehead shape and height
    
    ## SKIN
    - Exact skin tone description (use Fitzpatrick scale I-VI)
    - Undertones (warm, cool, neutral?)
    - Texture characteristics
    - Any distinctive marks, freckles, etc.
    
    ## NOSE
    - Bridge shape (straight, curved, bumped?)
    - Tip shape (rounded, pointed, upturned?)
    - Nostril shape and size
    - Overall nose width and length
    - ANY PIERCINGS (septum, nostril, etc.) - IMPORTANT
    
    ## LIPS
    - Upper lip shape and fullness
    - Lower lip shape and fullness
    - Lip width relative to face
    - Cupid's bow definition
    - Natural lip color
    
    ## EYES
    - Eye shape (almond, round, hooded, monolid?)
    - Eye size relative to face
    - Eye spacing (close-set, wide-set?)
    - Eye color
    - Eyelid characteristics
    
    ## EYEBROWS
    - Shape (arched, straight, rounded?)
    - Thickness
    - Natural arch position
    - Color
    
    ## OTHER DISTINCTIVE FEATURES
    - Any unique identifying features
    - Expression tendencies
    - Asymmetries (natural, character-adding)
    
    Provide this as a detailed, structured profile that could be used to recreate this person's face accurately.
    Be SPECIFIC with measurements and descriptions.
    
    Output as a detailed text profile.
    """
    
    with console.status("[bold cyan]   Analyzing facial features across all photos...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=TEXT_MODEL,
            contents=[analysis_prompt] + image_parts,
            config=types.GenerateContentConfig(
                temperature=0.3,  # Low temp for accurate analysis
                max_output_tokens=2000
            )
        )
    
    schema = response.text
    console.print("[green]   ✅ Facial DNA schema extracted![/green]")
    console.print(f"[dim]   Schema length: {len(schema)} chars[/dim]")
    
    return schema

async def generate_with_schema(client, schema: str, best_photo, character: dict, output_dir: Path) -> Path:
    """Generate using text schema + single best photo"""
    
    prompt = f"""
═══════════════════════════════════════════════════════════════════════════════
PROFESSIONAL COSPLAY PHOTOGRAPHY - {character['name']} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

Create a PROFESSIONAL PHOTOGRAPH of this person as {character['name']}.

═══════════════════════════════════════════════════════════════════════════════
🔒 FACIAL DNA PROFILE (EXTRACTED FROM 14 REFERENCE PHOTOS) 🔒
═══════════════════════════════════════════════════════════════════════════════

The following is a comprehensive analysis of this person's facial features from multiple angles:

{schema}

USE THIS PROFILE TO ENSURE PERFECT FACIAL PRESERVATION.
The one reference photo provided shows this person - match it exactly.

═══════════════════════════════════════════════════════════════════════════════
CHARACTER TRANSFORMATION: {character['name']}
═══════════════════════════════════════════════════════════════════════════════

{character['description']}

═══════════════════════════════════════════════════════════════════════════════
📷 SPECIFICATIONS
═══════════════════════════════════════════════════════════════════════════════

CAMERA: Sony A7R V, 85mm f/1.4, f/1.8 DOF
COMPOSITION: 9:16 vertical (1080x1920), full body
QUALITY: 8K, natural skin, professional magazine quality
SCENE: {character['scene']}

Generate ONE ultra-realistic professional cosplay photograph.
═══════════════════════════════════════════════════════════════════════════════
"""
    
    with Progress(SpinnerColumn("dots12"), TextColumn("[cyan]{task.description}"), 
                  BarColumn(bar_width=40), TimeElapsedColumn(), console=console) as prog:
        task = prog.add_task("⚡ Generating with text schema...", total=100)
        
        prog.update(task, advance=10)
        response = await client.aio.models.generate_content(
            model=MODEL,
            contents=[prompt, best_photo],
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
        
        prog.update(task, advance=70)
        
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                prog.update(task, advance=20, description="💾 Saving...")
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                fn = f"OPTION1_TextSchema_{character['name']}_{ts}.png"
                sp = output_dir / fn
                with open(sp, "wb") as f:
                    f.write(part.inline_data.data)
                console.print(f"   [green]✅ {fn} ({sp.stat().st_size/1024:.0f} KB)[/green]")
                return sp
    
    console.print("   [yellow]⚠️ No image generated[/yellow]")
    return None

# ═══════════════════════════════════════════════════════════════════════
# OPTION 3: Face Math (Geometric Analysis)
# ═══════════════════════════════════════════════════════════════════════

async def extract_face_math(client, image_parts: list) -> dict:
    """Extract precise geometric facial measurements"""
    
    console.print("[bold cyan]🔬 OPTION 3: Extracting facial geometry (Face Math)...[/bold cyan]")
    
    math_prompt = """
    You are a facial geometry specialist. Analyze ALL these photos of the same person.
    
    Extract PRECISE GEOMETRIC MEASUREMENTS as ratios and descriptions:
    
    {
        "face_proportions": {
            "face_width_to_height_ratio": "e.g., 0.68",
            "eye_spacing_ratio": "distance between eyes / face width",
            "nose_length_ratio": "nose length / face height",
            "mouth_width_ratio": "mouth width / face width",
            "forehead_to_chin_ratio": "forehead height / chin to nose"
        },
        "bone_structure": {
            "face_shape": "oval/round/square/heart/oblong",
            "jawline_angle": "sharp/soft/rounded - angle description",
            "cheekbone_prominence": "high/medium/low - placement",
            "chin_shape": "pointed/rounded/square"
        },
        "feature_details": {
            "nose": {
                "bridge": "straight/curved/bumped",
                "tip": "rounded/pointed/upturned",
                "width": "narrow/medium/wide",
                "piercings": "septum/nostril/none - IMPORTANT"
            },
            "lips": {
                "upper_fullness": "thin/medium/full",
                "lower_fullness": "thin/medium/full",
                "cupids_bow": "defined/subtle/flat"
            },
            "eyes": {
                "shape": "almond/round/hooded/monolid",
                "size": "small/medium/large relative to face",
                "spacing": "close-set/average/wide-set",
                "color": "specific color"
            },
            "eyebrows": {
                "shape": "arched/straight/rounded",
                "thickness": "thin/medium/thick",
                "arch_position": "high/medium/low"
            }
        },
        "skin": {
            "fitzpatrick_scale": "I-VI",
            "undertone": "warm/cool/neutral",
            "notable_features": "any marks, texture notes"
        },
        "distinctive_identifiers": [
            "list of unique features that make this person recognizable"
        ]
    }
    
    Output as valid JSON.
    """
    
    with console.status("[bold cyan]   Computing facial geometry...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=TEXT_MODEL,
            contents=[math_prompt] + image_parts,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=2000
            )
        )
    
    # Extract JSON from response
    text = response.text
    try:
        # Find JSON in response
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            geometry = json.loads(text[start:end])
        else:
            geometry = {"raw": text}
    except:
        geometry = {"raw": text}
    
    console.print("[green]   ✅ Facial geometry extracted![/green]")
    
    return geometry

async def generate_with_face_math(client, geometry: dict, best_photo, character: dict, output_dir: Path) -> Path:
    """Generate using geometric face math + single photo"""
    
    geometry_text = json.dumps(geometry, indent=2) if isinstance(geometry, dict) else str(geometry)
    
    prompt = f"""
═══════════════════════════════════════════════════════════════════════════════
PROFESSIONAL COSPLAY PHOTOGRAPHY - {character['name']} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

Create a PROFESSIONAL PHOTOGRAPH of this person as {character['name']}.

═══════════════════════════════════════════════════════════════════════════════
🔒 FACIAL GEOMETRY PROFILE (MATHEMATICAL ANALYSIS FROM 14 PHOTOS) 🔒
═══════════════════════════════════════════════════════════════════════════════

The following geometric measurements define this person's facial structure:

{geometry_text}

USE THESE PRECISE GEOMETRIC RATIOS to ensure accurate facial reproduction.
The reference photo shows this person - match the geometry exactly.

═══════════════════════════════════════════════════════════════════════════════
CHARACTER TRANSFORMATION: {character['name']}
═══════════════════════════════════════════════════════════════════════════════

{character['description']}

═══════════════════════════════════════════════════════════════════════════════
📷 SPECIFICATIONS
═══════════════════════════════════════════════════════════════════════════════

CAMERA: Sony A7R V, 85mm f/1.4, f/1.8 DOF
COMPOSITION: 9:16 vertical (1080x1920), full body
QUALITY: 8K, natural skin, professional magazine quality
SCENE: {character['scene']}

Generate ONE ultra-realistic professional cosplay photograph.
═══════════════════════════════════════════════════════════════════════════════
"""
    
    with Progress(SpinnerColumn("dots12"), TextColumn("[cyan]{task.description}"), 
                  BarColumn(bar_width=40), TimeElapsedColumn(), console=console) as prog:
        task = prog.add_task("⚡ Generating with face math...", total=100)
        
        prog.update(task, advance=10)
        response = await client.aio.models.generate_content(
            model=MODEL,
            contents=[prompt, best_photo],
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
        
        prog.update(task, advance=70)
        
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                prog.update(task, advance=20, description="💾 Saving...")
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                fn = f"OPTION3_FaceMath_{character['name']}_{ts}.png"
                sp = output_dir / fn
                with open(sp, "wb") as f:
                    f.write(part.inline_data.data)
                console.print(f"   [green]✅ {fn} ({sp.stat().st_size/1024:.0f} KB)[/green]")
                return sp
    
    console.print("   [yellow]⚠️ No image generated[/yellow]")
    return None

# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

async def main():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║   🧪 MULTI-REFERENCE COMPARISON TEST 🧪                              ║
    ║                                                                       ║
    ║   OPTION 1: Pre-Analysis Text Schema + 1 Photo                       ║
    ║   OPTION 3: Face Math Geometry + 1 Photo                             ║
    ║                                                                       ║
    ║   Testing: Nezuko (Demon Slayer) | Buffer: 70s                       ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", box=box.DOUBLE_EDGE))
    console.print()
    
    # Initialize
    with console.status("[bold cyan]⚡ Initializing...", spinner="dots12"):
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    console.print("[green]✅ Client ready![/green]")
    
    # Setup
    input_dir = Path("c:/Yuki_Local/snow test")
    output_dir = Path("c:/Yuki_Local/snow_test_comparison")
    output_dir.mkdir(exist_ok=True)
    
    # Load ALL 14 photos for analysis
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    console.print(f"\n[cyan]📸 Loading {len(input_images)} photos for analysis...[/cyan]")
    
    image_parts = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
    console.print(f"[green]✅ Loaded {len(image_parts)} reference photos[/green]")
    
    # Best photo (first one) for generation
    best_photo = image_parts[0]
    
    results = []
    start = time.time()
    
    # ═══════════════════════════════════════════════════════════════════
    # OPTION 1: Text Schema Approach
    # ═══════════════════════════════════════════════════════════════════
    console.print("\n" + "═" * 70)
    console.print("[bold magenta]🔬 TESTING OPTION 1: Pre-Analysis Text Schema[/bold magenta]")
    console.print("═" * 70 + "\n")
    
    try:
        schema = await analyze_photos_to_schema(client, image_parts)
        
        # Save schema for reference
        with open(output_dir / "facial_schema.txt", "w") as f:
            f.write(schema)
        
        console.print()
        result1 = await generate_with_schema(client, schema, best_photo, TEST_CHARACTER, output_dir)
        if result1:
            results.append(("Option 1: Text Schema", result1))
    except Exception as e:
        console.print(f"[red]❌ Option 1 failed: {e}[/red]")
    
    # Buffer
    console.print()
    await countdown(BUFFER_SECONDS, "⏳ Cooling down...")
    
    # ═══════════════════════════════════════════════════════════════════
    # OPTION 3: Face Math Approach
    # ═══════════════════════════════════════════════════════════════════
    console.print("\n" + "═" * 70)
    console.print("[bold magenta]🔬 TESTING OPTION 3: Face Math Geometry[/bold magenta]")
    console.print("═" * 70 + "\n")
    
    try:
        geometry = await extract_face_math(client, image_parts)
        
        # Save geometry for reference
        with open(output_dir / "face_geometry.json", "w") as f:
            json.dump(geometry, f, indent=2)
        
        console.print()
        result3 = await generate_with_face_math(client, geometry, best_photo, TEST_CHARACTER, output_dir)
        if result3:
            results.append(("Option 3: Face Math", result3))
    except Exception as e:
        console.print(f"[red]❌ Option 3 failed: {e}[/red]")
    
    # Summary
    elapsed = time.time() - start
    console.print("\n" + "═" * 70)
    
    summary = Table(title="🧪 COMPARISON RESULTS", box=box.DOUBLE_EDGE)
    summary.add_column("Method", style="magenta")
    summary.add_column("Output", style="cyan")
    summary.add_column("Size", style="green")
    
    for method, path in results:
        summary.add_row(method, path.name, f"{path.stat().st_size/1024:.0f} KB")
    
    console.print(summary)
    console.print(f"\n[cyan]⏱️ Total time: {elapsed/60:.1f} min[/cyan]")
    console.print(f"[green]📂 Output: {output_dir}[/green]")
    console.print("[dim]Also saved: facial_schema.txt, face_geometry.json[/dim]")
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)

if __name__ == "__main__":
    asyncio.run(main())
