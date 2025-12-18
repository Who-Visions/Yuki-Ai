
import requests
import google.auth
import google.auth.transport.requests

PROJECT_ID = "gifted-cooler-479623-r7"
ENDPOINT = "https://us-central1-aiplatform.googleapis.com/v1/projects/gifted-cooler-479623-r7/locations/us-central1/reasoningEngines/7435157111765467136:query"

def test_rest_call():
    print(f"🚀 Calling Reasoning Engine REST Endpoint...")
    
    # Get credentials
    credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)
    token = credentials.token
    
    payload = {
        "input": {
            "user_instruction": "Hello Yuki, testing your REST orchestration. What are your core directives?"
        }
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"💬 Response: {result.get('output', result)}")
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            print(f"📝 Detail: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_rest_call()
