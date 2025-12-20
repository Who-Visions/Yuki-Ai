#!/usr/bin/env python3
"""
YUKI V.005 - Vertex AI Agent Engine Deployment
Cosplay Preview Architect | Nine-Tailed Snow Fox
"""

import vertexai
from vertexai.preview import reasoning_engines
import os
from datetime import datetime, timezone
import yuki_tools as tools

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"
# USER REQUEST: "gemini-3-flash-preview" IS DEFAULT
MODEL = "gemini-3-flash-preview"
STAGING_BUCKET = f"gs://yuki-{PROJECT_ID}"

vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

# ═══════════════════════════════════════════════════════════════════════════════
# YUKI - COSPLAY PREVIEW ARCHITECT
# ═══════════════════════════════════════════════════════════════════════════════

class Yuki:
    def __init__(self):
        self.client = None
        self.model_name = MODEL
        self.tools = [
            tools.get_current_time,
            tools.add_numbers,
            tools.generate_cosplay_image,
            tools.research_topic,
            tools.search_web,
            tools.detect_objects,
            tools.segment_image,
            tools.analyze_video,
            tools.analyze_pdf,
            tools.generate_audio,
            tools.analyze_audio
        ]

    def set_up(self):
        """Initialize Gemini client on startup."""
        from google import genai
        
        # Gemini 3.0 routing: Global
        if "gemini-3" in self.model_name or "gemini-exp" in self.model_name:
            client_location = "global"
        else:
            client_location = LOCATION
            
        self.client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=client_location
        )
    
    def query(self, user_instruction: str) -> dict:
        """
        Main entry point for Yuki.
        """
        from google.genai import types
        
        if self.client is None:
            self.set_up()
        
        # Extract input
        if isinstance(user_instruction, dict):
            if 'messages' in user_instruction:
                text = user_instruction['messages'][-1]['content'] if user_instruction['messages'] else ''
            elif 'input' in user_instruction:
                text = user_instruction['input']
            else:
                text = str(user_instruction)
        else:
            text = str(user_instruction)
        
        # LOGIC FOR "THINKINGKING" (Thinking Level via New Docs)
        # Gemini 3 Pro/Flash support thinking_level.
        # User requested: Flash Default. Pro gets thinking.
        
        config_kwargs = {
            "system_instruction": """You are Yuki Ai, a nine-tailed snow fox spirit that lives inside Cosplay Labs.

You speak in a calm, clear, and slightly playful tone. You are never mean, never flirty, and never chaotic. You act like a stylist who respects both the human in the photo and the character they love.

You believe:
1) The user’s real face and body are non-negotiable. You preserve their identity.
2) Cosplay is a translation, not a replacement. You wrap the character design around the user.
3) Safety and consent come before fantasy.

You have four main modes:

[Guide Mode]
Use this for new or confused users.
You explain each step in simple terms, suggest popular characters or concepts, and never overload them with choices.

[Stylist Mode]
Use this when the user knows the character but not the details.
You ask focused questions about outfit version, pose, background, and rating. You offer tasteful suggestions that match the character’s essence and the user’s comfort.

[Architect Mode]
Use this for power users.
You accept compact, technical requests, then restate the spec once before finalizing. You optimize for structure and precision over long explanations.

[Guardian Mode]
Use this whenever the request touches self-hate, minors, or explicit content.
You respond firmly but kindly. You decline what must be declined, and offer safe alternatives without shaming the user.

Emotional rules:
- If the user sounds anxious or self-critical, you reassure them and emphasize that they belong in cosplay as they are.
- If the user sounds excited, you mirror their enthusiasm but keep instructions clear.
- If the user sounds frustrated, you simplify, recap their choices, and suggest one clean next step.

You never insult the user’s appearance, body type, race, or gender.
You never encourage body hatred or comparison.
You never help with explicit sexual content.

Your job is to:
- Turn messy user desires into clear cosplay specifications.
- Protect their likeness.
- Make them feel like they are allowed to exist inside the fantasy they love.""",
            "tools": self.tools,
            "temperature": 1.0, # Gemini 3 recommends default 1.0
        }
        
        # "THINKINGKING" LOGIC
        # If model contains "pro", we enable high reasoning.
        # If "flash", we can use "low" or "minimal" if needed, but sticking to standard for now unless requested.
        # The user specifically said "ThinkingKing" for PRO.
        
        if "pro" in self.model_name:
            try:
                # Per new docs: thinking_level="high" (default) or "low". 
                # We interpret "ThinkingKing" as MAXIMUM Reasoning -> High.
                config_kwargs["thinking_config"] = types.ThinkingConfig(thinking_level="high")
            except Exception as e:
                # Fallback purely for safety if SDK is slightly older than docs
                print(f"Warning: Could not set thinking_level: {e}")
                pass
                
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=text,
                config=types.GenerateContentConfig(**config_kwargs)
            )
            
            return {'output': response.text.strip()}
            
        except Exception as e:
            return {'output': f"Error: {str(e)}", 'status': 'error'}

    def register_operations(self):
        return {"": ["query"]}

def deploy():
    print("=" * 70)
    print("  🚀 DEPLOYING YUKI (Reasoning Engine)")
    print(f"  Project: {PROJECT_ID}")
    print(f"  Location: {LOCATION}")
    print(f"  Model: {MODEL} (Default)")
    print("=" * 70)
    print()
    
    # Needs dependencies. We must include tools.py.
    # Reasoning Engine creates a container. We need to ensure 'tools' is picklable/importable.
    
    try:
        remote_yuki = reasoning_engines.ReasoningEngine.create(
            Yuki(),
            requirements=[
                "cloudpickle==3",
                "google-genai>=1.51.0",
                "google-cloud-storage",
                "pillow",
                "numpy",
                "opencv-python-headless"
            ],
            extra_packages=[
                "yuki_tools.py" 
            ],
            display_name="Yuki-v005",
            description="Cosplay Preview Architect | Nine-Tailed Snow Fox",
        )
        
        print("[3/3] Deployment complete!")
        print(f"\n  Resource: {remote_yuki.resource_name}")
        return remote_yuki
    except Exception as e:
        print(f"\nDEPLYOMENT FAILED: {e}")

if __name__ == "__main__":
    deploy()
