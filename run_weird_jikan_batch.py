import asyncio
import os
from pathlib import Path
from jikan_client import JikanClient
from image_gen.v12_pipeline import V12Pipeline

# Target characters
WEIRD_CHARACTERS = [
    {"name": "Ryuk", "series": "Death Note"},
    {"name": "Orochimaru", "series": "Naruto"},
    {"name": "Hisoka Morrow", "series": "Hunter x Hunter"}
]

ELON_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Elon Musk")
OUTPUT_DIR = Path("C:/Yuki_Local/Renders_V12_Weird_Jikan")

async def fetch_and_render():
    pipeline = V12Pipeline()
    
    async with JikanClient() as jikan:
        for char_info in WEIRD_CHARACTERS:
            print(f"\n--- Processing {char_info['name']} ---")
            
            # 1. Find the anime to get the right ID
            search_results = await jikan.search_anime(char_info['series'], limit=1)
            if not search_results:
                print(f"❌ Series not found: {char_info['series']}")
                continue
            
            mal_id = search_results[0].mal_id
            print(f"✓ Found Series: {search_results[0].title} (MAL ID: {mal_id})")
            
            # 2. Get characters for this anime
            characters = await jikan.get_anime_characters(mal_id)
            
            # 3. Find our specific character
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
            print(f"✓ Image URL: {image_url}")
            
            # 4. Download reference image temporarily
            ref_path = Path(f"temp_ref_{char_info['name'].lower().replace(' ', '_')}.jpg")
            import requests
            resp = requests.get(image_url)
            with open(ref_path, "wb") as f:
                f.write(resp.content)
            
            # 5. Run V12 Pipeline
            print(f"🚀 Launching V12 Render for Elon as {target_char['name']}...")
            try:
                await pipeline.run(
                    subject_name="Elon Musk",
                    target_character=target_char['name'],
                    subject_dir=ELON_DIR,
                    reference_path=ref_path,
                    output_dir=OUTPUT_DIR
                )
            except Exception as e:
                print(f"❌ Pipeline error: {e}")
            
            # Cleanup
            if ref_path.exists():
                os.remove(ref_path)

if __name__ == "__main__":
    asyncio.run(fetch_and_render())
