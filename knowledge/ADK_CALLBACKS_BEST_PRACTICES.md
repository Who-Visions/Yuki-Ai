# Design Patterns and Best Practices for Callbacks

**Supported in ADK:** Python v0.1.0, Go v0.1.0, Java v0.1.0

## Design Patterns

1.  **Guardrails & Policy Enforcement:**
    *   Use `before_model_callback` or `before_tool_callback`.
    *   Return predefined response if violation detected.

2.  **Dynamic State Management:**
    *   Read/Write `context.state`.
    *   Pass data between steps (e.g., tool result to agent greeting).

3.  **Logging and Monitoring:**
    *   Log agent name, tool name, invocation ID, args.

4.  **Caching:**
    *   **Before:** Check cache in `before_` callback. Return cached result if hit.
    *   **After:** Store result in cache in `after_` callback if miss.

5.  **Request/Response Modification:**
    *   Modify `llm_request`, `LlmResponse`, tool args, or tool response.

6.  **Conditional Skipping of Steps:**
    *   Return value from `before_` callback to skip execution.

7.  **Tool-Specific Actions:**
    *   **Auth:** Call `tool_context.request_credential`.
    *   **Summarization:** Set `tool_context.actions.skip_summarization = True`.

8.  **Artifact Handling:**
    *   Use `save_artifact` / `load_artifact` for files/blobs.

## Best Practices

*   **Design Principles:** Keep focused, mind performance (avoid blocking).
*   **Error Handling:** Handle errors gracefully, don't crash process.
*   **State Management:** Use specific keys, prefixes (`user:`, `app:`).
*   **Reliability:** Idempotency for side effects.
*   **Testing:** Unit test with mocks, integration tests.
