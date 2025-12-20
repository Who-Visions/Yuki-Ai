"""
Yuki Knowledge Graph Schema
Defines the database structure for Anime, Characters, and detailed visual breakdowns.
Designed for SQLAlchemy (supports SQLite/PostgreSQL).
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Text, JSON, Boolean, Float, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum
from datetime import datetime

Base = declarative_base()

# --- Association Tables ---
# Many-to-Many relationship between Series and Genres
series_genres = Table('series_genres', Base.metadata,
    Column('series_id', Integer, ForeignKey('series.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

# Many-to-Many for Character Tags (Archetypes, etc.)
character_tags = Table('character_tags', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class GenderEnum(enum.Enum):
    FEMALE = "Female"
    MALE = "Male"
    NON_BINARY = "Non-binary"
    OTHER = "Other"
    UNKNOWN = "Unknown"

class RoleEnum(enum.Enum):
    MAIN = "Main"
    SUPPORTING = "Supporting"
    BACKGROUND = "Background"

# --- Core Models ---

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    category = Column(String(50)) # e.g., "Personality", "Physical", "Meta"

class Series(Base):
    __tablename__ = 'series'
    
    id = Column(Integer, primary_key=True)
    
    # Metadata
    title_romaji = Column(String(255), nullable=False)
    title_english = Column(String(255))
    title_native = Column(String(255))
    description = Column(Text)
    format = Column(String(20)) # TV, MOVIE, OVA
    status = Column(String(20))
    season = Column(String(20)) # WINTER 2024
    release_date = Column(String(20))
    
    # External IDs (The "Rosetta Stone")
    anilist_id = Column(Integer, unique=True)
    mal_id = Column(Integer, unique=True)
    anidb_id = Column(Integer, unique=True)
    kitsu_id = Column(Integer)
    
    # Relationships
    genres = relationship('Genre', secondary=series_genres, backref='series')
    characters = relationship('Character', back_populates='series')
    
    created_at = Column(Integer, default=func.now()) # Unix timestamp

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey('series.id'))
    
    # Basic Info
    name_romaji = Column(String(255), nullable=False)
    name_native = Column(String(255))
    alternative_names = Column(JSON) # List of nicknames
    
    gender = Column(Enum(GenderEnum), default=GenderEnum.UNKNOWN)
    age = Column(String(50)) # String because "16" or "1000+"
    height = Column(String(50))
    weight = Column(String(50))
    blood_type = Column(String(5))
    
    description = Column(Text)
    role = Column(Enum(RoleEnum), default=RoleEnum.MAIN)
    
    # GenAI Specifics
    base_prompt = Column(Text) # Core prompt describing the character generally
    
    # External IDs
    anilist_id = Column(Integer, unique=True)
    mal_id = Column(Integer)
    
    # Relationships
    series = relationship('Series', back_populates='characters')
    variants = relationship('AppearanceVariant', back_populates='character')
    tags = relationship('Tag', secondary=character_tags, backref='characters')

class AppearanceVariant(Base):
    """
    Represents a specific "look" or "form" of a character.
    e.g., "School Uniform", "Magical Girl Form", "Casual Winter".
    This is CRITICAL for accurate image generation.
    """
    __tablename__ = 'appearance_variants'
    
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    
    name = Column(String(100), nullable=False) # e.g., "Default", "Swimsuit"
    is_default = Column(Boolean, default=False)
    
    # Visual Breakdown
    hair_style = Column(String(100)) # e.g., "Twin-tails", "Long straight"
    hair_color = Column(String(50)) # e.g., "Silver", "#C0C0C0"
    eye_color = Column(String(50))
    skin_tone = Column(String(50))
    
    # Detailed JSON descriptors for flexibility
    # Structure: {"head": ["ribbon", "hat"], "upper": ["white shirt", "red tie"], ...}
    outfit_structure = Column(JSON) 
    
    # GenAI Prompting
    prompt_tags = Column(Text) # Comma-separated tags specific to this outfit
    negative_prompt = Column(Text)
    
    # Color Palette (Extracted from reference images)
    # Structure: {"primary": "#HEX", "secondary": "#HEX", "accent": "#HEX"}
    color_palette = Column(JSON)
    
    character = relationship('Character', back_populates='variants')

# --- Database Initialization ---

def init_db(db_path="sqlite:///c:/Yuki_Local/database/yuki_knowledge.db"):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    print("Initializing Yuki Knowledge Database...")
    engine = init_db()
    print(f"Database created at {engine.url}")
