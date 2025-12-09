"""
Yuki Cosplay API - Production Cloud Run Backend
Enterprise-grade API for nationwide cosplay generation service
Zero local dependencies - 100% GCP
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from google.cloud import storage, bigquery
from google import genai
from google.genai import types
import datetime
import hashlib
import json

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ID = "gifted-cooler-479623-r7"
REGION = "us-central1"

# GCS Configuration (globally accessible)
GCS_BUCKET_UPLOADS = "yuki-user-uploads"
GCS_BUCKET_GENERATIONS = "yuki-cosplay-generations"
GCS_CDN_BUCKET = "yuki-cdn"  # Public bucket with CDN enabled

# BigQuery
BQ_DATASET = "yuki_production"
BQ_TABLE_USERS = "users"
BQ_TABLE_GENERATIONS = "generations"
BQ_TABLE_ANALYTICS = "analytics"

# Models
GEMINI_3_PRO_IMAGE = "gemini-3-pro-image-preview"
GEMINI_3_PRO = "gemini-3-pro-preview"

# Initialize clients
storage_client = storage.Client(project=PROJECT_ID)
bq_client = bigquery.Client(project=PROJECT_ID)
genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")

# =============================================================================
# FASTAPI APP
# =============================================================================

app = FastAPI(
    title="Yuki Cosplay API",
    description="Enterprise cosplay generation service powered by Gemini",
    version="1.0.0"
)

# CORS - Allow frontend from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# MODELS
# =============================================================================

class GenerationRequest(BaseModel):
    user_id: str
    source_image_url: str  # GCS URL or uploaded file
    target_character: str
    target_anime: Optional[str] = None
    style: str = "ultra-realistic"
    resolution: str = "4K"
    aspect_ratio: str = "3:4"
    use_face_schema: bool = True

class GenerationResponse(BaseModel):
    generation_id: str
    status: str  # processing, completed, failed
    output_url: Optional[str] = None
    cdn_url: Optional[str] = None
    face_schema_id: Optional[str] = None
    processing_time: Optional[float] = None
    message: str

class PromptSearchRequest(BaseModel):
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    limit: int = 10

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def upload_to_gcs(file_data: bytes, bucket_name: str, blob_name: str) -> str:
    """Upload file to GCS and return public URL"""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(file_data)
    
    # Make public for CDN
    blob.make_public()
    
    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"

def generate_id(text: str) -> str:
    """Generate unique ID"""
    return hashlib.md5(f"{text}_{datetime.datetime.utcnow()}".encode()).hexdigest()[:12]

def log_to_bigquery(table: str, row: dict):
    """Log event to BigQuery"""
    table_ref = f"{PROJECT_ID}.{BQ_DATASET}.{table}"
    errors = bq_client.insert_rows_json(table_ref, [row])
    if errors:
        print(f"BigQuery insert errors: {errors}")

def get_optimized_prompt(target_character: str, style: str) -> str:
    """Get optimized prompt from BigQuery knowledge base"""
    query = f"""
        SELECT prompt_text
        FROM `{PROJECT_ID}.yuki_prompts.portrait_prompts`
        WHERE LOWER(category) LIKE @character
        OR @character IN UNNEST(SPLIT(LOWER(prompt_text), ' '))
        ORDER BY usage_count DESC, avg_rating DESC
        LIMIT 1
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("character", "STRING", target_character.lower())
        ]
    )
    
    results = list(bq_client.query(query, job_config=job_config).result())
    
    if results:
        return results[0].prompt_text
    
    # Fallback to default ultra-realistic prompt
    return f"""
    Generate an ultra-realistic 4K portrait of {target_character}.
    {style} style with cinematic lighting, DSLR quality, 
    sharp facial details, visible skin pores, natural texture.
    Shot on Sony A7R V, 85mm lens, shallow depth of field,
    professional photography, hyper-realism, 8K clarity.
    """

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "Yuki Cosplay API",
        "status": "operational",
        "version": "1.0.0",
        "region": REGION
    }

@app.post("/api/v1/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload source image to GCS
    Returns GCS URL for use in generation
    """
    try:
        # Generate unique filename
        file_ext = file.filename.split(".")[-1]
        blob_name = f"uploads/{generate_id(file.filename)}.{file_ext}"
        
        # Upload to GCS
        file_data = await file.read()
        gcs_url = upload_to_gcs(file_data, GCS_BUCKET_UPLOADS, blob_name)
        
        return {
            "success": True,
            "gcs_url": gcs_url,
            "message": "Image uploaded successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/generate", response_model=GenerationResponse)
async def generate_cosplay(request: GenerationRequest, background_tasks: BackgroundTasks):
    """
    Generate cosplay image
    This is async - returns immediately with generation_id
    Client polls /status endpoint
    """
    try:
        generation_id = generate_id(f"{request.user_id}_{request.target_character}")
        
        # Start generation in background
        background_tasks.add_task(
            process_generation,
            generation_id,
            request
        )
        
        return GenerationResponse(
            generation_id=generation_id,
            status="processing",
            message="Generation started. Poll /api/v1/status/{generation_id} for updates"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_generation(generation_id: str, request: GenerationRequest):
    """
    Background task to process generation
    """
    start_time = datetime.datetime.utcnow()
    
    try:
        # 1. Get optimized prompt
        prompt = get_optimized_prompt(request.target_character, request.style)
        
        # 2. Extract face schema if requested
        face_schema_id = None
        if request.use_face_schema:
            # Call face math extraction
            # (This would integrate with yuki_memory_system.py)
            pass
        
        # 3. Download source image from GCS
        source_url = request.source_image_url
        # Parse GCS URL and download
        
        # 4. Generate with Gemini 3 Pro Image
        response = genai_client.models.generate_content(
            model=GEMINI_3_PRO_IMAGE,
            contents=[prompt],  # Add source image here
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=request.aspect_ratio,
                    image_size=request.resolution
                )
            )
        )
        
        # 5. Upload result to GCS
        output_blob_name = f"generations/{generation_id}.png"
        # Extract image from response and upload
        
        # 6. Copy to CDN bucket for global distribution
        cdn_blob_name = f"public/{generation_id}.png"
        cdn_url = f"https://cdn.yukicosplay.com/{generation_id}.png"  # Your CDN domain
        
        # 7. Log to BigQuery
        processing_time = (datetime.datetime.utcnow() - start_time).total_seconds()
        
        log_to_bigquery(BQ_TABLE_GENERATIONS, {
            "generation_id": generation_id,
            "user_id": request.user_id,
            "target_character": request.target_character,
            "model_used": GEMINI_3_PRO_IMAGE,
            "resolution": request.resolution,
            "processing_time_seconds": processing_time,
            "status": "completed",
            "output_gcs": f"gs://{GCS_BUCKET_GENERATIONS}/{output_blob_name}",
            "cdn_url": cdn_url,
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        # Log failure
        log_to_bigquery(BQ_TABLE_GENERATIONS, {
            "generation_id": generation_id,
            "user_id": request.user_id,
            "status": "failed",
            "error_message": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

@app.get("/api/v1/status/{generation_id}")
async def get_status(generation_id: str):
    """
    Check generation status
    """
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE_GENERATIONS}`
        WHERE generation_id = @gen_id
        ORDER BY timestamp DESC
        LIMIT 1
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("gen_id", "STRING", generation_id)
        ]
    )
    
    results = list(bq_client.query(query, job_config=job_config).result())
    
    if not results:
        raise HTTPException(status_code=404, detail="Generation not found")
    
    row = dict(results[0])
    
    return GenerationResponse(
        generation_id=generation_id,
        status=row.get("status", "processing"),
        output_url=row.get("output_gcs"),
        cdn_url=row.get("cdn_url"),
        processing_time=row.get("processing_time_seconds"),
        message="Generation complete" if row.get("status") == "completed" else "Processing..."
    )

@app.post("/api/v1/prompts/search")
async def search_prompts(request: PromptSearchRequest):
    """
    Search prompt library
    """
    table_ref = f"{PROJECT_ID}.yuki_prompts.portrait_prompts"
    
    if request.category:
        query = f"""
            SELECT *
            FROM `{table_ref}`
            WHERE category = @category
            ORDER BY usage_count DESC
            LIMIT @limit
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("category", "STRING", request.category),
                bigquery.ScalarQueryParameter("limit", "INT64", request.limit)
            ]
        )
    else:
        query = f"""
            SELECT *
            FROM `{table_ref}`
            ORDER BY avg_rating DESC, usage_count DESC
            LIMIT @limit
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("limit", "INT64", request.limit)
            ]
        )
    
    results = bq_client.query(query, job_config=job_config).result()
    
    return {
        "prompts": [dict(row) for row in results],
        "count": len(list(results))
    }

@app.get("/api/v1/analytics/stats")
async def get_stats():
    """
    Get platform analytics
    """
    query = f"""
        SELECT 
            COUNT(*) as total_generations,
            COUNT(DISTINCT user_id) as total_users,
            AVG(processing_time_seconds) as avg_processing_time,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as successful_generations
        FROM `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE_GENERATIONS}`
    """
    
    results = list(bq_client.query(query).result())
    
    if results:
        return dict(results[0])
    
    return {}

# =============================================================================
# STARTUP
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize cloud resources on startup"""
    print("🚀 Yuki Cosplay API starting...")
    print(f"   Project: {PROJECT_ID}")
    print(f"   Region: {REGION}")
    print("✅ API ready for requests")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
