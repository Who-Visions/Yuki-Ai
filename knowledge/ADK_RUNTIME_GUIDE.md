# ADK Runtime

**Supported in ADK:** Python v0.1.0, Go v0.1.0, Java v0.1.0

The ADK Runtime is the engine that powers your agent application, orchestrating agents, tools, and callbacks in an Event Loop.

## Core Idea: The Event Loop

The Runtime operates on a back-and-forth communication between the **Runner** and your **Execution Logic** (Agents, Tools, Callbacks).

1.  **Runner** receives a query and starts the Agent.
2.  **Agent** runs until it yields an **Event** (response, tool call, state change).
3.  **Runner** processes the Event (commits state changes via Services) and forwards it.
4.  **Agent** resumes execution.

## Key Components

*   **Runner:** The orchestrator. Manages the loop, coordinates with Services, and drives the conversation.
*   **Execution Logic:**
    *   **Agent:** Primary logic units (e.g., `LlmAgent`).
    *   **Tools:** External capabilities.
    *   **Callbacks:** Hooks into execution flow.
*   **Event:** The message passed between Runner and Logic. Carries content and actions (side effects).
*   **Services:** Backend persistence (SessionService, ArtifactService, MemoryService).
*   **Session:** Container for state and history of a conversation.
*   **Invocation:** Everything happening in response to a single user query.

## Important Runtime Behaviors

### State Updates & Commitment Timing
State changes (e.g., `context.state['key'] = 'val'`) are locally recorded but only **committed** (persisted) after the Event carrying the `state_delta` is yielded and processed by the Runner. Code resuming after a yield can rely on the committed state.

### "Dirty Reads"
Code running *before* a yield can see local, uncommitted changes ("dirty reads"). This allows coordination within a step but carries risk if the invocation fails before commitment.

### Streaming vs. Non-Streaming
*   **Streaming:** LLM yields multiple `partial=True` events. Runner forwards them but only processes/commits on the final `partial=False` event.
*   **Non-Streaming:** Single non-partial event, fully processed.

### Async is Primary
The Runtime is built on asynchronous libraries (asyncio, RxJava). `Runner.run_async` is the primary entry point.
