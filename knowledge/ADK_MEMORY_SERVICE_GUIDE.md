# Memory: Long-Term Knowledge with MemoryService

**Supported in ADK:** Python v0.1.0, Go v0.1.0, Java v0.2.0

The `MemoryService` allows agents to recall information from past conversations (long-term knowledge), distinct from the short-term `Session` state.

## The MemoryService Role

*   **Ingesting Information (`add_session_to_memory`):** Adds session content to the store.
*   **Searching Information (`search_memory`):** Retrieves relevant snippets based on a query.

## Choosing the Right Memory Service

| Feature | InMemoryMemoryService | VertexAiMemoryBankService |
| :--- | :--- | :--- |
| **Persistence** | None (lost on restart) | Yes (Vertex AI) |
| **Use Case** | Prototyping, testing | Production, evolving memories |
| **Search** | Basic keyword matching | Advanced semantic search |
| **Dependencies** | None | Google Cloud Project, Vertex AI API |

## In-Memory Memory

Best for prototyping.

```python
from google.adk.memory import InMemoryMemoryService
memory_service = InMemoryMemoryService()
```

## Vertex AI Memory Bank

Connects to Vertex AI Memory Bank for persistent, semantic memory.

### Prerequisites

1.  Google Cloud Project with Vertex AI API.
2.  Agent Engine created in Vertex AI.
3.  Authentication (`gcloud auth application-default login`).
4.  Env vars: `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`.

### Configuration

**Via CLI:**
```bash
adk web path/to/agents --memory_service_uri="agentengine://1234567890"
```

**Via Code:**
```python
from google.adk.memory import VertexAiMemoryBankService

memory_service = VertexAiMemoryBankService(
    project="PROJECT_ID",
    location="LOCATION",
    agent_engine_id="AGENT_ENGINE_ID"
)
```

## Using Memory in Your Agent

Use tools or callbacks.

**Tools:**
*   `PreloadMemoryTool`: Retrieves memory at start of turn.
*   `LoadMemoryTool`: Agent decides when to retrieve memory.

```python
from google.adk.agents import Agent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

agent = Agent(
    model=MODEL_ID,
    name='weather_sentiment_agent',
    instruction="...",
    tools=[PreloadMemoryTool()]
)
```

**Auto-save callback:**
```python
async def auto_save_session_to_memory_callback(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session)
```

## Advanced: Using Multiple Services

You can manually instantiate a second service within an agent to combine sources (e.g., chat history + doc knowledge base).

```python
class MultiMemoryAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.memory_service = InMemoryMemoryService()
        self.vertexai_memorybank_service = VertexAiMemoryBankService(...)

    async def run(self, request: types.Content, **kwargs) -> types.Content:
        # Search both
        conv_ctx = await self.memory_service.search_memory(query=...)
        doc_ctx = await self.vertexai_memorybank_service.search_memory(query=...)
        # Combine and generate response...
```
