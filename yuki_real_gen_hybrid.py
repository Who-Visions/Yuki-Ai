"""
Yuki Real Gen HYBRID - Production Optimized
- Gemini 2.5 Flash for fast DNA analysis (~14 sec)
- Gemini 3 Pro Image Preview for high-quality generation (~1-2 min)
- Total: ~1.5-2.5 min per image (vs 3-5 min with multi-agent)
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
OUTPUT_DIR = Path("real_gen_results_hybrid")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("real_gen_hybrid.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("YukiHybrid")


class YukiRealGenHybrid:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("\n=== 🚀 YUKI HYBRID GEN (FLASH ANALYSIS + 3 PRO GENERATION) ===")
        
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
- Estimated age range (e.g., 8-12, 25-35, 50-60)
- Age category (child/teen/young adult/adult/senior)
- Key age markers (skin texture, facial maturity, etc.)

**SKIN TONE:**
- Exact description (e.g., "warm medium brown", "cool pale ivory")
- Fitzpatrick scale (I-VI)
- Undertones (warm/cool/neutral)
- Any distinctive features (freckles, beauty marks, etc.)

**FACIAL STRUCTURE:**
- Face shape (oval/round/square/heart/diamond/oblong)
- Facial proportions (forehead, cheekbones, jawline)
- Ethnic features and characteristics
- Bone structure details

**DETAILED FEATURES:**
- Hair: Natural color, texture, thickness, style
- Eyes: Color, shape, size, spacing, eyelid type
- Eyebrows: Shape, thickness, arch
- Nose: Shape, size, bridge, tip
- Mouth: Lip fullness, shape, cupid's bow
- Chin & Jaw: Shape, prominence

**BODY COMPOSITION:**
- Build type (slim/average/athletic/muscular/plus-size)
- Height proportions (tall/average/petite)
- Shoulder width
- Overall body confidence notes

**GENDER PRESENTATION:**
- Apparent gender (male/female/androgynous)
- Key gender markers
- Confidence level

Respond in clear, detailed prose (not JSON). Be specific and descriptive."""
        
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
            
            # Build preservation prompt
            preservation_prompt = f"""=== DNA-AUTHENTIC PRESERVATION ANALYSIS ===

{analysis_text}

=== CRITICAL PRESERVATION RULES ===
1. PRESERVE ALL: Face structure, facial proportions, ethnic features, skin tone, age appearance
2. PRESERVE BODY: Height proportions, build type, body composition - DO NOT alter
3. PRESERVE GENDER: Maintain user's gender presentation (apply Rule 63 if character gender differs)
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

    @retry.Retry(predicate=retry.if_transient_error, initial=2.0, maximum=64.0, timeout=600)
    async def generate_image(self, prompt: str, input_image_path: Path, analysis: dict, save_path: Path):
        """Generate with Gemini 3 Pro Image Preview"""
        logger.info(f"      🎨 Generating with gemini-3-pro-image-preview...")
        
        try:
            input_img = Image.open(input_image_path)
            
            # Build comprehensive prompt
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

QUALITY: 4K resolution, highly detailed, photorealistic masterpiece."""
            
            response = self.pro_client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=[input_img, full_prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    http_options=types.HttpOptions(timeout=15*60*1000)
                )
            )
            
            # Extract and save image
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
        
        logger.info(f"\n=== 🎯 YUKI HYBRID: DAVE SCENARIO ===")
        logger.info(f"   📂 Input: {INPUT_DIR}")
        logger.info(f"   📂 Output: {OUTPUT_DIR}")
        logger.info(f"   ⚡ Analysis: gemini-2.5-flash")
        logger.info(f"   🎨 Generation: gemini-3-pro-image-preview")
        
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
        successful = 0
        
        for char_idx, target in enumerate(targets):
            logger.info(f"\n=== 🎭 Character {char_idx+1}/{len(targets)}: {target['char']} ===")
            
            for i in range(2):
                iter_start = time.time()
                
                global_idx = (char_idx * 2) + i
                img_path = images[global_idx % len(images)]
                convention = conventions[(char_idx + i) % len(conventions)]
                
                res_tag = "2K resolution, highly detailed" if i == 0 else "4K resolution, ultra-detailed masterpiece, 8k textures"
                res_label = "2k" if i == 0 else "4k"
                
                logger.info(f"   📸 [{global_idx+1}/{total_gens}] {img_path.name} -> {target['char']} @ {convention} ({res_label})")
                
                # PHASE 1: Fast Analysis (Flash)
                logger.info(f"   ⚡ Analyzing DNA features (Flash)...")
                analysis_start = time.time()
                analysis = await self.analyze_dna_features(img_path)
                analysis_time = time.time() - analysis_start
                logger.info(f"      ✅ Analysis complete ({analysis_time:.2f}s)")
                
                # PHASE 2: High-Quality Generation (3 Pro)
                base_prompt = f"Cosplay of {target['char']} from {target['anime']} at {convention}. {res_tag}, convention lighting, detailed costume."
                fname = f"dave_{target['char'].replace(' ', '_')}_{res_label}_{convention.replace(' ', '_')}.png"
                save_path = self.output_dir / fname
                
                gen_start = time.time()
                try:
                    await self.generate_image(base_prompt, img_path, analysis, save_path)
                    successful += 1
                    gen_time = time.time() - gen_start
                    logger.info(f"      ✅ Generation complete ({gen_time:.2f}s)")
                except Exception as e:
                    logger.error(f"      ❌ Generation failed: {e}")
                    gen_time = time.time() - gen_start
                
                iter_time = time.time() - iter_start
                logger.info(f"   ⏱️  Total iteration: {iter_time:.2f}s (Analysis: {analysis_time:.2f}s, Gen: {gen_time:.2f}s)")
        
        total_time = time.time() - start_time
        avg_time = total_time / total_gens if total_gens > 0 else 0
        
        logger.info("\n=== ✨ HYBRID GENERATION COMPLETE ===")
        logger.info(f"   📊 Total Iterations: {total_gens}")
        logger.info(f"   ✅ Successful: {successful}")
        logger.info(f"   ⏱️  Total Time: {total_time:.2f}s ({total_time/60:.2f} min)")
        logger.info(f"   ⚡ Average per image: {avg_time:.2f}s ({avg_time/60:.2f} min)")
        logger.info(f"\n   💡 Hybrid approach: ~{avg_time/60:.1f}min per image")
        logger.info(f"   💡 vs Multi-agent: ~3-5min per image")
        logger.info(f"   💡 Speed improvement: ~{(3*60)/avg_time:.1f}x faster!")


if __name__ == "__main__":
    gen = YukiRealGenHybrid()
    asyncio.run(gen.run())
