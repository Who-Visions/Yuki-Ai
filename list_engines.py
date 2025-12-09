import vertexai
from vertexai.preview import reasoning_engines

vertexai.init(project="gifted-cooler-479623-r7", location="us-central1")

print("Listing Reasoning Engines...")
engines = reasoning_engines.ReasoningEngine.list()
for engine in engines:
    print(f"Name: {engine.display_name}")
    print(f"Resource: {engine.resource_name}")
    print(f"Created: {engine.create_time}")
    print("-" * 20)
