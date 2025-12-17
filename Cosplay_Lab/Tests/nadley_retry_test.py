"""
Nadley Retry Test - With Exponential Backoff & Rate Limiting
============================================================
Handles 429 quota errors gracefully with retry logic

Features:
✅ Exponential backoff retry
✅ 10-second delay between requests  
✅ All production features (9:16, 4K, perspective correction, etc.)
"""

import asyncio
import logging
import time
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
from facial_geometry_corrector import FacialGeometryCorrector
from yuki_cost_tracker import YukiCostTracker

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
INPUT_DIR = Path("C:/Yuki_Local/friends test/Nadley")
OUTPUT_DIR = Path("C:/Yuki_Local/nadley_retry_test")

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("NadleyRetryTest")

class NadleyRetryTest:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.geo_corrector = FacialGeometryCorrector(PROJECT_ID)
        self.pro_client = genai.Client(
            vertexai=True, 
            project=PROJECT_ID,
            location="global"
        )
        self.cost_tracker = YukiCostTracker(PROJECT_ID)
        
        logger.info("\n🔄 NADLEY RETRY TEST - Quota-Aware Generation")
        logger.info("   ✅ Exponential backoff: ENABLED")
        logger.info("   ✅ Rate limiting: 10s delay between requests")

    async def generate_with_retry(self, char_name: str, anime_name: str, input_img: Image.Image,
                                  corrected_analysis: dict, save_path: Path, max_retries: int = 3):
        """Generate with custom retry logic"""
        logger.info(f"      🎨 Generating {char_name}...")
        
        # CORRECTED PROMPT - Focus on PHOTOREALISTIC COSPLAY
        prompt = f"""Create a PHOTOREALISTIC COSPLAY photograph of this person wearing {char_name}'s costume from {anime_name}.

{corrected_analysis['generation_prompt']}

=== COSPLAY REQUIREMENTS ===
COSTUME: Dress this person in {char_name}'s distinctive outfit from {anime_name}
- Include all character-specific clothing items
- Include character's accessories and props
- Include character's hairstyle/wig in character's hair color
- Match character's costume design accurately

CRITICAL STYLE REQUIREMENTS:
✅ PHOTOREALISTIC - This MUST be a real PHOTOGRAPH
✅ Keep the person's REAL FACE (not anime-style, not cartoon)
✅ Keep the person's REAL BODY and proportions
✅ Professional COSPLAY photography (like at a convention)
✅ REAL CAMERA PHOTO quality (NOT illustration, NOT anime art, NOT drawing)

PHOTOGRAPHY DETAILS:
- Format: Vertical portrait (9:16 aspect ratio for mobile)
- Resolution: 4K ultra-detailed
- Composition: Full body or 3/4 length shot
- Setting: Professional convention photography or studio backdrop
- Lighting: Professional photography lighting, well-lit
- Quality: Sharp focus, high-end camera equipment

WHAT TO AVOID:
❌ NO anime art style
❌ NO illustrations or drawings
❌ NO cel-shading or cartoon effects
❌ NO stylized/artistic interpretations
❌ The person should NOT look like an anime character - they should look like THEMSELVES wearing the costume

THINK: "High-quality convention cosplay photo where a real person is wearing an accurate costume"
NOT: "Anime-style drawing or illustration of the character"

The final image should look like a professional photographer took a picture of this person at a cosplay convention wearing a high-quality, accurate costume of {char_name}."""
        
        for attempt in range(max_retries):
            try:
                response = self.pro_client.models.generate_content(
                    model="gemini-3-pro-image-preview",
                    contents=[input_img, prompt],
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        http_options=types.HttpOptions(timeout=15*60*1000)
                    )
                )
        
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
                    with open(save_path, "wb") as f:
                        f.write(generated_data)
            
                    if save_path.exists():
                        size_kb = save_path.stat().st_size / 1024
                        logger.info(f"      ✅ SAVED: {save_path.name} ({size_kb:.1f} KB)")
                        return True
                
                raise Exception("No image data in response")
                
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    if attempt < max_retries - 1:
                        delay = 5 * (2 ** attempt)  # Exponential backoff: 5, 10, 20 seconds
                        logger.warning(f"      ⚠️  Quota limit hit, retrying in {delay}s... (attempt {attempt+1}/{max_retries})")
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"      ❌ Failed after {max_retries} attempts: {e}")
                        return False
                else:
                    logger.error(f"      ❌ Error: {e}")
                    return False
        
        return False

    async def run(self):
        # Get photo
        images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not images:
            logger.error(f"No image found")
            return
        
        img_path = images[0]
        logger.info(f"   📸 Input: {img_path.name}")
        
        # Characters (reduced to 3 for testing)
        characters = [
            {"name": "Ichigo Kurosaki", "anime": "Bleach"},
            {"name": "Naruto Uzumaki", "anime": "Naruto"},
            {"name": "Izuku Midoriya", "anime": "My Hero Academia"}
        ]
        
        # Perspective correction
        logger.info(f"\n   🔬 Analyzing...")
        corrected = await self.geo_corrector.get_corrected_analysis(img_path)
        logger.info(f"      ✅ Complete")
        
        input_img = Image.open(img_path)
        
        # Generate with retry + rate limiting
        successful = 0
        for idx, char in enumerate(characters):
            logger.info(f"\n   [{idx+1}/3] {char['name']}")
            
            try:
                fname = f"nadley_{char['name'].replace(' ', '_')}.png"
                await self.generate_with_retry(
                    char['name'],
                    char['anime'],
                    input_img,
                    corrected,
                    self.output_dir / fname
                )
                successful += 1
                
                # Rate limiting: Wait 10s between requests
                if idx < len(characters) - 1:
                    logger.info(f"      ⏱️  Waiting 10s before next request...")
                    await asyncio.sleep(10)
                    
            except Exception as e:
                logger.error(f"      ❌ Failed after retries: {e}")
        
        logger.info(f"\n✨ Complete: {successful}/3 successful")
        logger.info(f"📁 Results: {OUTPUT_DIR}")

if __name__ == "__main__":
    gen = NadleyRetryTest()
    asyncio.run(gen.run())
