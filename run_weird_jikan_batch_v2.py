import asyncio
import os
from pathlib import Path
from jikan_client import JikanClient
from image_gen.v12_pipeline import V12Pipeline

# Target characters with MAL IDs
WEIRD_CHARACTERS = [
    {"name": "Ryuk", "mal_id": 1535, "char_id": 10},
    {"name": "Orochimaru", "mal_id": 20, "char_id": 102},
    {"name": "Hisoka Morrow", "mal_id": 11061, "char_id": 31}
]

ELON_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Elon Musk")
OUTPUT_DIR = Path("C:/Yuki_Local/Renders_V12_Weird_Jikan")

async def fetch_and_render():
    pipeline = V12Pipeline()
    
    async with JikanClient() as jikan:
        for char_info in WEIRD_CHARACTERS:
            print(f"\n--- Processing {char_info['name']} ---")
            
            # Use direct IDs to avoid 404s on search
            try:
                # Get characters for this anime
                characters = await jikan.get_anime_characters(char_info['mal_id'])
                
                target_char = None
                for c in characters:
                    if char_info['name'].lower() in c['character']['name'].lower():
                        target_char = c['character']
                        break
                
                if not target_char:
                    print(f"❌ Character not found in series: {char_info['name']}")
                    continue
                
                image_url = target_char['images']['webp']['image_url']
                print(f"✓ Found Character: {target_char['name']}")
                
                # Download reference image temporarily
                ref_path = Path(f"temp_ref_{char_info['name'].lower().replace(' ', '_')}.jpg")
                import requests
                resp = requests.get(image_url)
                with open(ref_path, "wb") as f:
                    f.write(resp.content)
                
                # Run V12 Pipeline
                print(f"🚀 Launching V12 Render for Elon as {target_char['name']}...")
                await pipeline.run(
                    subject_name="Elon Musk",
                    target_character=target_char['name'],
                    subject_dir=ELON_DIR,
                    reference_path=ref_path,
                    output_dir=OUTPUT_DIR
                )
                
                # Cleanup
                if ref_path.exists():
                    os.remove(ref_path)
                    
            except Exception as e:
                print(f"❌ Pipeline error: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_and_render())
