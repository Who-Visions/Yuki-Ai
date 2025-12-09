"""
Single Image Test - Sung Jin-Woo (Solo Leveling) - 4K Quality
"""

import asyncio
import logging
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

PROJECT_ID = "gifted-cooler-479623-r7"
INPUT_DIR = Path("C:/Yuki_Local/dave test images")
OUTPUT_DIR = Path("real_gen_results_test")

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("SoloLevelingTest")

async def generate_solo_leveling():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    logger.info("\n=== 🗡️ SOLO LEVELING TEST: Sung Jin-Woo (4K) ===")
    
    # Get first image
    images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
    if not images:
        logger.error("No images found!")
        return
    
    img_path = images[0]
    logger.info(f"   📸 Input: {img_path.name}")
    
    # Initialize client
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    logger.info("   ✅ Gemini 3 Pro Image Preview initialized")
    
    # Load image
    input_img = Image.open(img_path)
    logger.info(f"   ✅ Image loaded: {input_img.size}")
    
    # Detailed 4K prompt for Sung Jin-Woo
    prompt = """Transform this person into Sung Jin-Woo from Solo Leveling at a high-end cosplay convention.

CHARACTER DETAILS:
- Sung Jin-Woo, the Shadow Monarch
- Iconic black armor with glowing purple accents
- Dual daggers or shadow weapons
- Intense, confident expression
- Dark, sleek hairstyle
- Powerful, commanding presence

PRESERVE (DNA-AUTHENTIC):
- Natural facial structure and bone structure
- Exact skin tone and ethnic features
- Age appearance (maintain natural age)
- Eye shape, nose shape, lip shape
- Facial proportions and geometry
- Body build and height proportions

TRANSFORM:
- Hair: Dark, styled like Jin-Woo
- Outfit: Black armor with purple glowing details
- Weapons: Dual daggers or shadow effects
- Expression: Confident, intense hunter gaze
- Lighting: Dramatic, with purple shadow aura

SETTING:
- High-end cosplay convention
- Professional photography lighting
- Dramatic background with shadow effects

QUALITY:
- 4K resolution
- Ultra-detailed masterpiece
- 8k textures
- Photorealistic
- Highly detailed armor and weapon details
- Professional cosplay photography quality

CONTENT SAFETY:
- Maintain appropriate coverage
- No explicit content
- Focus on powerful, heroic aesthetic"""
    
    logger.info("   🎨 Generating 4K Sung Jin-Woo transformation...")
    
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[input_img, prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                http_options=types.HttpOptions(timeout=15*60*1000)  # 15 min
            )
        )
        
        logger.info("   ✅ Response received")
        
        # Extract image
        generated_data = None
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'image') and part.image:
                    generated_data = part.image.image_bytes
                    break
                elif hasattr(part, 'inline_data') and part.inline_data:
                    generated_data = part.inline_data.data
                    break
        
        if generated_data:
            save_path = OUTPUT_DIR / "test_sung_jinwoo_4k.png"
            with open(save_path, "wb") as f:
                f.write(generated_data)
            
            # Get file size
            size_mb = len(generated_data) / (1024 * 1024)
            
            logger.info(f"   ✅ SAVED: {save_path}")
            logger.info(f"   📊 File size: {size_mb:.2f} MB")
            logger.info(f"\n   🎉 SUCCESS! Sung Jin-Woo 4K render complete!")
            logger.info(f"   📁 Location: {save_path.absolute()}")
        else:
            logger.error("   ❌ No image data in response")
            
    except Exception as e:
        logger.error(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(generate_solo_leveling())
