"""
📊 YUKI AUDIT: TRUE USAGE TODAY 📊
Scans filesystem and DB to count actual generations and API calls.
"""
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path("c:/Yuki_Local")
DB_PATH = ROOT / "Cosplay_Lab/Brain/yuki_memory.db"

def get_file_count_since(directory, hours=24):
    count = 0
    now = datetime.now()
    cutoff = now - timedelta(hours=hours)
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = Path(root) / file
                if path.stat().st_ctime > cutoff.timestamp():
                    count += 1
    return count

def get_db_stats():
    if not DB_PATH.exists(): return 0
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Count chars with descriptions (research calls)
    c.execute("SELECT COUNT(*) FROM characters WHERE description IS NOT NULL")
    researched = c.fetchone()[0]
    conn.close()
    return researched

def main():
    print("📊 YUKI SYSTEM AUDIT (Last 24h)")
    print("-" * 30)
    
    # 1. IMAGE GENERATIONS
    img_count = get_file_count_since(ROOT)
    print(f"🖼️  Images Generated: {img_count}")
    
    # 2. KNOWLEDGE RESEARCH
    researched_count = get_db_stats()
    print(f"🧠 Characters Researched: {researched_count}")
    
    # 3. COST ESTIMATION
    # Pricing: ~$0.04 - $0.12 per image (Gemini 3 Preview vs Pro)
    # Pricing: ~$0.001 per text query
    
    cost_img_low = img_count * 0.04
    cost_img_high = img_count * 0.12 # Assuming full rate
    cost_text = researched_count * 0.002
    
    total_low = cost_img_low + cost_text
    total_high = cost_img_high + cost_text
    
    print("-" * 30)
    print(f"💰 EST TOTAL COST: ${total_low:.2f} - ${total_high:.2f}")

if __name__ == "__main__":
    main()
