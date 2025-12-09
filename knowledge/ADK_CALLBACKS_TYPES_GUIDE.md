# Types of Callbacks

**Supported in ADK:** Python v0.1.0, Go v0.1.0, Java v0.1.0

## Agent Lifecycle Callbacks

### Before Agent Callback
*   **When:** Before `_run_async_impl`.
*   **Purpose:** Setup, validation, logging entry.
*   **Return Effect:**
    *   `None`: Proceed with agent execution.
    *   `types.Content`: Skip agent execution, use returned content as final response.

### After Agent Callback
*   **When:** After `_run_async_impl` completes.
*   **Purpose:** Cleanup, validation, logging completion, modifying final output.
*   **Return Effect:**
    *   `None`: Use agent's original output.
    *   `types.Content`: Replace agent's output with returned content.

## LLM Interaction Callbacks

### Before Model Callback
*   **When:** Before `generate_content_async`.
*   **Purpose:** Inspect/modify request, guardrails, caching.
*   **Return Effect:**
    *   `None`: Proceed with LLM call.
    *   `LlmResponse`: Skip LLM call, use returned response.

### After Model Callback
*   **When:** After `LlmResponse` received.
*   **Purpose:** Inspect/modify raw LLM response, logging, censoring.
*   **Return Effect:**
    *   `None`: Use original LLM response.
    *   `LlmResponse`: Replace LLM response.

## Tool Execution Callbacks

### Before Tool Callback
*   **When:** Before tool's `run_async`.
*   **Purpose:** Inspect/modify args, authorization, logging, caching.
*   **Return Effect:**
    *   `None`: Execute tool with (potentially modified) args.
    *   `dict`: Skip tool execution, use returned dict as result.

```python
def simple_before_tool_modifier(tool, args, tool_context):
    if tool.name == 'get_capital_city' and args.get('country') == 'Canada':
        args['country'] = 'France' # Modify args
        return None
    if args.get('country') == 'BLOCK':
        return {"result": "Blocked"} # Skip execution
    return None
```

### After Tool Callback
*   **When:** After tool's `run_async`.
*   **Purpose:** Inspect/modify result, post-processing.
*   **Return Effect:**
    *   `None`: Use original tool response.
    *   `dict`: Replace tool response.

```python
def simple_after_tool_modifier(tool, args, tool_context, tool_response):
    if tool.name == 'get_capital_city' and tool_response.get("result") == "Washington, D.C.":
        new_response = deepcopy(tool_response)
        new_response["result"] += " (USA)"
        return new_response # Replace result
    return None
```
