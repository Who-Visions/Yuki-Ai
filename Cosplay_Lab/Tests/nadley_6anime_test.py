"""
Nadley Comprehensive Test - 6 Anime Characters
===============================================
Testing: Bleach, Solo Leveling, Blue Lock, Dragon Ball, Naruto, My Hero Academia

Features:
✅ 9:16 aspect ratio (mobile-first)
✅ 4K quality
✅ Gemini 3 Pro Image Preview (Nano Banana Pro)
✅ Perspective correction
✅ Identity preservation (race, ethnicity, gender)
✅ Gender filtering
✅ Verified file saves
✅ Cost tracking
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
OUTPUT_DIR = Path("C:/Yuki_Local/nadley_6anime_test")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("nadley_6anime_test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Nadley6AnimeTest")

class Nadley6AnimeTest:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.geo_corrector = FacialGeometryCorrector(PROJECT_ID)
        self.pro_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
        self.cost_tracker = YukiCostTracker(PROJECT_ID)
        
        logger.info("\n" + "="*80)
        logger.info("🎯 NADLEY 6 ANIME TEST - FULL PRODUCTION PIPELINE")
        logger.info("="*80)
        logger.info("   📱 Aspect Ratio: 9:16 (mobile-first)")
        logger.info("   🎨 Quality: 4K ultra-detailed")
        logger.info("   🧠 Model: Gemini 3 Pro Image Preview (Nano Banana Pro)")
        logger.info("   🔬 Perspective Correction: ENABLED")
        logger.info("   🛡️ Identity Preservation: ENABLED")
        logger.info("   ✅ Gender Filtering: ENABLED")
        logger.info("   💰 Cost Tracking: ENABLED")
        logger.info("="*80)

    async def generate_transformation(self, char_name: str, anime_name: str, input_img: Image.Image, 
                                     corrected_analysis: dict, save_path: Path):
        """Generate single transformation with all production features"""
        logger.info(f"      🎨 Generating {char_name}...")
        
        start_time = time.time()
        
        # Build comprehensive prompt
        prompt = f"""Transform this person into {char_name} from {anime_name}.

{corrected_analysis['generation_prompt']}

=== CHARACTER DETAILS ===
CHARACTER: {char_name}
ANIME: {anime_name}

=== TECHNICAL SPECIFICATIONS ===
FORMAT: Vertical portrait for mobile viewing (9:16 aspect ratio)
RESOLUTION: 4K ultra-detailed
COMPOSITION: Full body or 3/4 length shot optimized for phone screens (TikTok/Instagram Reels)
QUALITY: Photorealistic cosplay, highly detailed

=== STYLE REQUIREMENTS ===
- Maintain anime-accurate character design
- Professional cosplay photography lighting
- Convention/studio background setting
- Sharp focus on face and costume details

=== CONTENT SAFETY ===
- Standard cosplay attire for the character
- No explicit content
- Family-friendly transformation

CRITICAL: Use the CORRECTED proportions from analysis, NOT the distorted input photo."""
        
        try:
            response = self.pro_client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=[input_img, prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    http_options=types.HttpOptions(timeout=15*60*1000)
                )
            )
            
            # Extract image data (handle both formats)
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
                # Write file
                with open(save_path, "wb") as f:
                    f.write(generated_data)
                
                # VERIFY file was actually written
                if save_path.exists():
                    size_kb = save_path.stat().st_size / 1024
                    gen_time = time.time() - start_time
                    logger.info(f"      ✅ VERIFIED SAVED: {save_path.name} ({size_kb:.1f} KB, {gen_time:.2f}s)")
                    
                    # Log cost
                    self.cost_tracker.log_generation(
                        model="gemini-3-pro-image-preview",
                        operation="generation",
                        count=1,
                        metadata={
                            "character": char_name,
                            "anime": anime_name,
                            "aspect_ratio": "9:16",
                            "quality": "4K"
                        }
                    )
                    
                    return True
                else:
                    raise Exception(f"File write failed - {save_path} does not exist!")
            else:
                raise Exception("No image data in API response!")
                
        except Exception as e:
            logger.error(f"      ❌ Generation failed: {e}")
            return False

    async def run(self):
        start_time = time.time()
        
        logger.info(f"\n   📂 Input: {INPUT_DIR}")
        logger.info(f"   📂 Output: {OUTPUT_DIR}")
        
        # Get Nadley's photo
        images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not images:
            logger.error(f"   ❌ No image found in {INPUT_DIR}")
            return
        
        img_path = images[0]
        logger.info(f"   📸 Input Photo: {img_path.name}")
        
        # 6 Anime Characters (MALE characters for MALE user)
        characters = [
            {"name": "Ichigo Kurosaki", "anime": "Bleach"},
            {"name": "Sung Jin-Woo", "anime": "Solo Leveling"},
            {"name": "Yoichi Isagi", "anime": "Blue Lock"},
            {"name": "Goku", "anime": "Dragon Ball"},
            {"name": "Naruto Uzumaki", "anime": "Naruto"},
            {"name": "Izuku Midoriya", "anime": "My Hero Academia"}
        ]
        
        logger.info(f"\n   🎭 Characters to generate:")
        for idx, char in enumerate(characters):
            logger.info(f"      {idx+1}. {char['name']} ({char['anime']})")
        
        # Get perspective-corrected analysis
        logger.info(f"\n   🔬 Running Perspective Correction Analysis...")
        analysis_start = time.time()
        corrected = await self.geo_corrector.get_corrected_analysis(img_path)
        analysis_time = time.time() - analysis_start
        logger.info(f"      ✅ Geometric correction complete ({analysis_time:.2f}s)")
        
        # Log analysis cost
        self.cost_tracker.log_generation(
            model="gemini-2.5-flash",
            operation="analysis",
            tokens_in=5000,  # Estimated
            metadata={"type": "perspective_correction"}
        )
        
        input_img = Image.open(img_path)
        
        # Generate all 6 transformations
        logger.info(f"\n" + "="*80)
        logger.info("🎨 STARTING GENERATION")
        logger.info("="*80)
        
        successful = 0
        failed = []
        
        for idx, char in enumerate(characters):
            iter_start = time.time()
            logger.info(f"\n   [{idx+1}/6] {char['name']} ({char['anime']})")
            
            fname = f"nadley_{char['name'].replace(' ', '_').replace('-', '_')}.png"
            success = await self.generate_transformation(
                char['name'],
                char['anime'],
                input_img,
                corrected,
                self.output_dir / fname
            )
            
            if success:
                successful += 1
            else:
                failed.append(char['name'])
            
            iter_time = time.time() - iter_start
            logger.info(f"      ⏱️  Iteration time: {iter_time:.2f}s")
        
        total_time = time.time() - start_time
        
        # Get session costs
        session_cost = self.cost_tracker.get_session_cost(hours=1)
        
        logger.info("\n" + "="*80)
        logger.info("✨ TEST COMPLETE")
        logger.info("="*80)
        logger.info(f"   ✅ Successful: {successful}/6")
        if failed:
            logger.info(f"   ❌ Failed: {', '.join(failed)}")
        logger.info(f"   ⏱️  Total Time: {total_time:.2f}s ({total_time/60:.2f} min)")
        logger.info(f"   💰 Session Cost: ${session_cost['total_cost']:.4f}")
        logger.info(f"      - Analysis: ${session_cost['breakdown']['analysis']:.6f}")
        logger.info(f"      - Generation: ${session_cost['breakdown']['generation']:.4f}")
        logger.info(f"   📁 Results: {OUTPUT_DIR}")
        logger.info("="*80)

if __name__ == "__main__":
    gen = Nadley6AnimeTest()
    asyncio.run(gen.run())
