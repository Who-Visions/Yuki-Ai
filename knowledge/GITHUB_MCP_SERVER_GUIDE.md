# GitHub MCP Server

The GitHub MCP Server connects AI tools directly to GitHub's platform, enabling repository management, issue/PR automation, and code analysis.

## Use cases

*   **Repository Management:** Browse code, search files, analyze commits.
*   **Issue & PR Automation:** Create/manage issues and PRs.
*   **Code Analysis:** Security findings, Dependabot alerts, code patterns.

## Prerequisites

1.  **Create a Personal Access Token (PAT)** in GitHub.

## Use with agent

**Remote MCP Server:**

```python
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"

root_agent = Agent(
    model="gemini-2.5-pro",
    name="github_agent",
    instruction="Help users get information from GitHub",
    tools=[
        McpToolset(
            connection_params=StreamableHTTPServerParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "X-MCP-Toolsets": "all",
                    "X-MCP-Readonly": "true"
                },
            ),
        )
    ],
)
```

## Available tools

*   `context`: User/GitHub context.
*   `copilot`: Copilot related tools.
*   `copilot_spaces`: Copilot Spaces tools.
*   `actions`: GitHub Actions workflows.
*   `code_security`: Code scanning.
*   `dependabot`: Dependabot tools.
*   `discussions`: GitHub Discussions.
*   `experiments`: Experimental features.
*   `gists`: GitHub Gist tools.
*   `github_support_docs_search`: Search support docs.
*   `issues`: GitHub Issues.
*   `labels`: GitHub Labels.
*   `notifications`: GitHub Notifications.
*   `orgs`: GitHub Organizations.
*   `projects`: GitHub Projects.
*   `pull_requests`: GitHub Pull Requests.
*   `repos`: GitHub Repositories.
*   `secret_protection`: Secret scanning.
*   `security_advisories`: Security advisories.
*   `stargazers`: GitHub Stargazers.
*   `users`: GitHub Users.

## Configuration

Optional headers for Remote GitHub MCP server:

*   `X-MCP-Toolsets`: Comma-separated list of toolsets to enable (e.g., "repos,issues"). Default is all.
*   `X-MCP-Readonly`: Enables only "read" tools. Default is false.
