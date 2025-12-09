# Callbacks: Observe, Customize, and Control Agent Behavior

**Supported in ADK:** Python v0.1.0, Go v0.1.0, Java v0.1.0

Callbacks allow you to hook into an agent's execution process to observe, customize, and control behavior without modifying the core framework.

## Key Checkpoints

1.  **Agent:** `before_agent` (before main work), `after_agent` (after result prepared).
2.  **Model (LLM):** `before_model` (before request sent), `after_model` (after response received).
3.  **Tool:** `before_tool` (before execution), `after_tool` (after execution).

## The Callback Mechanism: Interception and Control

Callbacks receive context objects (`CallbackContext`, `ToolContext`) and can influence flow via their return value.

### `return None` (Allow Default Behavior)
Signals that the callback has finished work (logging, inspection) and the ADK should proceed normally.
*   **Before:** Next step (agent logic, LLM call, tool exec) occurs.
*   **After:** Result just produced is used as is.

### `return <Specific Object>` (Override Default Behavior)
Overrides default behavior, skipping the next step or replacing the result.

*   **`before_agent_callback` → `types.Content`:** Skips agent logic. Returned Content is final output.
*   **`before_model_callback` → `LlmResponse`:** Skips LLM call. Returned response is used (e.g., cache/guardrail).
*   **`before_tool_callback` → `dict`:** Skips tool execution. Returned dict is tool result.
*   **`after_agent_callback` → `types.Content`:** Replaces agent's produced Content.
*   **`after_model_callback` → `LlmResponse`:** Replaces LLM's response.
*   **`after_tool_callback` → `dict`:** Replaces tool's result.

## Why use them?
*   **Observe & Debug:** Log info.
*   **Customize & Control:** Modify data or bypass steps.
*   **Implement Guardrails:** Enforce safety.
*   **Manage State:** Read/update session state.
