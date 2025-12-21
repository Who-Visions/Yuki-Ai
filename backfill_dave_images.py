import sqlite3
import os
from pathlib import Path
from datetime import datetime

DB_PATH = r'c:\Yuki_Local\Cosplay_Lab\Brain\yuki_memory.db'
RENDER_ROOT = r'c:\Yuki_Local\Cosplay_Lab\Renders'
SUBJECT_ID = 12 # Dave

def backfill():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print(f"Scanning {RENDER_ROOT} for Dave/Dav3 images...")
        
        count = 0
        
        # Walk through directories
        for root, dirs, files in os.walk(RENDER_ROOT):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    lower_name = file.lower()
                    lower_root = root.lower()
                    
                    # Logic: Check if "dave" or "dav3" is in the filename OR the parent folder path
                    if ('dave' in lower_name or 'dav3' in lower_name or 
                        'dave' in lower_root or 'dav3' in lower_root):
                        
                        # Check complete relative path for uniqueness/storage if needed
                        # But API serves flat filenames from Assets Server usually?
                        # Assets server serves everything under Renders/ so we need relative path from Renders
                        
                        abs_path = Path(root) / file
                        rel_path = abs_path.relative_to(RENDER_ROOT)
                        # On Windows rel_path might have backslashes, web needs forward slashes
                        web_path = str(rel_path).replace('\\', '/')
                        
                        timestamp = datetime.fromtimestamp(os.path.getmtime(abs_path)).strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Check if already exists (using filename matches)
                        cursor.execute("SELECT id FROM generation_log WHERE filename = ?", (web_path,))
                        if cursor.fetchone():
                            # print(f"Skipping existing: {web_path}")
                            continue
                            
                        # Insert
                        clean_prompt = f"Imported: {file}"
                        # Try to guess prompt from filename
                        parts = file.split('_')
                        if len(parts) > 2:
                             clean_prompt = f"Dave as {parts[2]}" 

                        cursor.execute("""
                            INSERT INTO generation_log (subject_id, filename, prompt, status, confidence_score, timestamp)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            SUBJECT_ID, 
                            web_path, 
                            clean_prompt, 
                            'SUCCESS_SYNCED', 
                            1.0, 
                            timestamp
                        ))
                        count += 1
                        print(f"Imported: {web_path}")

        conn.commit()
        print(f"--- Sync Complete ---")
        print(f"Imported {count} new images for Dave.")
        conn.close()

    except Exception as e:
        print(f"Backfill failed: {e}")

if __name__ == "__main__":
    backfill()
