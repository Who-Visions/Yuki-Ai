"""
V10 Masked Generation Pipeline
Goal: Physically mask the reference face to force full replacement with Kai Taylor's identity.

Steps:
1. Detect face bbox in reference using Gemini 2.5 Flash.
2. Mask (black out) the face using PIL.
3. Generate using Gemini 2.5 Flash (or 3 Pro) with Kai's photos + Masked Reference.
"""

import asyncio
import os
import io
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw
from google.genai import types
from google import genai
from dotenv import load_dotenv

# Config
# AI Studio API Key (separate quota from Vertex AI)
API_KEY = os.environ.get("GEMINI_API_KEY")
IMAGE_MODEL = "gemini-3-pro-image-preview"
TEXT_MODEL = "gemini-3-flash-preview"

client = genai.Client(api_key=API_KEY)

# Paths
BASE_DIR = Path("c:/Yuki_Local")
REF_DIR = BASE_DIR / "Cosplay_Lab/References"
SUBJECT_DIR = BASE_DIR / "Cosplay_Lab/Subjects/Kai Taylor"
RENDER_DIR = BASE_DIR / "Cosplay_Lab/Renders/kai_bella_v10_masked"
RENDER_DIR.mkdir(parents=True, exist_ok=True)

async def get_face_bbox(ref_path: Path):
    """Ask Gemini to detect the face bounding box [ymin, xmin, ymax, xmax]"""
    print(f"   🔍 Detecting face in {ref_path.name}...")
    
    with open(ref_path, "rb") as f:
        img_part = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
        
    prompt = """Return the bounding box of the MAIN PERSON's face in this image.
    Format: [ymin, xmin, ymax, xmax] where values are 0-1000 (normalized).
    Only return the list. nothing else."""
    
    response = await client.aio.models.generate_content(
        model=TEXT_MODEL,
        contents=[img_part, prompt]
    )
    
    try:
        text = response.text
        # Extract list
        match = re.search(r"\[([\d,\s]+)\]", text)
        if match:
            coords = [int(x.strip()) for x in match.group(1).split(",")]
            # Validate
            if len(coords) == 4:
                return coords
            if len(coords) == 4 and all(0 <= c <= 1000 for c in coords):
                 return coords
    except Exception as e:
        print(f"    ❌ Error parsing bbox: {e}")
        
    # Fallback/Default if detection fails (should verify manually or retry)
    print("    ⚠️ Failed to detect face, using safe center crop assumption or manual")
    return None

from PIL import Image, ImageDraw, ImageFilter

def apply_mask(ref_path: Path, bbox=None):
    """Obscure the face using heavy blur (removes identity but keeps lighting)"""
    img = Image.open(ref_path)
    w, h = img.size
    
    if not bbox:
        # Default center upper area
        print("    ⚠️ Using default mask region")
        box = (w//3, h//6, 2*w//3, h//2)
    else:
        ymin, xmin, ymax, xmax = bbox
        
        # Apply slight padding
        pad_x = (xmax - xmin) * 0.1
        pad_y = (ymax - ymin) * 0.1
        
        box = (
            max(0, int((xmin - pad_x) / 1000 * w)),
            max(0, int((ymin - pad_y) / 1000 * h)),
            min(w, int((xmax + pad_x) / 1000 * w)),
            min(h, int((ymax + pad_y) / 1000 * h))
        )
    
    # Create mask for blur
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle(box, fill=255)
    
    # Blur the original image significantly
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=20))
    
    # Composite: use blurred version in the box, original elsewhere
    final_img = Image.composite(blurred_img, img, mask)
    
    # Save temp masked
    masked_path = RENDER_DIR / f"temp_masked_{ref_path.name}"
    final_img.save(masked_path)
    return masked_path

async def generate_masked_image(ref_path: Path, ref_index: int, kai_parts: list):
    """Generate the final image using masked reference"""
    print(f"\n🎨 Processing Image {ref_index}: {ref_path.name}")
    
    # 1. Detect
    bbox = await get_face_bbox(ref_path)
    if not bbox:
        print("    ❌ Skipping due to detection failure (or implement fallback)")
        return
        
    print(f"    📍 Face detected: {bbox}")
    
    # 2. Mask
    masked_path = apply_mask(ref_path, bbox)
    print(f"    🎭 Mask applied: {masked_path}")
    
    # 3. Generate
    with open(masked_path, "rb") as f:
        masked_part = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
        
    prompt = """FACE RECONSTRUCTION TASK

Input Image 1: A reference photo with the FACE BLURRED/OBSCURED.
Input Images 2-4: Kai Taylor (the target identity).

TASK:
RECONSTRUCT the blurred face in Image 1 using KAI TAYLOR'S features.
The blurring hides the original identity but preserves the lighting and skin tone.
Use the blurred area as a guide for lighting/position, but generate KAI TAYLOR'S face details.

CRITICAL:
- The reconstructed face must be KAI TAYLOR (Photos 2-4).
- Use Kai's EXACT facial features: Heart-shaped face, olive skin, almond eyes (positive tilt), upturned nose, sharp Cupid's bow.
- Blend the new face seamlessy with the neck/body.

OUTPUT: The complete image with Kai's face seamlessly integrated."""

    contents = [
        "=== BLURRED REFERENCE (Scene/Body) ===",
        masked_part,
        "=== TARGET IDENTITY (Kai Taylor) ===",
    ] + kai_parts + [prompt]
    
    print("    🚀 Generating...")
    response = await client.aio.models.generate_content(
        model=IMAGE_MODEL,
        contents=contents,
         config=types.GenerateContentConfig(
            response_modalities=['IMAGE', 'TEXT'],
            temperature=0.25 # Low temp for precision
        )
    )
    
    # Save
    if response.candidates and response.candidates[0].content:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                ref_name = ref_path.stem[:30].replace(" ", "_")
                out_path = RENDER_DIR / f"kai_bella_masked_{ref_index:02d}_{ref_name}.png"
                with open(out_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"    ✅ Saved: {out_path}")
                return str(out_path)
            else:
                print(f"    ⚠️ Part found but no inline_data: {part}")
    
    print("    ❌ Generation failed")
    print(f"    🔍 Full Response Candidates: {response.candidates}")
    try:
        print(f"    🔍 Prompt Feedback: {response.prompt_feedback}")
    except:
        pass

async def main():
    # Load Kai photos once
    kai_photos = sorted(list(SUBJECT_DIR.glob("kai_new_*.jpg")))[:3] # Use 3 best
    kai_parts = []
    for p in kai_photos:
        with open(p, "rb") as f:
            kai_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
            
    # Load References
    ref_files = sorted(list(REF_DIR.glob("*.[jJ][pP][gG]")))
    
    # Run for Image 4 (Index 3 since 0-based list, or 4 if matching 1-based index)
    # User said Image 4 failed. Let's find image 4.
    # From previous `check_index.py`: 4: HD-wallpaper-bella-forest...
    
    target_index = 4 
    if target_index <= len(ref_files):
        target_ref = ref_files[target_index-1] # 1-based to 0-based
        await generate_masked_image(target_ref, target_index, kai_parts)
    else:
        print(f"Index {target_index} out of range")

if __name__ == "__main__":
    asyncio.run(main())
