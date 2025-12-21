
import sqlite3
import os

db_paths = ['anime_cache.db', 'database/yuki_knowledge.db', 'Cosplay_Lab/Brain/yuki_memory.db']

for p in db_paths:
    print(f'--- {p} ---')
    if os.path.exists(p):
        try:
            conn = sqlite3.connect(p)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
                # optionally inspect columns for relevant tables
                if 'user' in row[0].lower() or 'image' in row[0].lower():
                    cursor.execute(f"PRAGMA table_info({row[0]})")
                    cols = cursor.fetchall()
                    print(f"  Columns: {[c[1] for c in cols]}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("File not found")
