import os
import shutil
import asyncio
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import subprocess
import uvicorn
import logging
from typing import Optional, Dict, Any, List, Union, Literal
import base64
import time
import uuid

# Early Cloud detection
IS_CLOUD = os.getenv("K_SERVICE") is not None

# Optional: Load .env for local dev
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YukiServer")

# Conditional heavy imports
YukiAgent = None
tools_imports_ok = False

try:
    from google import genai
    from google.genai import types
    logger.info("GenAI SDK imported successfully")
except ImportError as e:
    logger.error(f"Failed to import GenAI SDK: {e}")
    genai = None
    types = None

try:
    from yuki_local import YUKI_SYSTEM_PROMPT, Colors
    logger.info("yuki_local imported successfully")
except Exception as e:
    logger.warning(f"Could not import yuki_local: {e}")
    YUKI_SYSTEM_PROMPT = "You are Yuki, a helpful AI assistant."
    class Colors:
        ICE_BLUE = FOX_FIRE = NEON_PINK = ERROR_RED = RESET = ""

try:
    from yuki_tools import (
        get_current_time, add_numbers, generate_cosplay_image, generate_cosplay_video,
        research_topic, list_files, read_file, write_file, search_web, fetch_url,
        identify_anime_screenshot, detect_objects, segment_image, analyze_video,
        analyze_pdf, upload_to_gcs, download_from_gcs,
    )
    tools_imports_ok = True
    logger.info("yuki_tools imported successfully")
except Exception as e:
    logger.warning(f"Could not import yuki_tools: {e}")
    # Define stub functions
    def get_current_time(): return "Tool not available"
    def add_numbers(a, b): return a + b
    generate_cosplay_image = generate_cosplay_video = research_topic = None
    list_files = read_file = write_file = search_web = fetch_url = None
    identify_anime_screenshot = detect_objects = segment_image = None
    analyze_video = analyze_pdf = upload_to_gcs = download_from_gcs = None

if not IS_CLOUD:
    try:
        from agent import YukiAgent
        import sqlite3
    except ImportError as e:
        logger.warning(f"Could not import local modules: {e}")

app = FastAPI()

# Allow Expo/Localhost access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration (IS_CLOUD defined at top of file)
GCS_BUCKET = "yuki-ai-assets"  # For reference images and cache

if IS_CLOUD:
    INPUT_DIR = "/tmp/inputs"
    OUTPUT_DIR = "/tmp/outputs"
    SCRIPT_PATH = "/app/image_gen/v12_pipeline.py"  # Bundled in Docker image
    REF_DIR = "/tmp/subjects"  # Downloaded from GCS on demand
    CACHE_DIR = "/tmp/cache/cloud_vision"
else:
    INPUT_DIR = r"C:\Yuki_Local\Inputs"
    OUTPUT_DIR = r"C:\Yuki_Local\Cosplay_Lab\Renders\Server_Output"
    SCRIPT_PATH = r"C:\Yuki_Local\image_gen\v14_pipeline.py"
    REF_DIR = r"C:\Yuki_Local\Cosplay_Lab\Subjects"
    CACHE_DIR = r"C:\Yuki_Local\cache\cloud_vision"

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"
RE_ID = "projects/914641083224/locations/us-central1/reasoningEngines/8949824538980384768"

# Ensure directories exist (graceful failure for Cloud Run)
try:
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(REF_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
except Exception as e:
    logger.warning(f"Could not create directories: {e}")

# Initialize Agent (Skip on Cloud Run - not needed for chat API)
yuki_agent = None
if not IS_CLOUD:
    logger.info("Initializing Yuki Agent (Gemini 3)...")
    try:
        yuki_agent = YukiAgent(
            model="gemini-3-pro-preview",
            tools=[get_current_time, add_numbers],
            project=PROJECT_ID,
            location="global",
        )
        yuki_agent.set_up()
        logger.info("Yuki Agent initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Yuki Agent: {e}")
        yuki_agent = None
else:
    logger.info("Cloud Run mode: Skipping YukiAgent (using GenAI Client only)")

# Initialize GenAI Client for /v1/chat/completions
logger.info("Initializing GenAI Client...")
try:
    api_key = os.getenv("YUKI_API_KEY")
    if api_key:
        # 🔑 API Key mode (Don't provide project/location as they are for Vertex mode)
        genai_client = genai.Client(api_key=api_key)
        logger.info("Found YUKI_API_KEY, using for authentication.")
    else:
        # ☁️ Vertex AI mode
        genai_client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location="global",
        )
        logger.info("No API key found, falling back to Vertex AI default auth.")
    logger.info("GenAI Client initialized.")
except Exception as e:
    logger.error(f"Failed to initialize GenAI Client: {e}")
    genai_client = None

# Tool Definitions for GenAI
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

# Structured Output Models
class YukiResponse(BaseModel):
    thought: str = Field(description="Your internal reasoning about the cosplay architect process.")
    message: str = Field(description="Clear, encouraging message to the user.")
    action: Literal["chat", "generate", "ask_for_photo", "refuse"] = Field(description="The logical next step.")
    refined_prompt: Optional[str] = Field(description="Engine-optimized prompt (Imagen 3 style) if action is 'generate'.", default=None)

# OpenAI Compatible Models
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
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    reasoning_effort: Optional[str] = Field(default=None, alias="reasoningEffort")
    thinking_level: Optional[str] = Field(default=None, alias="thinkingLevel")
    include_thoughts: Optional[bool] = Field(default=False, alias="includeThoughts")
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

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    metadata: Optional[Dict[str, Any]] = None

# GCS Helper for downloading reference images
def download_reference_from_gcs(character_name: str) -> Optional[str]:
    """Download a character reference image from GCS to local /tmp."""
    try:
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)
        
        # Try to find matching reference
        prefix = "subjects/"
        blobs = list(bucket.list_blobs(prefix=prefix))
        
        for blob in blobs:
            if character_name.lower().replace(" ", "_") in blob.name.lower():
                local_path = os.path.join(REF_DIR, os.path.basename(blob.name))
                if not os.path.exists(local_path):
                    blob.download_to_filename(local_path)
                    logger.info(f"Downloaded reference: {blob.name} -> {local_path}")
                return local_path
        
        # Default fallback
        default_ref = "subjects/top15_10_Ichigo_Kurosaki_4k.png"
        local_path = os.path.join(REF_DIR, "top15_10_Ichigo_Kurosaki_4k.png")
        if not os.path.exists(local_path):
            blob = bucket.blob(default_ref)
            if blob.exists():
                blob.download_to_filename(local_path)
                logger.info(f"Downloaded default reference: {default_ref}")
        return local_path if os.path.exists(local_path) else None
        
    except Exception as e:
        logger.error(f"GCS download failed: {e}")
        return None

async def run_generation_script(input_path: str, prompt: str, request_id: str):
    """
    Executes the existing v12 generation pipeline as a subprocess.
    """
    logger.info(f"Starting generation for {request_id} with prompt: {prompt}")
    
    # Try to find a reference image based on character in prompt
    # Default to Ichigo if we can't find one.
    ref_image = os.path.join(REF_DIR, "top15_10_Ichigo_Kurosaki_4k.png")
    character_name = "Ichigo Kurosaki"
    
    # Basic heuristic to match character from prompt
    for filename in os.listdir(REF_DIR):
        if filename.endswith(".png"):
            # e.g. top15_01_Luffy_4k.png -> luffy
            char_part = filename.split('_')[2].lower()
            if char_part in prompt.lower():
                ref_image = os.path.join(REF_DIR, filename)
                character_name = filename.split('_')[2].replace('_', ' ')
                break

    try:
        # v12_pipeline.py arguments: --name --character --subject_dir --ref --output
        subject_dir = os.path.dirname(input_path)
        
        process = await asyncio.create_subprocess_exec(
            "python", SCRIPT_PATH,
            "--name", "User_Upload",
            "--character", character_name,
            "--subject_dir", subject_dir,
            "--ref", ref_image,
            "--output", OUTPUT_DIR,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ, "YUKI_INPUT_IMAGE": input_path, "YUKI_USER_EMAIL": "whoentertains@gmail.com"}
        )
        
        stdout, stderr = await process.communicate()
        
        if stdout:
            logger.info(f"[Script Output]: {stdout.decode()}")
        if stderr:
            logger.error(f"[Script Error]: {stderr.decode()}")
            
        logger.info(f"Generation complete for {request_id}")
        
    except Exception as e:
        logger.error(f"Failed to run script: {e}")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Fallback to GenAI Client if Agent is not initialized (Cloud Run Mode)
    if not yuki_agent:
        if not genai_client:
            raise HTTPException(status_code=503, detail="Service Unavailable: Neither Yuki Agent nor GenAI Client initialized.")
        
        try:
            logger.info(f"☁️ [Cloud Mode] Using GenAI Client for chat: {request.message}")
            # Use Gemini 3 Flash for fast, lightweight responses in Cloud Mode
            response = genai_client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=request.message,
                config=types.GenerateContentConfig(
                    system_instruction=YUKI_SYSTEM_PROMPT,
                    temperature=0.7
                )
            )
            return ChatResponse(response=response.text)
        except Exception as e:
            logger.error(f"GenAI Fallback failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Standard Local/Full Agent Mode
    try:
        logger.info(f"Received chat message: {request.message}")
        
        # Invoke the agent asynchronously
        # Expected output from LangGraph agent is typically a dict with 'messages' or 'output'
        result = await yuki_agent.async_query(
            messages=[{"role": "user", "content": request.message}]
        )
        
        # Parse result - assuming standard LangGraph React Agent output structure
        # The output usually contains the full conversation history. We want the last AI message.
        messages = result.get("messages", [])
        if messages:
            last_message = messages[-1]
            response_text = last_message.content
        else:
            response_text = "I'm not sure what to say."

        return ChatResponse(response=response_text)
        
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "yuki",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "yuki-org",
            },
            {
                "id": "gemini-3-pro-preview",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "google",
            }
        ]
    }

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    if not genai_client:
        raise HTTPException(status_code=503, detail="GenAI Client is not initialized")

    print(f"\n{Colors.NEON_PINK}[🦊 YUKI SERVER] Request received for model: {request.model}{Colors.RESET}")
    
    # 1. Convert OpenAI Messages to Gemini Content
    gemini_contents = []
    last_gemini_role = None

    for msg in request.messages:
        if msg.role == "system":
            continue
            
        role = msg.role
        content = msg.content
        parts = []

        if isinstance(content, str) and content.strip():
            parts.append(types.Part(text=content))
        elif isinstance(content, list):
            for item in content:
                if item.get("type") == "text" and item.get("text", "").strip():
                    parts.append(types.Part(text=item["text"]))
                elif item.get("type") == "image_url":
                    url = item["image_url"]["url"]
                    if url.startswith("data:image"):
                        try:
                            # Robust decoding with header check
                            header, encoded = url.split(",", 1)
                            image_bytes = base64.b64decode(encoded)
                            mime = "image/png" if "png" in header else ("image/webp" if "webp" in header else "image/jpeg")
                            parts.append(types.Part.from_bytes(data=image_bytes, mime_type=mime))
                        except Exception as e:
                            logger.error(f"Image decode fatal error: {e}")
                    else:
                        parts.append(types.Part(text=f"[Reference Image URL: {url}]"))

        if not parts:
            continue

        gemini_role = "user" if role == "user" else "model"
        
        # 🛡️ ROLE ALTERNATION GUARD
        if last_gemini_role == gemini_role:
            gemini_contents[-1].parts.extend(parts)
            logger.debug(f"Merged identical role turn: {gemini_role}")
        else:
            if not gemini_contents and gemini_role == "model":
                logger.warning("Intercepted leading model message; skipping to satisfy User-first requirement.")
                continue
            
            gemini_contents.append(types.Content(role=gemini_role, parts=parts))
            last_gemini_role = gemini_role

    if not gemini_contents:
        gemini_contents.append(types.Content(role="user", parts=[types.Part(text="Hello Yuki!")]))

    # Log Sequence
    logger.info(f"🚀 Dispatching Gemini Request: {len(gemini_contents)} turns | roles: {[c.role for c in gemini_contents]}")

    # 2. Configure Generation
    is_yuki = "yuki" in request.model.lower()
    model_name = "gemini-3-flash-preview"
    if request.model and "gemini" in request.model and "yuki" not in request.model:
        model_name = request.model
    
    thinking_level = (request.thinking_level or request.reasoning_effort or "medium").upper()
    
    thinking_config = types.ThinkingConfig(
        include_thoughts=request.include_thoughts,
        thinking_level=thinking_level
    )
    if request.thinking_budget is not None:
        thinking_config.thinking_budget = request.thinking_budget

    gen_config = {
        "tools": tools_list,
        "temperature": request.temperature if request.temperature != 0.7 else 1.0, 
        "top_p": request.top_p,
        "candidate_count": 1,
        "system_instruction": YUKI_SYSTEM_PROMPT,
    }
    
    # Enable thinking/reasoning if applicable
    if "pro" in model_name.lower() and not is_yuki:
        gen_config["thinking_config"] = thinking_config

    # Apply Structured Output for Yuki
    if is_yuki:
        gen_config["response_mime_type"] = "application/json"
        gen_config["response_json_schema"] = YukiResponse.model_json_schema()
        logger.info("Enabling Structured Output (YukiResponse)")

    config = types.GenerateContentConfig(**gen_config)

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
                finish_reason = "error"
                final_text = "Error: No response from the model."
                break
                
            candidate = response.candidates[0]
            
            # 🛡️ Protection: Skip empty contents
            if not candidate.content or not candidate.content.parts:
                logger.warning(f"Model returned empty content. Finish reason: {candidate.finish_reason}")
                if not final_text:
                    if is_yuki:
                        final_text = '{"thought": "Safety triggered", "message": "I hit a snag. Let\'s try a different vibe.", "action": "chat"}'
                    else:
                        final_text = "I hit a safety filter or a limit."
                break

            function_calls = []
            for part in candidate.content.parts:
                if part.function_call:
                    function_calls.append(part.function_call)
            
            if not function_calls:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.thought:
                            if request.include_thoughts:
                                final_text += f"[THOUGHTS]\n{part.text}\n[END THOUGHTS]\n"
                        elif part.text:
                            final_text += part.text
                break
            
            gemini_contents.append(candidate.content)
            
            for call in function_calls:
                func_name = call.name
                func_args = call.args
                print(f"{Colors.FOX_FIRE}[⚙️ TOOL EXEC] {func_name}{Colors.RESET}")
                
                if func_name in tool_map:
                    try:
                        result = tool_map[func_name](**func_args)
                    except Exception as e:
                        result = f"Error executing {func_name}: {e}"
                else:
                    result = f"Error: Tool {func_name} not found."

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
        logger.error(f"Error in generation: {e}")
        final_text = f"Internal Error: {str(e)}"
        finish_reason = "error"

    # 4. Construct Response
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

@app.post("/generate")
async def generate_cosplay(background_tasks: BackgroundTasks, file: UploadFile = File(...), prompt: str = "Ichigo Kurosaki"):
    """
    Generate cosplay image using V14 Pipeline.
    Cloud Run: Runs V14 pipeline synchronously
    Local: Uses v14 pipeline via subprocess
    """
    import base64
    from pathlib import Path
    
    try:
        # Read the uploaded file
        content = await file.read()
        logger.info(f"Received file: {file.filename}, size: {len(content)} bytes, prompt: {prompt}")
        
        # Save uploaded file
        timestamp = int(time.time())
        safe_filename = file.filename.rsplit('.', 1)[0] + ".jpg" # Force .jpg extension
        filename = f"u_{timestamp}_{safe_filename}"
        subject_dir = os.path.join(INPUT_DIR, f"sub_{timestamp}")
        os.makedirs(subject_dir, exist_ok=True)
        
        file_location = os.path.join(subject_dir, filename)
        with open(file_location, "wb") as f:
            f.write(content)
        logger.info(f"File saved to {file_location}")
        
        if IS_CLOUD:
            # Cloud Run: Run V14 pipeline directly (no reference images needed - RAG/DB has character data)
            try:
                # Import the pipeline module
                import sys
                sys.path.insert(0, "/app/image_gen")
                from v14_pipeline import V12Pipeline
                
                # Run the full V14 pipeline (no reference needed - Gemini knows characters)
                pipeline = V12Pipeline(project_id=PROJECT_ID)
                
                # Prepare paths
                subject_path = Path(subject_dir)
                output_path = Path(OUTPUT_DIR)
                
                # Run pipeline (async) - returns image bytes directly
                image_data = await pipeline.run(
                    subject_name="User",
                    target_character=prompt,
                    subject_dir=subject_path,
                    output_dir=output_path,
                    bypass_lock=False
                )
                
                # Check if image was generated
                if image_data:
                    image_b64 = base64.b64encode(image_data).decode('utf-8')
                    return {
                        "status": "success",
                        "message": "V14 Pipeline render complete!",
                        "image": f"data:image/png;base64,{image_b64}",
                        "prompt": prompt,
                        "pipeline": "V14"
                    }
                else:
                    error_msg = getattr(pipeline, 'last_error', 'Unknown pipeline error')
                    return {"status": "error", "message": f"V14 Pipeline failed: {error_msg}"}
                    
            except ImportError as ie:
                logger.error(f"Pipeline import failed: {ie}")
                return await _gemini_pro_image_fallback(content, file.content_type, prompt)
            except Exception as pe:
                logger.error(f"Pipeline execution failed: {pe}")
                return {"status": "error", "message": f"V14 Pipeline failed: {str(pe)}"}
        
        else:
            # Local: Use v14 pipeline via subprocess
            background_tasks.add_task(run_generation_script, file_location, prompt, filename)
            return {"status": "processing", "message": "Image uploaded. V14 Pipeline triggered.", "id": filename}
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return {"status": "error", "message": str(e)}


async def _gemini_pro_image_fallback(content: bytes, mime_type: str, prompt: str):
    """Fallback to Gemini Pro Image when V14 pipeline is unavailable."""
    import base64
    from google.genai import types
    
    if not genai_client:
        return {"status": "error", "message": "GenAI client not initialized"}
    
    mime = mime_type or "image/jpeg"
    image_part = types.Part.from_bytes(data=content, mime_type=mime)
    
    generation_prompt = f"""COSPLAY TRANSFORMATION

Subject: The person in the uploaded photo
Character: {prompt}

TASK: Generate a high-quality cosplay render of the subject as the specified character.

REQUIREMENTS:
- PRESERVE the subject's exact facial features, skin tone, and unique characteristics
- Dress them in the iconic costume of the character
- Use cinematic lighting and professional photography style
- 8K quality, photorealistic rendering
- Full body or portrait shot as appropriate

Generate a stunning cosplay transformation image."""
    
    try:
        response = await genai_client.aio.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=["=== SUBJECT PHOTO ===", image_part, generation_prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE', 'TEXT'],
                temperature=1.0
            )
        )
        
        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data
                    image_b64 = base64.b64encode(image_data).decode('utf-8')
                    return {
                        "status": "success",
                        "message": "Render complete (Gemini Pro Image)!",
                        "image": f"data:image/png;base64,{image_b64}",
                        "prompt": prompt,
                        "pipeline": "GeminiProImage"
                    }
        
        return {"status": "error", "message": "No image generated. Model may have blocked the request."}
        
    except Exception as e:
        logger.error(f"Gemini fallback failed: {e}")
        return {"status": "error", "message": f"Generation failed: {str(e)}"}

@app.get("/health")
def health_check():
    return {
        "status": "online", 
        "system": "Yuki AI Server", 
        "agent_status": "ready" if yuki_agent else "offline",
        "project": PROJECT_ID,
        "config": "stabilized-v2"
    }

@app.get("/v1/debug")
def debug_info():
    return {
        "reasoning_engine": RE_ID,
        "model_default": "gemini-3-flash-preview"
    }

@app.get("/v1/user/images")
async def get_user_images(email: str):
    try:
        conn = sqlite3.connect(r"C:\Yuki_Local\Cosplay_Lab\Brain\yuki_memory.db")
        cursor = conn.cursor()
        
        # 1. Get Subject ID from email
        cursor.execute("SELECT id, name FROM subjects WHERE email = ?", (email,))
        subject = cursor.fetchone()
        
        if not subject:
             return {"images": [], "message": "User not found"}
             
        subject_id = subject[0]
        
        # 2. Get Images for Subject
        # Joining with updated logic if needed, but simple query first
        cursor.execute("""
            SELECT filename, prompt, timestamp 
            FROM generation_log 
            WHERE subject_id = ? 
            ORDER BY timestamp DESC
        """, (subject_id,))
        
        rows = cursor.fetchall()
        
        images = []
        for row in rows:
            filename = row[0]
            # Construct accessible URL
            url = f"http://localhost:8083/{filename}"
            images.append({
                "filename": filename,
                "prompt": row[1],
                "timestamp": row[2],
                "uri": url,
                "id": filename # use filename as ID
            })
            
        conn.close()
        return {"images": images}
        
    except Exception as e:
        logger.error(f"Error fetching user images: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def get_subject_credits(subject_id):
    conn = sqlite3.connect(r"C:\Yuki_Local\Cosplay_Lab\Brain\yuki_memory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT credits FROM subjects WHERE id = ?", (subject_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def deduct_credits(subject_id, amount=10):
    conn = sqlite3.connect(r"C:\Yuki_Local\Cosplay_Lab\Brain\yuki_memory.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE subjects SET credits = credits - ? WHERE id = ?", (amount, subject_id))
    conn.commit()
    conn.close()

def get_subject_id_by_email(email):
    conn = sqlite3.connect(r"C:\Yuki_Local\Cosplay_Lab\Brain\yuki_memory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM subjects WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

@app.get("/v1/user/credits")
async def get_user_credits(email: str):
    subject_id = get_subject_id_by_email(email)
    if not subject_id:
        return {"credits": 0}
    credits = get_subject_credits(subject_id)
    return {"credits": credits}


@app.get("/agent.json")
async def get_agent_card():
    card_path = "agent.json"
    # Check current directory
    if os.path.exists(card_path):
        return FileResponse(card_path, media_type="application/json")
    # Check /app directory (Cloud Run standard)
    elif os.path.exists("/app/agent.json"):
        return FileResponse("/app/agent.json", media_type="application/json")
    # Check mapped volume if applicable or dev path
    elif os.path.exists(r"C:\Yuki_Local\agent.json"):
        return FileResponse(r"C:\Yuki_Local\agent.json", media_type="application/json")
    else:
        raise HTTPException(status_code=404, detail="Agent card not found")

@app.get("/.well-known/a2a/agent.json")
async def get_well_known_agent_card():
    return await get_agent_card()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
