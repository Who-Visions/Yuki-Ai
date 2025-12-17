"""
⚡ STORM V2 - ENHANCED REALISM + FACIAL DNA LOCK ⚡
Professional photography quality + exact facial preservation
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

# Enhanced prompts with photography terminology + facial DNA lock
STORM_VERSIONS_V2 = [
    {
        "name": "Classic_White_V2",
        "costume": """
        COSTUME: Storm's iconic white costume from X-Men comics
        - Flowing white bodysuit with gold accents
        - Dramatic white cape billowing naturally
        - Gold tiara headpiece with ruby gem
        - White thigh-high boots with gold trim
        - Gold arm cuffs and waist belt
        
        HAIR: Transform to long, flowing SILVER-WHITE hair
        EYES: Keep her natural brown eyes (NOT glowing)
        """,
        "scene": "Studio environment with dramatic side lighting, dark gradient background with subtle storm clouds"
    },
    {
        "name": "MCU_Leather_V2",
        "costume": """
        COSTUME: Modern MCU-style black leather X-Men tactical suit
        - Sleek black leather with subtle texture and stitching
        - Silver X-insignia on chest
        - High collar with silver accents
        - Form-fitting but realistic proportions
        - Combat boots with silver buckles
        
        HAIR: Transform to long, flowing SILVER-WHITE hair, elegantly styled
        EYES: Keep her natural brown eyes
        """,
        "scene": "Professional photo studio with dramatic rim lighting, dark moody background"
    },
    {
        "name": "90s_Animated_V2",
        "costume": """
        COSTUME: 90s X-Men Animated Series Storm
        - White bodysuit with gold accents
        - Long dramatic black cape with gold clasp
        - Gold headband/tiara
        - White boots with gold trim
        - Gold arm bands
        
        HAIR: Transform to voluminous SILVER-WHITE hair, big 90s style
        EYES: Keep her natural brown eyes
        """,
        "scene": "Dramatic hero lighting, stormy sky backdrop, lightning in distance"
    },
    {
        "name": "Mohawk_Punk_V2",
        "costume": """
        COSTUME: 80s Punk Storm with mohawk
        - Black leather jacket with silver studs and zippers
        - Black leather pants
        - Silver chains and punk accessories
        - Combat boots with buckles
        - Edgy punk aesthetic
        
        HAIR: Transform to dramatic WHITE MOHAWK, shaved sides, styled up
        EYES: Keep her natural brown eyes, add dramatic dark makeup
        """,
        "scene": "Urban night setting, neon lights in background, moody cinematic lighting"
    }
]

def build_enhanced_prompt(version: dict) -> str:
    """Build prompt with professional photography + facial DNA lock"""
    
    return f"""
═══════════════════════════════════════════════════════════════════════════════
PROFESSIONAL COSPLAY PHOTOGRAPHY - STORM FROM MARVEL X-MEN
═══════════════════════════════════════════════════════════════════════════════

You are creating a PROFESSIONAL PHOTOGRAPH of this woman in Storm cosplay.
This must look like it was shot by a professional photographer with a high-end camera.

═══════════════════════════════════════════════════════════════════════════════
🔒 FACIAL DNA LOCK - CRITICAL - DO NOT VIOLATE 🔒
═══════════════════════════════════════════════════════════════════════════════

Study this woman's face carefully and PRESERVE EXACTLY:

BONE STRUCTURE:
- Her exact face shape and bone structure
- Her exact jawline contour
- Her exact cheekbone placement and height
- Her exact chin shape and size

SKIN:
- Her exact skin tone (rich dark brown, Fitzpatrick V-VI)
- Her skin texture and natural glow
- Any natural skin characteristics

FEATURES - COPY PRECISELY:
- Her exact nose shape, bridge, and tip (she has a nose ring/septum piercing - KEEP IT)
- Her exact lip shape, fullness, and proportions
- Her exact eye shape, size, and spacing
- Her exact eyebrow shape and arch
- Her eyelash style

EXPRESSION:
- Confident, powerful expression
- Slight knowing smile or fierce determination

THE FINAL FACE MUST BE RECOGNIZABLE AS THE SAME PERSON.
If her own mother looked at the photo, she would immediately recognize her daughter.

═══════════════════════════════════════════════════════════════════════════════
CHARACTER TRANSFORMATION: STORM
═══════════════════════════════════════════════════════════════════════════════

{version['costume']}

═══════════════════════════════════════════════════════════════════════════════
📷 PROFESSIONAL PHOTOGRAPHY SPECIFICATIONS
═══════════════════════════════════════════════════════════════════════════════

CAMERA & LENS:
- Shot on Sony A7R V or Canon EOS R5
- 85mm f/1.4 portrait lens
- Shallow depth of field, f/1.8-2.8
- Sharp focus on eyes and face
- Natural bokeh in background

LIGHTING:
- Professional 3-point lighting setup
- Key light: Soft, diffused from 45 degrees
- Fill light: Subtle, reducing shadows
- Rim/hair light: Creating separation from background
- Catch lights visible in eyes

IMAGE QUALITY:
- 8K resolution, ultra-sharp
- Professional color grading
- Natural skin tones, no over-smoothing
- Visible skin texture and pores (realistic)
- No artificial HDR or over-processing

COMPOSITION:
- ASPECT RATIO: 9:16 vertical portrait (1080x1920 or equivalent)
- Full body shot showing head to mid-thigh
- Subject centered, using rule of thirds
- {version['scene']}

REALISM REQUIREMENTS:
- This must look like a REAL photograph, not AI-generated
- Natural fabric wrinkles and texture in costume
- Realistic hair physics and individual strands visible
- Natural shadowing on face and body
- Professional magazine or portfolio quality

═══════════════════════════════════════════════════════════════════════════════
OUTPUT: Generate ONE ultra-realistic professional cosplay photograph
═══════════════════════════════════════════════════════════════════════════════
"""

async def generate_storm_v2():
    """Generate enhanced Storm versions with professional realism"""
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    input_path = Path("c:/Yuki_Local/storm_input.png")
    output_dir = Path("c:/Yuki_Local/storm_results_v2")
    output_dir.mkdir(exist_ok=True)
    
    with open(input_path, "rb") as f:
        image_data = f.read()
    image_part = types.Part.from_bytes(data=image_data, mime_type="image/png")
    
    print("=" * 70)
    print("⚡ STORM V2 - ENHANCED REALISM + FACIAL DNA LOCK ⚡")
    print("=" * 70)
    print(f"Model: {MODEL}")
    print(f"Location: {LOCATION}")
    print(f"Output: {output_dir}")
    print("=" * 70)
    
    results = []
    
    for i, version in enumerate(STORM_VERSIONS_V2, 1):
        print(f"\n🌩️ [{i}/4] Generating: {version['name']}...")
        
        prompt = build_enhanced_prompt(version)
        
        try:
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
                    filename = f"Storm_{version['name']}_{timestamp}.png"
                    save_path = output_dir / filename
                    
                    with open(save_path, "wb") as f:
                        f.write(part.inline_data.data)
                    
                    size_kb = save_path.stat().st_size / 1024
                    print(f"   ✅ SAVED: {filename} ({size_kb:.1f} KB)")
                    results.append({"name": version['name'], "path": save_path, "size": size_kb})
                    break
            else:
                print(f"   ⚠️ No image in response")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # 60 second buffer
        if i < len(STORM_VERSIONS_V2):
            print(f"   ⏳ Waiting 60s...")
            await asyncio.sleep(60)
    
    print("\n" + "=" * 70)
    print(f"✅ Generated {len(results)}/4 - Opening folder...")
    print("=" * 70)
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    return results

if __name__ == "__main__":
    asyncio.run(generate_storm_v2())
