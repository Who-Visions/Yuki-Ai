
import vertexai
from vertexai.preview import reasoning_engines

PROJECT_ID = "gifted-cooler-479623-r7"
REASONING_ENGINE_ID = "projects/914641083224/locations/us-central1/reasoningEngines/8197233019023523840"

def test_sdk_call():
    print(f"🚀 Calling Reasoning Engine {REASONING_ENGINE_ID} via SDK (No Server)...")
    vertexai.init(project=PROJECT_ID, location="us-central1")
    
    try:
        remote_agent = reasoning_engines.ReasoningEngine(REASONING_ENGINE_ID)
        response = remote_agent.query(input="Hello Yuki, what is your current reasoning status?")
        print(f"✅ SUCCESS!")
        print(f"💬 Response: {response}")
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    test_sdk_call()
