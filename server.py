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
from typing import Optional, Dict, Any, List, Union

# Import Yuki Agent
import sqlite3
from agent import YukiAgent
from yuki_tools import (
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
from google import genai
from google.genai import types
import time
import uuid
from typing import List, Union

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YukiServer")

app = FastAPI()

# Allow Expo/Localhost access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
INPUT_DIR = r"C:\Yuki_Local\Inputs"
OUTPUT_DIR = r"C:\Yuki_Local\Cosplay_Lab\Renders\Server_Output"
SCRIPT_PATH = r"C:\Yuki_Local\run_paris_single_photo_v12.py"
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"

# Ensure directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Agent
logger.info("Initializing Yuki Agent (Gemini 3)...")
try:
    yuki_agent = YukiAgent(
        model="gemini-3-pro-preview",
        tools=[get_current_time, add_numbers],
        project=PROJECT_ID,
        location="global", # Gemini 3 is global
    )
    yuki_agent.set_up()
    logger.info("Yuki Agent initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Yuki Agent: {e}")
    yuki_agent = None

# Initialize GenAI Client for /v1/chat/completions
logger.info("Initializing GenAI Client...")
try:
    genai_client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
    )
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

async def run_generation_script(input_path: str, request_id: str):
    """
    Executes the existing v12 generation pipeline as a subprocess.
    """
    logger.info(f"Starting generation for {request_id}")
    try:
        process = await asyncio.create_subprocess_exec(
            "python", SCRIPT_PATH,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ, "YUKI_INPUT_IMAGE": input_path, "YUKI_USER_EMAIL": "whoentertains@gmail.com"} # Hardcoded for now, should come from request 
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
    if not yuki_agent:
        raise HTTPException(status_code=503, detail="Yuki Agent is not initialized (Check credentials/network)")
    
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
    
    for msg in request.messages:
        role = msg.role
        content = msg.content
        
        parts = []
        if content:
            if isinstance(content, str):
                parts.append(types.Part(text=content))
            elif isinstance(content, list):
                # Handle multimodal content
                for item in content:
                    if item.get("type") == "text":
                        parts.append(types.Part(text=item["text"]))
                    elif item.get("type") == "image_url":
                         parts.append(types.Part(text=f"[Image URL provided: {item['image_url']['url']}]"))
        
        if role == "system":
            pass # Handled via config
        elif role == "user":
            gemini_contents.append(types.Content(role="user", parts=parts))
        elif role == "assistant":
             gemini_contents.append(types.Content(role="model", parts=parts))

    # 2. Configure Generation
    model_name = "gemini-3-pro-preview"
    if "gemini" in request.model:
        model_name = request.model
    
    thinking_level = (request.thinking_level or request.reasoning_effort or "high").upper()
    
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
                finish_reason = "error"
                final_text = "Error: No response from model."
                break
                
            candidate = response.candidates[0]
            
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
async def generate_cosplay(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        # Safe filename
        filename = f"server_input_{file.filename}"
        file_location = os.path.join(INPUT_DIR, filename)
        
        # Save uploaded file
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
            
        logger.info(f"File saved to {file_location}")
        
        # Trigger Generation in Background
        background_tasks.add_task(run_generation_script, file_location, filename)
        
        return {"status": "processing", "message": "Image uploaded. Generation started.", "id": filename}
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/health")
def health_check():
    return {"status": "online", "system": "Yuki AI Server", "agent_status": "ready" if yuki_agent else "offline"}

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
