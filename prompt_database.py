"""
Prompt Database - BigQuery Backend
Store, search, and manage ultra-realistic portrait prompts
"""

from google.cloud import bigquery
from google.cloud.bigquery import SchemaField
import datetime
from typing import List, Dict, Optional
import json

PROJECT_ID = "gifted-cooler-479623-r7"
DATASET_ID = "yuki_prompts"
TABLE_ID = "portrait_prompts"

class PromptDatabase:
    """
    BigQuery-backed prompt database with semantic search
    """
    
    def __init__(self):
        self.client = bigquery.Client(project=PROJECT_ID)
        self.dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
        self.table_ref = f"{self.dataset_ref}.{TABLE_ID}"
        self._ensure_dataset_exists()
        self._ensure_table_exists()
    
    def _ensure_dataset_exists(self):
        """Create dataset if it doesn't exist"""
        try:
            self.client.get_dataset(self.dataset_ref)
            print(f"✓ Dataset exists: {self.dataset_ref}")
        except Exception:
            dataset = bigquery.Dataset(self.dataset_ref)
            dataset.location = "US"
            dataset = self.client.create_dataset(dataset, timeout=30)
            print(f"✓ Created dataset: {self.dataset_ref}")
    
    def _ensure_table_exists(self):
        """Create table with schema if it doesn't exist"""
        schema = [
            SchemaField("prompt_id", "STRING", mode="REQUIRED"),
            SchemaField("prompt_text", "STRING", mode="REQUIRED"),
            SchemaField("category", "STRING", mode="REQUIRED"),
            SchemaField("style_tags", "STRING", mode="REPEATED"),
            SchemaField("use_case", "STRING", mode="REPEATED"),
            SchemaField("model_recommended", "STRING", mode="NULLABLE"),
            SchemaField("resolution", "STRING", mode="NULLABLE"),
            SchemaField("aspect_ratio", "STRING", mode="NULLABLE"),
            SchemaField("gender_target", "STRING", mode="NULLABLE"),
            SchemaField("setting", "STRING", mode="NULLABLE"),
            SchemaField("lighting", "STRING", mode="NULLABLE"),
            SchemaField("mood", "STRING", mode="NULLABLE"),
            SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            SchemaField("usage_count", "INTEGER", mode="NULLABLE"),
            SchemaField("avg_rating", "FLOAT", mode="NULLABLE"),
            SchemaField("source", "STRING", mode="NULLABLE"),
        ]
        
        try:
            self.client.get_table(self.table_ref)
            print(f"✓ Table exists: {self.table_ref}")
        except Exception:
            table = bigquery.Table(self.table_ref, schema=schema)
            table = self.client.create_table(table)
            print(f"✓ Created table: {self.table_ref}")
    
    def add_prompt(
        self,
        prompt_text: str,
        category: str,
        style_tags: List[str],
        use_case: List[str],
        prompt_id: Optional[str] = None,
        model_recommended: str = "gemini-3-pro-image-preview",
        resolution: str = "4K",
        aspect_ratio: str = "3:4",
        gender_target: Optional[str] = None,
        setting: Optional[str] = None,
        lighting: Optional[str] = None,
        mood: Optional[str] = None,
        source: str = "manual"
    ) -> str:
        """Add a prompt to the database"""
        if not prompt_id:
            import hashlib
            prompt_id = hashlib.md5(prompt_text.encode()).hexdigest()[:12]
        
        row = {
            "prompt_id": prompt_id,
            "prompt_text": prompt_text,
            "category": category,
            "style_tags": style_tags,
            "use_case": use_case,
            "model_recommended": model_recommended,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "gender_target": gender_target,
            "setting": setting,
            "lighting": lighting,
            "mood": mood,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "usage_count": 0,
            "avg_rating": None,
            "source": source
        }
        
        errors = self.client.insert_rows_json(self.table_ref, [row])
        if errors:
            print(f"❌ Error inserting: {errors}")
            return ""
        
        print(f"✓ Added prompt: {category} ({prompt_id})")
        return prompt_id
    
    def search_by_category(self, category: str) -> List[Dict]:
        """Search prompts by category"""
        query = f"""
            SELECT *
            FROM `{self.table_ref}`
            WHERE category = @category
            ORDER BY created_at DESC
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("category", "STRING", category)
            ]
        )
        
        results = self.client.query(query, job_config=job_config).result()
        return [dict(row) for row in results]
    
    def search_by_tags(self, tags: List[str]) -> List[Dict]:
        """Search prompts by style tags"""
        query = f"""
            SELECT *
            FROM `{self.table_ref}`,
            UNNEST(style_tags) AS tag
            WHERE tag IN UNNEST(@tags)
            GROUP BY prompt_id, prompt_text, category, style_tags, use_case,
                     model_recommended, resolution, aspect_ratio, gender_target,
                     setting, lighting, mood, created_at, usage_count, avg_rating, source
            ORDER BY created_at DESC
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter("tags", "STRING", tags)
            ]
        )
        
        results = self.client.query(query, job_config=job_config).result()
        return [dict(row) for row in results]
    
    def get_top_prompts(self, limit: int = 10) -> List[Dict]:
        """Get top-rated prompts"""
        query = f"""
            SELECT *
            FROM `{self.table_ref}`
            ORDER BY usage_count DESC, avg_rating DESC
            LIMIT @limit
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("limit", "INT64", limit)
            ]
        )
        
        results = self.client.query(query, job_config=job_config).result()
        return [dict(row) for row in results]
    
    def increment_usage(self, prompt_id: str):
        """Increment usage count for a prompt"""
        query = f"""
            UPDATE `{self.table_ref}`
            SET usage_count = COALESCE(usage_count, 0) + 1
            WHERE prompt_id = @prompt_id
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("prompt_id", "STRING", prompt_id)
            ]
        )
        
        self.client.query(query, job_config=job_config).result()
    
    def rate_prompt(self, prompt_id: str, rating: float):
        """Rate a prompt (1-5 stars)"""
        # Get current avg
        query = f"""
            SELECT avg_rating, usage_count
            FROM `{self.table_ref}`
            WHERE prompt_id = @prompt_id
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("prompt_id", "STRING", prompt_id)
            ]
        )
        
        result = list(self.client.query(query, job_config=job_config).result())
        if not result:
            return
        
        current_avg = result[0].avg_rating or 0
        count = result[0].usage_count or 0
        
        # Calculate new average
        new_avg = ((current_avg * count) + rating) / (count + 1)
        
        # Update
        update_query = f"""
            UPDATE `{self.table_ref}`
            SET avg_rating = @new_avg
            WHERE prompt_id = @prompt_id
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("prompt_id", "STRING", prompt_id),
                bigquery.ScalarQueryParameter("new_avg", "FLOAT64", new_avg)
            ]
        )
        
        self.client.query(update_query, job_config=job_config).result()
        print(f"✓ Rated prompt: {rating:.1f} stars (new avg: {new_avg:.2f})")

# =============================================================================
# PRE-POPULATE WITH ULTRA-REALISTIC PORTRAIT PROMPTS
# =============================================================================

PORTRAIT_PROMPTS = [
    {
        "prompt_text": "Generate an ultra-realistic 4K portrait of a young Indian man standing on a city street at night under neon lights. He is wearing a black bomber jacket, slim-fit jeans and premium sneakers. Wet asphalt reflecting colorful lights. Background softly blurred with moving traffic bokeh. Sharp facial details, visible skin pores, natural texture, sharp jawline, realistic hairstyle. Shot on Sony A7R V, 85mm lens, shallow depth of field, cinematic color grading, dramatic shadows, ultra-HD, hyper-realism.",
        "category": "Urban Night Street Style",
        "style_tags": ["ultra-realistic", "4K", "cinematic", "neon", "bokeh", "hyper-realism"],
        "use_case": ["Instagram", "Fashion", "Street Photography"],
        "gender_target": "Male",
        "setting": "City Street at Night",
        "lighting": "Neon Lights, Dramatic Shadows",
        "mood": "Urban, Edgy"
    },
    {
        "prompt_text": "Create a 4K ultra-realistic portrait of a stylish Indian man during golden hour. He is wearing a beige linen shirt with sleeves rolled up, standing near an old brick wall. Soft warm sunlight falling on one side of his face, natural shadows, wind in hair. Background blurred with trees and buildings. Natural skin texture, film-like tones, DSLR quality, 8K clarity, professional photography style.",
        "category": "Golden Hour Model Look",
        "style_tags": ["ultra-realistic", "4K", "golden-hour", "DSLR", "film-like", "professional"],
        "use_case": ["Instagram", "Model Portfolio", "Lifestyle"],
        "gender_target": "Male",
        "setting": "Outdoor Brick Wall",
        "lighting": "Golden Hour, Soft Warm Sunlight",
        "mood": "Warm, Natural, Stylish"
    },
    {
        "prompt_text": "Generate a hyper-realistic 4K portrait of an Indian man wearing a royal blue embroidered sherwani, standing in a heritage palace courtyard. Traditional architecture in the background with soft depth blur. Golden sunlight highlighting embroidery details. Elegant posture, confident expression. Ultra-sharp focus, cinematic lighting, natural skin texture, luxury fashion photography, captured in 4K, professional studio finish.",
        "category": "Royal Sherwani Look",
        "style_tags": ["hyper-realistic", "4K", "traditional", "luxury", "cinematic", "heritage"],
        "use_case": ["Wedding", "Traditional Fashion", "Cultural"],
        "gender_target": "Male",
        "setting": "Heritage Palace Courtyard",
        "lighting": "Golden Sunlight, Cinematic",
        "mood": "Royal, Elegant, Confident"
    },
    {
        "prompt_text": "Create a 4K HD ultra-real portrait of a young Indian boy in oversized hoodie, cargo pants and sneakers, standing against a graffiti wall. Urban vibe, soft neon lights, cinematic shadows. One hand in pocket, confident look. Texture details in clothes, visible pores, realistic lighting. DSLR quality, sand-blasted background, high contrast, ultra-detail.",
        "category": "Trendy Streetwear Vibe",
        "style_tags": ["ultra-realistic", "4K", "streetwear", "urban", "graffiti", "high-contrast"],
        "use_case": ["Instagram", "Street Fashion", "Youth Culture"],
        "gender_target": "Male",
        "setting": "Graffiti Wall",
        "lighting": "Soft Neon, Cinematic Shadows",
        "mood": "Urban, Confident, Trendy"
    },
    {
        "prompt_text": "Generate a 4K cinematic portrait of an Indian man standing in the rain at night. Wet hair, soaked shirt, water droplets on face and skin. Emotional expression. Dark blue tones, dramatic lighting, streetlights in background with blurred bokeh. Hyper-realistic skin, sharp eyelashes, visible textures, professional movie-scene look.",
        "category": "Monsoon Rain Cinematic Portrait",
        "style_tags": ["cinematic", "4K", "rain", "dramatic", "emotional", "hyper-realistic"],
        "use_case": ["Cinematic", "Artistic", "Emotional Storytelling"],
        "gender_target": "Male",
        "setting": "Night Rain",
        "lighting": "Dramatic, Streetlights, Dark Blue Tones",
        "mood": "Emotional, Dramatic, Moody"
    },
    {
        "prompt_text": "Create a hyper-realistic 4K portrait of an Indian traveler in a desert. Wearing rugged jacket, scarf around neck, aviator sunglasses. Wind blowing sand slightly, dunes in background. Golden sunlight, warm tones. Sharp focus on face, cinematic depth, ultra-realistic details, adventure photography style.",
        "category": "Desert Adventure Look",
        "style_tags": ["hyper-realistic", "4K", "adventure", "desert", "cinematic", "travel"],
        "use_case": ["Travel", "Adventure", "Lifestyle"],
        "gender_target": "Male",
        "setting": "Desert Dunes",
        "lighting": "Golden Sunlight, Warm Tones",
        "mood": "Adventurous, Rugged"
    },
    {
        "prompt_text": "Generate a 4K realistic portrait of a man sitting in an aesthetic café with a coffee cup in hand. Wearing a casual shirt, soft smile, messy hairstyle. Warm indoor light through window. Blurred cozy background, realistic skin tone, DSLR effect, natural color grading, soft bokeh.",
        "category": "Café Candid Lifestyle Shot",
        "style_tags": ["realistic", "4K", "lifestyle", "café", "candid", "cozy"],
        "use_case": ["Lifestyle", "Instagram", "Casual"],
        "gender_target": "Male",
        "setting": "Aesthetic Café",
        "lighting": "Warm Indoor Light",
        "mood": "Cozy, Relaxed, Casual"
    },
    {
        "prompt_text": "Create a 4K portrait of a South Indian man in white veshti and traditional shirt standing near a temple entrance. Morning sunlight, peaceful expression. High realism, sharp eye details, natural skin texture. Heritage vibes, cinematic depth, DSLR quality, professional photography.",
        "category": "South Indian Traditional Portrait",
        "style_tags": ["4K", "traditional", "heritage", "cultural", "realistic", "cinematic"],
        "use_case": ["Cultural", "Traditional", "Heritage"],
        "gender_target": "Male",
        "setting": "Temple Entrance",
        "lighting": "Morning Sunlight",
        "mood": "Peaceful, Traditional"
    },
    {
        "prompt_text": "Generate a hyper-realistic 4K portrait of an Indian businessman wearing a charcoal grey tailored suit and watch. Studio lighting setup, clean blurred background. Sleek hairstyle, confident pose, glossy skin tones, ultra-sharp facial detail, premium fashion photography style.",
        "category": "Luxury Suit Professional Portrait",
        "style_tags": ["hyper-realistic", "4K", "professional", "luxury", "studio", "business"],
        "use_case": ["Professional", "Business", "Corporate"],
        "gender_target": "Male",
        "setting": "Studio",
        "lighting": "Studio Lighting",
        "mood": "Professional, Confident, Luxury"
    },
    {
        "prompt_text": "Create an ultra-realistic 4K portrait of a muscular Indian man in gym, wearing sleeveless tank top. Sweat on skin, intense expression, gym equipment blurred in background. Strong lighting highlighting muscle definition. Crisp detailing, cinematic contrast, hyper realism.",
        "category": "Fitness Model Gym Look",
        "style_tags": ["ultra-realistic", "4K", "fitness", "gym", "muscular", "intense"],
        "use_case": ["Fitness", "Sports", "Health"],
        "gender_target": "Male",
        "setting": "Gym",
        "lighting": "Strong, Highlighting Muscles",
        "mood": "Intense, Strong, Fitness"
    }
]

def populate_database():
    """Populate database with ultra-realistic portrait prompts"""
    db = PromptDatabase()
    
    print("\n🎨 Populating BigQuery with Ultra-Realistic Portrait Prompts...\n")
    
    for prompt_data in PORTRAIT_PROMPTS:
        db.add_prompt(**prompt_data)
    
    print(f"\n✅ Added {len(PORTRAIT_PROMPTS)} prompts to BigQuery!")
    print(f"📊 Dataset: {db.dataset_ref}")
    print(f"📋 Table: {db.table_ref}")

if __name__ == "__main__":
    populate_database()
    
    # Test search
    db = PromptDatabase()
    print("\n🔍 Testing search by category...")
    results = db.search_by_category("Urban Night Street Style")
    if results:
        print(f"Found {len(results)} prompts")
        print(f"Sample: {results[0]['category']}")
    
    print("\n🔍 Testing search by tags...")
    results = db.search_by_tags(["cinematic", "4K"])
    print(f"Found {len(results)} prompts with cinematic + 4K tags")
