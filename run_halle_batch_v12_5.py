import asyncio
import os
import requests
from pathlib import Path
from jikan_client import JikanClient
from image_gen.v12_5_pipeline import V12_5Pipeline

# Winter 2025 Waifus
HALLE_WAIFUS = [
    {"name": "Maomao", "mal_id": 54492},           # The Apothecary Diaries
    {"name": "Hina Chono", "mal_id": 57094},       # Blue Box
    {"name": "Alina Clover", "mal_id": 56684},     # I May Be A Guild Receptionist
    {"name": "Miyo Saimori", "mal_id": 57682},     # My Happy Marriage S2
    {"name": "Sakiko Togawa", "mal_id": 55198}      # BanG Dream! Ave Mujica
]

HALLE_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/halle berry")
OUTPUT_DIR = Path("C:/Yuki_Local/Renders_Halle_V12_5")

async def run_halle_batch():
    pipeline = V12_5Pipeline()
    
    images = sorted(list(HALLE_DIR.glob("*"))) 
    # Just filter for common image types
    images = [f for f in images if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.avif']]
    
    if not images:
        print(f"❌ No images found for Halle Berry in {HALLE_DIR}")
        return

    async with JikanClient() as jikan:
        print(f"--- Starting Halle Berry V12.5 Batch (Streamlined) ---")
        
        bypass = False
        
        for char_info in HALLE_WAIFUS:
            print(f"\n🚀 Processing Target: {char_info['name']}...")
            try:
                # Get character from Jikan
                chars = await jikan.get_anime_characters(char_info['mal_id'])
                # Stricter search for name
                target = next(c for c in chars if char_info['name'].lower() in c['character']['name'].lower())['character']
                
                image_url = target['images']['webp']['image_url']
                print(f"   ✓ Character found: {target['name']}")
                
                ref_path = Path(f"temp_halle_v12_5_{char_info['name'].split()[0].lower()}.jpg")
                ref_path.write_bytes(requests.get(image_url).content)
                
                # Run the pipeline
                await pipeline.run(
                    subject_name="Halle Berry",
                    target_character=target['name'],
                    subject_dir=HALLE_DIR,
                    reference_path=ref_path,
                    output_dir=OUTPUT_DIR,
                    bypass_lock=bypass
                )
                
                bypass = True # Reuse structural lock
                
                if ref_path.exists():
                    os.remove(ref_path)
                    
            except Exception as e:
                print(f"   ❌ Batch snag on {char_info['name']}: {e}")
            
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(run_halle_batch())
