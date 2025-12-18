
import json
import requests

URL = "http://localhost:8080/v1/reasoning"

def test_reasoning_engine():
    payload = {
        "model": "vertex-reasoning-engine",
        "messages": [
            {"role": "user", "content": "Tell me about the current status of the Yuki project and your core capabilities as a reasoning engine."}
        ]
    }

    print(f"\n📡 Testing Vertex AI Reasoning Engine Integration...")
    
    try:
        # Note: This requires the server to be running on 8080
        response = requests.post(URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS: Reasoning Engine Responded!")
            print(f"💬 Response: {result['choices'][0]['message']['content']}")
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            print(f"📝 Detail: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_reasoning_engine()
