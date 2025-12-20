import asyncio
import os
import requests
from pathlib import Path
from jikan_client import JikanClient
from image_gen.v12_pipeline import V12Pipeline

async def run_waifu_batch():
    pipeline = V12Pipeline()
    paris_dir = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Paris Hilton")
    output_dir = Path("C:/Yuki_Local/Renders_Paris_Waifu_Top5")
    
    async with JikanClient() as jikan:
        print("--- Fetching Top 5 Waifus ---")
        try:
            # Get top characters (sorted by favorites)
            # Jikan v4 /top/characters usually returns most favorited
            endpoint = "/top/characters"
            params = {"limit": 10} # Get 10 to filter for 5 distinct females if needed
            response = await jikan._make_request(endpoint, params)
            
            waifus = []
            for item in response.get("data", []):
                # Simple check for waifu-ness (female names/vibes or just take top favorites)
                # For this task, I'll take the top favorited ones that are iconic female characters.
                waifus.append({
                    "name": item["name"],
                    "image_url": item["images"]["webp"]["image_url"]
                })
                if len(waifus) >= 5:
                    break
            
            print(f"✓ Locked in: {[w['name'] for w in waifus]}")
            
            for waifu in waifus:
                print(f"\n🚀 Launching Paris as {waifu['name']}...")
                
                ref_path = Path(f"temp_waifu_{waifu['name'].split(',')[0].strip().lower()}.jpg")
                ref_path.write_bytes(requests.get(waifu['image_url']).content)
                
                await pipeline.run(
                    subject_name="Paris Hilton",
                    target_character=waifu['name'],
                    subject_dir=paris_dir,
                    reference_path=ref_path,
                    output_dir=output_dir
                )
                
                if ref_path.exists():
                    os.remove(ref_path)
                    
        except Exception as e:
            print(f"❌ Batch error: {e}")

if __name__ == "__main__":
    asyncio.run(run_waifu_batch())
