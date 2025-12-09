"""
Database-First Generation System
Uses local anime DB for character data, only calls API for image generation
"""

import sys
sys.path.append('C:/Yuki_Local')

import asyncio
import logging
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
from anime_characters_data import ANIME_CHARACTER_DATA
from facial_geometry_corrector import FacialGeometryCorrector

PROJECT_ID = "gifted-cooler-479623-r7"

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("DBFirstGen")

class DatabaseFirstGenerator:
    """
    Smart generation that uses local DB first, API only when necessary
    """
    
    def __init__(self):
        self.geo_corrector = FacialGeometryCorrector(PROJECT_ID)
        self.pro_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
        
        # Load character DB into memory (instant, no API)
        self.characters_db = ANIME_CHARACTER_DATA
        logger.info(f"✅ Loaded {len(self.characters_db)} anime from local DB (0 API calls)")
    
    def get_characters_by_year(self, year: int, limit: int = 10, gender: str = "male"):
        """Get top characters from a specific year - LOCAL DB ONLY"""
        year_anime = [a for a in self.characters_db if a.get('year') == year]
        sorted_anime = sorted(year_anime, key=lambda x: x.get('rank', 999))[:limit * 3]  # Get more to filter
        
        characters = []
        
        # Gender keywords for filtering (basic heuristic)
        female_keywords = ['Sakura', 'Rei', 'Asuka', 'Mikasa', 'Nezuko', 'Shizuku', 'Female', 'Girl', 
                          'Megumin', 'Aqua', 'Darkness', 'Emilia', 'Rem', 'Ram', 'Yor', 'Makima', 
                          'Power', 'Lucy', 'Nami', 'Robin', 'Bulma', 'Android 18', 'Hinata', 'Sakura']
        
        for anime in sorted_anime:
            for char in anime.get('characters', []):
                # Skip if we hit the limit
                if len(characters) >= limit:
                    break
                
                # Gender filter (heuristic - check if name matches known female patterns)
                is_likely_female = any(keyword in char for keyword in female_keywords)
                
                if gender == "male" and not is_likely_female:
                    characters.append({
                        'name': char,
                        'anime': anime['title'],
                        'year': anime['year']
                    })
                elif gender == "female" and is_likely_female:
                    characters.append({
                        'name': char,
                        'anime': anime['title'],
                        'year': anime['year']
                    })
            
            if len(characters) >= limit:
                break
        
        logger.info(f"📊 Found {len(characters)} {gender} characters from {year} in local DB")
        return characters
    
    async def generate_batch(self, input_path: Path, output_dir: Path, year: int, limit: int = 5):
        """
        Generate batch using DB-first approach
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"\n=== 🎯 DB-FIRST GENERATION (Year: {year}) ===")
        logger.info(f"   📂 Input: {input_path}")
        logger.info(f"   📂 Output: {output_dir}")
        
        # Step 1: Get characters from DB (LOCAL - no API call)
        characters = self.get_characters_by_year(year, limit)
        
        if not characters:
            logger.error(f"   ❌ No characters found for year {year} in DB")
            return
        
        logger.info(f"\n   Characters to generate:")
        for idx, char in enumerate(characters):
            logger.info(f"      {idx+1}. {char['name']} ({char['anime']})")
        
        # Step 2: Analyze image once (1 API call)
        logger.info(f"\n   🔬 Analyzing perspective (1 API call)...")
        corrected = await self.geo_corrector.get_corrected_analysis(input_path)
        logger.info(f"      ✅ Analysis complete")
        
        input_img = Image.open(input_path)
        
        # Step 3: Generate images (N API calls)
        successful = 0
        for idx, char in enumerate(characters):
            logger.info(f"\n   🎭 [{idx+1}/{len(characters)}] {char['name']}")
            
            try:
                fname = f"{char['name'].replace(' ', '_')}.png"
                await self._generate_single(char, input_img, corrected, output_dir / fname)
                successful += 1
            except Exception as e:
                logger.error(f"      ❌ Failed: {e}")
        
        logger.info(f"\n=== ✨ COMPLETE ===")
        logger.info(f"   ✅ Success: {successful}/{len(characters)}")
        logger.info(f"   📊 Total API calls: {1 + successful} (1 analysis + {successful} generations)")
    
    async def _generate_single(self, char_data: dict, input_img: Image.Image, corrected_analysis: dict, save_path: Path):
        """Generate single image"""
        prompt = f"""Transform this person into {char_data['name']} from {char_data['anime']}.

{corrected_analysis['generation_prompt']}

CHARACTER: {char_data['name']}
ANIME: {char_data['anime']} ({char_data['year']})
QUALITY: 4K, photorealistic cosplay
FORMAT: Vertical portrait for mobile viewing (9:16 aspect ratio)
COMPOSITION: Full body or 3/4 length shot optimized for phone screens"""
        
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
                logger.info(f"      ✅ VERIFIED SAVED: {save_path.name} ({size_kb:.1f} KB)")
            else:
                raise Exception(f"File write failed - {save_path} does not exist!")
        else:
            raise Exception("No image data in API response!")


# Example usage
async def test_nadley_2012():
    gen = DatabaseFirstGenerator()
    
    input_path = Path("C:/Yuki_Local/friends test/Nadley")
    images = list(input_path.glob("*.jpg")) + list(input_path.glob("*.png"))
    
    if images:
        await gen.generate_batch(
            input_path=images[0],
            output_dir=Path("C:/Yuki_Local/nadley_db_results"),
            year=2012,
            limit=5  # Start small to test quota
        )

if __name__ == "__main__":
    asyncio.run(test_nadley_2012())
