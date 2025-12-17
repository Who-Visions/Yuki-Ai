"""
Nadley Test - Top 10 Anime from 2012
WITH Perspective Correction for accurate facial proportions
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
INPUT_DIR = Path("C:/Yuki_Local/friends test/Nadley")
OUTPUT_DIR = Path("C:/Yuki_Local/nadley_2012_results")

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("nadley_test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NadleyTest")

class Nadley2012Test:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.geo_corrector = FacialGeometryCorrector(PROJECT_ID)
        self.pro_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
        
        logger.info("\n=== 🎯 NADLEY - TOP 10 ANIME FROM 2012 ===")
        logger.info("   🔬 Perspective Correction: ENABLED")

    async def generate_transformation(self, char_name: str, anime_name: str, input_img: Image.Image, corrected_analysis: dict, save_path: Path):
        """Generate with perspective-corrected proportions"""
        logger.info(f"      🎨 Generating {char_name}...")
        
        full_prompt = f"""Transform this person into {char_name} from {anime_name}.

{corrected_analysis['generation_prompt']}

CHARACTER: {char_name} from {anime_name}
YEAR: 2012 anime aesthetic
STYLE: Photorealistic cosplay, 4K resolution
QUALITY: Highly detailed, accurate character design

CRITICAL: Use the CORRECTED proportions above, NOT the distorted input photo."""
        
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
                        logger.info(f"      ✅ Saved: {save_path.name}")
                        return True
        except Exception as e:
            logger.error(f"      ❌ Error: {e}")
        return False

    async def run(self):
        start_time = time.time()
        
        # Get Nadley's photo
        images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not images:
            logger.error(f"   ❌ No image found in {INPUT_DIR}")
            return
        
        img_path = images[0]
        logger.info(f"   📸 Input: {img_path.name}")
        
        # Top 10 Anime from 2012 (with main characters)
        anime_2012 = [
            {"name": "Kirito", "anime": "Sword Art Online"},
            {"name": "Shinya Kogami", "anime": "Psycho-Pass"},
            {"name": "Kiritsugu Emiya", "anime": "Fate/Zero 2nd Season"},
            {"name": "Houtarou Oreki", "anime": "Hyouka"},
            {"name": "Joseph Joestar", "anime": "JoJo's Bizarre Adventure"},
            {"name": "Sorata Kanda", "anime": "Sakurasou no Pet na Kanojo"},
            {"name": "Yuuta Togashi", "anime": "Chuunibyou demo Koi ga Shitai!"},
            {"name": "Taichi Yaegashi", "anime": "Kokoro Connect"},
            {"name": "Koyomi Araragi", "anime": "Nisemonogatari"},
            {"name": "Kouichi Sakakibara", "anime": "Another"}
        ]
        
        # Get perspective-corrected analysis
        logger.info(f"\n   🔬 Running Perspective Correction Analysis...")
        analysis_start = time.time()
        corrected = await self.geo_corrector.get_corrected_analysis(img_path)
        analysis_time = time.time() - analysis_start
        logger.info(f"      ✅ Geometric correction complete ({analysis_time:.2f}s)")
        
        input_img = Image.open(img_path)
        
        # Generate all 10 transformations
        successful = 0
        for idx, char in enumerate(anime_2012):
            iter_start = time.time()
            logger.info(f"\n   🎭 [{idx+1}/10] {char['name']} ({char['anime']})")
            
            fname = f"nadley_{char['name'].replace(' ', '_')}.png"
            result = await self.generate_transformation(
                char['name'], 
                char['anime'], 
                input_img, 
                corrected, 
                self.output_dir / fname
            )
            
            if result:
                successful += 1
            
            iter_time = time.time() - iter_start
            logger.info(f"      ⏱️  Time: {iter_time:.2f}s")
        
        total_time = time.time() - start_time
        
        logger.info("\n=== ✨ TEST COMPLETE ===")
        logger.info(f"   ✅ Successful: {successful}/10")
        logger.info(f"   ⏱️  Total Time: {total_time:.2f}s ({total_time/60:.2f} min)")
        logger.info(f"   📁 Results: {OUTPUT_DIR}")

if __name__ == "__main__":
    gen = Nadley2012Test()
    asyncio.run(gen.run())
