import sqlite3
import os

DB_PATH = r'c:\Yuki_Local\Cosplay_Lab\Brain\yuki_memory.db'

def migrate_credits():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(subjects)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'credits' not in columns:
            print("Adding 'credits' column to 'subjects' table...")
            cursor.execute("ALTER TABLE subjects ADD COLUMN credits INTEGER DEFAULT 100")
            
            # Set Dave (ID 12) to 2400 credits as requested
            cursor.execute("UPDATE subjects SET credits = 2400 WHERE id = 12")
            
            conn.commit()
            print("Credits column added and Dave updated.")
        else:
            print("'credits' column already exists.")
            # Ensure Dave has 2400 if it exists
            cursor.execute("UPDATE subjects SET credits = 2400 WHERE id = 12")
            conn.commit()
            print("Verified Dave's credits.")
            
        conn.close()

    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate_credits()
