#!/usr/bin/env python3
"""Inspect the deployed Yuki agent to see available methods."""

import vertexai
from vertexai.preview import reasoning_engines

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"
AGENT_RESOURCE_NAME = "projects/gifted-cooler-479623-r7/locations/us-central1/reasoningEngines/1543164569583616000"

# Initialize
print("🔧 Initializing Vertex AI...")
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Load the agent
print(f"📡 Loading Yuki...")
agent = reasoning_engines.ReasoningEngine(AGENT_RESOURCE_NAME)

print(f"\n🔍 Agent type: {type(agent)}")
print(f"📋 Available attributes/methods:")
for attr in dir(agent):
    if not attr.startswith('_'):
        print(f"  • {attr}")

print(f"\n🎯 Agent operations (if registered):")
try:
    operations = agent.operations()
    print(operations)
except Exception as e:
    print(f"  No operations registered or error: {e}")
