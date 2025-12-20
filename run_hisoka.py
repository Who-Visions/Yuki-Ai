import asyncio
import os
import requests
from pathlib import Path
from jikan_client import JikanClient
from image_gen.v12_pipeline import V12Pipeline

async def run_hisoka():
    pipeline = V12Pipeline()
    elon_dir = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Elon Musk")
    output_dir = Path("C:/Yuki_Local/Renders_V12_Weird_Jikan")
    
    async with JikanClient() as jikan:
        print("--- Processing Hisoka ---")
        try:
            # Hunter x Hunter 2011 (MAL ID: 11061)
            characters = await jikan.get_anime_characters(11061)
            
            target_char = next(c for c in characters if "Hisoka" in c['character']['name'])['character']
            image_url = target_char['images']['webp']['image_url']
            print(f"✓ Found: {target_char['name']}")
            
            ref_path = Path("temp_hisoka.jpg")
            ref_path.write_bytes(requests.get(image_url).content)
            
            await pipeline.run(
                subject_name="Elon Musk",
                target_character=target_char['name'],
                subject_dir=elon_dir,
                reference_path=ref_path,
                output_dir=output_dir
            )
            
            if ref_path.exists():
                os.remove(ref_path)
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_hisoka())
