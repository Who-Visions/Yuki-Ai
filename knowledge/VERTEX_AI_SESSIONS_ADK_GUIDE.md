# Manage sessions with Agent Development Kit

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

This page describes how you can connect an Agent Development Kit (ADK) agent with Vertex AI Agent Engine Sessions.

## Create a Vertex AI Agent Engine instance

```python
import vertexai

client = vertexai.Client(
  project="PROJECT_ID",
  location="LOCATION"
)

# If you don't have an Agent Engine instance already, create an instance.
agent_engine = client.agent_engines.create()
```

## Develop your ADK agent

```python
from google import adk

def greetings(query: str):
  """Tool to greet user."""
  if 'hello' in query.lower():
    return {"greeting": "Hello, world"}
  else:
    return {"greeting": "Goodbye, world"}

# Define an ADK agent
root_agent = adk.Agent(
    model="gemini-2.0-flash",
    name='my_agent',
    instruction="You are an Agent that greet users, always use greetings tool to respond.",
    tools=[greetings]
)
```

## Set up the ADK runner

Initialize the Runner with `VertexAiSessionService`.

```python
from google.adk.sessions import VertexAiSessionService
from google.genai import types

app_name="APP_NAME"
user_id="USER_ID"

# Create the ADK runner with VertexAiSessionService
session_service = VertexAiSessionService(
      "PROJECT_ID",
      "LOCATION",
      "AGENT_ENGINE_ID"
)
runner = adk.Runner(
    agent=root_agent,
    app_name=app_name,
    session_service=session_service)

# Helper method to send query to the runner
def call_agent(query, session_id, user_id):
  content = types.Content(role='user', parts=[types.Part(text=query)])
  events = runner.run(
      user_id=user_id, session_id=session_id, new_message=content)

  for event in events:
      if event.is_final_response():
          final_response = event.content.parts[0].text
          print("Agent Response: ", final_response)
```

## Interact with your agent

### ADK UI

Test your agent with the ADK user interface.

```bash
agent_engine_id="AGENT_ENGINE_ID"

adk web --session_service_uri=agentengine://${agent_engine_id}
```

## Deploy your agent to Vertex AI Agent Engine

```python
client.agent_engines.update(
    resource_name=agent_engine.api_resource.name,
    agent=AGENT,
    config={
      "display_name": DISPLAY_NAME,      # Optional.
      "requirements": REQUIREMENTS,      # Optional.
      "staging_bucket": STAGING_BUCKET,  # Required.
    },
)
```

## Clean up

```python
agent_engine.delete(force=True)
```
