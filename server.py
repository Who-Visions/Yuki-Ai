import os
import shutil
import asyncio
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import uvicorn
import logging
from typing import Optional, Dict, Any

# Import Yuki Agent
from agent import YukiAgent
from yuki_tools import get_current_time, add_numbers

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
            env={**os.environ, "YUKI_INPUT_IMAGE": input_path} 
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
