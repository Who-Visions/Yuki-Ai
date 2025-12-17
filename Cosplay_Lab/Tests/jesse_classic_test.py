"""
Jesse Classic Anime Test - 10 Male Character Transformations
Testing DNA-authentic male → male transformations with classic anime icons
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
INPUT_DIR = Path("C:/Yuki_Local/jesse 1 pic test")
OUTPUT_DIR = Path("C:/Yuki_Local/jesse_test_results")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("jesse_test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("JesseTest")

class JesseClassicTest:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("\n=== 🎭 JESSE CLASSIC ANIME TEST ===")
        
        # Initialize clients
        self.flash_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        self.pro_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
        
        logger.info("   ⚡ Gemini 2.5 Flash Online (Analysis)")
        logger.info("   🎨 Gemini 3 Pro Image Preview Online (Generation)")

    async def analyze_dna_features(self, image_path: Path) -> dict:
        """Fast comprehensive analysis using Gemini 2.5 Flash"""
        img = Image.open(image_path)
        
        prompt = """Analyze this person's facial features for authentic male anime character cosplay transformation.

Provide detailed analysis:
1. AGE: Estimated age and category
2. SKIN TONE: Exact description and undertones
3. FACE STRUCTURE: Face shape, facial proportions, masculine features
4. FEATURES: Hair color/texture, eye shape/color, nose, jawline, etc.
5. BUILD: Body type and proportions
6. ETHNICITY: Natural ethnic features to preserve

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
            
            preservation_prompt = f"""=== DNA-AUTHENTIC PRESERVATION ===

{analysis_text}

=== TRANSFORMATION RULES ===
1. PRESERVE: Exact facial structure, skin tone, age, masculine features, ethnic characteristics
2. TRANSFORM: Hair style/color, outfit, accessories to match character
3. MAINTAIN: Natural bone structure, eye shape, nose, jawline
4. OUTPUT: Photorealistic cosplay honoring authentic features"""
            
            return {
                "raw_analysis": analysis_text,
                "preservation_prompt": preservation_prompt
            }
            
        except Exception as e:
            logger.warning(f"   ⚠️ Analysis failed: {e}")
            return {
                "raw_analysis": "Analysis unavailable",
                "preservation_prompt": "PRESERVE: Natural facial features, skin tone, age, and ethnic characteristics."
            }

    @retry.Retry(predicate=retry.if_transient_error, initial=2.0, maximum=64.0, timeout=900)
    async def generate_image(self, char_name: str, anime_name: str, input_img: Image.Image, analysis: dict, save_path: Path):
        """Generate with Gemini 3 Pro Image Preview"""
        logger.info(f"      🎨 Generating {char_name}...")
        
        try:
            full_prompt = f"""Transform this person into {char_name} from {anime_name}.

{analysis['preservation_prompt']}

CHARACTER: {char_name} from {anime_name}
STYLE: Classic 1990s anime aesthetic, photorealistic cosplay
QUALITY: 4K resolution, highly detailed, accurate character design
SETTING: Convention photoshoot, professional lighting

CONTENT SAFETY: Standard cosplay, no explicit content."""
            
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
            logger.error(f"      ❌ Error: {e}")
            raise

    async def run(self):
        start_time = time.time()
        
        logger.info(f"\n=== 🎯 STARTING TEST ===")
        logger.info(f"   📂 Input: {INPUT_DIR}")
        logger.info(f"   📂 Output: {OUTPUT_DIR}")
        
        # Get Jesse's photo
        images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not images:
            logger.error("   ❌ No image found in input directory!")
            return
        
        img_path = images[0]
        logger.info(f"   📸 Input Photo: {img_path.name}")
        
        # 10 Classic Male Characters
        characters = [
            {"name": "Spike Spiegel", "anime": "Cowboy Bebop"},
            {"name": "Vash the Stampede", "anime": "Trigun"},
            {"name": "Kenshin Himura", "anime": "Rurouni Kenshin"},
            {"name": "Guts", "anime": "Berserk"},
            {"name": "Shinji Ikari", "anime": "Neon Genesis Evangelion"},
            {"name": "Goku", "anime": "Dragon Ball Z"},
            {"name": "Yusuke Urameshi", "anime": "Yu Yu Hakusho"},
            {"name": "Heero Yuy", "anime": "Gundam Wing"},
            {"name": "Takumi Fujiwara", "anime": "Initial D"},
            {"name": "Eikichi Onizuka", "anime": "Great Teacher Onizuka"}
        ]
        
        # Load image and analyze once
        logger.info(f"\n   ⚡ Analyzing Jesse's features...")
        analysis_start = time.time()
        analysis = await self.analyze_dna_features(img_path)
        analysis_time = time.time() - analysis_start
        logger.info(f"      ✅ Analysis complete ({analysis_time:.2f}s)")
        
        input_img = Image.open(img_path)
        
        # Generate transformations
        successful = 0
        for idx, char in enumerate(characters):
            iter_start = time.time()
            logger.info(f"\n   🎭 [{idx+1}/10] {char['name']} ({char['anime']})")
            
            fname = f"jesse_{char['name'].replace(' ', '_')}.png"
            save_path = self.output_dir / fname
            
            try:
                await self.generate_image(char['name'], char['anime'], input_img, analysis, save_path)
                successful += 1
            except Exception as e:
                logger.error(f"      ❌ Failed: {e}")
            
            iter_time = time.time() - iter_start
            logger.info(f"      ⏱️  Time: {iter_time:.2f}s")
        
        total_time = time.time() - start_time
        
        logger.info("\n=== ✨ TEST COMPLETE ===")
        logger.info(f"   ✅ Successful: {successful}/10")
        logger.info(f"   ⏱️  Total Time: {total_time:.2f}s ({total_time/60:.2f} min)")
        logger.info(f"   📁 Results: {OUTPUT_DIR}")

if __name__ == "__main__":
    gen = JesseClassicTest()
    asyncio.run(gen.run())
