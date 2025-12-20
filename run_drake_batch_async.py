import asyncio
import os
import aiohttp
import time
from pathlib import Path
from image_gen.v12_5_pipeline import V12_5Pipeline

# Winter 2025 "Loser" Anime Characters (Verified Stable URLs from MAL)
DRAKE_WAIFUS = [
    {"name": "Kazuya Kinoshita", "anime": "Rent-a-Girlfriend", "url": "https://cdn.myanimelist.net/images/characters/9/396701.jpg"},
    {"name": "Kazuma Satou", "anime": "Konosuba", "url": "https://cdn.myanimelist.net/images/characters/8/301302.jpg"},
    {"name": "Subaru Natsuki", "anime": "Re:Zero", "url": "https://cdn.myanimelist.net/images/characters/15/315153.jpg"},
    {"name": "Shinji Ikari", "anime": "Evangelion", "url": "https://cdn.myanimelist.net/images/characters/5/225177.jpg"},
    {"name": "Takemichi Hanagaki", "anime": "Tokyo Revengers", "url": "https://cdn.myanimelist.net/images/characters/6/448782.jpg"}
]

DRAKE_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Drake")
OUTPUT_DIR = Path("C:/Yuki_Local/Renders_Drake_V12_5_Async") # Separate output dir for async test

async def download_image(session, url, path):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    if path.exists():
        return True # Cache hit for reference images
        
    try:
        async with session.get(url, headers=headers, timeout=15) as response:
            if response.status == 200:
                content = await response.read()
                path.write_bytes(content)
                return True
    except Exception as e:
        print(f"      ⚠️ Download error for {url}: {e}")
    return False

async def process_character(pipeline, session, char_info, bypass_lock):
    print(f"🚀 Starting: {char_info['name']}...")
    try:
        ref_path = Path(f"temp_drake_async_{char_info['name'].replace(' ', '_').lower()}.jpg")
        
        # Download
        if await download_image(session, char_info['url'], ref_path):
            # Run Pipeline with REALISM ENFORCEMENT
            target = f"{char_info['name']} from {char_info['anime']} (Live Action Cosplay, Hyper-Realistic)"
            
            await pipeline.run(
                subject_name="Drake",
                target_character=target,
                subject_dir=DRAKE_DIR,
                reference_path=ref_path,
                output_dir=OUTPUT_DIR,
                bypass_lock=bypass_lock
            )
            
            # Cleanup ref image usually happens here but in async we might want to keep it until end or delete individually
            if ref_path.exists():
                os.remove(ref_path)
            return True
        else:
            print(f"   ❌ Could not download image for {char_info['name']}")
    except Exception as e:
        print(f"   ❌ Failure for {char_info['name']}: {e}")
    return False

async def run_drake_batch_async():
    start_time = time.time()
    pipeline = V12_5Pipeline()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    images = [f for f in DRAKE_DIR.glob("*") if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.avif']]
    if not images:
        print(f"❌ No subject images found in {DRAKE_DIR}")
        return

    print(f"--- Starting Drake V12.5 ASYNC Batch ---")
    
    # Check if we need to establish the lock first
    # In V12.5 pipeline, the lock path is determined by output_dir and subject_name
    # lock_path = output_dir / f"v12_5_struct_{safe_name}.json"
    lock_path = OUTPUT_DIR / "v12_5_struct_drake.json"
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        # Strategy: If lock doesn't exist, we MUST run one linearly first to create it.
        # Otherwise, 5 parallel calls trigger 5 Flash 68-point expansions (= waste money + time).
        
        pending_waifus = list(DRAKE_WAIFUS)
        
        if not lock_path.exists():
            print("🔒 Generating Structural Lock (First job)...")
            first_waifu = pending_waifus.pop(0)
            await process_character(pipeline, session, first_waifu, bypass_lock=False)
        else:
            print("🔒 Structural Lock found. Going full parallel.")

        # Prepare remaining tasks
        if pending_waifus:
            print(f"⚡ Launching {len(pending_waifus)} jobs in PARALLEL...")
            for char_info in pending_waifus:
                tasks.append(process_character(pipeline, session, char_info, bypass_lock=True))
            
            await asyncio.gather(*tasks)

    duration = time.time() - start_time
    print(f"\n✅ Async Batch Complete in {duration:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(run_drake_batch_async())
