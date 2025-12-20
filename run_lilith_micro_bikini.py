import asyncio
import os
import aiohttp
from pathlib import Path
from image_gen.v12_5_pipeline import V12_5Pipeline

# LILITH - MICRO BIKINI SINGLE GENERATION
PLACEHOLDER_URL = "https://cdn.myanimelist.net/images/characters/15/315153.jpg"

SUBJECT_NAME = "Lilith"
SUBJECT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Lilith")
OUTPUT_DIR = Path("C:/Yuki_Local/Renders_Lilith_Micro_Bikini")

async def download_image(session, url, path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.google.com/"
    }
    path = Path(path)
    if path.exists(): return True
    try:
        async with session.get(url, headers=headers, timeout=15) as response:
            if response.status == 200:
                path.write_bytes(await response.read())
                return True
    except Exception as e:
        print(f"⚠️ Download error: {e}")
    return False

async def run_single_generation():
    pipeline = V12_5Pipeline()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"--- Starting Lilith (Micro Bikini) ---")
    
    ref_path = Path("temp_lilith_micro_bikini.jpg")
    
    async with aiohttp.ClientSession() as session:
        print("📥 Downloading reference...")
        if await download_image(session, PLACEHOLDER_URL, ref_path):
            # MICRO BIKINI PROMPT
            target = (
                f"Model {SUBJECT_NAME} as anime character, "
                "(Perfect Facial Identity), (Same Face), (Hyper-Realistic), "
                "micro bikini, string bikini, minimal coverage, tiny swimsuit, beach, 8k"
            )
            
            print(f"🎨 Generating...")
            
            await pipeline.run(
                subject_name=SUBJECT_NAME,
                target_character=target,
                subject_dir=SUBJECT_DIR,
                reference_path=ref_path,
                output_dir=OUTPUT_DIR,
                bypass_lock=False
            )
            
            if ref_path.exists(): 
                os.remove(ref_path)
            
            print("✅ Generation Complete!")
        else:
            print("❌ Failed to download reference image")

if __name__ == "__main__":
    asyncio.run(run_single_generation())
