"""
V11 Stage 4 - Cloud Vision Cached Identity Approach

Uses cached face_identity.json from Cloud Vision extraction.
Single best photo at high resolution with face geometry in prompt.
"""
import time
import json
import random
from pathlib import Path
from datetime import datetime
from typing import Optional

from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel

# Config - Vertex AI (NO API KEYS)
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
IMAGE_MODEL = "gemini-3-pro-image-preview"

SUBJECT_NAME = "Kai Taylor"
SUBJECT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Kai Taylor new")
OUTPUT_DIR = SUBJECT_DIR / "Renders_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

console = Console()


def load_face_identity() -> dict:
    """Load cached face identity from Cloud Vision extraction."""
    identity_path = SUBJECT_DIR / "face_identity.json"
    
    if not identity_path.exists():
        console.print(f"[red]No face_identity.json found![/red]")
        console.print(f"[yellow]Run first: python extract_face_identity.py \"{SUBJECT_DIR}\"[/yellow]")
        return None
    
    with open(identity_path) as f:
        identity = json.load(f)
    
    console.print(f"[green]✓[/green] Loaded cached identity: {identity['best_photo']} ({identity['best_score']}/50)")
    return identity


def get_random_characters(count: int = 10) -> list:
    """
    Generate random character list for testing.
    Avoids repeating characters from previous runs.
    """
    all_characters = [
        # Bella Swan Solo
        ("Bella Swan - Twilight Poster", "Pale skin, brown wavy hair, intense gaze, forest background, blue-tinted lighting, movie poster composition, dramatic shadows"),
        ("Bella Swan - New Moon Poster", "Sad expression, autumn leaves falling, Edward's ghostly silhouette behind, golden hour lighting, heartbreak atmosphere"),
        ("Bella Swan - Eclipse Poster", "Between two worlds, split lighting warm and cold, determined expression, Seattle skyline at night"),
        ("Bella Swan - Breaking Dawn Bride", "Elegant white wedding gown, Isle Esme forest, ethereal backlighting, romantic movie poster"),
        ("Bella Swan - Vampire Queen", "Red vampire eyes, pale flawless skin, powerful stance, Cullen crest, golden throne room, regal poster"),
        
        # Bella with Edward (movie poster style)
        ("Twilight Poster - Embrace", "Romantic embrace with Edward Cullen, forest clearing, blue moonlight, iconic Twilight movie poster recreation"),
        ("New Moon Poster - Separation", "Edward walking away, reaching out, autumn forest, emotional distance, theatrical poster style"),
        ("Eclipse Poster - Love Triangle", "Between Edward and Jacob silhouettes, mountain backdrop, dramatic storm clouds, choosing sides"),
        ("Breaking Dawn Part 1 - Wedding", "Walking down aisle with Edward in tuxedo, forest wedding arch, fairy lights, romantic poster"),
        ("Breaking Dawn Part 2 - Power Couple", "Standing with vampire Edward, matching formal attire, Cullen family behind, powerful united stance"),
    ]
    
    # Check what already exists in output folder
    existing_chars = set()
    for f in OUTPUT_DIR.glob("*.png"):
        # Extract character name from filename
        parts = f.stem.split("_")[1:-1]  # Remove index and timestamp
        char_name = " ".join(parts)[:15]
        existing_chars.add(char_name.lower())
    
    # Filter out already-generated characters
    available = [(name, desc) for name, desc in all_characters 
                 if name[:15].lower().replace(" ", "_")[:10] not in 
                 "".join(existing_chars)]
    
    if len(available) < count:
        console.print(f"[yellow]Only {len(available)} new characters available[/yellow]")
        return available
    
    return random.sample(available, count)


def generate_cosplay_edit(
    client: genai.Client,
    photo_path: Path,
    face_identity: dict,
    character_name: str,
    costume_description: str,
    index: int
) -> Optional[Path]:
    """
    Generate cosplay using SINGLE photo with cached face geometry.
    """
    from PIL import Image
    import io
    
    # Load and resize photo
    with Image.open(photo_path) as img:
        max_size = 1536  # High resolution for single image
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            console.print(f"   [dim]Resized to {new_size}[/dim]")
        
        buf = io.BytesIO()
        img.convert('RGB').save(buf, format='JPEG', quality=95)
        photo_data = buf.getvalue()
    
    photo_part = types.Part.from_bytes(data=photo_data, mime_type="image/jpeg")
    
    # Build identity-aware prompt with face geometry
    best_photo_data = None
    for p in face_identity.get("photos", []):
        if p["filename"] == face_identity["best_photo"]:
            best_photo_data = p
            break
    
    # Extract key landmarks for prompt
    landmarks_text = ""
    if best_photo_data and best_photo_data.get("landmarks"):
        lm = best_photo_data["landmarks"]
        landmarks_text = f"""
FACE GEOMETRY (from Cloud Vision analysis):
- Left eye position: ({lm.get('left_eye', {}).get('x', 'N/A')}, {lm.get('left_eye', {}).get('y', 'N/A')})
- Right eye position: ({lm.get('right_eye', {}).get('x', 'N/A')}, {lm.get('right_eye', {}).get('y', 'N/A')})
- Nose tip: ({lm.get('nose_tip', {}).get('x', 'N/A')}, {lm.get('nose_tip', {}).get('y', 'N/A')})
- Mouth center: ({lm.get('mouth_center', {}).get('x', 'N/A')}, {lm.get('mouth_center', {}).get('y', 'N/A')})
- Chin: ({lm.get('chin', {}).get('x', 'N/A')}, {lm.get('chin', {}).get('y', 'N/A')})
"""
    
    # Build prompt
    prompt = f"""Transform this person into {character_name} cosplay.

CRITICAL: PRESERVE THIS EXACT FACE
{landmarks_text}
The face geometry above describes THIS SPECIFIC PERSON.
The output must have the SAME face with the SAME proportions.

COSTUME: {costume_description}

STYLE: Cinematic photorealistic, shot on RED V-RAPTOR XL.
Professional movie lighting, color grading, 85mm lens.
NOT a cartoon, illustration, or 3D render.

ONLY CHANGE:
- Hair/wig to match {character_name}
- Outfit/costume as described
- Background to match character setting

DO NOT CHANGE:
- Face shape, eyes, nose, lips, jawline
- Skin tone and texture
- Facial hair pattern
- Any unique features

OUTPUT: Photorealistic image of THIS PERSON in a professional {character_name} photoshoot."""

    try:
        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=[photo_part, prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE', 'TEXT'],
                temperature=1.0,
                image_config=types.ImageConfig(
                    image_size="2K"
                )
            )
        )
        
        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    char_safe = character_name.replace(" ", "_").replace("(", "").replace(")", "").replace("'", "").replace("-", "_")[:25]
                    timestamp = datetime.now().strftime("%H%M%S")
                    filename = f"{index:02d}_{char_safe}_{timestamp}.png"
                    output_path = OUTPUT_DIR / filename
                    
                    with open(output_path, "wb") as f:
                        f.write(part.inline_data.data)
                    
                    return output_path
        
        return None
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return None


def main():
    console.print(Panel.fit(
        f"[bold cyan]⚡ V11 Stage 4 - CACHED IDENTITY[/bold cyan]\n"
        f"Subject: [yellow]{SUBJECT_NAME}[/yellow]\n"
        f"Method: [green]Cloud Vision Cache + Single Photo[/green]\n"
        f"Using: [bold green]Vertex AI Project Quota[/bold green]"
    ))
    
    # Load cached face identity
    face_identity = load_face_identity()
    if not face_identity:
        return
    
    # Get best photo path
    best_photo = SUBJECT_DIR / face_identity["best_photo"]
    if not best_photo.exists():
        console.print(f"[red]Best photo not found: {best_photo}[/red]")
        return
    
    # Initialize Vertex AI client
    client = genai.Client(
        vertexai=True, 
        project=PROJECT_ID, 
        location=LOCATION,
        http_options={'timeout': 1800000}
    )
    console.print(f"[green]✓[/green] Vertex AI ready (Timeout: 30m)")
    
    # Get random characters (new ones each run)
    characters = get_random_characters(10)
    console.print(f"[green]✓[/green] Selected {len(characters)} new characters")
    
    console.print(f"\n[bold]Generating {len(characters)} cosplay edits...[/bold]\n")
    
    for i, (char_name, costume) in enumerate(characters):
        console.print(f"[cyan]{i+1}/{len(characters)}:[/cyan] {char_name}")
        
        with console.status("[green]Generating with cached identity...[/green]"):
            result = generate_cosplay_edit(
                client, best_photo, face_identity, 
                char_name, costume, i+1
            )
        
        if result:
            console.print(f"   [green]✅ {result.name}[/green]")
        else:
            console.print(f"   [red]❌ Failed[/red]")
        
        time.sleep(5)
    
    console.print(f"\n[bold green]Done![/bold green] Check: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
