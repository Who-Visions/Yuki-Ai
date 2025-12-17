#!/usr/bin/env python3
"""
YUKI V.005 - Vertex AI Agent Engine Deployment
Cosplay Preview Architect | Nine-Tailed Snow Fox
"""

import vertexai
from vertexai.preview import reasoning_engines
import os
from datetime import datetime, timezone

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"  # Reasoning Engine requires a specific region
MODEL = "gemini-3-pro-preview"
STAGING_BUCKET = f"gs://yuki-{PROJECT_ID}"

vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

# ═══════════════════════════════════════════════════════════════════════════════
# YUKI - COSPLAY PREVIEW ARCHITECT
# ═══════════════════════════════════════════════════════════════════════════════

def get_current_time() -> str:
    """Returns the current time in UTC."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    def set_up(self):
        """Initialize Gemini client on startup."""
        from google import genai
        
        # Gemini 3.0 models require global location (new model, different routing)
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
        
        Args:
            user_instruction: Natural language input.
            
        Returns:
            dict: Response from Yuki.
        """
        from google.genai import types
        
        # Lazy initialization - set up client if not already initialized
        if self.client is None:
            self.set_up()
        
        # Extract input string
        if isinstance(user_instruction, dict):
            if 'messages' in user_instruction:
                text = user_instruction['messages'][-1]['content'] if user_instruction['messages'] else ''
            elif 'input' in user_instruction:
                text = user_instruction['input']
            else:
                text = str(user_instruction)
        else:
            text = str(user_instruction)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction="""You are Yuki Ai, a nine-tailed snow fox spirit that lives inside Cosplay Labs.

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
                    tools=self.tools,
                    temperature=1.0,
                )
            )
            
            return {'output': response.text.strip()}
            
        except Exception as e:
            return {
                'output': f"Error: {str(e)}",
                'status': 'error'
            }

    def register_operations(self):
        """
        Register operations for the deployed agent.
        """
        return {
            "": ["query"]
        }


    yuki = Yuki()
    yuki.set_up()
    test_result = yuki.query("Hello")
    print(f"      ✓ Local test passed")
    
    # Deploy
    print("[2/3] Deploying to Vertex AI Agent Engine...")
    print("      This may take 3-5 minutes...")
    
    remote_yuki = reasoning_engines.ReasoningEngine.create(
        Yuki(),
        requirements=[
            "cloudpickle==3",
            "google-genai>=1.51.0"
        ],
        display_name="Yuki-v005",
        description="Cosplay Preview Architect | Nine-Tailed Snow Fox",
    )
    
    # Success
    print("[3/3] Deployment complete!")
    print()
    print("=" * 70)
    print("  ✓ YUKI IS ONLINE")
    print("=" * 70)
    print(f"\n  Resource: {remote_yuki.resource_name}")
    print()
    
    return remote_yuki


if __name__ == "__main__":
    deploy()
