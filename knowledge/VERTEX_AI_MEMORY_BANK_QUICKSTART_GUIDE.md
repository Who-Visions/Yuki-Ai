# Quickstart with Vertex AI Agent Engine SDK

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

This tutorial demonstrates how to make API calls directly to Vertex AI Agent Engine Sessions and Memory Bank using the Vertex AI Agent Engine SDK.

## Generate memories with Vertex AI Agent Engine Sessions

After setting up Vertex AI Agent Engine Sessions and Memory Bank, you can create sessions and append events to them.

### Create a session

```python
import vertexai

client = vertexai.Client(
  project="PROJECT_ID",
  location="LOCATION"
)

session = client.agent_engines.sessions.create(
  name="AGENT_ENGINE_NAME",
  user_id="USER_ID"
)
```
*   `AGENT_ENGINE_NAME`: `projects/{your project}/locations/{your location}/reasoningEngine/{your reasoning engine}`.
*   `USER_ID`: An identifier for your user.

### Iteratively upload events

```python
import datetime

client.agent_engines.sessions.events.append(
  name=session.response.name,
  author="user",
  invocation_id="1",
  timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
  config={
    "content": {
      "role": "user",
      "parts": [{"text": "hello"}]
    }
  }
)
```

### Generate memories

```python
client.agent_engines.memories.generate(
  name=agent_engine.api_resource.name,
  vertex_session_source={
    "session": session.response.name
  },
  # Optional when using Agent Engine Sessions. Defaults to {"user_id": session.user_id}.
  scope=SCOPE
)
```

## Upload memories

As an alternative to generating memories using raw dialogue, you can upload memories directly.

### GenerateMemories with pre-extracted facts

```python
client.agent_engines.memories.generate(
    name=agent_engine.api_resource.name,
    direct_memories_source={"direct_memories": [{"fact": "FACT"}]},
    scope=SCOPE
)
```
*   `FACT`: The pre-extracted fact (e.g., "I am a software engineer").

### CreateMemory

Caution: Memories uploaded using `CreateMemory` won't be consolidated with existing memories.

```python
memory = client.agent_engines.memories.create(
    name=agent_engine.api_resource.name,
    fact="This is a fact.",
    scope={"user_id": "123"}
)
```

## Retrieve and use memories

Retrieve memories for your user and include them in your system instructions.

```python
# Retrieve all memories for User ID 123.
retrieved_memories = list(
    client.agent_engines.memories.retrieve(
        name=agent_engine.api_resource.name,
        scope={"user_id": "123"}
    )
)
```

### Use Jinja to convert structured memories into a prompt

```python
from jinja2 import Template

template = Template("""
<MEMORIES>
Here is some information about the user:
{% for retrieved_memory in data %}* {{ retrieved_memory.memory.fact }}
{% endfor %}</MEMORIES>
""")

prompt = template.render(data=retrieved_memories)
```

## Delete memories

```python
client.agent_engines.memories.delete(name=MEMORY_NAME)
```

## Clean up

Use the following code sample to delete the Vertex AI Agent Engine instance, which also deletes any sessions or memories associated with it.

```python
agent_engine.delete(force=True)
```
