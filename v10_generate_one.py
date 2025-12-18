"""
⚡ V10 GENERATION ONLY - Uses Pre-Extracted 50-Node Mocap ⚡
Uses gemini-3-pro-image-preview for generation via Vertex AI with delays to avoid 429
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
import json

# AI Studio API Key (separate quota from Vertex AI)
API_KEY = "AIzaSyCFsFL0Ps7V8UX-zDTbadxj5wRD4ks_Maw"
IMAGE_MODEL = "gemini-3-pro-image-preview"  # Gemini 3 image generation

async def generate_one(ref_index: int = 1):
    """Generate one image at a time to avoid 429"""
    print("=" * 70)
    print(f"⚡ V10 GENERATION - Image {ref_index} ⚡")
    print("=" * 70)
    
    client = genai.Client(api_key=API_KEY)
    
    # Load 50-node mocap
    mocap_path = Path("c:/Yuki_Local/Cosplay_Lab/Subjects/Kai Taylor/kai_v10_50node_mocap.json")
    with open(mocap_path, "r", encoding="utf-8") as f:
        mocap = json.load(f)
    
    print(f"✅ Loaded 50-node mocap for {mocap['subject_identity']['name']}")
    
    # Load Kai's photos
    kai_dir = Path("c:/Yuki_Local/Cosplay_Lab/Subjects/Kai Taylor")
    kai_images = sorted(list(kai_dir.glob("kai_new_*.jpg")))[:3]
    
    print(f"📸 Loading {len(kai_images)} subject photos...")
    
    kai_parts = []
    for img in kai_images:
        with open(img, "rb") as f:
            kai_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
    
    # Get reference
    ref_dir = Path("c:/Yuki_Local/Cosplay_Lab/References")
    refs = sorted([f for f in ref_dir.glob("*.jpg")])
    
    if ref_index > len(refs):
        print(f"❌ Only {len(refs)} references available")
        return
    
    ref_path = refs[ref_index - 1]
    print(f"🎭 Reference: {ref_path.name}")
    
    # Build mocap-locked prompt
    nodes = mocap.get("facial_skeleton_nodes", {})
    markers = mocap.get("critical_identity_markers", [])
    lock = mocap.get("generation_lock_rules", {}).get("ABSOLUTE_PRESERVE", [])
    
    # Load reference
    with open(ref_path, "rb") as f:
        ref_part = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    prompt = """FULL FACE REPLACEMENT - NOT A BLEND

Look at Photos A. That is KAI TAYLOR. Memorize her face EXACTLY.
Look at Photo B. That is a REFERENCE for clothes, pose, and scene ONLY.

YOUR OUTPUT MUST SHOW:
- KAI TAYLOR'S EXACT FACE (100% from Photos A, 0% from Photo B)
- The outfit/clothes from Photo B
- The pose from Photo B  
- The scene/background from Photo B

THE FACE IN YOUR OUTPUT MUST BE IDENTICAL TO PHOTOS A:
- Kai's specific eye shape (almond, upward tilt)
- Kai's specific nose (upturned tip)
- Kai's specific lips (sharp Cupid's bow)
- Kai's specific cheekbones (high, prominent)
- Kai's specific jaw (soft angle)
- Kai's olive skin tone

DO NOT BLEND. DO NOT AVERAGE. DO NOT MIX FACES.
The reference person's face should be COMPLETELY GONE, replaced 100% by Kai's face.

Generate Kai Taylor wearing the reference outfit in the reference scene."""

    # Structure: FACE photos first, then instruction, then SCENE photo
    contents = [
        "=== PHOTOS A: THE FACE (Use this face) ===",
        kai_parts[0],
        kai_parts[1],
        kai_parts[2],
        prompt,
        "=== PHOTO B: THE SCENE (Recreate this scene, but with the face from Photos A) ===",
        ref_part
    ]
    
    print("🔬 Generating with Gemini 2.5 Flash...")
    
    try:
        response = await client.aio.models.generate_content(
            model=IMAGE_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE', 'TEXT'],
                temperature=1.0
            )
        )
        
        # Save
        render_dir = Path("c:/Yuki_Local/Cosplay_Lab/Renders/kai_bella_v10_50node")
        render_dir.mkdir(parents=True, exist_ok=True)
        
        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # Include reference name in filename for tracking
                    ref_name = ref_path.stem[:30].replace(" ", "_")  # First 30 chars of ref name
                    out_path = render_dir / f"kai_bella_{ref_index:02d}_{ref_name}.png"
                    with open(out_path, "wb") as f:
                        f.write(part.inline_data.data)
                    print(f"✅ Saved: {out_path}")
                    return str(out_path)
        
        print("⚠️ No image in response")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


if __name__ == "__main__":
    import sys
    idx = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    asyncio.run(generate_one(idx))
