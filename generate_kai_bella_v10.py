"""
⚡ KAI TAYLOR V10 BELLA SWAN GENERATION - SLOW MODE ⚡
CRITICAL: Face = Kai Taylor, Clothes/Scene = Bella Swan reference
Using longer delays to avoid 429 rate limits
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
import json
import random

# AI Studio API Key
API_KEY = "AIzaSyCFsFL0Ps7V8UX-zDTbadxj5wRD4ks_Maw"
IMAGE_MODEL = "gemini-3-pro-image-preview"

async def generate_with_retry(client, model, contents, config, max_retries=5):
    """Generate with exponential backoff on 429 errors"""
    for attempt in range(max_retries):
        try:
            return await client.aio.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait_time = (2 ** attempt) * 10 + random.uniform(0, 5)  # Much longer waits
                print(f"   ⏳ Rate limited, waiting {wait_time:.0f}s (attempt {attempt+1}/{max_retries})")
                await asyncio.sleep(wait_time)
            else:
                raise e
    raise Exception("Max retries exceeded")

async def generate_bella_renders():
    print("=" * 70)
    print("⚡ KAI TAYLOR V10 BELLA SWAN GENERATION (SLOW MODE) ⚡")
    print("🔒 FACE = KAI | COSTUME = BELLA")
    print("=" * 70)
    
    client = genai.Client(api_key=API_KEY)
    
    # Load Kai's V10 facial IP
    ip_path = Path("c:/Yuki_Local/Cosplay_Lab/Subjects/Kai Taylor/kai_taylor_facial_ip_v10.json")
    with open(ip_path, "r", encoding="utf-8") as f:
        facial_ip = json.load(f)
    
    print(f"✅ Loaded V10 Facial IP for {facial_ip['profile']['name']}")
    
    # Load just 2 references to minimize API calls
    ref_dir = Path("c:/Yuki_Local/Cosplay_Lab/References")
    valid_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    all_refs = [f for f in ref_dir.iterdir() 
                if f.suffix.lower() in valid_extensions 
                and not f.name.startswith('Unconfirmed')]
    references = all_refs[:3]  # Start with first 3 to test new photos
    
    print(f"📸 Using {len(references)} references (test batch)")
    
    # Use the NEW clearer photos of Kai (just added)
    kai_dir = Path("c:/Yuki_Local/Cosplay_Lab/Subjects/Kai Taylor")
    kai_images = sorted(list(kai_dir.glob("kai_new_*.jpg")))  # Use new clear photos
    
    print(f"👤 Loading {len(kai_images)} NEW subject images")
    
    kai_parts = []
    for img in kai_images:
        with open(img, "rb") as f:
            kai_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
    
    # Create output directory
    output_dir = Path("c:/Yuki_Local/Cosplay_Lab/Renders/kai_bella_v10_slow")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract key identity features
    critical_lock = facial_ip.get("critical_lock", [])
    
    # Simplified prompt for faster processing
    base_prompt = f"""COSPLAY GENERATION:

SUBJECT: The person shown in the first 2 photos is Kai Taylor.
TASK: Generate Kai Taylor wearing Bella Swan's (Twilight) costume from the reference.

🔒 PRESERVE KAI'S FACE EXACTLY:
- Ethnicity: {facial_ip.get('demographics', {}).get('ethnicity', 'Hispanic/Mediterranean')}  
- Skin: {facial_ip.get('skin', {}).get('tone', 'Medium Olive')} (NOT pale like Bella)
- Nose: Upturned with visible nostrils
- Eyes: Dark brown, almond shape
- Lips: Full with sharp cupid's bow

❌ DO NOT copy the face from the reference - that is Kristen Stewart.
✅ DO copy the costume, pose, and scene from the reference.

Generate Kai Taylor in Bella Swan's costume."""

    results = []
    
    for i, ref_path in enumerate(references, 1):
        print(f"\n{'='*70}")
        print(f"🎬 Generating {i}/{len(references)}: {ref_path.name}")
        print("="*70)
        
        try:
            # Load reference
            mime_type = "image/jpeg" if ref_path.suffix.lower() in ['.jpg', '.jpeg'] else f"image/{ref_path.suffix[1:]}"
            with open(ref_path, "rb") as f:
                ref_part = types.Part.from_bytes(data=f.read(), mime_type=mime_type)
            
            contents = kai_parts + [base_prompt, "Reference (costume only):", ref_part]
            
            response = await generate_with_retry(
                client,
                IMAGE_MODEL,
                contents,
                types.GenerateContentConfig(
                    response_modalities=['IMAGE', 'TEXT'],
                    temperature=1.0
                )
            )
            
            # Save image
            saved = False
            if response.candidates and response.candidates[0].content:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        output_name = f"kai_bella_{i:02d}_{ref_path.stem[:25]}.png"
                        output_path = output_dir / output_name
                        
                        with open(output_path, "wb") as f:
                            f.write(part.inline_data.data)
                        
                        print(f"   ✅ Saved: {output_name}")
                        results.append({"ref": ref_path.name, "out": str(output_path), "ok": True})
                        saved = True
                        break
            
            if not saved:
                print(f"   ⚠️ No image")
                results.append({"ref": ref_path.name, "ok": False})
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({"ref": ref_path.name, "ok": False, "err": str(e)})
        
        # 30 second delay
        if i < len(references):
            print(f"   ⏳ Waiting 30s...")
            await asyncio.sleep(30)
    
    print("\n" + "=" * 70)
    print(f"📊 DONE: {sum(1 for r in results if r.get('ok'))}/{len(references)} successful")
    print(f"📁 {output_dir}")
    print("=" * 70)
    
    return results

if __name__ == "__main__":
    asyncio.run(generate_bella_renders())
