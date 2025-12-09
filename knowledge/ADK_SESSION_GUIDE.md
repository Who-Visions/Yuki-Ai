# Session: Tracking Individual Conversations

**Supported in ADK:** Python v0.1.0, Go v0.1.0, Java v0.1.0

`Session` tracks individual conversation threads, holding history (`events`) and temporary data (`state`).

## The Session Object

*   **Identification:** `id`, `app_name`, `user_id`.
*   **History (`events`):** Chronological sequence of interactions.
*   **State (`state`):** Temporary scratchpad for the interaction.
*   **Activity (`lastUpdateTime`):** Timestamp of last event.

## SessionService Implementations

The `SessionService` manages the lifecycle (create, resume, save, delete).

### InMemorySessionService
*   **Persistence:** None (lost on restart).
*   **Best for:** Prototyping, testing.

```python
from google.adk.sessions import InMemorySessionService
session_service = InMemorySessionService()
```

### VertexAiSessionService
*   **Persistence:** Yes (Vertex AI Agent Engine).
*   **Best for:** Production on Google Cloud.

```python
from google.adk.sessions import VertexAiSessionService
session_service = VertexAiSessionService(project="PROJECT_ID", location="LOCATION")
```

### DatabaseSessionService
*   **Persistence:** Yes (SQL Database).
*   **Best for:** Self-managed persistence.

```python
from google.adk.sessions import DatabaseSessionService
session_service = DatabaseSessionService(db_url="sqlite:///./my_agent_data.db")
```

## The Session Lifecycle

1.  **Start/Resume:** `sessionService.create_session` or retrieve by ID.
2.  **Context:** Runner provides Session to agent.
3.  **Processing:** Agent generates response/state updates.
4.  **Save:** Runner calls `sessionService.append_event` (updates history and state).
5.  **End:** `sessionService.delete_session` (cleanup).
