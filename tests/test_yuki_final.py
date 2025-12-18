#!/usr/bin/env python3
"""Test Yuki agent with proper error handling."""

import vertexai
from vertexai.preview import reasoning_engines
import json

try:
    # Initialize
    vertexai.init(project="gifted-cooler-479623-r7", location="us-central1")
    
    # Load agent (latest deployment from 2025-12-01 08:01)
    agent = reasoning_engines.ReasoningEngine(
        "projects/914641083224/locations/us-central1/reasoningEngines/2780528567203659776"
    )
    
    print("🧪 Testing Yuki with Gemini 3.0 Pro (global routing)...")
    print()
    
    # Query the agent
    response = agent.query(user_instruction="Hello Yuki! What time is it right now?")
    
    print("✅ Response received:")
    print(json.dumps(response, indent=2))
    print()
    
    # If we got here, it worked!
    if response and 'output' in response:
        print(f"📝 Yuki says: {response['output']}")
    
except Exception as e:
    print('❌ Error:', e)
    import traceback
    traceback.print_exc()
