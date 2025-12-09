# ADK Context

**Supported in ADK:** Python v0.1.0, Go v0.1.0, Java v0.1.0

"Context" refers to the bundle of information available to your agent and tools during operations (state, services, identity, etc.).

## The Different types of Context

### InvocationContext
*   **Where Used:** `_run_async_impl`, `_run_live_impl`.
*   **Purpose:** Access entire state of current invocation. Most comprehensive.
*   **Key Contents:** Session, agent instance, `invocation_id`, services.

### ReadonlyContext
*   **Where Used:** Instruction providers.
*   **Purpose:** Safe, read-only view.
*   **Key Contents:** `invocation_id`, `agent_name`, read-only state.

### CallbackContext
*   **Where Used:** Agent/Model callbacks (`before_agent_callback`, etc.).
*   **Purpose:** Inspect/modify state, interact with artifacts in callbacks.
*   **Key Capabilities:** Mutable `state`, `load_artifact`, `save_artifact`.

### ToolContext
*   **Where Used:** Tool functions, tool callbacks.
*   **Purpose:** Tool execution specifics.
*   **Key Capabilities:** Auth (`request_credential`), Artifact listing (`list_artifacts`), Memory search (`search_memory`), `function_call_id`.

## Common Tasks

### Accessing Information
*   **Reading State:** `tool_context.state.get("key")`
*   **Identifiers:** `tool_context.invocation_id`, `tool_context.function_call_id`

### Managing State
*   **Writing State:** `context.state['key'] = value` (persisted via `state_delta`).
*   **Passing Data:** Tool 1 writes to state, Tool 2 reads from state.
*   **Prefixes:** `app:`, `user:`, `temp:` for scoping.

### Working with Artifacts
*   **Save:** `context.save_artifact("name", part)` (stores reference/blob).
*   **Load:** `context.load_artifact("name")`.
*   **List:** `tool_context.list_artifacts()`.

### Handling Tool Authentication
*   **Request:** `tool_context.request_credential(auth_config)`.
*   **Retrieve:** `tool_context.get_auth_response(auth_config)`.

### Leveraging Memory
*   **Search:** `tool_context.search_memory(query)`.

### Direct InvocationContext Usage
*   **End Invocation:** `ctx.end_invocation = True`.
