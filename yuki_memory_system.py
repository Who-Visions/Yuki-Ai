"""
Yuki Memory System - Cloud-Native Knowledge & Learning
Stores resources, knowledge, face schemas, and learns from every iteration
"""

from google.cloud import bigquery, storage
from google.cloud import aiplatform
from google.cloud.aiplatform.matching_engine import MatchingEngineIndex
import datetime
from typing import List, Dict, Optional, Any
import json
import hashlib
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ID = "gifted-cooler-479623-r7"
REGION = "us-central1"

# BigQuery Datasets
BQ_DATASET_MEMORY = "yuki_memory"
BQ_TABLE_KNOWLEDGE = "knowledge_base"
BQ_TABLE_FACE_SCHEMAS = "face_schema_library"
BQ_TABLE_GENERATION_HISTORY = "generation_history"
BQ_TABLE_LEARNINGS = "learnings"
BQ_TABLE_CHARACTER_MAPPINGS = "character_consistency_mappings"

# GCS Buckets
GCS_BUCKET_KNOWLEDGE = "yuki-knowledge-base"
GCS_BUCKET_FACE_SCHEMAS = "yuki-face-schemas"
GCS_BUCKET_TRAINING_DATA = "yuki-training-data"

# Vector Search (for semantic knowledge retrieval)
VECTOR_SEARCH_INDEX = "yuki-knowledge-index"

# =============================================================================
# YUKI MEMORY SYSTEM
# =============================================================================

class YukiMemorySystem:
    """
    Complete memory and learning system for Yuki
    
    Components:
    1. Knowledge Base - MD files, guides, resources
    2. Face Schema Library - Character face mappings
    3. Generation History - Track all generations + results
    4. Learning System - Improve with each iteration
    5. Character Consistency - Map faces across styles
    """
    
    def __init__(self):
        print("\n🧠 Initializing Yuki Memory System...")
        
        self.bq_client = bigquery.Client(project=PROJECT_ID)
        self.gcs_client = storage.Client(project=PROJECT_ID)
        
        self._ensure_datasets()
        self._ensure_tables()
        self._ensure_buckets()
        
        print("✅ Memory System ready!\n")
    
    def _ensure_datasets(self):
        """Create BigQuery datasets"""
        dataset_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}"
        try:
            self.bq_client.get_dataset(dataset_ref)
        except:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            self.bq_client.create_dataset(dataset)
            print(f"✓ Created dataset: {BQ_DATASET_MEMORY}")
    
    def _ensure_tables(self):
        """Create all memory tables"""
        self._create_knowledge_table()
        self._create_face_schema_table()
        self._create_generation_history_table()
        self._create_learnings_table()
        self._create_character_mapping_table()
    
    def _create_knowledge_table(self):
        """Store markdown docs, guides, and resources"""
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_KNOWLEDGE}"
        
        schema = [
            bigquery.SchemaField("knowledge_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("title", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("content", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("content_type", "STRING"),  # markdown, guide, tutorial, reference
            bigquery.SchemaField("category", "STRING"),  # face_math, prompting, model_guides, etc
            bigquery.SchemaField("tags", "STRING", mode="REPEATED"),
            bigquery.SchemaField("gcs_path", "STRING"),  # Original file location
            bigquery.SchemaField("importance_score", "FLOAT"),  # How critical is this knowledge
            bigquery.SchemaField("last_accessed", "TIMESTAMP"),
            bigquery.SchemaField("access_count", "INTEGER"),
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
        ]
        
        try:
            self.bq_client.get_table(table_ref)
        except:
            table = bigquery.Table(table_ref, schema=schema)
            self.bq_client.create_table(table)
            print("✓ Created knowledge base table")
    
    def _create_face_schema_table(self):
        """Store face math schemas for character consistency"""
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_FACE_SCHEMAS}"
        
        schema = [
            bigquery.SchemaField("schema_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("character_id", "STRING"),
            bigquery.SchemaField("character_name", "STRING"),
            bigquery.SchemaField("anime_title", "STRING"),
            
            # Face Math Data
            bigquery.SchemaField("identity_vector", "JSON"),  # Geometric ratios
            bigquery.SchemaField("feature_map", "JSON"),  # Eye, nose, lips details
            bigquery.SchemaField("distinctive_marks", "STRING", mode="REPEATED"),
            bigquery.SchemaField("expression_weights", "JSON"),
            
            # Metadata
            bigquery.SchemaField("extraction_model", "STRING"),
            bigquery.SchemaField("extraction_quality", "FLOAT"),  # Confidence score
            bigquery.SchemaField("reference_images_gcs", "STRING", mode="REPEATED"),
            
            # Usage tracking
            bigquery.SchemaField("times_used", "INTEGER"),
            bigquery.SchemaField("avg_generation_quality", "FLOAT"),
            bigquery.SchemaField("successful_generations", "INTEGER"),
            bigquery.SchemaField("failed_generations", "INTEGER"),
            
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("last_used", "TIMESTAMP"),
        ]
        
        try:
            self.bq_client.get_table(table_ref)
        except:
            table = bigquery.Table(table_ref, schema=schema)
            self.bq_client.create_table(table)
            print("✓ Created face schema library table")
    
    def _create_generation_history_table(self):
        """Track every generation with results for learning"""
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_GENERATION_HISTORY}"
        
        schema = [
            bigquery.SchemaField("generation_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("schema_id", "STRING"),  # Face schema used
            bigquery.SchemaField("prompt_id", "STRING"),  # Prompt used
            
            # Input
            bigquery.SchemaField("source_character", "STRING"),
            bigquery.SchemaField("target_character", "STRING"),
            bigquery.SchemaField("prompt_text", "STRING"),
            bigquery.SchemaField("model_used", "STRING"),
            bigquery.SchemaField("resolution", "STRING"),
            bigquery.SchemaField("aspect_ratio", "STRING"),
            
            # Output
            bigquery.SchemaField("output_gcs_path", "STRING"),
            bigquery.SchemaField("generation_time_seconds", "FLOAT"),
            bigquery.SchemaField("success", "BOOLEAN"),
            bigquery.SchemaField("error_message", "STRING"),
            
            # Quality Metrics
            bigquery.SchemaField("identity_preserved", "FLOAT"),  # 0-1 score
            bigquery.SchemaField("costume_accuracy", "FLOAT"),
            bigquery.SchemaField("image_quality", "FLOAT"),
            bigquery.SchemaField("user_rating", "INTEGER"),  # 1-5 stars
            
            # Learning Data
            bigquery.SchemaField("what_worked", "STRING"),
            bigquery.SchemaField("what_failed", "STRING"),
            bigquery.SchemaField("improvements_needed", "STRING"),
            
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        ]
        
        try:
            self.bq_client.get_table(table_ref)
        except:
            table = bigquery.Table(table_ref, schema=schema)
            self.bq_client.create_table(table)
            print("✓ Created generation history table")
    
    def _create_learnings_table(self):
        """Store learnings from iterations to improve over time"""
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_LEARNINGS}"
        
        schema = [
            bigquery.SchemaField("learning_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("category", "STRING"),  # prompt_improvement, model_selection, face_schema, etc
            bigquery.SchemaField("insight", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("confidence", "FLOAT"),  # How sure are we this works
            bigquery.SchemaField("evidence", "JSON"),  # Generation IDs that prove this
            bigquery.SchemaField("implementation_status", "STRING"),  # tested, validated, deployed
            bigquery.SchemaField("impact_score", "FLOAT"),  # How much did this improve results
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("validated_at", "TIMESTAMP"),
        ]
        
        try:
            self.bq_client.get_table(table_ref)
        except:
            table = bigquery.Table(table_ref, schema=schema)
            self.bq_client.create_table(table)
            print("✓ Created learnings table")
    
    def _create_character_mapping_table(self):
        """Map character appearances across different styles/scenarios"""
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_CHARACTER_MAPPINGS}"
        
        schema = [
            bigquery.SchemaField("mapping_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("base_character_id", "STRING"),
            bigquery.SchemaField("base_schema_id", "STRING"),
            
            # Variations
            bigquery.SchemaField("variation_type", "STRING"),  # different_outfit, different_age, different_style
            bigquery.SchemaField("variation_schema_id", "STRING"),
            bigquery.SchemaField("variation_gcs_path", "STRING"),
            
            # Consistency
            bigquery.SchemaField("consistency_score", "FLOAT"),  # How well identity was preserved
            bigquery.SchemaField("key_features_maintained", "STRING", mode="REPEATED"),
            
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
        ]
        
        try:
            self.bq_client.get_table(table_ref)
        except:
            table = bigquery.Table(table_ref, schema=schema)
            self.bq_client.create_table(table)
            print("✓ Created character mapping table")
    
    def _ensure_buckets(self):
        """Create GCS buckets for storage"""
        for bucket_name in [GCS_BUCKET_KNOWLEDGE, GCS_BUCKET_FACE_SCHEMAS, GCS_BUCKET_TRAINING_DATA]:
            try:
                self.gcs_client.get_bucket(bucket_name)
            except:
                bucket = self.gcs_client.create_bucket(bucket_name, location=REGION)
                print(f"✓ Created bucket: {bucket_name}")
    
    # =========================================================================
    # KNOWLEDGE BASE OPERATIONS
    # =========================================================================
    
    def store_knowledge(
        self,
        title: str,
        content: str,
        category: str,
        tags: List[str],
        content_type: str = "markdown",
        local_path: Optional[str] = None
    ) -> str:
        """Store knowledge (MD files, guides, resources)"""
        
        knowledge_id = hashlib.md5(title.encode()).hexdigest()[:12]
        
        # Upload to GCS if local file provided
        gcs_path = None
        if local_path:
            gcs_path = f"knowledge/{category}/{Path(local_path).name}"
            bucket = self.gcs_client.bucket(GCS_BUCKET_KNOWLEDGE)
            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(local_path)
            gcs_path = f"gs://{GCS_BUCKET_KNOWLEDGE}/{gcs_path}"
        
        # Store in BigQuery
        row = {
            "knowledge_id": knowledge_id,
            "title": title,
            "content": content,
            "content_type": content_type,
            "category": category,
            "tags": tags,
            "gcs_path": gcs_path,
            "importance_score": 1.0,  # Default, can be adjusted
            "last_accessed": datetime.datetime.utcnow().isoformat(),
            "access_count": 0,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "updated_at": datetime.datetime.utcnow().isoformat(),
        }
        
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_KNOWLEDGE}"
        errors = self.bq_client.insert_rows_json(table_ref, [row])
        
        if not errors:
            print(f"✓ Stored knowledge: {title}")
            return knowledge_id
        else:
            print(f"❌ Error storing knowledge: {errors}")
            return ""
    
    def search_knowledge(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """Search knowledge base"""
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_KNOWLEDGE}"
        
        if category:
            sql = f"""
                SELECT *
                FROM `{table_ref}`
                WHERE category = @category
                AND (LOWER(title) LIKE @query OR LOWER(content) LIKE @query)
                ORDER BY importance_score DESC, access_count DESC
                LIMIT 10
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("category", "STRING", category),
                    bigquery.ScalarQueryParameter("query", "STRING", f"%{query.lower()}%")
                ]
            )
        else:
            sql = f"""
                SELECT *
                FROM `{table_ref}`
                WHERE LOWER(title) LIKE @query OR LOWER(content) LIKE @query
                ORDER BY importance_score DESC, access_count DESC
                LIMIT 10
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("query", "STRING", f"%{query.lower()}%")
                ]
            )
        
        results = self.bq_client.query(sql, job_config=job_config).result()
        return [dict(row) for row in results]
    
    # =========================================================================
    # FACE SCHEMA OPERATIONS
    # =========================================================================
    
    def store_face_schema(
        self,
        character_name: str,
        schema_data: Dict,
        character_id: Optional[str] = None,
        anime_title: Optional[str] = None,
        reference_images: Optional[List[str]] = None
    ) -> str:
        """Store face math schema for character consistency"""
        
        schema_id = hashlib.md5(f"{character_name}_{datetime.datetime.utcnow()}".encode()).hexdigest()[:12]
        
        row = {
            "schema_id": schema_id,
            "character_id": character_id,
            "character_name": character_name,
            "anime_title": anime_title,
            "identity_vector": json.dumps(schema_data.get("identity_vector", {})),
            "feature_map": json.dumps(schema_data.get("feature_map", {})),
            "distinctive_marks": schema_data.get("distinctive_marks", []),
            "expression_weights": json.dumps(schema_data.get("expression_weights", {})),
            "extraction_model": schema_data.get("model_used", "unknown"),
            "extraction_quality": schema_data.get("quality", 1.0),
            "reference_images_gcs": reference_images or [],
            "times_used": 0,
            "avg_generation_quality": None,
            "successful_generations": 0,
            "failed_generations": 0,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "last_used": None
        }
        
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_FACE_SCHEMAS}"
        errors = self.bq_client.insert_rows_json(table_ref, [row])
        
        if not errors:
            print(f"✓ Stored face schema: {character_name}")
            return schema_id
        else:
            print(f"❌ Error storing schema: {errors}")
            return ""
    
    def get_face_schema(self, character_name: str) -> Optional[Dict]:
        """Retrieve face schema for character"""
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_FACE_SCHEMAS}"
        
        sql = f"""
            SELECT *
            FROM `{table_ref}`
            WHERE character_name = @char_name
            ORDER BY created_at DESC
            LIMIT 1
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("char_name", "STRING", character_name)
            ]
        )
        
        results = list(self.bq_client.query(sql, job_config=job_config).result())
        
        if results:
            return dict(results[0])
        return None
    
    # =========================================================================
    # GENERATION HISTORY & LEARNING
    # =========================================================================
    
    def log_generation(
        self,
        source_character: str,
        target_character: str,
        prompt_text: str,
        model_used: str,
        output_path: str,
        success: bool,
        quality_metrics: Optional[Dict] = None,
        schema_id: Optional[str] = None,
        prompt_id: Optional[str] = None
    ) -> str:
        """Log generation for learning"""
        
        generation_id = hashlib.md5(f"{source_character}_{target_character}_{datetime.datetime.utcnow()}".encode()).hexdigest()[:12]
        
        metrics = quality_metrics or {}
        
        row = {
            "generation_id": generation_id,
            "schema_id": schema_id,
            "prompt_id": prompt_id,
            "source_character": source_character,
            "target_character": target_character,
            "prompt_text": prompt_text,
            "model_used": model_used,
            "resolution": "4K",
            "aspect_ratio": "3:4",
            "output_gcs_path": output_path,
            "generation_time_seconds": metrics.get("time", 0),
            "success": success,
            "error_message": metrics.get("error"),
            "identity_preserved": metrics.get("identity_score"),
            "costume_accuracy": metrics.get("costume_score"),
            "image_quality": metrics.get("quality_score"),
            "user_rating": metrics.get("rating"),
            "what_worked": metrics.get("what_worked"),
            "what_failed": metrics.get("what_failed"),
            "improvements_needed": metrics.get("improvements"),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_GENERATION_HISTORY}"
        errors = self.bq_client.insert_rows_json(table_ref, [row])
        
        if not errors:
            print(f"✓ Logged generation: {generation_id}")
            return generation_id
        else:
            print(f"❌ Error logging generation: {errors}")
            return ""
    
    def add_learning(
        self,
        category: str,
        insight: str,
        confidence: float,
        evidence: List[str]
    ) -> str:
        """Add learning from iterations"""
        
        learning_id = hashlib.md5(insight.encode()).hexdigest()[:12]
        
        row = {
            "learning_id": learning_id,
            "category": category,
            "insight": insight,
            "confidence": confidence,
            "evidence": json.dumps(evidence),
            "implementation_status": "tested",
            "impact_score": None,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "validated_at": None
        }
        
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_LEARNINGS}"
        errors = self.bq_client.insert_rows_json(table_ref, [row])
        
        if not errors:
            print(f"✓ Added learning: {category}")
            return learning_id
        else:
            print(f"❌ Error adding learning: {errors}")
            return ""
    
    def get_learnings(self, category: Optional[str] = None) -> List[Dict]:
        """Get learnings to improve next iteration"""
        table_ref = f"{PROJECT_ID}.{BQ_DATASET_MEMORY}.{BQ_TABLE_LEARNINGS}"
        
        if category:
            sql = f"""
                SELECT *
                FROM `{table_ref}`
                WHERE category = @category
                ORDER BY confidence DESC, impact_score DESC
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("category", "STRING", category)
                ]
            )
        else:
            sql = f"""
                SELECT *
                FROM `{table_ref}`
                ORDER BY confidence DESC, impact_score DESC
                LIMIT 20
            """
            job_config = None
        
        results = self.bq_client.query(sql, job_config=job_config).result()
        return [dict(row) for row in results]

# =============================================================================
# USAGE EXAMPLE
# =============================================================================

if __name__ == "__main__":
    memory = YukiMemorySystem()
    
    # Store knowledge
    memory.store_knowledge(
        title="Nano Banana Pro Prompting Guide",
        content="Use ultra-realistic 4K, cinematic lighting, DSLR quality...",
        category="prompting",
        tags=["nano-banana-pro", "prompting", "4k", "realistic"]
    )
    
    # Store face schema
    schema_data = {
        "identity_vector": {"eye_spacing": 0.45, "jaw_width": 0.72},
        "feature_map": {"eyes": "large, expressive", "nose": "small"},
        "distinctive_marks": ["scar on left cheek"],
        "expression_weights": {"neutral": 0.8}
    }
    
    memory.store_face_schema(
        character_name="Edward Elric",
        schema_data=schema_data,
        anime_title="Fullmetal Alchemist"
    )
    
    # Log generation
    memory.log_generation(
        source_character="Edward Elric",
        target_character="Dante",
        prompt_text="Generate Edward as Dante...",
        model_used="gemini-3-pro-image-preview",
        output_path="gs://yuki-cosplay-generations/ed_dante.png",
        success=True,
        quality_metrics={
            "identity_score": 0.95,
            "costume_score": 0.92,
            "quality_score": 0.98,
            "rating": 5,
            "what_worked": "Face schema preserved identity perfectly",
            "time": 35.2
        }
    )
    
    # Add learning
    memory.add_learning(
        category="prompt_improvement",
        insight="Adding 'visible skin pores' increases realism by 15%",
        confidence=0.92,
        evidence=["gen_123", "gen_456", "gen_789"]
    )
    
    print("\n✅ Memory system test complete!")
