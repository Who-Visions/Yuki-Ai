# Quickstart with Agent Development Kit (ADK)

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

After you configure your Agent Development Kit (ADK) agent to use Memory Bank, your agent orchestrates calls to Memory Bank to manage long-term memories for you.

## Set environment variables

```python
import os

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
os.environ["GOOGLE_CLOUD_PROJECT"] = "PROJECT_ID"
os.environ["GOOGLE_CLOUD_LOCATION"] = "LOCATION"
```

## Create your ADK agent

Include a Memory tool that controls when the agent retrieves memories.

```python
from google import adk

agent = adk.Agent(
    model="gemini-2.0-flash",
    name='stateful_agent',
    instruction="You are a Vehicle Voice Agent...",
    tools=[adk.tools.preload_memory_tool.PreloadMemoryTool()]
)
```

## Create a VertexAiMemoryBankService

```python
from google.adk.memory import VertexAiMemoryBankService
import vertexai

client = vertexai.Client(
  project="PROJECT_ID",
  location="LOCATION"
)

# Create an Agent Engine Memory Bank instance using the default configuration.
agent_engine = client.agent_engines.create()
agent_engine_id = agent_engine.api_resource.name.split("/")[-1]

memory_service = VertexAiMemoryBankService(
    project="PROJECT_ID",
    location="LOCATION",
    agent_engine_id=agent_engine_id
)
```

## Create an ADK Runtime

```python
import asyncio
from google.adk.sessions import VertexAiSessionService
from google.genai import types

session_service = VertexAiSessionService(
    project="PROJECT_ID",
    location="LOCATION",
    agent_engine_id=agent_engine_id
)

app_name="APP_NAME"

runner = adk.Runner(
    agent=agent,
    app_name=app_name,
    session_service=session_service,
    memory_service=memory_service
)

async def call_agent(query, session, user_id):
  content = types.Content(role='user', parts=[types.Part(text=query)])
  events = runner.run_async(
    user_id=user_id, session_id=session, new_message=content)

  async for event in events:
      if event.is_final_response():
          final_response = event.content.parts[0].text
          print("Agent Response: ", final_response)
```

## Interact with your agent

### Create your first session

```python
session = await session_service.create_session(
    app_name="APP_NAME",
    user_id="USER_ID"
)

await call_agent(
    "Can you update the temperature to my preferred temperature?",
    session.id,
    "USER_ID"
)
# Agent response: "What is your preferred temperature?"

await call_agent(
  "I like it at 71 degrees", session.id, "USER_ID")
# Agent Response:  Setting the temperature to 71 degrees Fahrenheit.
```

### Generate memories

```python
async def trigger_memory_generation(app_name, session):
    # Refresh your `session` object so that all of the session events locally available.
    session = await session_service.get_session(
        app_name=app_name,
        user_id="USER_ID",
        session_id=session.id
    )
    await memory_service.add_session_to_memory(session)

await trigger_memory_generation(app_name, session)
```

### Create your second session

The agent retrieves memories at the beginning of each turn.

```python
session = await session_service.create_session(
    app_name=app_name,
    user_id="USER_ID"
)

await call_agent("Fix the temperature!", session.id, "USER_ID")
# Agent Response:  Setting temperature to 71 degrees.  Is that correct?
```

### Direct memory search

```python
await memory_service.search_memory(
    app_name="APP_NAME",
    user_id="USER_ID",
    query="Fix the temperature!",
)
```

## Clean up

```python
agent_engine.delete(force=True)
```
