import vertexai
import logging
import asyncio
from tools import get_current_time, add_numbers # Import tools for local testing/initialization

# --- Configuration ---
PROJECT_ID = "gifted-cooler-479623-r7" # Your Project ID
LOCATION = "us-central1"
# 🚨 CRITICAL: REPLACE THIS WITH THE RESOURCE NAME PRINTED BY deploy.py 🚨
# Example format: 'projects/PROJECT_NUMBER/locations/us-central1/reasoningEngines/1234567890'
RESOURCE_NAME = "REPLACE_WITH_YOUR_RESOURCE_NAME" 
# ---------------------

def initialize_client():
    """Initializes the Vertex AI client."""
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    return vertexai.Client()

def get_remote_agent(client):
    """Retrieves the deployed agent instance."""
    print(f"Connecting to deployed agent: {RESOURCE_NAME}")
    try:
        agent = client.agent_engines.get(name=RESOURCE_NAME)
        return agent
    except Exception as e:
        logging.error(f"Failed to get agent. Did you update RESOURCE_NAME? Error: {e}")
        return None

def test_query(agent, query_text):
    """Tests the synchronous query method."""
    print(f"\n--- Testing Synchronous Query ---")
    print(f"Query: {query_text}")
    try:
        response = agent.query(input=query_text)
        # The agent response is often a dictionary with an 'output' key
        output = response.get('output', response)
        print(f"\n✅ Agent Response:\n{output}")
    except Exception as e:
        print(f"❌ Query failed: {e}")

async def test_streaming_query(agent, query_text):
    """Tests the asynchronous streaming query method."""
    print(f"\n--- Testing Asynchronous Streaming Query ---")
    print(f"Query: {query_text}")
    print("\n▶️ Agent Stream:")
    try:
        # Use async_stream_query for a non-blocking stream
        async for chunk in agent.async_stream_query(input=query_text):
            # Print only the 'output' part of the chunk for cleaner display
            if 'output' in chunk:
                # Use end="" to print chunks on the same line
                print(chunk['output'], end="", flush=True)
            elif 'messages' in chunk:
                # Optionally print messages for debugging the thought process
                pass
            
        print("\n\n✅ Streaming Complete.")
    except Exception as e:
        print(f"\n❌ Streaming query failed: {e}")

async def main():
    client = initialize_client()
    agent = get_remote_agent(client)

    if not agent:
        print("\nAgent connection failed. Please check your configuration and ensure the agent is deployed.")
        return

    # 1. Test using a tool (add_numbers)
    test_query(agent, "What is the result of adding 1300 and 42?")
    
    # 2. Test general LLM capability and stream
    await test_streaming_query(agent, "Explain the difference between LangChain and LangGraph in the context of building AI agents.")

if __name__ == "__main__":
    # Ensure the correct tool names are imported for initialization purposes
    if not (get_current_time and add_numbers):
        print("Error: Could not import tools.py functions. Check tools.py.")
    
    # Python's asyncio module is required to run async methods
    asyncio.run(main())
