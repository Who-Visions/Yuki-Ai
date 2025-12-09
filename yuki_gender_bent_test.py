"""
Yuki Gender Bent Test - Top 10 Anime Females
Testing Rule 63 logic: Male Subject -> Female Character Transformation
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
OUTPUT_DIR = Path("real_gen_results_gender_bent")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("gender_bent_test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("YukiGenderBent")

class YukiGenderBentTest:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("\n=== ⚧️ YUKI GENDER BENT TEST (RULE 63) ===")
        
        # Initialize clients
        self.flash_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        self.pro_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
        
        logger.info("   ⚡ Gemini 2.5 Flash Online (Analysis)")
        logger.info("   🎨 Gemini 3 Pro Image Preview Online (Generation)")

    async def analyze_dna_features(self, image_path: Path) -> dict:
        """Fast comprehensive analysis using Gemini 2.5 Flash"""
        img = Image.open(image_path)
        
        prompt = """Analyze this person's features for a GENDER-BENT cosplay transformation (Male -> Female). 
        
        Identify the core facial features that MUST be preserved to maintain identity while feminizing the presentation.

        Provide:
        1. CORE IDENTITY FEATURES (Do not change): Eye shape, nose structure, lip shape, ethnic features, skin tone.
        2. FEMINIZATION STRATEGY: How to soften jawline slightly, apply makeup, and style hair to achieve a female look while keeping the person recognizable.
        3. AGE & BUILD: Current age and build.

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
            
            preservation_prompt = f"""=== GENDER-BENT PRESERVATION STRATEGY ===

{analysis_text}

=== RULE 63 TRANSFORMATION RULES ===
1. IDENTITY: The output MUST look like the user if they were female. Do not replace the face with a generic anime girl.
2. PRESERVE: Eye shape, nose shape, lip shape, skin tone, and ethnic features.
3. TRANSFORM: Apply feminine contouring, makeup, eyelashes, and hairstyle matching the character.
4. BODY: Adapt body proportions to a female build (hips, waist, chest) matching the character's physique but respecting the user's scale.
5. COSTUME: Use the female character's authentic outfit."""
            
            return {
                "raw_analysis": analysis_text,
                "preservation_prompt": preservation_prompt
            }
            
        except Exception as e:
            logger.warning(f"   ⚠️ Analysis failed: {e}. Using fallback.")
            return {
                "raw_analysis": "Analysis unavailable",
                "preservation_prompt": "PRESERVE: Natural facial features and identity. TRANSFORM: Gender presentation to female."
            }

    @retry.Retry(predicate=retry.if_transient_error, initial=2.0, maximum=64.0, timeout=900)
    async def generate_image(self, prompt: str, input_image_path: Path, analysis: dict, save_path: Path):
        """Generate with Gemini 3 Pro Image Preview"""
        logger.info(f"      🎨 Generating Gender-Bent Image...")
        
        try:
            input_img = Image.open(input_image_path)
            
            full_prompt = f"""Transform this MALE person into a FEMALE version of: {prompt}

{analysis['preservation_prompt']}

=== TRANSFORMATION INSTRUCTIONS ===
- Apply Rule 63: Gender Swap (Male -> Female)
- Keep the person's face recognizable but feminized (makeup, softer jaw, feminine styling)
- High-quality cosplay photography style
- 4K resolution, highly detailed

=== CONTENT SAFETY ===
- Sexy/sensual is allowed (e.g., cleavage, midriff)
- NO NUDITY
- NO EXPLICIT CONTENT"""
            
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
        
        logger.info(f"\n=== ⚧️ STARTING GENDER BENT BATCH ===")
        
        # Get Images
        images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not images:
            logger.warning("   ⚠️ No images found!")
            return
        
        # Top 10 Female Targets
        targets = [
            {"char": "Sailor Moon", "anime": "Sailor Moon"},
            {"char": "Mikasa Ackerman", "anime": "Attack on Titan"},
            {"char": "Yor Forger", "anime": "Spy x Family"},
            {"char": "Makima", "anime": "Chainsaw Man"},
            {"char": "Nezuko Kamado", "anime": "Demon Slayer"},
            {"char": "Asuka Langley", "anime": "Neon Genesis Evangelion"},
            {"char": "Rem", "anime": "Re:Zero"},
            {"char": "Zero Two", "anime": "Darling in the Franxx"},
            {"char": "Motoko Kusanagi", "anime": "Ghost in the Shell"},
            {"char": "Frieren", "anime": "Frieren: Beyond Journey's End"}
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
            
            logger.info(f"\n=== 💃 [{idx+1}/10] {target['char']} ({target['anime']}) ===")
            logger.info(f"   📸 Input: {img_path.name}")
            
            # PHASE 1: Fast Analysis (Flash)
            logger.info(f"   ⚡ Analyzing for Gender Swap...")
            analysis_start = time.time()
            analysis = await self.analyze_dna_features(img_path)
            analysis_time = time.time() - analysis_start
            logger.info(f"      ✅ Analysis: {analysis_time:.2f}s")
            
            # PHASE 2: Generation (3 Pro)
            base_prompt = f"Female Cosplay of {target['char']} from {target['anime']} at {convention}. 4K resolution, detailed costume."
            fname = f"gender_bent_{idx+1:02d}_{target['char'].replace(' ', '_')}_4k.png"
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
        
        logger.info("\n=== ✨ GENDER BENT BATCH COMPLETE ===")
        logger.info(f"   📊 Total: 10 Images")
        logger.info(f"   ✅ Successful: {successful}")
        logger.info(f"   ⏱️  Total Time: {total_time:.2f}s ({total_time/60:.2f} min)")
        logger.info(f"   ⚡ Average per image: {avg_time:.2f}s ({avg_time/60:.2f} min)")

if __name__ == "__main__":
    gen = YukiGenderBentTest()
    asyncio.run(gen.run())
