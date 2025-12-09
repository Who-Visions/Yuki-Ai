#!/usr/bin/env python3
"""Quick test of deployed Yuki agent."""

import vertexai
from vertexai.preview import reasoning_engines
import json

# Initialize
vertexai.init(project="gifted-cooler-479623-r7", location="us-central1")

# Load agent
agent = reasoning_engines.ReasoningEngine(
    "projects/914641083224/locations/us-central1/reasoningEngines/8076761728991363072"
)

print("🧪 Testing Yuki with Gemini 3.0 Pro...")
print()

try:
    response = agent.query(user_instruction="Hello Yuki! What time is it right now?")
    print("✅ Response received:")
    print(json.dumps(response, indent=2))
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
