"""
Jesse Improved Test - WITH Perspective Correction
Includes geometric distortion compensation for accurate facial proportions
"""

import sys
sys.path.append('C:/Yuki_Local')

import asyncio
import logging
import time
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
from facial_geometry_corrector import FacialGeometryCorrector

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
INPUT_DIR = Path("C:/Yuki_Local/jesse 1 pic test")
OUTPUT_DIR = Path("C:/Yuki_Local/jesse_corrected_results")

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("JesseCorrectedTest")

class JesseCorrectedTest:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.geo_corrector = FacialGeometryCorrector(PROJECT_ID)
        self.pro_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
        
        logger.info("\n=== 🔬 JESSE CORRECTED TEST (Perspective-Aware) ===")

    async def generate_corrected(self, char_name: str, anime_name: str, input_img: Image.Image, corrected_analysis: dict, save_path: Path):
        """Generate with perspective-corrected proportions"""
        logger.info(f"      🎨 Generating {char_name} (Corrected)...")
        
        full_prompt = f"""Transform this person into {char_name} from {anime_name}.

{corrected_analysis['generation_prompt']}

CHARACTER: {char_name} from {anime_name}
STYLE: Classic anime aesthetic, photorealistic cosplay
QUALITY: 4K resolution, highly detailed

CRITICAL: Use the CORRECTED proportions above, NOT the distorted input."""
        
        try:
            response = self.pro_client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=[input_img, full_prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    http_options=types.HttpOptions(timeout=15*60*1000)
                )
            )
            
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'image') and part.image:
                        with open(save_path, "wb") as f:
                            f.write(part.image.image_bytes)
                        logger.info(f"      ✅ Saved (corrected): {save_path.name}")
                        return True
        except Exception as e:
            logger.error(f"      ❌ Error: {e}")
        return False

    async def run(self):
        images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not images:
            return
        
        img_path = images[0]
        logger.info(f"   📸 Input: {img_path.name}")
        
        # Get perspective-corrected analysis
        logger.info(f"\n   🔬 Running Perspective Correction...")
        corrected = await self.geo_corrector.get_corrected_analysis(img_path)
        logger.info(f"      ✅ Geometric correction complete")
        
        input_img = Image.open(img_path)
        
        # Test with 3 characters
        test_chars = [
            {"name": "Spike Spiegel", "anime": "Cowboy Bebop"},
            {"name": "Vash the Stampede", "anime": "Trigun"},
            {"name": "Kenshin Himura", "anime": "Rurouni Kenshin"}
        ]
        
        for idx, char in enumerate(test_chars):
            logger.info(f"\n   🎭 [{idx+1}/3] {char['name']}")
            fname = f"corrected_{char['name'].replace(' ', '_')}.png"
            await self.generate_corrected(char['name'], char['anime'], input_img, corrected, self.output_dir / fname)

if __name__ == "__main__":
    gen = JesseCorrectedTest()
    asyncio.run(gen.run())
