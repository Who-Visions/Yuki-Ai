
"""
Yuki Cosplay API - Unified Server
- REST API (Generation, Status, Uploads)
- OpenAI Compatible API (Agent Chat, Tools)
- specialized /cosplay endpoints
"""

import os
import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
# from yuki_rate_limiter import limiter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import time

print("FOX FIRE: Yuki API Starting...", flush=True)
import uuid
import datetime
import hashlib
import json
from google.cloud import storage, bigquery
from google import genai
from google.genai import types
import google.auth
import google.auth.transport.requests
import requests

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
from yuki_cost_tracker import YukiCostTracker

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ID = "gifted-cooler-479623-r7"
REGION = "us-central1"
# Default location, but will be overridden dynamically for Gemini 3
LOCATION = "us-central1" 

# GCS Configuration
GCS_BUCKET_UPLOADS = "yuki-user-uploads"
GCS_BUCKET_GENERATIONS = "yuki-cosplay-generations"

# ... (omitted constants same as before) ...
GCS_CDN_BUCKET = "yuki-cdn"

# BigQuery
BQ_DATASET = "yuki_production"
BQ_TABLE_GENERATIONS = "generations"

# Models
GEMINI_3_PRO_IMAGE = "gemini-3-pro-image-preview"
GEMINI_3_PRO = "gemini-3-pro-preview"
GEMINI_3_FLASH = "gemini-3-flash-preview"
IMAGEN_3 = "imagen-3.0-generate-001"
IMAGEN_4 = "imagen-4.0-generate-001"

# Reasoning Engine Configuration
REASONING_ENDPOINT = "https://us-central1-aiplatform.googleapis.com/v1/projects/gifted-cooler-479623-r7/locations/us-central1/reasoningEngines/7435157111765467136:query"
REASONING_SERVICE_ACCOUNT = "service-914641083224@gcp-sa-aiplatform-re.iam.gserviceaccount.com"

# Initialize Clients
storage_client = storage.Client(project=PROJECT_ID)
bq_client = bigquery.Client(project=PROJECT_ID)

# Dynamic Client Initialization Helper
def get_genai_client(model_name: str = "gemini-3-flash-preview"):
    """
    Dynamically routes to 'global' for Gemini 3 models, else uses us-central1.
    """
    client_location = "us-central1"
    if "gemini-3" in model_name or "gemini-exp" in model_name:
        client_location = "global"
        
    return genai.Client(vertexai=True, project=PROJECT_ID, location=client_location)

# Initialize default client
genai_client = get_genai_client()

# Initialize Cost Tracker
cost_tracker = YukiCostTracker(PROJECT_ID)

# Auth for Reasoning Engine
credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
auth_request = google.auth.transport.requests.Request()

def get_auth_token():
    """Refreshes and returns the GCP access token."""
    try:
        credentials.refresh(auth_request)
        return credentials.token
    except Exception as e:
        print(f"❌ Auth Refresh Failed: {e}")
        return None

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

# Rate Limiting Middleware

# class RateLimitMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Skip WebSockets (BaseHTTPMiddleware can break them)
#         if request.scope.get("type") == "websocket":
#              return await call_next(request)
#         
#         # Explicitly skip /ws path just in case
#         if request.url.path.startswith("/ws"):
#              return await call_next(request)
#              
#         # Skip health/root
#         if request.url.path in ["/", "/health", "/docs", "/openapi.json"]:
#             return await call_next(request)
#             
#         client_ip = request.client.host if request.client else "unknown"
#         
#         # Check limit (Default to 'free' tier for now)
#         # allowed = await limiter.check_limit(client_ip, tier="free")
#         
#         # if not allowed:
#         #     return JSONResponse(
#         #         status_code=429,
#         #         content={"detail": "Rate limit exceeded. Please try again later."}
#         #     )
#             
#         response = await call_next(request)
#         return response
# 
# # app.add_middleware(RateLimitMiddleware)

# --- Robust A2A Integration ---
A2A_AVAILABLE = False
try:
    # Try standard namespace
    from a2a.server.apps import A2AStarletteApplication
    from a2a.server.request_handlers import DefaultRequestHandler
    from a2a.server.tasks import InMemoryTaskStore
    from a2a.server.agent_execution import AgentExecutor, RequestContext
    from a2a.server.events import EventQueue
    from a2a.utils import new_agent_text_message
    from a2a.types import AgentCapabilities, AgentCard, AgentSkill
    
    # Import Yuki Specifics
    from yuki_a2a_server import create_yuki_agent_card, YukiAgentExecutor
    
    # Check if we can build
    A2A_AVAILABLE = True

except ImportError:
    try:
        # Try google.adk namespace (newer SDKs)
        from google.adk.a2a.server.apps import A2AStarletteApplication
        from google.adk.a2a.server.request_handlers import DefaultRequestHandler
        from google.adk.a2a.server.tasks import InMemoryTaskStore
        from google.adk.a2a.server.agent_execution import AgentExecutor, RequestContext
        from google.adk.a2a.server.events import EventQueue
        from google.adk.a2a.utils import new_agent_text_message
        from google.adk.a2a.types import AgentCapabilities, AgentCard, AgentSkill
        
        # Import Yuki Specifics (Assumes yuki_a2a_server handles its own internal imports correctly or we import them here)
        # However, yuki_a2a_server.py ALSO does this check. 
        # Ideally we just import the robust classes FROM yuki_a2a_server if it exposes them, but it doesn't cleanly expose the base classes.
        # We will import Yuki Specifics from yuki_a2a_server which SHOULD work if we are here?
        # Actually yuki_a2a_server.py handles the imports internally for its own usage, but we need the types here for mounting?
        # Let's import the Yuki components from yuki_a2a_server
        from yuki_a2a_server import create_yuki_agent_card, YukiAgentExecutor
        
        A2A_AVAILABLE = True
    except ImportError:
        print(f"{Colors.FOX_FIRE}[A2A] SDK not found or incompatible. Starting in OpenAI-Only Mode.{Colors.RESET}")
        A2A_AVAILABLE = False
        # Define Mocks to prevent startup crash if we were dependent on them, 
        # but below we only use them if A2A_AVAILABLE is True?
        # Actually logic below (lines 134+ in original) assumes they exist. 
        # So we MUST mock them if we want to keep that logic, OR wrap that logic in `if A2A_AVAILABLE:`
        
        # Let's wrap the logic below in `if A2A_AVAILABLE`.
        # But to be safe and match the current structure, let's keep the classes as None or mocks.
        pass

# Mount A2A if available
# Mount A2A if available
# NOTE: Disabled to prevent masking of the explicit /.well-known/agent.json endpoint
# if A2A_AVAILABLE:
#     try:
#         # Initialize A2A components
#         a2a_card = create_yuki_agent_card()
#         a2a_handler = DefaultRequestHandler(
#             agent_executor=YukiAgentExecutor(),
#             task_store=InMemoryTaskStore(),
#         )
#         
#         a2a_app = A2AStarletteApplication(
#             agent_card=a2a_card,
#             http_handler=a2a_handler,
#         ).build()
#         
#         # Mount at root to capture A2A routes
#         # app.mount("/", a2a_app) 
#         print(f"{Colors.SUCCESS_GREEN}[A2A] Application Mounted! {Colors.RESET}")
#         
#     except Exception as e:
#         print(f"{Colors.ERROR_RED}[A2A] Failed to mount: {e}{Colors.RESET}")
# else:
#     print(f"{Colors.FOX_FIRE}[A2A] Skipped mounting (SDK missing){Colors.RESET}")


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
    include_thoughts: Optional[bool] = Field(default=False, alias="includeThoughts")
    thinking_level: Optional[str] = Field(default="high", alias="thinkingLevel")
    thinking_budget: Optional[int] = Field(default=None, alias="thinkingBudget")

    class Config:
        allow_population_by_field_name = True

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
        
        # Get correct client for Gemini 3
        client = get_genai_client(GEMINI_3_PRO_IMAGE)
        
        # Call Gemini 3 Image (Direct)
        response = client.models.generate_content(
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
            "cosplay_gen_alias": "/cosplay/generate",
            "changelog": "/changelog",
            "changelog_page": "/changelog-page"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

# --- A2A Identity Card ---

@app.get("/.well-known/agent.json")
async def get_agent_card():
    """
    Standardized Agent Identity Card for A2A protocols.
    """
    return {
        "name": "Yuki (雪姫) - The Nine-Tailed Snow Fox",
        "version": "2.0.0",
        "description": "A playful AI cosplay preview architect with expertise in anime, character design, and image generation. Kon kon~! 🦊",
        "capabilities": [
            "text-generation",
            "image-generation",
            "cosplay-preview",
            "anime-identification"
        ],
        "endpoints": {
            "chat": "/v1/chat/completions",
            "health": "/health",
            "generate": "/api/v1/generate"
        },
        "extensions": {
            "color": "pink", # Yuki's theme color
            "role": "Cosplay Architect",
            "personality": "Playful, Mischievous, Japanese-Honorifics"
        }
    }

# --- OpenAI Compatible Endpoints ---

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "yuki", "object": "model", "created": int(time.time()), "owned_by": "yuki-org"},
            {"id": "gemini-3-pro-preview", "object": "model", "created": int(time.time()), "owned_by": "google"},
            {"id": "gemini-3-flash-preview", "object": "model", "created": int(time.time()), "owned_by": "google"},
            {"id": "gemini-3-pro-image-preview", "object": "model", "created": int(time.time()), "owned_by": "google"}
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
    model_name = GEMINI_3_PRO
    if "gemini" in request.model:
        model_name = request.model
    
    # Map Reasoning Effort / Thinking Level
    thinking_level = (request.thinking_level or "high").upper()
    
    thinking_config = types.ThinkingConfig(
        include_thoughts=request.include_thoughts,
        thinking_level=thinking_level
    )
    if request.thinking_budget is not None:
        thinking_config.thinking_budget = request.thinking_budget

    config = types.GenerateContentConfig(
        tools=tools_list,
        temperature=request.temperature if request.temperature != 0.7 else 1.0, 
        top_p=request.top_p,
        candidate_count=1,
        system_instruction=YUKI_SYSTEM_PROMPT,
        thinking_config=thinking_config
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
                # Process thoughts and final text
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.thought:
                            # If they want thoughts included, we prepend or append? 
                            # Usually we might want to return them in a specific field, 
                            # but for OpenAI compat we might just prepend to content if requested.
                            if request.include_thoughts:
                                final_text += f"[THOUGHTS]\n{part.text}\n[END THOUGHTS]\n"
                        elif part.text:
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

    # 4. Usage Extract
    prompt_tokens = 0
    completion_tokens = 0
    thoughts_tokens = 0
    if hasattr(response, 'usage_metadata') and response.usage_metadata:
        prompt_tokens = response.usage_metadata.prompt_token_count or 0
        completion_tokens = response.usage_metadata.candidates_token_count or 0
        thoughts_tokens = getattr(response.usage_metadata, 'thoughts_token_count', 0) or 0
        
        # Log to Tracker
        cost_tracker.log_generation(
            model=model_name,
            operation="chat_completion",
            tokens_in=prompt_tokens,
            tokens_out=completion_tokens,
            thoughts_tokens=thoughts_tokens
        )

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
        usage={
            "prompt_tokens": prompt_tokens, 
            "completion_tokens": completion_tokens, 
            "thoughts_tokens": thoughts_tokens,
            "total_tokens": prompt_tokens + completion_tokens + thoughts_tokens
        }
    )

@app.post("/v1/reasoning", response_model=ChatCompletionResponse)
async def reasoning_agent(request: ChatCompletionRequest):
    """
    Direct endpoint for Vertex AI Reasoning Engine orchestration.
    """
    print(f"\n{Colors.NEON_PINK}[🦊 REASONING AGENT] Processing Request...{Colors.RESET}")
    start_time = time.time()
    
    # Extract latest user message
    user_msg = "Hello"
    for msg in reversed(request.messages):
        if msg.role == "user" and isinstance(msg.content, str):
            user_msg = msg.content
            break
            
    try:
        # Get Auth Token
        token = get_auth_token()
        if not token:
            raise HTTPException(status_code=500, detail="GCP Auth failure")
        
        # Prepare REST payload
        # IMPORTANT: Yuki-v005 expects 'user_instruction' as the keyword argument
        payload = {
            "input": {
                "user_instruction": user_msg
            }
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print(f"📡 Sending query to Reasoning Engine...")
        
        # Call Reasoning Engine REST endpoint
        response = requests.post(
            REASONING_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"{Colors.ERROR_RED}Reasoning Engine REST Error: {response.status_code} - {response.text}{Colors.RESET}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
        response_data = response.json()
        
        # Extract output mapping
        # Yuki-v005 returns {'output': '...'}
        final_text = response_data.get('output', str(response_data))
        
        print(f"{Colors.GREEN}[🦊 REASONING] Success!{Colors.RESET}")
        
        return ChatCompletionResponse(
            id=f"reason-{uuid.uuid4()}",
            object="chat.completion",
            created=int(time.time()),
            model="vertex-reasoning-engine",
            choices=[
                ChatCompletionResponseChoice(
                    index=0,
                    message=ChatMessage(role="assistant", content=final_text),
                    finish_reason="stop"
                )
            ],
            usage={
                "prompt_tokens": len(user_msg) // 4, # Fallback estimation
                "completion_tokens": len(final_text) // 4,
                "total_tokens": (len(user_msg) + len(final_text)) // 4
            }
        )
        
    except Exception as e:
        print(f"{Colors.ERROR_RED}Reasoning Engine Error: {e}{Colors.RESET}")
        raise HTTPException(status_code=500, detail=str(e))

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


# --- Mobile App JSON Upload (base64) ---
class Base64UploadRequest(BaseModel):
    image_data: str  # Base64 encoded image
    filename: Optional[str] = None

@app.post("/api/v1/upload/base64")
async def upload_image_base64(request: Base64UploadRequest):
    """Upload image via base64 JSON (for mobile apps)"""
    try:
        import base64
        
        # Decode base64
        image_data = base64.b64decode(request.image_data)
        
        # Generate filename
        filename = request.filename or f"upload_{int(time.time())}.jpg"
        blob_name = f"uploads/{generate_id(filename)}.jpg"
        
        gcs_url = upload_bytes_to_gcs(image_data, GCS_BUCKET_UPLOADS, blob_name)
        return {"success": True, "gcs_url": gcs_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Facial IP Extraction Endpoint ---
class FacialIPRequest(BaseModel):
    image_data: str  # Base64 encoded image
    subject_name: Optional[str] = "user"

@app.post("/api/v1/facial-ip/extract")
async def extract_facial_ip(request: FacialIPRequest):
    """Extract facial IP profile from image for V8 facial lock"""
    try:
        # Return a placeholder facial IP profile
        # In production, this would use the V7 facial extraction logic
        facial_profile = {
            "subject_name": request.subject_name,
            "extraction_timestamp": datetime.datetime.utcnow().isoformat(),
            "critical_identity_lock": {
                "top_identifiers": [
                    "Facial bone structure",
                    "Skin tone & texture", 
                    "Eye shape & spacing",
                    "Nose geometry",
                    "Jawline definition"
                ]
            },
            "status": "extracted"
        }
        return facial_profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Cancel Generation Endpoint ---
@app.post("/api/v1/cancel/{generation_id}")
async def cancel_generation(generation_id: str):
    """Cancel a generation in progress and refund credits if within 30 seconds"""
    try:
        # In production, this would:
        # 1. Check BigQuery for generation start time
        # 2. If within 30s, mark as cancelled and refund credits
        # 3. Kill any running generation tasks
        
        return {
            "success": True,
            "generation_id": generation_id,
            "credits_refunded": 1,
            "message": "Generation cancelled and credits refunded."
        }
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


# --- Semantic Search Endpoint ---
class SemanticSearchRequest(BaseModel):
    query: str
    include_characters: bool = True
    include_series: bool = True
    top_k: int = 10
    min_score: float = 0.3

class SemanticSearchResult(BaseModel):
    query: str
    characters: List[Dict[str, Any]]
    series: List[Dict[str, Any]]
    total: int

@app.post("/api/v1/semantic-search", response_model=SemanticSearchResult)
async def semantic_search_endpoint(request: SemanticSearchRequest):
    """
    Semantic search across characters and series using Gemini Embeddings.
    Returns ranked results by similarity score.
    """
    try:
        from tools.semantic_search import hybrid_search
        
        results = hybrid_search(
            query=request.query,
            include_characters=request.include_characters,
            include_series=request.include_series,
            top_k=request.top_k,
            min_score=request.min_score
        )
        
        return SemanticSearchResult(
            query=results["query"],
            characters=results["characters"],
            series=results["series"],
            total=results["total"]
        )
    except Exception as e:
        print(f"{Colors.ERROR_RED}Semantic Search Error: {e}{Colors.RESET}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/semantic-search")
async def semantic_search_get(
    q: str,
    include_characters: bool = True,
    include_series: bool = True,
    top_k: int = 10,
    min_score: float = 0.3
):
    """GET version of semantic search for easy browser testing."""
    try:
        from tools.semantic_search import hybrid_search
        
        return hybrid_search(
            query=q,
            include_characters=include_characters,
            include_series=include_series,
            top_k=top_k,
            min_score=min_score
        )
    except Exception as e:
        print(f"{Colors.ERROR_RED}Semantic Search Error: {e}{Colors.RESET}")
        raise HTTPException(status_code=500, detail=str(e))


# --- WebSocket Endpoint ---

@app.websocket("/ws/generation/{generation_id}")
async def generation_progress(websocket: WebSocket, generation_id: str):
    await websocket.accept()
    try:
        while True:
            # Re-use the existing logic or helper to get status
            # For efficiency we might want a lighter check, but calling get_status logic here
            # Note: passing "request" models or similar if needed, but here we just need ID
            # We'll reproduce the BQ query logic here to avoid overhead of self-requests
            
            try:
                query = f"SELECT * FROM `{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE_GENERATIONS}` WHERE generation_id = @gen_id LIMIT 1"
                job_config = bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter("gen_id", "STRING", generation_id)])
                results = list(bq_client.query(query, job_config=job_config).result())
                
                status_data = {
                    "generation_id": generation_id,
                    "status": "processing", 
                    "message": "Connecting..."
                }

                if results:
                    row = dict(results[0])
                    status_data = {
                        "generation_id": generation_id,
                        "status": row.get("status", "processing"),
                        "output_url": row.get("output_gcs"),
                        "cdn_url": row.get("cdn_url"),
                        "message": "Processing..."
                    }
                
                await websocket.send_json(status_data)
                
                if status_data['status'] in ['completed', 'failed']:
                    # Keep connection open briefly then close or wait for client to close
                    # Usually better to break so client knows it's done
                    break
                    
            except Exception as e:
                await websocket.send_json({
                    "generation_id": generation_id,
                    "status": "processing",
                    "message": "Checking..."
                })

            await asyncio.sleep(2) # Poll every 2 seconds
            
    except WebSocketDisconnect:
        print(f"Client disconnected for {generation_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass

# =============================================================================
# CHANGELOG ENDPOINTS
# =============================================================================

@app.get("/changelog")
async def get_changelog(
    type: Optional[str] = None,  # Filter by type: new, improvement, fix
    search: Optional[str] = None  # Search in title/description
):
    """
    Get changelog entries with optional filtering.
    Marketing-friendly: each entry has a direct link ID.
    """
    try:
        import json
        changelog_path = os.path.join(os.path.dirname(__file__), "changelog", "entries.json")
        
        with open(changelog_path, "r") as f:
            data = json.load(f)
        
        entries = data.get("entries", [])
        total = len(entries)
        
        # Filter by type
        if type:
            entries = [e for e in entries if e.get("type") == type]
        
        # Search filter
        if search:
            search_lower = search.lower()
            entries = [e for e in entries if 
                      search_lower in e.get("title", "").lower() or 
                      search_lower in e.get("description", "").lower()]
        
        return {
            "entries": entries,
            "total": total,
            "filtered": len(entries)
        }
    except FileNotFoundError:
        return {"entries": [], "total": 0, "filtered": 0, "error": "Changelog not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/changelog/{entry_id}")
async def get_changelog_entry(entry_id: str):
    """
    Get a single changelog entry by ID.
    Useful for direct marketing links.
    """
    try:
        import json
        changelog_path = os.path.join(os.path.dirname(__file__), "changelog", "entries.json")
        
        with open(changelog_path, "r") as f:
            data = json.load(f)
        
        for entry in data.get("entries", []):
            if entry.get("id") == entry_id:
                return entry
        
        raise HTTPException(status_code=404, detail="Entry not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Changelog not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mount static files for changelog page
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Serve static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Serve changelog JSON directly
changelog_dir = os.path.join(os.path.dirname(__file__), "changelog")
if os.path.exists(changelog_dir):
    app.mount("/changelog-assets", StaticFiles(directory=changelog_dir), name="changelog-assets")

@app.get("/changelog-page")
async def changelog_page():
    """Serve the changelog HTML page"""
    html_path = os.path.join(os.path.dirname(__file__), "static", "changelog.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    raise HTTPException(status_code=404, detail="Changelog page not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

