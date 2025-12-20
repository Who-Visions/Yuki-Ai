"""
⚡ V11 STAGE 4: Batch Image Generation for Keyosha Pullman ⚡

Features:
- Uses Vertex AI project quota (NO API keys)
- 30-minute delays between generations to avoid 429
- rich.live CLI for beautiful progress tracking
- Generates all character variants from database
"""
import asyncio
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict

from google import genai
from google.genai import types
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.layout import Layout
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add database path
import sys
sys.path.append("c:/Yuki_Local")
from database.schema import Character, AppearanceVariant

# =============================================================================
# CONFIG - Vertex AI (NO API KEYS)
# =============================================================================
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
IMAGE_MODEL = "gemini-3-pro-image-preview"

# Subject config
SUBJECT_NAME = "Keyosha Pullman"
SUBJECT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Keyosha Pullman")
OUTPUT_DIR = SUBJECT_DIR / "Renders"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Rate limiting - faster generation with 40 sec delays
DELAY_SECONDS = 40  # 40 seconds between renders

DB_PATH = "sqlite:///c:/Yuki_Local/database/yuki_knowledge.db"

console = Console()


def load_identity_lock() -> Dict:
    """Load the V11 identity lock for the subject"""
    lock_path = SUBJECT_DIR / "identity_lock_v11.json"
    with open(lock_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_subject_photos() -> List[types.Part]:
    """Load subject photos as Gemini parts"""
    photos = sorted(SUBJECT_DIR.glob("*.jpg"), key=lambda p: p.stat().st_size, reverse=True)[:4]
    parts = []
    for p in photos:
        with open(p, "rb") as f:
            parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
    return parts


def get_cosplay_characters() -> List[Dict]:
    """Get all cosplay characters from database"""
    engine = create_engine(DB_PATH)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Get the 10 cosplay characters (no series_id)
    characters = session.query(Character).filter(Character.series_id == None).all()
    
    result = []
    for char in characters:
        for variant in char.variants:
            result.append({
                "character_name": char.name_romaji,
                "variant_name": variant.name,
                "base_prompt": char.base_prompt,
                "hair_style": variant.hair_style,
                "hair_color": variant.hair_color,
                "outfit_structure": variant.outfit_structure,
                "prompt_tags": variant.prompt_tags,
                "negative_prompt": variant.negative_prompt,
                "color_palette": variant.color_palette,
                "is_default": variant.is_default
            })
    
    session.close()
    return result


def build_generation_prompt(identity_lock: Dict, character: Dict) -> str:
    """Build the generation prompt combining identity lock + character costume"""
    
    lock = identity_lock.get("deep_analysis", {}).get("identity_lock", {})
    preserve = lock.get("absolute_preserve", [])
    features = lock.get("feature_signatures", {})
    guidance = lock.get("generation_guidance", "")
    subject_info = lock.get("subject_info", {})
    geometric = lock.get("geometric_signatures", {})
    
    # Load 68-point geometry
    geo_path = SUBJECT_DIR / "facial_ip_68node_neck.json"
    geo_data = {}
    if geo_path.exists():
        with open(geo_path, "r", encoding="utf-8") as f:
            geo_data = json.load(f)
    
    expansion = geo_data.get("expansion_68", {})
    face_geometry = expansion.get("face_geometry", {})
    jawline_detail = expansion.get("jawline_detail", {})
    
    outfit = character.get("outfit_structure", {})
    outfit_text = ""
    if outfit:
        for area, items in outfit.items():
            if items:
                outfit_text += f"  - {area}: {', '.join(items)}\n"
    
    prompt = f"""⚠️⚠️⚠️ CRITICAL: EXACT FACE MATCH REQUIRED ⚠️⚠️⚠️

YOU MUST COPY THE EXACT FACE FROM THE SUBJECT PHOTOS PROVIDED.
DO NOT CREATE A NEW FACE. DO NOT BLEND FEATURES. COPY THE EXACT FACE.
THE OUTPUT IMAGE MUST BE IMMEDIATELY RECOGNIZABLE AS THE SAME PERSON IN THE REFERENCE PHOTOS.

🔒 SUBJECT: {SUBJECT_NAME}
Ethnicity: {subject_info.get('ethnicity', 'African American')}
Skin tone: {subject_info.get('skin_tone', 'Fitzpatrick V - Deep Bronze/Rich Chocolate')}

📐 FACIAL GEOMETRY (68-POINT LOCK - DO NOT DEVIATE):
- Face shape: {face_geometry.get('face_shape', 'oval')}
- Symmetry: {face_geometry.get('symmetry_score', 0.92)}
- Forehead to chin ratio: {face_geometry.get('proportions', {}).get('forehead_to_chin', 1.58)}
- Bizygomatic width: {face_geometry.get('proportions', {}).get('bizygomatic_width', 1.24)}
- Jaw to cheek ratio: {face_geometry.get('proportions', {}).get('jaw_to_cheek_ratio', 0.88)}

📐 JAWLINE GEOMETRY:
- Chin shape: {jawline_detail.get('chin_shape', 'rounded')}
- Mandible width: {jawline_detail.get('mandible_width', 'medium')}
- Jawline definition: {jawline_detail.get('jawline_definition', 'soft')}
- Left jaw angle: {jawline_detail.get('jaw_angle_left', '122.5')}°
- Right jaw angle: {jawline_detail.get('jaw_angle_right', '118.2')}°

👁️ FEATURE SIGNATURES (MUST MATCH EXACTLY):
- Eyes: {features.get('eyes', {}).get('shape', 'almond shaped')}
- Eyebrows: {features.get('eyebrows', {}).get('shape', 'natural arch')}
- Nose: {features.get('nose', {}).get('bridge_profile', 'medium bridge')}, {features.get('nose', {}).get('tip_shape', 'rounded tip')}
- Lips: {features.get('lips', {}).get('shape', 'full')}, cupid's bow: {features.get('lips', {}).get('cupids_bow', 'rounded')}

🚫 ABSOLUTE PRESERVE - NEVER REMOVE THESE:
{chr(10).join(f'• {p}' for p in preserve[:10])}

🎭 COSPLAY: {character['character_name']} - {character['variant_name']}

COSTUME ONLY (FACE STAYS AS SUBJECT):
{outfit_text}

HAIR/WIG: {character.get('hair_style', 'As character')} ({character.get('hair_color', 'As character')})

STYLE TAGS: {character.get('prompt_tags', '')}

⚠️ FINAL INSTRUCTIONS:
1. FACE = EXACT COPY of {SUBJECT_NAME} from reference photos - same bone structure, same features, same proportions
2. ONLY change: hair/wig, costume, background, pose
3. The result must be {SUBJECT_NAME} in cosplay, NOT a new person with similar features
4. If you cannot preserve the exact face, DO NOT GENERATE - the face is more important than the costume
5. Maintain septum piercing, ear tunnels, temple tattoo EXACTLY as in reference

Generate photorealistic 4K image of {SUBJECT_NAME} cosplaying as {character['character_name']}."""

    return prompt


async def generate_single_image(
    client: genai.Client,
    identity_lock: Dict,
    subject_parts: List[types.Part],
    character: Dict,
    index: int
) -> Optional[Path]:
    """Generate a single cosplay image"""
    
    prompt = build_generation_prompt(identity_lock, character)
    
    contents = [
        "=== SUBJECT PHOTOS (THIS IS THE PERSON - USE THIS FACE) ===",
        *subject_parts,
        prompt
    ]
    
    try:
        response = await client.aio.models.generate_content(
            model=IMAGE_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE', 'TEXT'],
                temperature=1.0,  # Gemini 3 optimized for 1.0
                image_config=types.ImageConfig(
                    image_size="4K"  # 4K resolution output
                )
            )
        )
        
        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # Generate filename
                    char_name = character['character_name'].replace(" ", "_").replace("(", "").replace(")", "")[:20]
                    var_name = character['variant_name'].replace(" ", "_")[:15]
                    timestamp = datetime.now().strftime("%H%M%S")
                    filename = f"{index:02d}_{char_name}_{var_name}_{timestamp}.png"
                    output_path = OUTPUT_DIR / filename
                    
                    with open(output_path, "wb") as f:
                        f.write(part.inline_data.data)
                    
                    return output_path
        
        return None
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return None


def create_status_table(characters: List[Dict], results: List[Dict], current_idx: int, time_remaining: int) -> Table:
    """Create a status table for rich.live display"""
    table = Table(title=f"🎨 V11 Generation Progress - {SUBJECT_NAME}")
    
    table.add_column("Idx", style="dim", width=4)
    table.add_column("Character", style="cyan", width=25)
    table.add_column("Variant", style="magenta", width=20)
    table.add_column("Status", width=15)
    table.add_column("Output", width=30)
    
    for i, char in enumerate(characters):
        status = results[i]["status"] if i < len(results) else "⏳ Pending"
        output = results[i].get("output", "-") if i < len(results) else "-"
        
        if i == current_idx:
            status = "🔄 Generating..."
        elif i > current_idx and status == "⏳ Pending":
            status = "⏳ Pending"
        
        table.add_row(
            str(i + 1),
            char["character_name"][:24],
            char["variant_name"][:19],
            status,
            str(output)[-29:] if output != "-" else "-"
        )
    
    return table


async def run_batch_generation(limit: int = 12, start_index: int = 0):
    """Run batch generation with delays and rich.live CLI"""
    
    console.print(Panel.fit(
        f"[bold cyan]⚡ V11 Stage 4: Batch Image Generation[/bold cyan]\n"
        f"Subject: [yellow]{SUBJECT_NAME}[/yellow]\n"
        f"Model: [green]{IMAGE_MODEL}[/green]\n"
        f"Delay: [red]{DELAY_SECONDS} seconds[/red] between requests\n"
        f"Starting at: [magenta]Image {start_index + 1}[/magenta]\n"
        f"Using: [bold green]Vertex AI Project Quota (NO API KEYS)[/bold green]"
    ))
    
    # Load data
    console.print("\n[cyan]Loading data...[/cyan]")
    identity_lock = load_identity_lock()
    subject_parts = load_subject_photos()
    all_characters = get_cosplay_characters()[:limit]
    characters = all_characters[start_index:]  # Skip already-rendered
    
    console.print(f"[green]✓[/green] Identity lock loaded")
    console.print(f"[green]✓[/green] Subject photos loaded ({len(subject_parts)})")
    console.print(f"[green]✓[/green] Characters loaded ({len(characters)})")
    
    # Initialize Vertex AI client (NO API KEY)
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    console.print(f"[green]✓[/green] Vertex AI client initialized")
    
    # Results tracking
    results = []
    
    console.print(f"\n[bold yellow]Starting generation of {len(characters)} images...[/bold yellow]")
    console.print(f"[dim]Estimated completion: {datetime.now() + timedelta(seconds=DELAY_SECONDS * len(characters))}[/dim]\n")
    
    for i, character in enumerate(characters):
        console.print(f"\n{'='*60}")
        console.print(f"[bold cyan]Image {i+1}/{len(characters)}:[/bold cyan] {character['character_name']} - {character['variant_name']}")
        console.print(f"{'='*60}")
        
        with console.status(f"[bold green]Generating image {i+1}...[/bold green]", spinner="dots"):
            output_path = await generate_single_image(
                client, identity_lock, subject_parts, character, i + 1
            )
        
        if output_path:
            results.append({
                "status": "✅ Done",
                "output": output_path.name,
                "path": str(output_path)
            })
            console.print(f"[green]✅ Saved:[/green] {output_path.name}")
        else:
            results.append({
                "status": "❌ Failed",
                "output": "-"
            })
            console.print(f"[red]❌ Generation failed[/red]")
        
        # Delay between requests (except for last one)
        if i < len(characters) - 1:
            next_time = datetime.now() + timedelta(seconds=DELAY_SECONDS)
            console.print(f"\n[yellow]⏳ Waiting {DELAY_SECONDS // 60} minutes to avoid 429...[/yellow]")
            console.print(f"[dim]Next generation at: {next_time.strftime('%H:%M:%S')}[/dim]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task(f"[cyan]Waiting for rate limit...", total=DELAY_SECONDS)
                for _ in range(DELAY_SECONDS):
                    await asyncio.sleep(1)
                    progress.update(task, advance=1)
    
    # Final summary
    console.print(f"\n{'='*60}")
    console.print(Panel.fit(
        f"[bold green]✅ BATCH GENERATION COMPLETE[/bold green]\n\n"
        f"Total: {len(results)}\n"
        f"Success: {sum(1 for r in results if r['status'] == '✅ Done')}\n"
        f"Failed: {sum(1 for r in results if r['status'] == '❌ Failed')}\n\n"
        f"Output: [cyan]{OUTPUT_DIR}[/cyan]"
    ))
    
    # Save results log
    log_path = OUTPUT_DIR / f"generation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({
            "subject": SUBJECT_NAME,
            "timestamp": datetime.now().isoformat(),
            "model": IMAGE_MODEL,
            "results": results
        }, f, indent=2)
    console.print(f"[dim]Log saved: {log_path}[/dim]")


if __name__ == "__main__":
    asyncio.run(run_batch_generation(limit=12, start_index=0))  # Start at image 5
