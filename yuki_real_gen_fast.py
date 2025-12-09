"""
Yuki Real Gen FAST - Gemini 2.5 Flash Edition
Optimized for speed while maintaining DNA authenticity
"""

import asyncio
import logging
import time
from pathlib import Path
from google import genai
from google.genai import types
from google.api_core import retry
from PIL import Image

from filename_utils import generate_filename

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
INPUT_DIR = Path("C:/Yuki_Local/dave test images")
OUTPUT_DIR = Path("real_gen_results_fast")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("real_gen_fast.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("YukiRealGenFast")


class YukiRealGenFast:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("\n=== ⚡ YUKI REAL GEN FAST (GEMINI 2.5 FLASH) ===")
        
        # Initialize client
        self.client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        logger.info("   ✅ Gemini 2.5 Flash Online")

    async def analyze_all_features(self, image_path: Path) -> dict:
        """Single comprehensive analysis using Gemini 2.5 Flash"""
        img = Image.open(image_path)
        
        prompt = """Analyze this person's features for authentic cosplay transformation. Provide:

1. AGE: Estimated age range and category (child/teen/young adult/adult/senior)
2. SKIN: Exact skin tone (RGB values if possible, Fitzpatrick scale)
3. FACE: Detailed facial structure (face shape, proportions, ethnic features)
4. HAIR: Natural hair color, texture, style
5. EYES: Eye color, shape, size
6. NOSE: Nose shape and size
7. MOUTH: Lip shape and fullness
8. BODY: Build type (slim/average/athletic/plus-size), height proportions
9. GENDER: Apparent gender presentation

Respond in JSON format with all details."""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[img, prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT"],
                    temperature=0.1
                )
            )
            
            # Parse response (simplified - in production would use structured output)
            analysis_text = response.text
            
            return {
                "raw_analysis": analysis_text,
                "preservation_prompt": f"""PRESERVE AUTHENTIC FEATURES:
{analysis_text}

CRITICAL: Maintain ALL natural features, proportions, skin tone, age appearance, and facial structure."""
            }
        except Exception as e:
            logger.warning(f"   ⚠️ Analysis failed: {e}. Using fallback.")
            return {
                "raw_analysis": "Analysis unavailable",
                "preservation_prompt": "PRESERVE: Natural facial features, skin tone, age appearance, and body proportions."
            }

    @retry.Retry(predicate=retry.if_transient_error, initial=2.0, maximum=32.0, timeout=300)
    async def generate_image(self, prompt: str, input_image_path: Path, analysis: dict, save_path: Path):
        """Generate with Gemini 2.5 Flash (text-only, no image gen yet in Flash)"""
        logger.info(f"      🎨 Generating with gemini-2.5-flash...")
        
        try:
            input_img = Image.open(input_image_path)
            
            # Build comprehensive prompt
            full_prompt = f"""Transform this person into: {prompt}

=== DNA-AUTHENTIC TRANSFORMATION PROTOCOL ===

{analysis['preservation_prompt']}

=== TRANSFORMATION RULES ===
1. PRESERVE: Face structure, facial proportions, ethnic features, skin tone, age appearance
2. TRANSFORM: Hair style/color, outfit, accessories, styling to match character
3. MAINTAIN: All natural bone structure, eye shape, nose shape, lip shape
4. OUTPUT: Photorealistic cosplay that honors the person's authentic features

QUALITY: 4K resolution, highly detailed, photorealistic masterpiece."""
            
            # NOTE: Gemini 2.5 Flash doesn't support image OUTPUT yet
            # We'll use it for analysis only and note this limitation
            logger.warning(f"      ⚠️ Gemini 2.5 Flash doesn't support image generation yet")
            logger.info(f"      📝 Prompt prepared: {save_path.name}")
            
            # Save prompt for reference
            prompt_path = save_path.with_suffix('.txt')
            with open(prompt_path, 'w', encoding='utf-8') as f:
                f.write(full_prompt)
            
            return True
            
        except Exception as e:
            logger.error(f"      ❌ Error: {e}")
            return False

    async def run(self):
        start_time = time.time()
        
        logger.info(f"\n=== 🎯 YUKI FAST TEST: DAVE SCENARIO ===")
        logger.info(f"   📂 Input: {INPUT_DIR}")
        logger.info(f"   📂 Output: {OUTPUT_DIR}")
        logger.info(f"   🔬 Model: gemini-2.5-flash (Analysis Only)")
        logger.info(f"   ⚡ Mode: Speed Test")
        
        # Get Images
        images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not images:
            logger.warning("   ⚠️ No images found!")
            return
        
        # Targets
        targets = [
            {"char": "Luffy", "anime": "One Piece"},
            {"char": "Gojo Satoru", "anime": "Jujutsu Kaisen"},
            {"char": "Tanjiro Kamado", "anime": "Demon Slayer"},
            {"char": "Naruto Uzumaki", "anime": "Naruto"},
            {"char": "Spike Spiegel", "anime": "Cowboy Bebop"},
            {"char": "Edward Elric", "anime": "Fullmetal Alchemist"}
        ]
        
        conventions = [
            "Tokyo Comic Con", "San Diego Comic-Con", "Anime Expo",
            "Comiket", "Dragon Con", "New York Comic Con"
        ]
        
        total_gens = len(targets) * 2
        
        for char_idx, target in enumerate(targets):
            logger.info(f"\n=== 🎭 Character {char_idx+1}/{len(targets)}: {target['char']} ===")
            
            for i in range(2):
                iter_start = time.time()
                
                global_idx = (char_idx * 2) + i
                img_path = images[global_idx % len(images)]
                convention = conventions[(char_idx + i) % len(conventions)]
                
                res_tag = "2K" if i == 0 else "4K"
                res_label = "2k" if i == 0 else "4k"
                
                logger.info(f"   📸 [{global_idx+1}/{total_gens}] {img_path.name} -> {target['char']} @ {convention} ({res_label})")
                logger.info(f"   🔬 Analyzing (Single Call)...")
                
                # Single comprehensive analysis
                analysis = await self.analyze_all_features(img_path)
                
                # Build prompt
                base_prompt = f"Cosplay of {target['char']} from {target['anime']} at {convention}. {res_tag} resolution, convention lighting, detailed costume."
                
                # Generate (prompt only for now)
                fname = f"dave_{target['char'].replace(' ', '_')}_{res_label}_{convention.replace(' ', '_')}.png"
                save_path = self.output_dir / fname
                
                await self.generate_image(base_prompt, img_path, analysis, save_path)
                
                iter_time = time.time() - iter_start
                logger.info(f"   ⏱️  Iteration time: {iter_time:.2f}s")
        
        total_time = time.time() - start_time
        avg_time = total_time / total_gens
        
        logger.info("\n=== ✨ SPEED TEST COMPLETE ===")
        logger.info(f"   📊 Total Iterations: {total_gens}")
        logger.info(f"   ⏱️  Total Time: {total_time:.2f}s ({total_time/60:.2f} min)")
        logger.info(f"   ⚡ Average per iteration: {avg_time:.2f}s")
        logger.info(f"\n   💡 NOTE: Gemini 2.5 Flash doesn't support image generation yet.")
        logger.info(f"   💡 This test measures ANALYSIS speed only.")
        logger.info(f"   💡 For actual image generation, use Gemini 3 Pro Image Preview or Imagen.")


if __name__ == "__main__":
    gen = YukiRealGenFast()
    asyncio.run(gen.run())
