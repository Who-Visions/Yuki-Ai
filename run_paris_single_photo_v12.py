import asyncio
import os
import requests
from pathlib import Path
from jikan_client import JikanClient
from image_gen.v12_pipeline import V12Pipeline

# Paris Waifu Top 5
PARIS_WAIFUS = [
    {"name": "Makima", "mal_id": 44511},
    {"name": "Boa Hancock", "mal_id": 21},
    {"name": "Marin Kitagawa", "mal_id": 48736},
    {"name": "Zero Two", "mal_id": 35849},
    {"name": "Yor Forger", "mal_id": 40221}
]

# TARGET: The pruned original folder
PARIS_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Paris Hilton")
OUTPUT_DIR = Path("C:/Yuki_Local/Renders_Paris_Single_V12")

async def run_paris_single_photo_batch():
    pipeline = V12Pipeline()
    
    # We know there is only 1 photo because we just isolated it
    images = sorted(list(PARIS_DIR.glob("*.jpg")))
    if not images:
        print("❌ No images found in isolated folder")
        return

    async with JikanClient() as jikan:
        print(f"--- Starting Paris Hilton SINGLE-PHOTO Batch ---")
        print(f"Source Image: {images[0].name}")
        
        # Track if we have already built the lock for this character run
        # bypass_lock will skip Stage 1-3
        bypass = False 
        
        for char_info in PARIS_WAIFUS:
            print(f"\n🚀 Processing Target: {char_info['name']}...")
            try:
                # Get character from Jikan
                chars = await jikan.get_anime_characters(char_info['mal_id'])
                target = next(c for c in chars if char_info['name'].split()[0].lower() in c['character']['name'].lower())['character']
                
                image_url = target['images']['webp']['image_url']
                print(f"   ✓ Character found: {target['name']}")
                
                ref_path = Path(f"temp_paris_single_{char_info['name'].split()[0].lower()}.jpg")
                ref_path.write_bytes(requests.get(image_url).content)
                
                # Run the pipeline
                await pipeline.run(
                    subject_name="Paris Hilton",
                    target_character=target['name'],
                    subject_dir=PARIS_DIR,
                    reference_path=ref_path,
                    output_dir=OUTPUT_DIR,
                    bypass_lock=bypass # First one will build the lock, subsequent ones reuse it
                )
                
                # Once the first lock is built, bypass for the rest
                bypass = True
                
                if ref_path.exists():
                    os.remove(ref_path)
                    
            except Exception as e:
                print(f"   ❌ Batch snag on {char_info['name']}: {e}")
            
            # Respect Jikan rate limits
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(run_paris_single_photo_batch())
