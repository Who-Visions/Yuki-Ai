"""
⚡ STORM 90s ANIMATED SERIES - RETRY ⚡
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
import subprocess

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
MODEL = "gemini-3-pro-image-preview"

STORM_90S = """
Storm in her iconic 90s X-Men Animated Series look.

COSTUME DETAILS:
- White one-piece swimsuit-style bodysuit
- Long dramatic black cape with gold clasp
- Gold headband/tiara
- Thigh-high white boots
- Gold arm bands

STORM'S SIGNATURE:
- BIG flowing WHITE hair, 90s cartoon volume
- Glowing WHITE pupil-less eyes
- Arms raised, summoning a massive tornado

SETTING: Standing on a cliff edge, tornado forming behind her,
lightning striking in the background. Bold comic book colors.

MOOD: Nostalgic 90s cartoon energy, "I summon the WIND!" vibes
"""

async def generate_90s():
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    input_path = Path("c:/Yuki_Local/storm_input.png")
    output_dir = Path("c:/Yuki_Local/storm_results")
    
    with open(input_path, "rb") as f:
        image_data = f.read()
    image_part = types.Part.from_bytes(data=image_data, mime_type="image/png")
    
    print("⚡ Generating 90s Animated Series Storm...")
    print(f"   Model: {MODEL}")
    print(f"   Location: {LOCATION}")
    
    prompt = f"""
    TASK: Transform this person into Storm from Marvel X-Men 90s Animated Series.
    
    ═══════════════════════════════════════════════════════════════
    ⚠️ CRITICAL IDENTITY PRESERVATION (DNA-AUTHENTIC) ⚠️
    ═══════════════════════════════════════════════════════════════
    
    PRESERVE EXACTLY (DO NOT CHANGE):
    - Her EXACT face shape, bone structure, and facial proportions
    - Her beautiful dark brown/black skin tone (Fitzpatrick Type V-VI)
    - Her exact nose shape and nose ring/septum piercing
    - Her exact lip shape and size
    - Her exact eye shape and warm brown eye color
    - Her exact eyebrow shape and arch
    - Her makeup style (dark lips, lashes)
    - Her natural beauty and elegance
    
    ═══════════════════════════════════════════════════════════════
    CHARACTER: 90s X-MEN ANIMATED SERIES STORM
    ═══════════════════════════════════════════════════════════════
    
    {STORM_90S}
    
    ═══════════════════════════════════════════════════════════════
    TECHNICAL REQUIREMENTS
    ═══════════════════════════════════════════════════════════════
    
    - Resolution: 4K ultra-high definition
    - Style: Photorealistic professional cosplay photography
    - Lighting: Dramatic lightning and storm effects
    - Camera: Full body or 3/4 shot, heroic angle
    - Quality: Cover of Marvel Comics quality
    
    GENERATE THE IMAGE NOW. Do not describe, just create the image.
    """
    
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=[prompt, image_part],
        config=types.GenerateContentConfig(
            temperature=1.0,
            top_p=0.95,
            top_k=40,
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
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Storm_90s_Animated_Series_{timestamp}.png"
            save_path = output_dir / filename
            
            with open(save_path, "wb") as f:
                f.write(part.inline_data.data)
            
            size_kb = save_path.stat().st_size / 1024
            print(f"   ✅ SAVED: {filename} ({size_kb:.1f} KB)")
            
            subprocess.Popen(f'explorer "{output_dir}"', shell=True)
            return save_path
    
    print("   ⚠️ No image generated, got text response")
    return None

if __name__ == "__main__":
    asyncio.run(generate_90s())
