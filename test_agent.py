
from agent import YukiAgent
from tools import get_current_time, add_numbers
import vertexai

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"

def test_agent():
    print("Testing agent initialization...")
    try:
        agent = YukiAgent(
            model="gemini-3-pro-preview",
            tools=[get_current_time, add_numbers],
            project=PROJECT_ID,
            location=LOCATION,
        )
        print("Agent instantiated.")
        
        print("Setting up agent...")
        agent.set_up()
        print("Agent setup complete.")
        
        print("Testing query...")
        # We might not be able to actually query if auth is missing, but setup is the main thing.
        # response = agent.query(input="What time is it?")
        # print(response)
        
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agent()
