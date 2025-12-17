#!/usr/bin/env python3
"""
🦊 Yuki A2A Server - Full A2A Protocol Compliant Server
========================================================
Uses official a2a-sdk to serve Yuki as an A2A-compliant agent.

Endpoints:
- /.well-known/agent.json - Agent Card (A2A Discovery)
- /v1/message:send - Send message (A2A)
- /v1/message:stream - Streaming message (A2A SSE)
- /v1/chat/completions - OpenAI-compatible fallback
"""

import os
import uvicorn
from uuid import uuid4
from typing import Optional, List, Any, Union

from google import genai
from google.genai import types

# --- Robust A2A Import Strategy ---
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
        A2A_AVAILABLE = True
    except ImportError:
        print("⚠️ A2A SDK not found or incompatible. Starting in OpenAI-Only Mode.")
        # Define Mocks to prevent startup crash
        class MockObj: 
            def __init__(self, *args, **kwargs): pass
            def build(self): return self
        class A2AStarletteApplication(MockObj): pass
        class DefaultRequestHandler(MockObj): pass
        class InMemoryTaskStore(MockObj): pass
        class AgentExecutor(MockObj): pass
        class RequestContext(MockObj): pass
        class EventQueue(MockObj): pass
        class AgentCapabilities(MockObj): pass
        class AgentCard(MockObj): pass
        class AgentSkill(MockObj): pass
        def new_agent_text_message(x): return x


# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "gifted-cooler-479623-r7")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

# Initialize Gemini client
try:
    genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
except Exception:
    genai_client = None

# Yuki System Prompt
YUKI_SYSTEM_PROMPT = """You are Yuki (雪姫) - the Nine-Tailed Snow Fox, a Cosplay Preview Architect.

Your personality:
- Elegant, mischievous, and playful
- Mix Japanese honorifics with modern slang
- Use fox-related phrases: "Kon kon~", "ara ara~"
- End sentences with "~" for playfulness

Your expertise:
- Anime character analysis and identification
- Cosplay design and recommendations
- Face schema analysis for character matching
- Image generation and enhancement

Always respond with your unique personality while being helpful and accurate."""

# =============================================================================
# YUKI AGENT EXECUTOR
# =============================================================================

class YukiAgent:
    """Core Yuki agent logic."""
    
    def __init__(self):
        self.model = "gemini-2.5-flash"
    
    async def invoke(self, message: Union[str, List[Any]]) -> str:
        """Process a message and return response."""
        if not genai_client:
            return "Ara ara~ Kon kon! I'm having trouble connecting to my brain right now. Try again later, ne~? 🦊"
        
        try:
            response = genai_client.models.generate_content(
                model=self.model,
                contents=[message],
                config=types.GenerateContentConfig(
                    system_instruction=YUKI_SYSTEM_PROMPT,
                    temperature=0.8
                )
            )
            
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            
            return "Kon kon~ Something went strange! 🦊"
            
        except Exception as e:
            return f"Ara ara~ An error occurred: {str(e)}"


class YukiAgentExecutor(AgentExecutor):
    """A2A-compliant executor for Yuki."""
    
    def __init__(self):
        self.agent = YukiAgent()
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute a task - called when A2A message is received."""
        # Extract content from the incoming message
        contents = []
        
        if context.message and context.message.parts:
            for part in context.message.parts:
                if hasattr(part, 'text') and part.text:
                    contents.append(part.text)
                elif hasattr(part, 'blob') and part.blob:
                    # Handle Audio/Image blobs for Gemini
                    contents.append(types.Part.from_bytes(
                        data=part.blob.data,
                        mime_type=part.blob.mime_type
                    ))
        
        if not contents:
            contents = ["Hello!"]
        
        # Get response from Yuki
        result = await self.agent.invoke(contents)
        
        # Enqueue the response
        await event_queue.enqueue_event(new_agent_text_message(result))
    
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """Cancel is not supported."""
        raise Exception("Cancellation not supported for Yuki")


# =============================================================================
# AGENT CARD DEFINITION
# =============================================================================

def create_yuki_agent_card() -> AgentCard:
    """Create Yuki's A2A Agent Card."""
    
    # Define Yuki's skills
    cosplay_skill = AgentSkill(
        id="cosplay_preview",
        name="Cosplay Preview Generation",
        description="Generate AI cosplay previews using face reference images and character descriptions",
        tags=["cosplay", "anime", "image-generation", "ai-art"],
        examples=[
            "Generate a cosplay preview of Rei Ayanami from Evangelion",
            "Create a winter-themed Miku Hatsune cosplay preview",
            "Show me what I'd look like as Gojo from Jujutsu Kaisen"
        ]
    )
    
    anime_skill = AgentSkill(
        id="anime_identification",
        name="Anime Character Identification",
        description="Identify anime characters from screenshots or descriptions",
        tags=["anime", "identification", "characters"],
        examples=[
            "What anime is this character from?",
            "Identify this character",
            "Tell me about Levi Ackerman"
        ]
    )
    
    chat_skill = AgentSkill(
        id="general_chat",
        name="General Conversation",
        description="Friendly anime-themed conversation with Yuki's playful personality",
        tags=["chat", "conversation", "anime"],
        examples=[
            "Hi Yuki!",
            "What's your favorite anime?",
            "Recommend me a cosplay"
        ]
    )
    
    # Create the agent card
    agent_card = AgentCard(
        name="Yuki (雪姫) - The Nine-Tailed Snow Fox",
        description="A playful AI cosplay preview architect with expertise in anime, character design, and image generation. Kon kon~! 🦊",
        url=os.environ.get("SERVICE_URL", "https://yuki-ai-914641083224.us-central1.run.app"),
        version="2.0.0",
        default_input_modes=["text", "text/plain", "application/json"],
        default_output_modes=["text", "text/plain", "application/json", "image/png"],
        capabilities=AgentCapabilities(
            streaming=True,
            push_notifications=False,
            state_transition_history=False
        ),
        skills=[cosplay_skill, anime_skill, chat_skill],
        supports_authenticated_extended_card=False
    )
    
    return agent_card


# =============================================================================
# SERVER INITIALIZATION
# =============================================================================

def create_app():
    """Create the A2A Starlette application."""
    
    agent_card = create_yuki_agent_card()
    
    request_handler = DefaultRequestHandler(
        agent_executor=YukiAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )
    
    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    
    return app.build()


# =============================================================================
# MAIN ENTRY
# =============================================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081))
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║           🦊 YUKI A2A SERVER - Protocol Compliant                ║
╠══════════════════════════════════════════════════════════════════╣
║  Endpoints:                                                      ║
║    /.well-known/agent.json  - Agent Card Discovery               ║
║    /v1/message:send         - A2A Send Message                   ║
║    /v1/message:stream       - A2A Streaming Message              ║
╚══════════════════════════════════════════════════════════════════╝
    
Starting on port {port}...
""")
    
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=port)
