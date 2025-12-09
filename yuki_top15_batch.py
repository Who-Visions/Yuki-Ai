"""
Yuki Top 15 Anime Batch Test - 4K Hybrid Generation
Timing test for 15 distinct character transformations.
"""

import asyncio
import logging
import time
from pathlib import Path
from google import genai
from google.genai import types
from google.api_core import retry
from PIL import Image

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
INPUT_DIR = Path("C:/Yuki_Local/dave test images")
OUTPUT_DIR = Path("real_gen_results_top15")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("top15_batch.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("YukiTop15")

class YukiTop15Batch:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("\n=== 🚀 YUKI TOP 15 BATCH TEST (HYBRID) ===")
        
        # Initialize clients
        self.flash_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        self.pro_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
        
        logger.info("   ⚡ Gemini 2.5 Flash Online (Analysis)")
        logger.info("   🎨 Gemini 3 Pro Image Preview Online (Generation)")

    async def analyze_dna_features(self, image_path: Path) -> dict:
        """Fast comprehensive analysis using Gemini 2.5 Flash"""
        img = Image.open(image_path)
        
        prompt = """Analyze this person's features for authentic cosplay transformation. Provide detailed analysis:

**AGE & MATURITY:**
- Estimated age range and category
- Key age markers

**SKIN TONE:**
- Exact description and Fitzpatrick scale
- Undertones and distinctive features

**FACIAL STRUCTURE:**
- Face shape and proportions
- Ethnic features and bone structure

**DETAILED FEATURES:**
- Hair, Eyes, Eyebrows, Nose, Mouth, Chin & Jaw details

**BODY COMPOSITION:**
- Build type and height proportions

**GENDER PRESENTATION:**
- Apparent gender

Respond in clear, detailed prose."""
        
        try:
            response = self.flash_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[img, prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT"],
                    temperature=0.1
                )
            )
            
            analysis_text = response.text
            
            preservation_prompt = f"""=== DNA-AUTHENTIC PRESERVATION ANALYSIS ===

{analysis_text}

=== CRITICAL PRESERVATION RULES ===
1. PRESERVE ALL: Face structure, facial proportions, ethnic features, skin tone, age appearance
2. PRESERVE BODY: Height proportions, build type, body composition
3. PRESERVE GENDER: Maintain user's gender presentation
4. TRANSFORM ONLY: Hair style/color, outfit, accessories, styling to match character
5. MAINTAIN: All natural bone structure, eye shape, nose shape, lip shape, facial geometry"""
            
            return {
                "raw_analysis": analysis_text,
                "preservation_prompt": preservation_prompt
            }
            
        except Exception as e:
            logger.warning(f"   ⚠️ Analysis failed: {e}. Using fallback.")
            return {
                "raw_analysis": "Analysis unavailable",
                "preservation_prompt": "PRESERVE: Natural facial features, skin tone, age appearance, body proportions, and gender presentation."
            }

    @retry.Retry(predicate=retry.if_transient_error, initial=2.0, maximum=64.0, timeout=900)
    async def generate_image(self, prompt: str, input_image_path: Path, analysis: dict, save_path: Path):
        """Generate with Gemini 3 Pro Image Preview"""
        logger.info(f"      🎨 Generating 4K image...")
        
        try:
            input_img = Image.open(input_image_path)
            
            full_prompt = f"""Transform this person into: {prompt}

{analysis['preservation_prompt']}

=== TRANSFORMATION RULES ===
1. PRESERVE: Face structure, facial proportions, ethnic features, skin tone, age appearance
2. TRANSFORM: Hair style/color, outfit, accessories, styling to match character
3. MAINTAIN: All natural bone structure, eye shape, nose shape, lip shape
4. OUTPUT: Photorealistic cosplay that honors the person's authentic features

=== CONTENT SAFETY GUIDELINES ===
ALLOWED: Sexy/sensual poses, revealing anime-accurate costumes.
PROHIBITED: Nudity, exposed nipples/genitalia.

QUALITY: 4K resolution, highly detailed, photorealistic masterpiece, 8k textures, cinematic lighting."""
            
            response = self.pro_client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=[input_img, full_prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    http_options=types.HttpOptions(timeout=15*60*1000)
                )
            )
            
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
                logger.info(f"      ✅ Saved: {save_path.name}")
                return True
            else:
                raise Exception("No image in response")
                
        except Exception as e:
            logger.error(f"      ❌ Generation error: {e}")
            raise

    async def run(self):
        start_time = time.time()
        
        logger.info(f"\n=== 🎯 STARTING TOP 15 BATCH ===")
        
        # Get Images
        images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not images:
            logger.warning("   ⚠️ No images found!")
            return
        
        # Top 15 Targets
        targets = [
            {"char": "Luffy", "anime": "One Piece"},
            {"char": "Gojo Satoru", "anime": "Jujutsu Kaisen"},
            {"char": "Tanjiro Kamado", "anime": "Demon Slayer"},
            {"char": "Naruto Uzumaki", "anime": "Naruto"},
            {"char": "Spike Spiegel", "anime": "Cowboy Bebop"},
            {"char": "Edward Elric", "anime": "Fullmetal Alchemist"},
            {"char": "Goku", "anime": "Dragon Ball Z"},
            {"char": "Levi Ackerman", "anime": "Attack on Titan"},
            {"char": "Saitama", "anime": "One Punch Man"},
            {"char": "Ichigo Kurosaki", "anime": "Bleach"},
            {"char": "Eren Yeager", "anime": "Attack on Titan"},
            {"char": "Gon Freecss", "anime": "Hunter x Hunter"},
            {"char": "Izuku Midoriya", "anime": "My Hero Academia"},
            {"char": "Natsu Dragneel", "anime": "Fairy Tail"},
            {"char": "Light Yagami", "anime": "Death Note"}
        ]
        
        conventions = [
            "Tokyo Comic Con", "San Diego Comic-Con", "Anime Expo", 
            "Comiket", "Dragon Con", "New York Comic Con"
        ]
        
        successful = 0
        
        for idx, target in enumerate(targets):
            iter_start = time.time()
            
            img_path = images[idx % len(images)]
            convention = conventions[idx % len(conventions)]
            
            logger.info(f"\n=== 🎭 [{idx+1}/15] {target['char']} ({target['anime']}) ===")
            logger.info(f"   📸 Input: {img_path.name}")
            
            # PHASE 1: Fast Analysis (Flash)
            logger.info(f"   ⚡ Analyzing DNA features...")
            analysis_start = time.time()
            analysis = await self.analyze_dna_features(img_path)
            analysis_time = time.time() - analysis_start
            logger.info(f"      ✅ Analysis: {analysis_time:.2f}s")
            
            # PHASE 2: Generation (3 Pro)
            base_prompt = f"Cosplay of {target['char']} from {target['anime']} at {convention}. 4K resolution, convention lighting, detailed costume."
            fname = f"top15_{idx+1:02d}_{target['char'].replace(' ', '_')}_4k.png"
            save_path = self.output_dir / fname
            
            gen_start = time.time()
            try:
                await self.generate_image(base_prompt, img_path, analysis, save_path)
                successful += 1
                gen_time = time.time() - gen_start
                logger.info(f"      ✅ Generation: {gen_time:.2f}s")
            except Exception as e:
                logger.error(f"      ❌ Failed: {e}")
                gen_time = time.time() - gen_start
            
            iter_time = time.time() - iter_start
            logger.info(f"   ⏱️  Total: {iter_time:.2f}s")
        
        total_time = time.time() - start_time
        avg_time = total_time / len(targets)
        
        logger.info("\n=== ✨ BATCH COMPLETE ===")
        logger.info(f"   📊 Total: 15 Images")
        logger.info(f"   ✅ Successful: {successful}")
        logger.info(f"   ⏱️  Total Time: {total_time:.2f}s ({total_time/60:.2f} min)")
        logger.info(f"   ⚡ Average per image: {avg_time:.2f}s ({avg_time/60:.2f} min)")

if __name__ == "__main__":
    gen = YukiTop15Batch()
    asyncio.run(gen.run())
