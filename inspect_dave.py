
import sqlite3
import os

p = 'Cosplay_Lab/Brain/yuki_memory.db'
if os.path.exists(p):
    try:
        conn = sqlite3.connect(p)
        cursor = conn.cursor()
        
        # Check columns of subjects again to be sure
        cursor.execute(f"PRAGMA table_info(subjects)")
        cols = cursor.fetchall()
        col_names = [c[1] for c in cols]
        print(f"Columns: {col_names}")

        # Search for Dave
        cursor.execute("SELECT * FROM subjects WHERE name LIKE '%Dave%'")
        rows = cursor.fetchall()
        print(f"Dave rows: {rows}")
        
        # If no email column, we might need another table or just key off name for now?
    except Exception as e:
        print(f"Error: {e}")
else:
    print("File not found")
