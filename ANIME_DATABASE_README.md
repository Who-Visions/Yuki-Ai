# Yuki Anime Character Database & Face Math Pipeline

A complete, intelligent system for managing anime character data, extracting facial geometry, and generating identity-preserving cosplay images.

## 🏗️ Architecture

```
Yuki_Local/
├── anime_database.py       # Smart database with indexing & search
├── anime_scraper.py        # Character scraper & training organizer  
├── character_processor.py  # Face Math extraction & batch generation
├── face_math.py           # Facial geometry extractor
├── tools.py               # Image/video generation tools
├── anime_database.json    # Persistent database storage
├── training/              # Organized character images
│   ├── Edward_Elric/
│   │   ├── ref_1.png
│   │   └── ref_2.png
│   └── training_manifest.json
├── face_schemas/          # Extracted Face Math schemas
│   └── char_id_schema.json
├── character_images/      # Downloaded reference images
└── generated_images/      # Cosplay outputs
```

## 🧠 Database Schema

### Smart Features
- **Type-Safe Dataclasses**: All entities use Python dataclasses for structure
- **Relational Links**: Anime ↔ Characters with foreign keys
- **Multi-Index Search**: Fast lookups by title, name, rank
- **Automatic ID Generation**: MD5-based unique IDs
- **Face Math Integration**: Embedded schema tracking per character

### Entities

**Anime**
```python
{
  "id": "abc123",
  "title_english": "Fullmetal Alchemist: Brotherhood",
  "rankings": {
    "myanimelist": {"rank": 1, "score": 9.1},
    "animenewsnetwork": {"rank": 21}
  },
  "character_ids": ["char_001", "char_002"]
}
```

**Character**
```python
{
  "id": "char_001",
  "name_full": "Edward Elric",
  "anime_id": "abc123",
  "face_schema": {
    "extracted": true,
    "schema_data": { "faces": [...] }
  },
  "cosplay_generations": [...]
}
```

## 🔧 Usage

### 1. Initialize Database
```python
from anime_database import AnimeDatabase

db = AnimeDatabase()  # Auto-loads anime_database.json
print(f"Loaded {len(db.anime)} anime, {len(db.characters)} characters")
```

### 2. Scrape & Add Data
```python
from anime_scraper import AnimeCharacterScraper, TrainingDataOrganizer

scraper = AnimeCharacterScraper(db)
scraper.scrape_myanimelist_top(limit=50)  # Add top 50 anime

# Add character manually
edward = {
    "name_full": "Edward Elric",
    "role": "Main",
    "image_urls": ["https://..."]
}
scraper.add_manual_character("Fullmetal Alchemist: Brotherhood", edward)
```

### 3. Organize Training Data
```python
organizer = TrainingDataOrganizer(db)
organizer.organize_all_characters()  # Creates training/Character_Name/ dirs
organizer.generate_training_manifest()  # Generates training_manifest.json
```

### 4. Extract Face Schemas
```python
from character_processor import CharacterFaceMathProcessor

processor = CharacterFaceMathProcessor(db)
processor.batch_extract_schemas(limit=10)  # Extract for 10 characters
```

### 5. Generate Cosplays
```python
# Generate cosplay of Dante using Edward's face
processor.generate_cosplay_for_character(
    character_id="char_001",
    target_character_name="Dante (Devil May Cry)",
    source_image_path="path/to/edward_reference.png",
    num_variations=2
)
```

### 6. Batch Processing
```python
# Generate multiple cosplays for multiple characters
processor.batch_generate_cosplays(
    target_characters=[
        "Dante (Devil May Cry)",
        "Cloud Strife (Final Fantasy VII)",
        "Kirito (Sword Art Online)"
    ],
    source_image_path="path/to/source.png",
    limit=5  # Process top 5 characters
)
```

## 🔍 Search & Query

```python
# Search by title
anime = db.search_anime("Fullmetal Alchemist")

# Search by character
char = db.search_character("Edward Elric")

# Get all characters for an anime
characters = db.get_characters_for_anime(anime.id)

# Get top ranked
top50 = db.get_top_anime(limit=50)
```

## 📊 Database Stats

The database automatically tracks:
- Total anime count
- Total character count
- Characters with Face Math schemas extracted
- Total cosplay generations

Access via:
```python
db.save()  # Stats printed to console
```

## 🎯 Model Hierarchy

Face extraction uses intelligent fallback:
1. **Gemini 3 Pro Preview** (Global) - Primary
2. **Gemini 2.5 Flash Image** (US-Central1) - Fallback

Image generation cascade:
1. **Gemini 3 Pro Image Preview** - Top tier
2. **Gemini 2.5 Flash Image** - Fast fallback
3. **Imagen 4 Ultra** - Quality fallback (future)
4. **Imagen 3** - Budget fallback (future)

## 🚀 Quick Start

```bash
cd c:\Yuki_Local

# Initialize database with sample data
python anime_database.py

# Scrape top anime
python anime_scraper.py

# Extract Face Math schemas
python character_processor.py
```

## 📝 Training Manifest Example

```json
{
  "generated": "2025-12-02 05:45:00",
  "total_characters": 10,
  "characters": [
    {
      "id": "char_001",
      "name": "Edward Elric",
      "anime": "Fullmetal Alchemist: Brotherhood",
      "directory": "c:/Yuki_Local/training/Edward_Elric",
      "image_count": 5,
      "images": ["ref_1.png", "ref_2.png", ...]
    }
  ]
}
```

## 🔧 Configuration

Edit these constants in the respective files:
- **Database Path**: `anime_database.py` → `db_path`
- **Image Directory**: `anime_scraper.py` → `self.image_dir`
- **Training Directory**: `anime_scraper.py` → `self.training_dir`
- **Face Schemas Directory**: `character_processor.py` → `self.schemas_dir`

## 🎨 Integration with Face Math

Every character entry links to their Face Math schema:
```python
character.face_schema.schema_data  # Full geometric data
character.face_schema.extracted   # Extraction status
character.cosplay_generations      # History of generations
```

## 📈 Future Enhancements

- [ ] Automated image downloading from Danbooru/Pixiv
- [ ] Jikan API integration for MyAnimeList data
- [ ] AniList GraphQL API integration
- [ ] Vector similarity search for character matching
- [ ] GCS-backed image storage
- [ ] REST API for database access
- [ ] Web UI for browsing & generating

---

**Built with ❄️ by Yuki (The Visionary)**
