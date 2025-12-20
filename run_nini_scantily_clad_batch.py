import asyncio
import os
import aiohttp
import time
from pathlib import Path
from image_gen.v12_5_pipeline import V12_5Pipeline
from tools.mal_pylib import MalClient

# NINI - SCANTILY CLAD BATCH (FAST TRACK)
# Strategy: Universal Placeholder + Minimal Clothing Prompt Injection
PLACEHOLDER_URL = "https://cdn.myanimelist.net/images/characters/15/315153.jpg"

CHARACTERS = [
    {"name": "Ryuko Matoi", "anime": "Kill la Kill", "type": "url", "url": PLACEHOLDER_URL},
    {"name": "Yoko Littner", "anime": "Gurren Lagann", "type": "url", "url": PLACEHOLDER_URL},
    {"name": "Rangiku Matsumoto", "anime": "Bleach", "type": "url", "url": PLACEHOLDER_URL},
]

SUBJECT_NAME = "Nini"
SUBJECT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Nini")
OUTPUT_DIR = Path("C:/Yuki_Local/Renders_Nini_Scantily_Clad")

CONCURRENCY_LIMIT = 1 # Serial execution to avoid 429s

async def download_image(session, url, path):
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
    # Fast Track: Always use URL (Placeholder)
    return await download_image(session, char_info["url"], ref_path)

async def process_character(pipeline, session, mal_client, char_info, bypass_lock, semaphore):
    async with semaphore:
        # Check if output already exists (Simple glob check)
        sanitized_name = char_info['name'].replace(' ', '_').lower()
        existing = list(OUTPUT_DIR.glob(f"*{sanitized_name}*.png"))
        if existing:
            print(f"⏩ Skipping {char_info['name']} (Already Exists): {existing[0].name}")
            return True

        print(f"🚀 Starting (Fast Track): {char_info['name']}...")
        try:
            ref_path = Path(f"temp_nini_scantily_{sanitized_name}.jpg")
            
            if await get_image_source(session, char_info, mal_client, ref_path):
                # SCANTILY CLAD PROMPT: Subject First + Facial Integrity + Minimal Clothing
                target = (
                    f"Model {SUBJECT_NAME} as {char_info['name']} from {char_info['anime']} (Live Action Cosplay), "
                    "(Perfect Facial Identity), (Same Face), (Hyper-Realistic), "
                    "minimal clothing, revealing outfit, skimpy, barely covered, cleavage, exposed skin, 8k"
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
                
                # PADDING DELAY FOR 429
                print("   💤 Cooling down (15s)...")
                await asyncio.sleep(15)
                
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
    
    print(f"--- Starting Nini (Scantily Clad Batch) ---")
    
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
