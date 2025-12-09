# Generate memories

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

Memory Bank lets you construct long-term memories from conversations between the user and your agent. This page describes how memory generation works, how you can customize how memories are extracted, and how to trigger memory generation.

## Understanding memory generation

Memory Bank extracts memories from source data and self-curates memories for a specific collection of memories (defined by a scope) by adding, updating, and removing memories over time.

When you trigger memory generation, Memory Bank performs the following operations:

1.  **Extraction:** Extracts information about the user from their conversations with the agent. Only information that matches at least one of your instance's memory topics will be persisted.
2.  **Consolidation:** Identifies if existing memories with the same scope should be deleted or updated based on the extracted information.

### Memory generation algorithm

You can inspect the intermediate steps of memory generation using memory revisions.

```python
list(client.agent_engines.memories.revisions.list(
  name="projects/.../locations/.../reasoningEngines/.../memories/.../revisions/..."))
```

## Memory topics

"Memory topics" identify what information Memory Bank considers to be meaningful.

*   **Managed topics:** Label and instructions are defined by Memory Bank (e.g., `USER_PERSONAL_INFO`, `USER_PREFERENCES`, `KEY_CONVERSATION_DETAILS`, `EXPLICIT_INSTRUCTIONS`).
*   **Custom topics:** Label and instructions are defined by you.

## Triggering memory generation

You can trigger memory generation using `GenerateMemories` at the end of a session or at regular intervals.

```python
AgentEngineGenerateMemoriesOperation(
  name="projects/.../locations/.../reasoningEngines/.../operations/...",
  done=True,
  response=GenerateMemoriesResponse(
    generatedMemories=[
      GenerateMemoriesResponseGeneratedMemory(
        memory=Memory(...),
        action="CREATED", # CREATED, UPDATED, or DELETED
      ),
      ...
    ]
  )
)
```

## Generating memories in the background

`GenerateMemories` is a long-running operation. To run it in the background:

```python
client.agent_engines.memories.generate(
    ...,
    config={
        "wait_for_completion": False
    }
)
```

## Data sources

### Using events in payload as the data source

Use `direct_contents_source` when you want to generate memories using events provided directly in the payload.

```python
events =  [
  {
    "content": {
      "role": "user",
      "parts": [
        {"text": "I work with LLM agents!"}
      ]
    }
  }
]

client.agent_engines.memories.generate(
    name=agent_engine.api_resource.name,
    direct_contents_source={
      "events": EVENTS
    },
    scope=SCOPE,
    config={
        "wait_for_completion": True
    }
)
```

### Using Vertex AI Agent Engine Sessions as the data source

With Agent Engine Sessions, Memory Bank uses session events as the source conversation.

```python
client.agent_engines.memories.generate(
  name=agent_engine.api_resource.name,
  vertex_session_source={
      "session": "SESSION_NAME"
  },
  scope=SCOPE,
  config={
      "wait_for_completion": True
  }
)
```

Optionally, provide a time range:

```python
import datetime

client.agent_engines.memories.generate(
  name=agent_engine.api_resource.name,
  vertex_session_source={
      "session": "SESSION_NAME",
      "start_time": datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(seconds=24 * 60),
      "end_time": datetime.datetime.now(tz=datetime.timezone.utc)
  },
  scope=SCOPE
)
```

### Consolidating pre-extracted memories

You can directly provide pre-extracted memories.

```python
client.agent_engines.memories.generate(
    name=agent_engine.api_resource.name,
    direct_memories_source={"direct_memories": [{"fact": "FACT"}]},
    scope=SCOPE
)
```

## Using multimodal input

Memories can be extracted from images, video, and audio provided by the user.

```python
with open(file_name, "rb") as f:
    inline_data = f.read()

events =  [
  {
    "content": {
      "role": "user",
      "parts": [
        {"text": "This is my dog"},
        {
          "inline_data": {
            "mime_type": "image/jpeg",
            "data": inline_data
          }
        },
        ...
      ]
    }
  }
]
```
