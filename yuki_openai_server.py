
print("DEBUG: Pre-imports", flush=True)
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel
from google import genai
from google.genai import types
import datetime

# Import Yuki's Tools and Prompt
print("DEBUG: Importing tools...", flush=True)
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
print("DEBUG: Importing yuki_local...", flush=True)
from yuki_local import YUKI_SYSTEM_PROMPT, Colors

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"

app = FastAPI(title="Yuki OpenAI Compatible API")

# Configure CORS for A2A compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini Client
print("DEBUG: Initializing GenAI Client...", flush=True)
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
)
print("DEBUG: Client Initialized.", flush=True)

# Tool Definitions
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
# Map for execution
tool_map = {func.__name__: func for func in tools_list}

# Pydantic Models for OpenAI API
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

@app.get("/")
async def root():
    return {
        "message": "Iyuki OpenAI-Compatible Server is Running",
        "docs": "/docs",
        "chat_endpoint": "/v1/chat/completions"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/.well-known/agent.json")
async def get_agent_card():
    """
    A2A Agent Identity Card - Standardized discovery endpoint.
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
            "models": "/v1/models"
        },
        "extensions": {
            "color": "pink",
            "role": "Cosplay Architect",
            "personality": "Playful, Mischievous, Japanese-Honorifics"
        }
    }

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
                "id": "gemini-2.5-pro",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "google",
            }
        ]
    }

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    print(f"\n{Colors.NEON_PINK}[🦊 YUKI SERVER] Request received for model: {request.model}{Colors.RESET}")
    start_time = time.time()
    
    # 1. Convert OpenAI Messages to Gemini Content
    gemini_contents = []
    
    # Handle System Prompt separately or as part of config
    system_instruction = YUKI_SYSTEM_PROMPT
    
    for msg in request.messages:
        role = msg.role
        content = msg.content
        
        parts = []
        if content:
            if isinstance(content, str):
                parts.append(types.Part(text=content))
            elif isinstance(content, list):
                # Handle multimodal content (simplified for now)
                for item in content:
                    if item.get("type") == "text":
                        parts.append(types.Part(text=item["text"]))
                    elif item.get("type") == "image_url":
                         # This needs handling implementation for image download/passing
                         parts.append(types.Part(text=f"[Image URL provided: {item['image_url']['url']}]"))
        
        if role == "system":
            # Override system prompt if provided in messages
            # Or prepend to history? Gemini 2.5 supports system_instruction config.
            # We'll stick to the global YUKI_SYSTEM_PROMPT unless specifically asked to change.
            pass 
        elif role == "user":
            gemini_contents.append(types.Content(role="user", parts=parts))
        elif role == "assistant":
             gemini_contents.append(types.Content(role="model", parts=parts))

    # 2. Configure Generation
    # Default to Gemini 2.5 Pro if not specified or if 'gpt-4' etc is requested
    model_name = "gemini-2.5-pro-preview-0219" # Or appropriate version
    if "gemini" in request.model:
        model_name = request.model
    
    config = types.GenerateContentConfig(
        tools=tools_list,
        temperature=request.temperature,
        top_p=request.top_p,
        candidate_count=1,
        system_instruction=system_instruction
    )

    # 3. Execution Loop (Handle Tool Calls)
    final_text = ""
    finish_reason = "stop"
    
    MAX_TURNS = 15
    turn_count = 0
    
    try:
        while turn_count < MAX_TURNS:
            turn_count += 1
            
            response = client.models.generate_content(
                model=model_name,
                contents=gemini_contents,
                config=config
            )
            
            if not response.candidates:
                finish_reason = "error"
                final_text = "Error: No response from model."
                break
                
            candidate = response.candidates[0]
            
            # Check for function calls
            function_calls = []
            for part in candidate.content.parts:
                if part.function_call:
                    function_calls.append(part.function_call)
            
            if not function_calls:
                # We have a final text response
                for part in candidate.content.parts:
                    if part.text:
                        final_text += part.text
                break
            
            # Execute Tools
            # Append model's request to history
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

                # Append result
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
        print(f"{Colors.ERROR_RED}Error in generation: {e}{Colors.RESET}")
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
        usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0} # Usage stats not easily available in this flow
    )

if __name__ == "__main__":
    print(f"{Colors.ICE_BLUE}🦊 Yuki OpenAI-Compatible Server Starting on Port 8000...{Colors.RESET}")
    import sys
    sys.stdout.flush()
    uvicorn.run(app, host="0.0.0.0", port=8000)
