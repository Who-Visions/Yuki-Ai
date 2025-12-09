"""
Yuki Real Gen - DNA-Authentic Face Transformation
Gemini 3 Pro Image Preview with Age, Skin, and Facial Feature Preservation
"""

import asyncio
import logging
import random
from pathlib import Path
from google import genai
from google.genai import types
from google.api_core import retry
from PIL import Image

# Import Yuki Modules
from filename_utils import generate_filename
from yuki_age_estimator import YukiAgeEstimator
from yuki_skin_analyzer import YukiSkinAnalyzer
from yuki_facial_analyzer import YukiFacialAnalyzer
from prompt_engineering_system import PromptEngineering

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"
INPUT_DIR = Path("C:/Yuki_Local/dave test images")
OUTPUT_DIR = Path("real_gen_results")

# Model Registry
MODELS = {
    "gemini_3_pro_image": {
        "id": "gemini-3-pro-image-preview",
        "location": "global",
        "method": "generate_content",
        "folder": "gemini_3_pro_image"
    }
}

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("real_gen.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("YukiRealGen")


class SelfCorrector:
    """Provides self-correction suggestions for common errors"""
    def analyze_error(self, context: str, error: Exception) -> str:
        error_str = str(error).lower()
        if "quota" in error_str or "rate" in error_str:
            return "Rate limit hit. Wait 60s and retry."
        elif "timeout" in error_str:
            return "Request timed out. Increase timeout or simplify prompt."
        elif "not found" in error_str or "404" in error_str:
            return "Model/resource not found. Check model ID and location."
        else:
            return f"Unknown error in {context}. Check logs."


class YukiRealGen:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("\n=== 🦊 YUKI REAL GEN INITIALIZATION ===")
        
        # Initialize Sub-Systems
        self.corrector = SelfCorrector()
        self.prompt_engine = PromptEngineering()
        
        # Initialize DNA-Authentic Analyzers
        self.age_estimator = YukiAgeEstimator(project_id=PROJECT_ID)
        self.skin_analyzer = YukiSkinAnalyzer()
        self.facial_analyzer = YukiFacialAnalyzer(project_id=PROJECT_ID)
        
        # Create subdirectories
        self.folders = {}
        for model_key, model_config in MODELS.items():
            folder_path = self.output_dir / model_config["folder"]
            folder_path.mkdir(parents=True, exist_ok=True)
            self.folders[model_key] = folder_path
            logger.info(f"   📁 Created: {model_config['folder']}/")
        
        # Initialize GenAI Clients
        self.clients = {}
        try:
            self.clients["global"] = genai.Client(
                vertexai=True,
                project=PROJECT_ID,
                location="global"
            )
            logger.info("   🎯 [System] Gemini 3 Pro Image Preview Online")
        except Exception as e:
            logger.error(f"   ❌ [System] Client Initialization Failed: {e}")
            self.clients = {}

    @retry.Retry(
        predicate=retry.if_transient_error,
        initial=2.0,
        maximum=64.0,
        multiplier=2.0,
        timeout=600
    )
    async def generate_image(self, model_key: str, prompt: str, input_image_path: Path,
                            age_info: dict, skin_info: dict, facial_info: dict, save_path: Path):
        model_config = MODELS[model_key]
        model_id = model_config["id"]
        location = model_config["location"]
        
        logger.info(f"      🎨 Generating with {model_id}...")
        
        client = self.clients.get(location)
        if not client:
            logger.warning(f"      ⚠️ Client for {location} offline. Skipping.")
            return

        try:
            input_img = Image.open(input_image_path)
            
            # Get preservation instructions
            age_instruction = self.age_estimator.get_age_appropriate_instruction(
                age_info,
                prompt.split("Cosplay of ")[1].split(" from")[0] if "Cosplay of" in prompt else "character"
            )
            skin_instruction = skin_info["preservation_prompt"]
            facial_instruction = facial_info["combined_prompt"]
            
            # Build full prompt
            full_prompt = f"""Transform this person into: {prompt}

=== DNA-AUTHENTIC TRANSFORMATION PROTOCOL ===

{age_instruction}

{skin_instruction}

{facial_instruction}

=== TRANSFORMATION RULES ===
1. PRESERVE: Face structure, facial proportions, ethnic features, skin tone, age appearance
2. TRANSFORM: Hair style/color, outfit, accessories, styling to match character
3. MAINTAIN: All natural bone structure, eye shape, nose shape, lip shape, facial geometry
4. OUTPUT: Photorealistic cosplay that honors the person's authentic features

=== CONTENT SAFETY GUIDELINES ===
ALLOWED: Sexy/sensual poses, revealing anime-accurate costumes.
PROHIBITED: Nudity, exposed nipples/genitalia.

Apply the character's aesthetic while maintaining content boundaries."""
            
            # Determine aspect ratio
            width, height = input_img.size
            ratio = width / height
            if 0.9 <= ratio <= 1.1: aspect_ratio = "1:1"
            elif ratio < 0.8: aspect_ratio = "9:16"
            elif ratio < 1.0: aspect_ratio = "3:4"
            elif ratio > 1.6: aspect_ratio = "16:9"
            else: aspect_ratio = "4:3"
            
            logger.info(f"      📐 Aspect Ratio: {aspect_ratio} (Input: {width}x{height})")
            
            # Add quality tag
            quality_prompt = f"{full_prompt}\n\nQUALITY: 4K resolution, highly detailed, photorealistic masterpiece."
            
            response = client.models.generate_content(
                model=model_id,
                contents=[input_img, quality_prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    http_options=types.HttpOptions(timeout=15*60*1000)  # 15 min timeout
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
            else:
                raise Exception("No image in response")
                
        except Exception as e:
            fix = self.corrector.analyze_error(f"Generating with {model_id}", e)
            logger.error(f"      ❌ Error: {e}")
            logger.info(f"      🧠 Self-Correction: {fix}")
            raise  # Re-raise to trigger retry

    async def run(self):
        logger.info(f"\n=== 🎯 YUKI REAL GEN: DAVE SCENARIO (GEMINI 3 PRO) ===")
        logger.info(f"   📂 Input: {INPUT_DIR}")
        logger.info(f"   📂 Output: {OUTPUT_DIR}")
        logger.info(f"   🔬 Model: gemini-3-pro-image-preview")
        logger.info(f"   ℹ️  Mode: DNA-Authentic Consistency Check")
        
        # Get Images
        images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not images:
            logger.warning("   ⚠️ No images found in input directory!")
            return
        
        # Specific Targets
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
            
            for i in range(2):  # 2 renders per character
                global_idx = (char_idx * 2) + i
                img_path = images[global_idx % len(images)]
                convention = conventions[(char_idx + i) % len(conventions)]
                
                # Quality Toggle
                res_tag = "2K resolution, highly detailed" if i == 0 else "4K resolution, ultra-detailed masterpiece, 8k textures"
                res_label = "2k" if i == 0 else "4k"
                
                logger.info(f"   📸 [{global_idx+1}/{total_gens}] {img_path.name} -> {target['char']} @ {convention} ({res_label.upper()})")
                logger.info(f"   🔬 Running DNA-Authentic Analysis...")
                
                # Run analyzers in parallel
                age_task = self.age_estimator.estimate_age(img_path)
                skin_task = self.skin_analyzer.analyze_skin_tone(img_path)
                facial_task = self.facial_analyzer.analyze_all_features(img_path)
                
                age_info, skin_info, facial_info = await asyncio.gather(
                    age_task, skin_task, facial_task
                )
                
                # Build prompt
                base_prompt = f"Cosplay of {target['char']} from {target['anime']} at {convention}. {res_tag}, convention lighting, detailed costume."
                
                # Generate
                for model_key, model_config in MODELS.items():
                    folder = self.folders[model_key]
                    model_tag = model_config["folder"]
                    
                    fname = generate_filename(
                        base_name=f"dave_{target['char'].replace(' ', '_')}_{res_label}_{convention.replace(' ', '_')}",
                        category="real_gen",
                        model_name=model_tag,
                        extension="png"
                    )
                    
                    await self.generate_image(model_key, base_prompt, img_path, age_info, skin_info, facial_info, folder / fname)
        
        logger.info("\n=== ✨ DAVE SCENARIO COMPLETE ===")
        logger.info(f"   📊 Total Transformations: {total_gens}")


if __name__ == "__main__":
    gen = YukiRealGen()
    asyncio.run(gen.run())
