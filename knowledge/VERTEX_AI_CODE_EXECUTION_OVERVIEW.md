# Agent Engine Code Execution

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

Agent Engine Code Execution lets your agent run code in a secure, isolated, and managed sandbox environment.

## Features

*   **Speed:** Sandboxes can be created and execute code in under a second.
*   **File I/O:** Sandboxes support file input and output up to 100MB for the entire request or response.
*   **State persistence:** Sandboxes maintain their execution state (memory) for up to 14 days (configurable TTL).

**Note:** Agent Engine Code Execution is supported in only the `us-central1` region.

## Operations

*   **Create sandbox:** Creates a secure, isolated space to run untrusted code.
*   **Get sandbox:** Shows the configuration and status of a specific sandbox.
*   **List sandboxes:** Lists all sandboxes in your project.
*   **Execute code:** Sends code and input files to the sandbox for execution. The sandbox maintains state across calls.
