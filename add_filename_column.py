import sqlite3
import os

DB_PATH = r'c:\Yuki_Local\Cosplay_Lab\Brain\yuki_memory.db'

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(generation_log)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'filename' not in columns:
            print("Adding 'filename' column to 'generation_log' table...")
            cursor.execute("ALTER TABLE generation_log ADD COLUMN filename TEXT")
            conn.commit()
            print("Column added successfully.")
        else:
            print("'filename' column already exists.")
            
        conn.close()

    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
