"""
🧠 YUKI BRAIN - KNOWLEDGE MIGRATION 🧠
Ingests Python character banks and JSON facial IPs into SQLite
"""
import sqlite3
import json
import importlib.util
from pathlib import Path
from rich.console import Console

console = Console()
DB_PATH = Path("c:/Yuki_Local/yuki_memory.db")

# Load Python Modules dynamically
def load_bank(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def migrate():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. MIGRATE SUBJECTS (JSON IPs)
    subjects = ["Jordan", "Snow", "Dav3", "Nadly", "Jesse"]
    console.print("[bold cyan]🔄 Migrating Subjects...[/bold cyan]")
    
    for sub in subjects:
        json_path = Path(f"c:/Yuki_Local/{sub.lower()}_v7_ip.json")
        if json_path.exists():
            with open(json_path) as f: ip_data = json.load(f)
            
            # Extract core markers
            skin = ip_data.get("zone_16_skin_surface", {}).get("tone", "unknown")
            shape = ip_data.get("face_calibration", {}).get("overall_shape", "unknown")
            dump = json.dumps(ip_data)
            
            try:
                c.execute("INSERT OR REPLACE INTO subjects (name, v7_map_json, skin_tone, face_shape, last_updated) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                          (sub, dump, skin, shape))
                console.print(f"   ✅ Indexed: {sub}")
            except Exception as e:
                console.print(f"   ❌ Error {sub}: {e}")
        else:
            console.print(f"   ⚠️ No V7 IP found for {sub} (Run Yuki Brain to generate)")

    # 2. MIGRATE CHARACTERS (Python Banks)
    console.print("\n[bold cyan]🔄 Migrating Character Banks...[/bold cyan]")
    
    banks = {
        "DC": "c:/Yuki_Local/dc_character_bank.py",
        "Anime": "c:/Yuki_Local/anime_character_bank.py",
        "Movies": "c:/Yuki_Local/movie_characters_bank.py",
        "Males": "c:/Yuki_Local/male_character_bank_1k.py"
    }
    
    total_chars = 0
    for franchise, path in banks.items():
        try:
            mod = load_bank(franchise, path)
            # Find the list variable (usually uppercase)
            char_list = []
            for name in dir(mod):
                if name.endswith("_BANK"):
                    char_list = getattr(mod, name)
                    break
            
            for char_name in char_list:
                c.execute("INSERT OR IGNORE INTO characters (name, source_franchise) VALUES (?, ?)", 
                          (char_name, franchise))
            
            count = len(char_list)
            total_chars += count
            console.print(f"   ✅ Indexed {count} from {franchise}")
            
        except Exception as e:
            console.print(f"   ❌ Failed to load {franchise}: {e}")

    console.print(f"\n[bold green]✨ Knowledge Migration Complete![/bold green]")
    console.print(f"   🧠 Total Knowledge Base: {total_chars} Characters")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
