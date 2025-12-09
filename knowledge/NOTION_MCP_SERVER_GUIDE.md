# Notion MCP Server

The Notion MCP Server connects your ADK agent to Notion, allowing it to search, create, and manage pages, databases, and more within a workspace.

## Use cases

*   **Search your workspace:** Find project pages, meeting notes, or documents.
*   **Create new content:** Generate new pages for meeting notes, project plans, or tasks.
*   **Manage tasks and databases:** Update task status, add items, change properties.
*   **Organize your workspace:** Move pages, duplicate templates, add comments.

## Prerequisites

1.  **Obtain a Notion integration token:** Go to Notion Integrations in your profile.
2.  **Grant access:** Ensure relevant pages and databases can be accessed by your integration (Access tab in Notion Integration settings).

## Use with agent

**Local MCP Server:**

```python
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

NOTION_TOKEN = "YOUR_NOTION_TOKEN"

root_agent = Agent(
    model="gemini-2.5-pro",
    name="notion_agent",
    instruction="Help users get information from Notion",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@notionhq/notion-mcp-server",
                    ],
                    env={
                        "NOTION_TOKEN": NOTION_TOKEN,
                    }
                ),
                timeout=30,
            ),
        )
    ],
)
```

## Available tools

*   `notion-search`: Search across your Notion workspace.
*   `notion-fetch`: Retrieves content from a Notion page or database by its URL.
*   `notion-create-pages`: Creates one or more Notion pages.
*   `notion-update-page`: Update a Notion page's properties or content.
*   `notion-move-pages`: Move one or more Notion pages or databases.
*   `notion-duplicate-page`: Duplicate a Notion page.
*   `notion-create-database`: Creates a new Notion database.
*   `notion-update-database`: Update a Notion data source.
*   `notion-create-comment`: Add a comment to a page.
*   `notion-get-comments`: Lists all comments on a specific page.
*   `notion-get-teams`: Retrieves a list of teams.
*   `notion-get-users`: Lists all users in the workspace.
*   `notion-get-user`: Retrieve your user information by ID.
*   `notion-get-self`: Retrieves information about your own bot user.
