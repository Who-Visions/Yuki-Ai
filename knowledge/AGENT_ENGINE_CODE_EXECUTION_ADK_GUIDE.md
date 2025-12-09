# Code Execution Tool with Agent Engine

> **Preview**
>
> The Agent Engine Code Execution feature is a Preview release. For more information, see the launch stage descriptions.

The Agent Engine Code Execution ADK Tool provides a low-latency, highly efficient method for running AI-generated code using the Google Cloud Agent Engine service.

## Use the Tool

1.  **Create a sandbox environment** (see Agent Engine Code Execution quickstart).
2.  **Create an ADK agent** with `AgentEngineSandboxCodeExecutor`.

```python
from google.adk.agents.llm_agent import Agent
from google.adk.code_executors.agent_engine_sandbox_code_executor import AgentEngineSandboxCodeExecutor

root_agent = Agent(
    model="gemini-2.5-flash",
    name="agent_engine_code_execution_agent",
    instruction="You are a helpful agent that can write and execute code...",
    code_executor=AgentEngineSandboxCodeExecutor(
        sandbox_resource_name="SANDBOX_RESOURCE_NAME",
    ),
)
```

## How it works

*   **Sandbox creation:** Automatically creates a sandbox if not pre-created.
*   **Code execution with persistence:** State persists across operations within a session.
*   **Result retrieval:** Captures stdout and stderr.
*   **Sandbox clean up:** Explicit delete or TTL.

## Configuration parameters

*   `sandbox_resource_name`: Path to an existing sandbox.
    *   Format: `projects/{$PROJECT_ID}/locations/{$LOCATION_ID}/reasoningEngines/{$REASONING_ENGINE_ID}/sandboxEnvironments/{$SANDBOX_ENVIRONMENT_ID}`
*   `agent_engine_resource_name`: Agent Engine resource name to create a new sandbox.
    *   Format: `projects/{$PROJECT_ID}/locations/{$LOCATION_ID}/reasoningEngines/{$REASONING_ENGINE_ID}`

## Advanced example

Includes recommended system instructions for code execution.

```python
from google.adk.agents.llm_agent import Agent
from google.adk.code_executors.agent_engine_sandbox_code_executor import AgentEngineSandboxCodeExecutor

def base_system_instruction():
  return """
  # Guidelines
  **Objective:** Assist the user in achieving their data analysis goals...
  **Code Execution:** All code snippets provided will be executed within the sandbox environment.
  **Statefulness:** All code snippets are executed and the variables stays in the environment...
  **Output Visibility:** Always print the output of code execution...
  """

root_agent = Agent(
    model="gemini-2.5-flash",
    name="agent_engine_code_execution_agent",
    instruction=base_system_instruction() + "...",
    code_executor=AgentEngineSandboxCodeExecutor(
        sandbox_resource_name="SANDBOX_RESOURCE_NAME",
    ),
)
```
