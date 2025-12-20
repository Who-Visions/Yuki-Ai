import asyncio
import os
import aiohttp
import json
from pathlib import Path
from image_gen.v12_5_pipeline import V12_5Pipeline

# Winter 2025 "Loser" Anime Characters (Verified Stable URLs from MAL)
DRAKE_WAIFUS = [
    # {"name": "Kazuya Kinoshita", "anime": "Rent-a-Girlfriend", "url": "https://cdn.myanimelist.net/images/characters/9/396701.jpg"},
    # {"name": "Kazuma Satou", "anime": "Konosuba", "url": "https://cdn.myanimelist.net/images/characters/8/301302.jpg"},
    {"name": "Subaru Natsuki", "anime": "Re:Zero", "url": "https://cdn.myanimelist.net/images/characters/15/315153.jpg"},
    {"name": "Shinji Ikari", "anime": "Evangelion", "url": "https://cdn.myanimelist.net/images/characters/5/225177.jpg"},
    {"name": "Takemichi Hanagaki", "anime": "Tokyo Revengers", "url": "https://cdn.myanimelist.net/images/characters/6/448782.jpg"}
]

DRAKE_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Drake")
OUTPUT_DIR = Path("C:/Yuki_Local/Renders_Drake_V12_5")

async def download_image(session, url, path):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        async with session.get(url, headers=headers, timeout=15) as response:
            if response.status == 200:
                content = await response.read()
                path.write_bytes(content)
                return True
    except Exception as e:
        print(f"      ⚠️ Download error for {url}: {e}")
    return False

async def run_drake_batch():
    pipeline = V12_5Pipeline()
    
    images = [f for f in DRAKE_DIR.glob("*") if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.avif']]
    if not images:
        print(f"❌ No subject images found in {DRAKE_DIR}")
        return

    print(f"--- Starting Drake V12.5 'Loser Characters' Batch ---")
    
    bypass = False
    
    async with aiohttp.ClientSession() as session:
        for char_info in DRAKE_WAIFUS:
            print(f"\n🚀 Processing: {char_info['name']} ({char_info['anime']})...")
            try:
                ref_path = Path(f"temp_drake_v12_5_{char_info['name'].replace(' ', '_').lower()}.jpg")
                
                # Download
                if await download_image(session, char_info['url'], ref_path):
                    print(f"   ✓ Character reference ready.")
                    
                    # Run Pipeline with REALISM ENFORCEMENT
                    target = f"{char_info['name']} from {char_info['anime']} (Live Action Cosplay, Hyper-Realistic)"
                    
                    await pipeline.run(
                        subject_name="Drake",
                        target_character=target,
                        subject_dir=DRAKE_DIR,
                        reference_path=ref_path,
                        output_dir=OUTPUT_DIR,
                        bypass_lock=bypass
                    )
                    
                    bypass = True # Reuse structural lock
                    
                    if ref_path.exists():
                        os.remove(ref_path)
                else:
                    print(f"   ❌ Could not download image for {char_info['name']}")

            except Exception as e:
                print(f"   ❌ Batch Failure for {char_info['name']}: {e}")
            
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run_drake_batch())
