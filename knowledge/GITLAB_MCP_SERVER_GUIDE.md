# GitLab MCP Server

The GitLab MCP Server connects your ADK agent directly to GitLab.com or your self-managed GitLab instance, enabling issue/MR management, pipeline inspection, and semantic code search.

## Use cases

*   **Semantic Code Exploration:** Navigate codebase using natural language.
*   **Accelerate Merge Request Reviews:** Retrieve MR contexts, analyze diffs, review commit history.
*   **Troubleshoot CI/CD Pipelines:** Diagnose build failures, inspect pipeline statuses, retrieve job logs.

## Prerequisites

1.  **GitLab account:** Premium or Ultimate subscription with GitLab Duo enabled.
2.  **Beta/Experimental features:** Enabled in GitLab settings.

## Use with agent

**Local MCP Server:**

```python
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Replace with your instance URL if self-hosted (e.g., "gitlab.example.com")
GITLAB_INSTANCE_URL = "gitlab.com"

root_agent = Agent(
    model="gemini-2.5-pro",
    name="gitlab_agent",
    instruction="Help users get information from GitLab",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "mcp-remote",
                        f"https://{GITLAB_INSTANCE_URL}/api/v4/mcp",
                        "--static-oauth-client-metadata",
                        "{\"scope\": \"mcp\"}",
                    ],
                ),
                timeout=30,
            ),
        )
    ],
)
```

> **Note:** When run for the first time, a browser window will open requesting OAuth permissions.

## Available tools

*   `get_mcp_server_version`: Returns current server version.
*   `create_issue`: Creates a new issue.
*   `get_issue`: Retrieves detailed issue info.
*   `create_merge_request`: Creates a merge request.
*   `get_merge_request`: Retrieves detailed MR info.
*   `get_merge_request_commits`: Retrieves commits in an MR.
*   `get_merge_request_diffs`: Retrieves diffs for an MR.
*   `get_merge_request_pipelines`: Retrieves pipelines for an MR.
*   `get_pipeline_jobs`: Retrieves jobs for a pipeline.
*   `gitlab_search`: Searches for a term across the instance.
*   `semantic_code_search`: Searches for relevant code snippets (semantic).
