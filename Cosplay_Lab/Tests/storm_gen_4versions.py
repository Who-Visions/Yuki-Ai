"""
Storm Cosplay Generator - 4 Iconic Versions
Uses Gemini 3 Pro Image for DNA-Authentic transformations
"""

import asyncio
import base64
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
import subprocess
import os

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"  # gemini-3-pro-image-preview requires global endpoint
MODEL = "gemini-3-pro-image-preview"  # TRUE Gemini 3 Pro Image

# Storm Versions - 4 Iconic Looks
STORM_VERSIONS = [
    {
        "name": "Classic_White_Costume",
        "description": """
        Storm in her CLASSIC white costume from the X-Men comics.
        
        COSTUME DETAILS:
        - Iconic flowing white bodysuit with gold accents and cape
        - Dramatic flowing white cape billowing in the wind
        - Gold tiara headpiece with ruby gem
        - Thigh-high white boots with gold trim
        - Gold arm cuffs and belt
        
        STORM'S SIGNATURE:
        - Long, flowing WHITE/silver hair blowing dramatically in wind
        - Glowing WHITE eyes (weather powers activated)
        - Lightning crackling around her hands
        
        SETTING: Storm floating in a stormy sky, dark clouds swirling behind her,
        lightning bolts illuminating the scene. Dramatic low-angle hero shot.
        
        MOOD: Powerful, regal, goddess-like presence
        """
    },
    {
        "name": "MCU_Black_Leather",
        "description": """
        Storm in MCU-style modern black leather X-Men uniform.
        
        COSTUME DETAILS:
        - Sleek black leather tactical suit with silver X-insignia
        - Form-fitting armored bodysuit with subtle texture
        - High collar with silver accents
        - Fingerless black gloves
        - Combat boots with silver buckles
        
        STORM'S SIGNATURE:
        - Long flowing WHITE/silver hair, styled elegantly
        - Glowing WHITE eyes showing power activation
        - Electricity arcing between fingers
        
        SETTING: Xavier's mansion garden at night during a thunderstorm,
        rain falling around her but not touching her. Cinematic lighting.
        
        MOOD: Modern superhero, fierce protector, MCU blockbuster quality
        """
    },
    {
        "name": "90s_Animated_Series",
        "description": """
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
    },
    {
        "name": "Mohawk_Punk_Storm",
        "description": """
        Storm in her iconic 80s PUNK/MOHAWK era look.
        
        COSTUME DETAILS:
        - Black leather punk jacket with silver studs
        - Black leather pants or leggings
        - Silver chains and punk accessories
        - Combat boots with buckles
        - Fishnet elements under leather
        
        STORM'S SIGNATURE:
        - Dramatic WHITE MOHAWK hairstyle, shaved sides
        - Intense eyes with dark dramatic makeup
        - Confident, rebellious expression
        - Lightning crackling around her
        
        SETTING: Urban rooftop at night, neon city lights below,
        storm clouds gathering above. Gritty, punk aesthetic.
        
        MOOD: Rebellious, fierce, "don't mess with me" energy, punk goddess
        """
    }
]

async def generate_storm_versions():
    """Generate 4 Storm versions preserving user's facial identity"""
    
    # Initialize client
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION
    )
    
    # Load input image
    input_path = Path("c:/Yuki_Local/storm_input.png")
    output_dir = Path("c:/Yuki_Local/storm_results")
    
    with open(input_path, "rb") as f:
        image_data = f.read()
    
    image_part = types.Part.from_bytes(
        data=image_data,
        mime_type="image/png"
    )
    
    print("=" * 60)
    print("⚡ STORM COSPLAY GENERATOR - 4 ICONIC VERSIONS ⚡")
    print("=" * 60)
    print(f"Input: {input_path}")
    print(f"Output: {output_dir}")
    print(f"Model: {MODEL}")
    print("=" * 60)
    
    results = []
    
    for i, version in enumerate(STORM_VERSIONS, 1):
        print(f"\n🌩️ [{i}/4] Generating: {version['name']}...")
        
        # DNA-Authentic prompt preserving user's identity
        prompt = f"""
        TASK: Transform this person into Storm from Marvel X-Men.
        
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
        CHARACTER TRANSFORMATION: STORM - {version['name']}
        ═══════════════════════════════════════════════════════════════
        
        {version['description']}
        
        ═══════════════════════════════════════════════════════════════
        TECHNICAL REQUIREMENTS
        ═══════════════════════════════════════════════════════════════
        
        - Resolution: 4K ultra-high definition
        - Style: Photorealistic professional cosplay photography
        - Lighting: Dramatic cinematic lighting with storm effects
        - Camera: Full body or 3/4 shot, heroic angle
        - Quality: Cover of Marvel Comics or movie poster quality
        - Aspect Ratio: Portrait orientation
        
        CREATE AN EPIC, POWERFUL IMAGE OF HER AS STORM!
        """
        
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
                        types.SafetySetting(
                            category="HARM_CATEGORY_HARASSMENT",
                            threshold="BLOCK_ONLY_HIGH"
                        ),
                        types.SafetySetting(
                            category="HARM_CATEGORY_HATE_SPEECH", 
                            threshold="BLOCK_ONLY_HIGH"
                        ),
                        types.SafetySetting(
                            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            threshold="BLOCK_ONLY_HIGH"
                        ),
                        types.SafetySetting(
                            category="HARM_CATEGORY_DANGEROUS_CONTENT",
                            threshold="BLOCK_ONLY_HIGH"
                        ),
                    ]
                )
            )
            
            # Extract and save image
            saved = False
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"Storm_{version['name']}_{timestamp}.png"
                    save_path = output_dir / filename
                    
                    image_bytes = part.inline_data.data
                    with open(save_path, "wb") as f:
                        f.write(image_bytes)
                    
                    size_kb = save_path.stat().st_size / 1024
                    print(f"   ✅ SAVED: {filename} ({size_kb:.1f} KB)")
                    results.append({
                        "version": version['name'],
                        "path": str(save_path),
                        "size_kb": size_kb
                    })
                    saved = True
                    break
            
            if not saved:
                print(f"   ⚠️ No image in response for {version['name']}")
                # Check for text response
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'text') and part.text:
                        print(f"   Text response: {part.text[:200]}...")
                        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "version": version['name'],
                "error": str(e)
            })
        
        # 60 second buffer between generations to avoid 429 rate limiting
        if i < len(STORM_VERSIONS):
            print(f"   ⏳ Waiting 60s before next generation...")
            await asyncio.sleep(60)
    
    # Summary
    print("\n" + "=" * 60)
    print("⚡ GENERATION COMPLETE ⚡")
    print("=" * 60)
    
    successful = [r for r in results if "path" in r]
    print(f"\n✅ Successfully generated: {len(successful)}/4 versions")
    
    for r in results:
        if "path" in r:
            print(f"   🌩️ {r['version']}: {r['path']}")
        else:
            print(f"   ❌ {r['version']}: {r.get('error', 'Unknown error')}")
    
    print(f"\n📁 Output folder: {output_dir}")
    print("=" * 60)
    
    # Auto-open folder in Windows Explorer
    print("\n📂 Opening output folder...")
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    
    return results

if __name__ == "__main__":
    asyncio.run(generate_storm_versions())
