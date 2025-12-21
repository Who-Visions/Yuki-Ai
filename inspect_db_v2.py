
import sqlite3
import os

p = 'Cosplay_Lab/Brain/yuki_memory.db'
print(f'--- {p} ---')
if os.path.exists(p):
    try:
        conn = sqlite3.connect(p)
        cursor = conn.cursor()
        tables = ['subjects', 'generation_log']
        for t in tables:
            print(f"Table: {t}")
            cursor.execute(f"PRAGMA table_info({t})")
            cols = cursor.fetchall()
            for c in cols:
                print(c)
            
            # Check for data
            cursor.execute(f"SELECT * FROM {t} LIMIT 5")
            rows = cursor.fetchall()
            print("  Data samples:")
            for r in rows:
                print(r)

    except Exception as e:
        print(f"Error: {e}")
else:
    print("File not found")
