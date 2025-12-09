"""
Quick Single Image Test - Verify Gemini 3 Pro Image Preview Works
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
logger = logging.getLogger("QuickTest")

async def test_single_generation():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    logger.info("\n=== 🧪 QUICK TEST: Single Image Generation ===")
    
    # Get first image
    images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
    if not images:
        logger.error("No images found!")
        return
    
    img_path = images[0]
    logger.info(f"   📸 Input: {img_path.name}")
    
    # Initialize client
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    logger.info("   ✅ Client initialized")
    
    # Load image
    input_img = Image.open(img_path)
    logger.info(f"   ✅ Image loaded: {input_img.size}")
    
    # Simple prompt
    prompt = """Transform this person into Luffy from One Piece at a cosplay convention.

PRESERVE: Natural facial features, skin tone, age appearance, facial structure.
TRANSFORM: Hair to black, add straw hat, pirate outfit.
OUTPUT: Photorealistic cosplay photo, high quality, detailed."""
    
    logger.info("   🎨 Generating...")
    
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[input_img, prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                http_options=types.HttpOptions(timeout=10*60*1000)  # 10 min
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
            save_path = OUTPUT_DIR / "test_luffy.png"
            with open(save_path, "wb") as f:
                f.write(generated_data)
            logger.info(f"   ✅ SAVED: {save_path}")
            logger.info(f"\n   🎉 SUCCESS! Check: {save_path.absolute()}")
        else:
            logger.error("   ❌ No image data in response")
            logger.info(f"   Response parts: {response.candidates[0].content.parts}")
            
    except Exception as e:
        logger.error(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_single_generation())
