"""
Yuki Crossplay Test - "Man in the Dress" Edition
Testing costume adaptation logic: Male Subject -> Female Character Outfit (No Gender Swap)
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
OUTPUT_DIR = Path("real_gen_results_crossplay")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("crossplay_test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("YukiCrossplay")

class YukiCrossplayTest:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("\n=== 👗 YUKI CROSSPLAY TEST (MAN IN DRESS) ===")
        
        self.flash_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        self.pro_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
        
        logger.info("   ⚡ Gemini 2.5 Flash Online (Analysis)")
        logger.info("   🎨 Gemini 3 Pro Image Preview Online (Generation)")

    async def analyze_dna_features(self, image_path: Path) -> dict:
        """Fast comprehensive analysis using Gemini 2.5 Flash"""
        img = Image.open(image_path)
        prompt = "Analyze this person's facial features and body build. We need to preserve their EXACT MALE IDENTITY while putting them in a female anime costume."
        try:
            response = self.flash_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[img, prompt],
                config=types.GenerateContentConfig(response_modalities=["TEXT"])
            )
            return {"preservation_prompt": f"PRESERVE MALE IDENTITY: {response.text}"}
        except:
            return {"preservation_prompt": "PRESERVE: Male identity, facial hair, masculine build, and natural features."}

    async def generate_level(self, char: str, anime: str, level: int, input_img: Image.Image, analysis: dict, save_path: Path):
        """Generate image at specific intensity level"""
        
        levels = {
            1: "Standard Fit",
            2: "Tight/Revealing",
            3: "Extreme/Risqué"
        }
        
        level_desc = levels[level]
        logger.info(f"      🔥 Level {level}: {level_desc}...")
        
        if level == 1:
            prompt_suffix = "wearing the character's outfit tailored to a male build. Funny but high quality."
        elif level == 2:
            prompt_suffix = "wearing the character's revealing outfit. Tight fit, showing off masculine muscles in the dress."
        elif level == 3:
            prompt_suffix = "wearing the skimpy/risqué version of the outfit. Extreme contrast between masculine body and feminine lingerie/bikini armor."
        
        full_prompt = f"""Transform this MALE person into a CROSSPLAY of {char} from {anime}.

{analysis['preservation_prompt']}

=== CROSSPLAY RULES ===
1. IDENTITY: PRESERVE MALE GENDER. Do NOT feminize the face or body. Keep facial hair, masculine jawline, and build.
2. COSTUME: Put him in {char}'s exact outfit (dress, skirt, armor, etc.).
3. FIT: {prompt_suffix}
4. VIBE: Confident, owning the look. High-quality cosplay photography.

=== CONTENT SAFETY ===
NO NUDITY.
Allow cross-dressing and revealing outfits on male subject.

QUALITY: 4K resolution, masterpiece."""

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
                        logger.info(f"      ✅ PASSED: Level {level}")
                        return True
            
            logger.warning(f"      ❌ BLOCKED/FAILED: Level {level}")
            return False
            
        except Exception as e:
            logger.error(f"      ❌ ERROR: Level {level} - {e}")
            return False

    async def run(self):
        images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not images: return
        
        targets = [
            {"char": "Sailor Moon", "anime": "Sailor Moon"},
            {"char": "Mikasa Ackerman", "anime": "Attack on Titan"},
            {"char": "Yor Forger", "anime": "Spy x Family"},
            {"char": "Makima", "anime": "Chainsaw Man"},
            {"char": "Nezuko Kamado", "anime": "Demon Slayer"},
            {"char": "Asuka Langley", "anime": "Evangelion"},
            {"char": "Rem", "anime": "Re:Zero"},
            {"char": "Zero Two", "anime": "Darling in the Franxx"},
            {"char": "Motoko Kusanagi", "anime": "Ghost in the Shell"},
            {"char": "Frieren", "anime": "Frieren"}
        ]
        
        for idx, target in enumerate(targets):
            img_path = images[idx % len(images)]
            logger.info(f"\n=== 👗 [{idx+1}/10] {target['char']} ===")
            
            analysis = await self.analyze_dna_features(img_path)
            input_img = Image.open(img_path)
            
            # Ramp Up Levels
            for level in range(1, 4):
                fname = f"crossplay_{idx+1:02d}_{target['char'].replace(' ', '_')}_L{level}.png"
                save_path = self.output_dir / fname
                
                success = await self.generate_level(target['char'], target['anime'], level, input_img, analysis, save_path)
                
                if not success:
                    logger.info(f"      🛑 STOPPING RAMP: Failed at Level {level}")
                    break
                
                time.sleep(2)

if __name__ == "__main__":
    gen = YukiCrossplayTest()
    asyncio.run(gen.run())
