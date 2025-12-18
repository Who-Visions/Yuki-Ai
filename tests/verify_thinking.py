
import json
import requests
import time

URL = "http://localhost:8080/v1/chat/completions"

def test_thinking_request(include_thoughts=True, thinking_level="HIGH", budget=None):
    payload = {
        "model": "gemini-3-pro-preview",
        "messages": [
            {"role": "user", "content": "Think deeply about the philosophical implications of a 'Boltzmann Brain'. Provide a concise summary of your thinking process and conclusion. DO NOT use any tools."}
        ],
        "includeThoughts": include_thoughts,
        "thinkingLevel": thinking_level
    }
    if budget is not None:
        payload["thinkingBudget"] = budget

    print(f"\n📡 Testing with includeThoughts={include_thoughts}, thinkingLevel={thinking_level}, budget={budget}")
    
    try:
        response = requests.post(URL, json=payload, timeout=120)
        result = response.json()
        
        print(f"✅ Status Code: {response.status_code}")
        
        if "choices" in result:
            content = result["choices"][0]["message"]["content"]
            if "[THOUGHTS]" in content:
                print("🌟 SUCCESS: Thoughts included in output!")
            else:
                print("❌ ERROR: Thoughts NOT found in output despite includeThoughts=True")
        
        usage = result.get("usage", {})
        print(f"📊 Usage: {json.dumps(usage, indent=2)}")
        
        if usage.get("thoughts_tokens", 0) > 0:
            print(f"💰 SUCCESS: Captured {usage['thoughts_tokens']} thinking tokens!")
        else:
            print("❓ WARNING: thinking tokens count is 0 or missing.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Advanced Thinking Verification...")
    # These tests assume the server is running on localhost:8080
    test_thinking_request(include_thoughts=True, thinking_level="HIGH")
    test_thinking_request(include_thoughts=False, thinking_level="LOW")
    test_thinking_request(include_thoughts=True, budget=4096)
