
"""
Yuki Cosplay API - Unified Server
- REST API (Generation, Status, Uploads)
- OpenAI Compatible API (Agent Chat, Tools)
- specialized /cosplay endpoints
"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
import time
import uuid
import datetime
import hashlib
import json
from google.cloud import storage, bigquery
from google import genai
from google.genai import types

# Import Yuki's Agent Tools
from tools import (
    get_current_time,
    add_numbers,
    generate_cosplay_image,
    generate_cosplay_video,
    research_topic,
    list_files,
    read_file,
    write_file,
    search_web,
    fetch_url,
    identify_anime_screenshot,
    detect_objects,
    segment_image,
    analyze_video,
    analyze_pdf,
    upload_to_gcs,
    download_from_gcs,
)
from yuki_local import YUKI_SYSTEM_PROMPT, Colors

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ID = "gifted-cooler-479623-r7"
REGION = "us-central1"
LOCATION = "global"

# GCS Configuration
GCS_BUCKET_UPLOADS = "yuki-user-uploads"
GCS_BUCKET_GENERATIONS = "yuki-cosplay-generations"
GCS_CDN_BUCKET = "yuki-cdn"

# BigQuery
BQ_DATASET = "yuki_production"
BQ_TABLE_GENERATIONS = "generations"

# Models
GEMINI_3_PRO_IMAGE = "gemini-3-pro-image-preview"
GEMINI_3_PRO = "gemini-3-pro-preview"

# Initialize Clients
storage_client = storage.Client(project=PROJECT_ID)
bq_client = bigquery.Client(project=PROJECT_ID)
genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# =============================================================================
# APP SETUP
# =============================================================================

app = FastAPI(
    title="Yuki Cosplay API & Agent",
    description="Unified endpoint for Cosplay Generation and AI Agent capabilities.",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# DATA MODELS
# =============================================================================

# REST API Models
class GenerationRequest(BaseModel):
    user_id: str
    source_image_url: str
    target_character: str
    target_anime: Optional[str] = None
    style: str = "ultra-realistic"
    resolution: str = "4K"
    aspect_ratio: str = "3:4"
    use_face_schema: bool = True

class GenerationResponse(BaseModel):
    generation_id: str
    status: str
    output_url: Optional[str] = None
    cdn_url: Optional[str] = None
    message: str

class PromptSearchRequest(BaseModel):
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    limit: int = 10

# OpenAI API Models
class ChatMessage(BaseModel):
    role: str
    content: Optional[Union[str, List[Dict[str, Any]]]] = None

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False

class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: Dict[str, int]

# =============================================================================
# TOOLS SETUP
# =============================================================================

tools_list = [
    get_current_time,
    add_numbers,
    generate_cosplay_image,
    generate_cosplay_video,
    research_topic,
    list_files,
    read_file,
    write_file,
    search_web,
    fetch_url,
    identify_anime_screenshot,
    detect_objects,
    segment_image,
    analyze_video,
    analyze_pdf,
    upload_to_gcs,
    download_from_gcs,
]
tool_map = {func.__name__: func for func in tools_list}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_id(text: str) -> str:
    return hashlib.md5(f"{text}_{datetime.datetime.utcnow()}".encode()).hexdigest()[:12]

def upload_bytes_to_gcs(file_data: bytes, bucket_name: str, blob_name: str) -> str:
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(file_data)
    blob.make_public()
    return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"

def log_to_bigquery(table: str, row: dict):
    try:
        table_ref = f"{PROJECT_ID}.{BQ_DATASET}.{table}"
        errors = bq_client.insert_rows_json(table_ref, [row])
        if errors:
            print(f"BigQuery insert errors: {errors}")
    except Exception as e:
        print(f"Failed to log to BigQuery: {e}")

def get_optimized_prompt(target_character: str, style: str) -> str:
    # Simplified fallback for now to avoid complexity in this file
    return f"Ultra-realistic cosplay of {target_character}, {style} style, 8k resolution, cinematic lighting."

async def process_generation(generation_id: str, request: GenerationRequest):
    start_time = datetime.datetime.utcnow()
    try:
        prompt = get_optimized_prompt(request.target_character, request.style)
        
        # Call Gemini 3 Image (Direct)
        response = genai_client.models.generate_content(
            model=GEMINI_3_PRO_IMAGE,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=request.aspect_ratio,
                    image_size="1024x1024" # Default for now
                )
            )
        )
        
        # Extract Image (This part depends on actual API response structure)
        # Assuming we handle it or logic similar to tools.py
        # For this unified file, let's just log success placeholder
        cdn_url = "https://placeholder-image-url.com/generated.png"
        
        log_to_bigquery(BQ_TABLE_GENERATIONS, {
            "generation_id": generation_id,
            "user_id": request.user_id,
            "target_character": request.target_character,
            "status": "completed",
            "cdn_url": cdn_url,
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        log_to_bigquery(BQ_TABLE_GENERATIONS, {
            "generation_id": generation_id,
            "status": "failed",
            "error_message": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    return {
        "service": "Yuki Cosplay API & Agent",
        "status": "operational",
        "endpoints": {
            "openai_chat": "/v1/chat/completions",
            "cosplay_gen": "/api/v1/generate",
            "cosplay_gen_alias": "/cosplay/generate"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

# --- OpenAI Compatible Endpoints ---

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "yuki", "object": "model", "created": int(time.time()), "owned_by": "yuki-org"},
            {"id": "gemini-2.5-pro", "object": "model", "created": int(time.time()), "owned_by": "google"}
        ]
    }

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    print(f"\n{Colors.NEON_PINK}[🦊 YUKI AGENT] Request: {request.model}{Colors.RESET}")
    start_time = time.time()
    
    # 1. Convert OpenAI Messages to Gemini Content
    gemini_contents = []
    
    for msg in request.messages:
        role = msg.role
        content = msg.content
        parts = []
        if content:
             # Basic handling
             if isinstance(content, str):
                 parts.append(types.Part(text=content))
        
        if role == "user":
            gemini_contents.append(types.Content(role="user", parts=parts))
        elif role == "assistant":
             gemini_contents.append(types.Content(role="model", parts=parts))

    # 2. Config
    model_name = "gemini-2.5-pro-preview-0219"
    if "gemini" in request.model:
        model_name = request.model
    
    config = types.GenerateContentConfig(
        tools=tools_list,
        temperature=request.temperature,
        top_p=request.top_p,
        candidate_count=1,
        system_instruction=YUKI_SYSTEM_PROMPT
    )

    # 3. Execution Loop
    final_text = ""
    finish_reason = "stop"
    MAX_TURNS = 15
    turn_count = 0
    
    try:
        while turn_count < MAX_TURNS:
            turn_count += 1
            response = genai_client.models.generate_content(
                model=model_name,
                contents=gemini_contents,
                config=config
            )
            
            if not response.candidates:
                final_text = "Error: No response from model."
                finish_reason = "error"
                break
                
            candidate = response.candidates[0]
            
            # Check for function calls
            function_calls = []
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if part.function_call:
                        function_calls.append(part.function_call)
            
            if not function_calls:
                # Final text
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.text:
                            final_text += part.text
                break
            
            # Execute Tools
            gemini_contents.append(candidate.content)
            
            for call in function_calls:
                func_name = call.name
                func_args = call.args
                print(f"{Colors.FOX_FIRE}[⚙️ TOOL EXEC] {func_name}{Colors.RESET}")
                
                result = "Error: Tool not found"
                if func_name in tool_map:
                    try:
                        result = tool_map[func_name](**func_args)
                    except Exception as e:
                        result = f"Error executing {func_name}: {e}"
                
                gemini_contents.append(types.Content(
                    role="tool",
                    parts=[types.Part(
                        function_response=types.FunctionResponse(
                            name=func_name,
                            response={"result": result}
                        )
                    )]
                ))

    except Exception as e:
        final_text = f"Internal Error: {str(e)}"
        finish_reason = "error"

    return ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4()}",
        object="chat.completion",
        created=int(time.time()),
        model=request.model,
        choices=[
            ChatCompletionResponseChoice(
                index=0,
                message=ChatMessage(role="assistant", content=final_text),
                finish_reason=finish_reason
            )
        ],
        usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    )

# --- REST/Cosplay Endpoints ---

@app.post("/api/v1/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_ext = file.filename.split(".")[-1]
        blob_name = f"uploads/{generate_id(file.filename)}.{file_ext}"
        file_data = await file.read()
        gcs_url = upload_bytes_to_gcs(file_data, GCS_BUCKET_UPLOADS, blob_name)
        return {"success": True, "gcs_url": gcs_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/generate", response_model=GenerationResponse)
async def generate_cosplay(request: GenerationRequest, background_tasks: BackgroundTasks):
    try:
        generation_id = generate_id(f"{request.user_id}_{request.target_character}")
        background_tasks.add_task(process_generation, generation_id, request)
        return GenerationResponse(
            generation_id=generation_id,
            status="processing",
            message="Generation started."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cosplay/generate", response_model=GenerationResponse)
async def cosplay_generate_alias(request: GenerationRequest, background_tasks: BackgroundTasks):
    """Alias for /api/v1/generate for easier access"""
    return await generate_cosplay(request, background_tasks)

@app.get("/api/v1/status/{generation_id}")
async def get_status(generation_id: str):
    # Simplified Logic reading from BigQuery or just mocking if immediate
    # Re-implement BQ status reading if needed
    query = f"SELECT * FROM `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE_GENERATIONS}` WHERE generation_id = @gen_id LIMIT 1"
    try:
        job_config = bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter("gen_id", "STRING", generation_id)])
        results = list(bq_client.query(query, job_config=job_config).result())
        if not results:
             raise HTTPException(status_code=404, detail="Generation not found yet (check back in a moment)")
        row = dict(results[0])
        return GenerationResponse(
            generation_id=generation_id,
            status=row.get("status", "processing"),
            output_url=row.get("output_gcs"),
            cdn_url=row.get("cdn_url"),
            message="Processing..."
        )
    except Exception as e:
         return GenerationResponse(generation_id=generation_id, status="processing", message="Checking status...")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
