import asyncio
import os
import aiohttp
import time
from pathlib import Path
from image_gen.v12_5_pipeline import V12_5Pipeline
from tools.mal_pylib import MalClient

# COMBINED LIST: Loser Anime + Cartoon/Comic
# Using already verified URLs for robustness as requested.
CHARACTERS = [
    # Loser Anime (Retry/Ensure)
    {"name": "Subaru Natsuki", "anime": "Re:Zero", "url": "https://cdn.myanimelist.net/images/characters/15/315153.jpg", "type": "url"},
    {"name": "Shinji Ikari", "anime": "Evangelion", "url": "https://cdn.myanimelist.net/images/characters/5/225177.jpg", "type": "url"},
    {"name": "Takemichi Hanagaki", "anime": "Tokyo Revengers", "url": "https://cdn.myanimelist.net/images/characters/6/448782.jpg", "type": "url"},
    
    # Cartoon/Comic (New)
    {"name": "Rock Lee", "anime": "Naruto", "url": "Rock Lee", "type": "mal_search"}, # Demo usage of new lib
    {"name": "Chuckie Finster", "anime": "Rugrats", "url": "https://static.wikia.nocookie.net/rugrats/images/a/ad/Chuckie_Finster.png/revision/latest?cb=20221101150149", "type": "url"},
    {"name": "Vince LaSalle", "anime": "Recess", "url": "https://static.wikia.nocookie.net/recess/images/0/0d/Vince_%283%29.jpg/revision/latest?cb=20150527113641", "type": "url"},
    {"name": "Jimmy Olsen", "anime": "Superman", "url": "https://static.wikia.nocookie.net/marvel_dc/images/c/cf/James_Olsen_New_Earth_001.jpg/revision/latest?cb=20210214101413", "type": "url"},
    {"name": "Daffy Duck", "anime": "Looney Tunes", "url": "https://static.wikia.nocookie.net/looneytunes/images/f/f9/Daffy005.png/revision/latest?cb=20130209222451", "type": "url"}
]

DRAKE_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Drake")
OUTPUT_DIR = Path("C:/Yuki_Local/Renders_Drake_Combined")

CONCURRENCY_LIMIT = 2 # Prevents 429 Resource Exhausted

async def download_image(session, url, path):
    headers = {"User-Agent": "Mozilla/5.0"}
    if path.exists(): return True
    try:
        async with session.get(url, headers=headers, timeout=15) as response:
            if response.status == 200:
                path.write_bytes(await response.read())
                return True
    except Exception as e:
        print(f"      ⚠️ Download error for {url}: {e}")
    return False

async def get_image_source(session, char_info, mal_client, ref_path):
    if char_info["type"] == "mal_search":
        url = await mal_client.get_character_image(char_info["name"])
        if not url: return False
    else:
        url = char_info["url"]
        
    return await download_image(session, url, ref_path)

async def process_character(pipeline, session, mal_client, char_info, bypass_lock, semaphore):
    async with semaphore:
        print(f"🚀 Starting: {char_info['name']}...")
        try:
            ref_path = Path(f"temp_drake_comb_{char_info['name'].replace(' ', '_').lower()}.jpg")
            
            if await get_image_source(session, char_info, mal_client, ref_path):
                target = f"{char_info['name']} from {char_info['anime']} (Live Action Cosplay, Hyper-Realistic)"
                
                await pipeline.run(
                    subject_name="Drake",
                    target_character=target,
                    subject_dir=DRAKE_DIR,
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
                await asyncio.sleep(10) # Simple backoff
        return False

async def run_batch():
    pipeline = V12_5Pipeline()
    mal_client = MalClient()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    print(f"--- Starting Drake Combined Batch (Limit: {CONCURRENCY_LIMIT}) ---")
    
    # Logic: 1st job establishes lock if missing. Then parallel.
    lock_path = OUTPUT_DIR / "v12_5_struct_drake.json"
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        pending = list(CHARACTERS)
        
        if not lock_path.exists():
            print("🔒 Generating Lock with first character...")
            first = pending.pop(0)
            # Use semaphore even for first to be safe, though not needed for concurrency
            await process_character(pipeline, session, mal_client, first, False, semaphore)
            
        print(f"⚡ Queueing {len(pending)} jobs...")
        for char in pending:
            tasks.append(process_character(pipeline, session, mal_client, char, True, semaphore))
            
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run_batch())
