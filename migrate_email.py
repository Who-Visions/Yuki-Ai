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

        # 1. Check if 'email' column exists in subjects
        cursor.execute("PRAGMA table_info(subjects)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'email' not in columns:
            print("Adding 'email' column to 'subjects' table...")
            cursor.execute("ALTER TABLE subjects ADD COLUMN email TEXT")
        else:
            print("'email' column already exists.")

        # 2. Update Dave (ID 12)
        email = 'whoentertains@gmail.com'
        subject_id = 12
        
        print(f"Linking Subject ID {subject_id} to {email}...")
        cursor.execute("UPDATE subjects SET email = ? WHERE id = ?", (email, subject_id))
        
        if cursor.rowcount > 0:
            print("Successfully updated Dave's record.")
        else:
            print("Warning: Subject ID 12 not found or no change needed.")

        conn.commit()
        
        # Verify
        cursor.execute("SELECT id, name, email FROM subjects WHERE id = ?", (subject_id,))
        row = cursor.fetchone()
        print(f"Verification: {row}")

        conn.close()

    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
