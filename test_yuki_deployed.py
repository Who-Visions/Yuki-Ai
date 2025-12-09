#!/usr/bin/env python3
"""Test the deployed Yuki agent via Python SDK."""

import vertexai
from vertexai.preview import reasoning_engines

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"
AGENT_RESOURCE_NAME = "projects/914641083224/locations/us-central1/reasoningEngines/3271420926587043840"

# Initialize
print("🔧 Initializing Vertex AI...")
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Load the agent
print(f"📡 Loading Yuki from: {AGENT_RESOURCE_NAME}")
agent = reasoning_engines.ReasoningEngine(AGENT_RESOURCE_NAME)

# Test query
print("\n💬 Testing query: 'What time is it?'")
try:
    response = agent.query(user_instruction="What time is it?")
    print(f"\n✅ Response:")
    print(response)
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nTrying with 'input' parameter instead...")
    try:
        response = agent.query(input="What time is it?")
        print(f"\n✅ Response:")
        print(response)
    except Exception as e2:
        print(f"❌ Also failed: {e2}")
