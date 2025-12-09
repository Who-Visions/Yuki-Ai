# State: The Session's Scratchpad

**Supported in ADK:** Python v0.1.0, Go v0.1.0, Java v0.1.0

`session.state` acts as the agent's dedicated scratchpad for a specific interaction, storing key-value pairs for personalization, task progress, and decision making.

## Key Characteristics

*   **Structure:** Serializable Key-Value pairs (Strings keys, basic types values).
*   **Persistence:** Depends on `SessionService` (InMemory is transient, Database/VertexAI are persistent).

## Organizing State with Prefixes

*   **No Prefix (Session State):** Specific to current session. E.g., `current_booking_step`.
*   **`user:` Prefix (User State):** Shared across all sessions for that user. E.g., `user:theme`.
*   **`app:` Prefix (App State):** Shared across all users/sessions. E.g., `app:api_endpoint`.
*   **`temp:` Prefix (Temporary Invocation State):** Discarded after invocation. E.g., `temp:raw_api_response`.

## Accessing Session State in Agent Instructions

*   **Templating:** Use `{key}` in instruction strings. E.g., `"Focus on theme: {topic}"`.
*   **InstructionProvider:** Use a function receiving `ReadonlyContext` to build instructions dynamically or bypass injection.

## How State is Updated: Recommended Methods

1.  **`output_key` (Agent Text Responses):** Save final text response directly to state.
    ```python
    agent = LlmAgent(..., output_key="last_greeting")
    ```
2.  **`EventActions.state_delta` (Complex Updates):** Manually construct delta when creating events.
    ```python
    actions = EventActions(state_delta={"task_status": "active"})
    ```
3.  **Via `CallbackContext` or `ToolContext` (Recommended):**
    ```python
    def my_tool(context: ToolContext):
        context.state["key"] = "value" # Automatically tracked
    ```

## Warning

**Avoid directly modifying `session.state`** on a Session object retrieved from the service outside of a managed context. Always use `append_event` or Context objects to ensure persistence and tracking.
