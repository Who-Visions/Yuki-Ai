"""
🧠 YUKI BRAIN - MEMORY INITIALIZATION (SQLite) 🧠
Creates the persistent memory structures for the Cosplay Engine.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("c:/Yuki_Local/yuki_memory.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. SUBJECTS (The "Soul" of the generation)
    c.execute('''CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        v7_map_json TEXT,  -- The full V7 Neck/Jaw/Math topology
        skin_tone TEXT,
        face_shape TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_updated DATETIME
    )''')
    
    # 2. CHARACTERS (The "Role" to play)
    c.execute('''CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        source_franchise TEXT, -- DC, Marvel, Anime, etc.
        description TEXT,      -- Costume/Hair details
        anti_drift_rules TEXT, -- "Do not generate Margot Robbie"
        difficulty_tier INTEGER DEFAULT 1 -- 1=Easy, 5=Furiosa/Green Paint
    )''')
    
    # 3. GENERATION_LOG (Short Term Memory / Stream)
    c.execute('''CREATE TABLE IF NOT EXISTS generation_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        character_id INTEGER,
        prompt_used TEXT,
        output_path TEXT,
        status TEXT, -- SUCCESS, FAILED, DRIFTED
        buffer_time REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(subject_id) REFERENCES subjects(id),
        FOREIGN KEY(character_id) REFERENCES characters(id)
    )''')
    
    # 4. LEARNING_FEEDBACK (Long Term Memory / Optimization)
    c.execute('''CREATE TABLE IF NOT EXISTS learning_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        generation_id INTEGER,
        user_rating INTEGER, -- 1-5 stars
        notes TEXT,          -- "Too much anime style" or "Skin tone perfect"
        optimization_tweak TEXT, -- "Increase anti-drift weight for next time"
        FOREIGN KEY(generation_id) REFERENCES generation_log(id)
    )''')

    print(f"🧠 Yuki Memory Database initialized at: {DB_PATH}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
