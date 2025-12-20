import asyncio
import os
import aiohttp
import time
from pathlib import Path
from image_gen.v12_5_pipeline import V12_5Pipeline
from tools.mal_pylib import MalClient

# PURPLE BRAND MODEL - WINTER EDITION BATCH
# PURPLE BRAND MODEL - WINTER EDITION BATCH
# USING UNIVERSAL PLACEHOLDER (Subaru) TO UNBLOCK EXECUTION
# The prompt will override the visual to "Female/Winter".
PLACEHOLDER_URL = "https://cdn.myanimelist.net/images/characters/15/315153.jpg"

CHARACTERS = [
    {"name": "Emilia", "anime": "Re:Zero", "type": "url", "url": PLACEHOLDER_URL},
    {"name": "Esdeath", "anime": "Akame ga Kill", "type": "url", "url": PLACEHOLDER_URL},
    {"name": "Frieren", "anime": "Frieren", "type": "url", "url": PLACEHOLDER_URL},
    {"name": "Holo", "anime": "Spice and Wolf", "type": "url", "url": PLACEHOLDER_URL},
    {"name": "Violet Evergarden", "anime": "Violet Evergarden", "type": "url", "url": PLACEHOLDER_URL},
]

SUBJECT_NAME = "Purple Brand Model"
SUBJECT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Purple Brand Model")
OUTPUT_DIR = Path("C:/Yuki_Local/Renders_Purple_Winter_Batch")

CONCURRENCY_LIMIT = 2 # Prevent 429

async def download_image(session, url, path):
    # Robust headers to bypass 403s on Wikia/Fandom
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.google.com/"
    }
    path = Path(path)
    if path.exists(): return True
    try:
        async with session.get(url, headers=headers, timeout=15) as response:
            if response.status == 200:
                path.write_bytes(await response.read())
                return True
            else:
                print(f"      ❌ Download Failed {response.status} for {url}")
    except Exception as e:
        print(f"      ⚠️ Download error for {url}: {e}")
    return False

async def get_image_source(session, char_info, mal_client, ref_path):
    if char_info["type"] == "mal_search":
        print(f"   🔍 Fetching image for {char_info['name']} via MalClient...")
        url = await mal_client.get_character_image(char_info["name"])
        if not url: return False
        print(f"      Found: {url}")
    else:
        url = char_info["url"]
        
    return await download_image(session, url, ref_path)

async def process_character(pipeline, session, mal_client, char_info, bypass_lock, semaphore):
    async with semaphore:
        print(f"🚀 Starting: {char_info['name']}...")
        try:
            ref_path = Path(f"temp_purple_winter_{char_info['name'].replace(' ', '_').lower()}.jpg")
            
            if await get_image_source(session, char_info, mal_client, ref_path):
                # Winter Theme Prompt Injection
                target = (
                    f"{char_info['name']} from {char_info['anime']} (Live Action Cosplay, Hyper-Realistic), "
                    "wearing winter outfit, heavy fur coat, scarf, snow background, cold breath, cinematic lighting"
                )
                
                await pipeline.run(
                    subject_name=SUBJECT_NAME,
                    target_character=target,
                    subject_dir=SUBJECT_DIR,
                    reference_path=ref_path,
                    output_dir=OUTPUT_DIR,
                    bypass_lock=bypass_lock
                )
                
                if ref_path.exists(): os.remove(ref_path)
                return True
            else:
                print(f"   ❌ Could not get image for {char_info['name']}")
        except Exception as e:
            print(f"   ❌ Failure for {char_info['name']}: {e}")
            if "429" in str(e):
                print("   ⚠️ 429 HIT! Backing off...")
                await asyncio.sleep(10)
        return False

async def run_batch():
    pipeline = V12_5Pipeline()
    mal_client = MalClient()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    print(f"--- Starting Purple Brand Model (Winter Batch) ---")
    
    # Logic: 1st job establishes lock if missing
    lock_path = OUTPUT_DIR / f"v12_5_struct_{SUBJECT_NAME.lower().replace(' ', '_')}.json"
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        pending = list(CHARACTERS)
        
        if not lock_path.exists():
            print("🔒 Generating Lock with first character...")
            first = pending.pop(0)
            await process_character(pipeline, session, mal_client, first, False, semaphore)
            
        print(f"⚡ Queueing {len(pending)} jobs...")
        for char in pending:
            tasks.append(process_character(pipeline, session, mal_client, char, True, semaphore))
            
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run_batch())
