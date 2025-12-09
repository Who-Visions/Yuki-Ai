"""
Yuki Cloud Brain - Complete GCP Backend
BigQuery for prompts + analytics
Cloud SQL for anime database
GCS for images/assets
Cloud-first, local-cache pattern
"""

from google.cloud import bigquery, storage
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
from typing import List, Dict, Optional, Any
import json
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ID = "gifted-cooler-479623-r7"
REGION = "us-central1"

# BigQuery (for prompts + analytics)
BQ_DATASET_PROMPTS = "yuki_prompts"
BQ_TABLE_PROMPTS = "portrait_prompts"
BQ_TABLE_USAGE_ANALYTICS = "prompt_usage_analytics"
BQ_TABLE_GENERATION_LOG = "generation_log"

# Cloud SQL (for anime database)
CLOUD_SQL_INSTANCE = f"{PROJECT_ID}:{REGION}:yuki-anime-db"
CLOUD_SQL_DATABASE = "yuki_anime"
CLOUD_SQL_USER = "yuki"

# GCS (for images/assets)
GCS_BUCKET_IMAGES = "yuki-anime-images"
GCS_BUCKET_GENERATIONS = "yuki-cosplay-generations"
GCS_BUCKET_BACKUPS = "yuki-database-backups"

# =============================================================================
# CLOUD SQL MODELS (Relational Database)
# =============================================================================

Base = declarative_base()

class AnimeModel(Base):
    """Anime table in Cloud SQL"""
    __tablename__ = 'anime'
    
    id = Column(String(12), primary_key=True)
    title_english = Column(String(500), nullable=False, index=True)
    title_romaji = Column(String(500))
    title_native = Column(String(500))
    year = Column(Integer)
    type = Column(String(50))
    episodes = Column(Integer)
    status = Column(String(50))
    genres = Column(JSON)
    studio = Column(String(200))
    mal_rank = Column(Integer)
    mal_score = Column(Float)
    poster_url = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    characters = relationship("CharacterModel", back_populates="anime")

class CharacterModel(Base):
    """Character table in Cloud SQL"""
    __tablename__ = 'characters'
    
    id = Column(String(12), primary_key=True)
    anime_id = Column(String(12), ForeignKey('anime.id'), nullable=False, index=True)
    name_full = Column(String(300), nullable=False, index=True)
    name_given = Column(String(150))
    name_family = Column(String(150))
    aliases = Column(JSON)
    role = Column(String(50))
    gender = Column(String(20))
    age = Column(Integer)
    hair_color = Column(String(50))
    eye_color = Column(String(50))
    popularity_rank = Column(Integer)
    
    # Face Math Schema
    face_schema_extracted = Column(Boolean, default=False)
    face_schema_data = Column(JSON)
    face_schema_model = Column(String(100))
    face_schema_date = Column(DateTime)
    
    # Reference images (GCS paths)
    reference_images = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    anime = relationship("AnimeModel", back_populates="characters")
    generations = relationship("GenerationModel", back_populates="character")

class GenerationModel(Base):
    """Cosplay generation records in Cloud SQL"""
    __tablename__ = 'generations'
    
    id = Column(String(12), primary_key=True)
    character_id = Column(String(12), ForeignKey('characters.id'), nullable=False, index=True)
    prompt_id = Column(String(12), index=True)
    target_character = Column(String(300))
    model_used = Column(String(100))
    prompt_text = Column(Text)
    source_image_gcs = Column(Text)
    output_image_gcs = Column(Text)
    output_local_path = Column(Text)
    resolution = Column(String(20))
    aspect_ratio = Column(String(10))
    generation_time_seconds = Column(Float)
    quality_score = Column(Float)
    user_rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    
    # Relationships
    character = relationship("CharacterModel", back_populates="generations")

# =============================================================================
# YUKI CLOUD BRAIN
# =============================================================================

class YukiCloudBrain:
    """
    Complete cloud-native brain for Yuki
    
    Architecture:
    - Cloud SQL: Anime/Character database (relational, ACID)
    - BigQuery: Prompts, analytics, generation logs (analytics)
    - GCS: Images, assets, backups (storage)
    
    Pattern: Cloud-first, local-cache
    """
    
    def __init__(self):
        print("\n🧠 Initializing Yuki Cloud Brain...")
        
        # BigQuery Client
        self.bq_client = bigquery.Client(project=PROJECT_ID)
        self.bq_dataset_ref = f"{PROJECT_ID}.{BQ_DATASET_PROMPTS}"
        
        # GCS Client
        self.gcs_client = storage.Client(project=PROJECT_ID)
        
        # Cloud SQL Connection
        self.sql_engine = None
        self.sql_session = None
        self._init_cloud_sql()
        
        # Ensure all resources exist
        self._ensure_bigquery_resources()
        self._ensure_gcs_buckets()
        self._ensure_sql_tables()
        
        print("✅ Cloud Brain initialized!\n")
    
    def _init_cloud_sql(self):
        """Initialize Cloud SQL connection"""
        try:
            connector = Connector()
            
            def getconn():
                conn = connector.connect(
                    CLOUD_SQL_INSTANCE,
                    "pymysql",
                    user=CLOUD_SQL_USER,
                    db=CLOUD_SQL_DATABASE,
                    password=os.getenv("CLOUD_SQL_PASSWORD", "yuki-secure-pass")
                )
                return conn
            
            self.sql_engine = create_engine(
                "mysql+pymysql://",
                creator=getconn,
            )
            
            Session = sessionmaker(bind=self.sql_engine)
            self.sql_session = Session()
            
            print("✓ Cloud SQL connected")
        except Exception as e:
            print(f"⚠️  Cloud SQL connection failed: {e}")
            print("   Running in BigQuery-only mode")
    
    def _ensure_bigquery_resources(self):
        """Ensure BigQuery datasets and tables exist"""
        # Create dataset
        try:
            self.bq_client.get_dataset(self.bq_dataset_ref)
        except:
            dataset = bigquery.Dataset(self.bq_dataset_ref)
            dataset.location = "US"
            self.bq_client.create_dataset(dataset)
            print("✓ Created BigQuery dataset")
        
        # Create prompt table
        self._create_prompt_table()
        
        # Create analytics tables
        self._create_analytics_tables()
    
    def _create_prompt_table(self):
        """Create prompt table in BigQuery"""
        table_ref = f"{self.bq_dataset_ref}.{BQ_TABLE_PROMPTS}"
        
        schema = [
            bigquery.SchemaField("prompt_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("prompt_text", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("style_tags", "STRING", mode="REPEATED"),
            bigquery.SchemaField("use_case", "STRING", mode="REPEATED"),
            bigquery.SchemaField("model_recommended", "STRING"),
            bigquery.SchemaField("resolution", "STRING"),
            bigquery.SchemaField("aspect_ratio", "STRING"),
            bigquery.SchemaField("gender_target", "STRING"),
            bigquery.SchemaField("setting", "STRING"),
            bigquery.SchemaField("lighting", "STRING"),
            bigquery.SchemaField("mood", "STRING"),
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("usage_count", "INTEGER"),
            bigquery.SchemaField("avg_rating", "FLOAT"),
            bigquery.SchemaField("source", "STRING"),
        ]
        
        try:
            self.bq_client.get_table(table_ref)
        except:
            table = bigquery.Table(table_ref, schema=schema)
            self.bq_client.create_table(table)
            print("✓ Created prompt table")
    
    def _create_analytics_tables(self):
        """Create analytics tables in BigQuery"""
        # Generation log table
        log_table_ref = f"{self.bq_dataset_ref}.{BQ_TABLE_GENERATION_LOG}"
        log_schema = [
            bigquery.SchemaField("generation_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("character_id", "STRING"),
            bigquery.SchemaField("prompt_id", "STRING"),
            bigquery.SchemaField("model_used", "STRING"),
            bigquery.SchemaField("resolution", "STRING"),
            bigquery.SchemaField("generation_time_seconds", "FLOAT"),
            bigquery.SchemaField("success", "BOOLEAN"),
            bigquery.SchemaField("error_message", "STRING"),
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        ]
        
        try:
            self.bq_client.get_table(log_table_ref)
        except:
            table = bigquery.Table(log_table_ref, log_schema=log_schema)
            self.bq_client.create_table(table)
            print("✓ Created generation log table")
    
    def _ensure_gcs_buckets(self):
        """Ensure GCS buckets exist"""
        for bucket_name in [GCS_BUCKET_IMAGES, GCS_BUCKET_GENERATIONS, GCS_BUCKET_BACKUPS]:
            try:
                self.gcs_client.get_bucket(bucket_name)
            except:
                bucket = self.gcs_client.create_bucket(bucket_name, location=REGION)
                print(f"✓ Created GCS bucket: {bucket_name}")
    
    def _ensure_sql_tables(self):
        """Ensure Cloud SQL tables exist"""
        if self.sql_engine:
            Base.metadata.create_all(self.sql_engine)
            print("✓ Cloud SQL tables ready")
    
    # =========================================================================
    # ANIME DATABASE OPERATIONS (Cloud SQL)
    # =========================================================================
    
    def add_anime(self, anime_data: Dict) -> str:
        """Add anime to Cloud SQL"""
        if not self.sql_session:
            print("❌ Cloud SQL not available")
            return ""
        
        try:
            import hashlib
            anime_id = hashlib.md5(anime_data['title_english'].encode()).hexdigest()[:12]
            
            anime = AnimeModel(
                id=anime_id,
                **anime_data
            )
            
            self.sql_session.add(anime)
            self.sql_session.commit()
            
            print(f"✓ Added anime: {anime_data['title_english']}")
            return anime_id
        except Exception as e:
            self.sql_session.rollback()
            print(f"❌ Error adding anime: {e}")
            return ""
    
    def add_character(self, character_data: Dict) -> str:
        """Add character to Cloud SQL"""
        if not self.sql_session:
            print("❌ Cloud SQL not available")
            return ""
        
        try:
            import hashlib
            char_id = hashlib.md5(
                f"{character_data['anime_id']}_{character_data['name_full']}".encode()
            ).hexdigest()[:12]
            
            character = CharacterModel(
                id=char_id,
                **character_data
            )
            
            self.sql_session.add(character)
            self.sql_session.commit()
            
            print(f"✓ Added character: {character_data['name_full']}")
            return char_id
        except Exception as e:
            self.sql_session.rollback()
            print(f"❌ Error adding character: {e}")
            return ""
    
    def search_anime(self, title: str) -> Optional[Dict]:
        """Search anime in Cloud SQL"""
        if not self.sql_session:
            return None
        
        anime = self.sql_session.query(AnimeModel).filter(
            AnimeModel.title_english.ilike(f"%{title}%")
        ).first()
        
        if anime:
            return {
                "id": anime.id,
                "title_english": anime.title_english,
                "year": anime.year,
                "type": anime.type
            }
        return None
    
    def search_character(self, name: str) -> Optional[Dict]:
        """Search character in Cloud SQL"""
        if not self.sql_session:
            return None
        
        char = self.sql_session.query(CharacterModel).filter(
            CharacterModel.name_full.ilike(f"%{name}%")
        ).first()
        
        if char:
            return {
                "id": char.id,
                "name_full": char.name_full,
                "anime_id": char.anime_id,
                "face_schema_extracted": char.face_schema_extracted
            }
        return None
    
    # =========================================================================
    # PROMPT OPERATIONS (BigQuery)
    # =========================================================================
    
    def add_prompt(self, prompt_data: Dict) -> str:
        """Add prompt to BigQuery"""
        import hashlib
        prompt_id = hashlib.md5(prompt_data['prompt_text'].encode()).hexdigest()[:12]
        
        row = {
            "prompt_id": prompt_id,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "usage_count": 0,
            **prompt_data
        }
        
        table_ref = f"{self.bq_dataset_ref}.{BQ_TABLE_PROMPTS}"
        errors = self.bq_client.insert_rows_json(table_ref, [row])
        
        if not errors:
            print(f"✓ Added prompt to BigQuery: {prompt_data.get('category', 'Unknown')}")
            return prompt_id
        else:
            print(f"❌ Error adding prompt: {errors}")
            return ""
    
    def search_prompts(self, category: Optional[str] = None, tags: Optional[List[str]] = None) -> List[Dict]:
        """Search prompts in BigQuery"""
        table_ref = f"{self.bq_dataset_ref}.{BQ_TABLE_PROMPTS}"
        
        if category:
            query = f"""
                SELECT *
                FROM `{table_ref}`
                WHERE category = @category
                ORDER BY usage_count DESC, avg_rating DESC
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("category", "STRING", category)
                ]
            )
        elif tags:
            query = f"""
                SELECT *
                FROM `{table_ref}`,
                UNNEST(style_tags) AS tag
                WHERE tag IN UNNEST(@tags)
                GROUP BY prompt_id, prompt_text, category, style_tags, use_case,
                        model_recommended, resolution, aspect_ratio, gender_target,
                        setting, lighting, mood, created_at, usage_count, avg_rating, source
                ORDER BY usage_count DESC
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("tags", "STRING", tags)
                ]
            )
        else:
            query = f"SELECT * FROM `{table_ref}` ORDER BY created_at DESC LIMIT 10"
            job_config = None
        
        results = self.bq_client.query(query, job_config=job_config).result()
        return [dict(row) for row in results]
    
    # =========================================================================
    # IMAGE OPERATIONS (GCS)
    # =========================================================================
    
    def upload_image(self, local_path: str, bucket_name: str, gcs_path: str) -> str:
        """Upload image to GCS"""
        try:
            bucket = self.gcs_client.bucket(bucket_name)
            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(local_path)
            
            gcs_uri = f"gs://{bucket_name}/{gcs_path}"
            print(f"✓ Uploaded to GCS: {gcs_uri}")
            return gcs_uri
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return ""
    
    def download_image(self, gcs_uri: str, local_path: str) -> bool:
        """Download image from GCS"""
        try:
            # Parse gs://bucket/path
            parts = gcs_uri.replace("gs://", "").split("/", 1)
            bucket_name, gcs_path = parts[0], parts[1]
            
            bucket = self.gcs_client.bucket(bucket_name)
            blob = bucket.blob(gcs_path)
            blob.download_to_filename(local_path)
            
            print(f"✓ Downloaded from GCS: {local_path}")
            return True
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False

# =============================================================================
# USAGE EXAMPLE
# =============================================================================

if __name__ == "__main__":
    brain = YukiCloudBrain()
    
    # Test anime database
    anime_id = brain.add_anime({
        "title_english": "Fullmetal Alchemist: Brotherhood",
        "year": 2009,
        "type": "TV",
        "status": "Finished",
        "genres": json.dumps(["Action", "Adventure"]),
        "mal_rank": 1,
        "mal_score": 9.1
    })
    
    # Test character database
    if anime_id:
        brain.add_character({
            "anime_id": anime_id,
            "name_full": "Edward Elric",
            "name_given": "Edward",
            "name_family": "Elric",
            "role": "Main",
            "gender": "Male"
        })
    
    # Test prompt database
    brain.add_prompt({
        "prompt_text": "Ultra-realistic 4K portrait...",
        "category": "Urban Night Street Style",
        "style_tags": ["4K", "cinematic", "ultra-realistic"],
        "use_case": ["Instagram", "Fashion"],
        "model_recommended": "gemini-3-pro-image-preview",
        "resolution": "4K",
        "aspect_ratio": "3:4"
    })
    
    print("\n✅ Cloud Brain test complete!")
