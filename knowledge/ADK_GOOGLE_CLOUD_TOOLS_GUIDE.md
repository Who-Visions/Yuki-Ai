# Google Cloud Tools

Google Cloud tools make it easier to connect your agents to Google Cloud’s products and services.

## Apigee API Hub Tools

**Supported in ADK:** Python v0.1.0

`ApiHubToolset` lets you turn any documented API from Apigee API hub into a tool with a few lines of code.

### Prerequisites

1.  Install ADK.
2.  Install the Google Cloud CLI.
3.  Apigee API hub instance with documented (i.e. OpenAPI spec) APIs.

### Create an API Hub Toolset

**Get your access token:**

```bash
gcloud auth print-access-token
```

**Create a tool with APIHubToolset:**

```python
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
from google.adk.tools.apihub_tool.apihub_toolset import APIHubToolset

# Provide authentication for your APIs.
auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey", "query", "apikey", apikey_credential_str
)

sample_toolset = APIHubToolset(
    name="apihub-sample-tool",
    description="Sample Tool",
    access_token="...",  # Copy your access token
    apihub_resource_name="...", # API Hub resource name
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
)
```

**Create your agent file:**

```python
from google.adk.agents.llm_agent import LlmAgent
from .tools import sample_toolset

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='enterprise_assistant',
    instruction='Help user, leverage the tools you have access to',
    tools=sample_toolset.get_tools(),
)
```

## Application Integration Tools

**Supported in ADK:** Python v0.1.0, Java v0.3.0

With `ApplicationIntegrationToolset`, you can seamlessly give your agents secure and governed access to enterprise applications using Integration Connectors' 100+ pre-built connectors.

### Prerequisites

1.  **Install ADK**
2.  **Install CLI:**
    ```bash
    gcloud config set project <project-id>
    gcloud auth application-default login
    gcloud auth application-default set-quota-project <project-id>
    ```
3.  **Provision Application Integration workflow and publish Connection Tool.**
4.  **Create project structure.**
5.  **Set roles and permissions:**
    *   `roles/integrations.integrationEditor`
    *   `roles/connectors.invoker`
    *   `roles/secretmanager.secretAccessor`

### Use Integration Connectors

**Create an Application Integration Toolset:**

```python
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset

connector_tool = ApplicationIntegrationToolset(
    project="test-project",
    location="us-central1",
    connection="test-connection",
    entity_operations={"Entity_One": ["LIST","CREATE"], "Entity_Two": []},
    actions=["action1"],
    service_account_json='{...}',
    tool_name_prefix="tool_prefix2",
    tool_instructions="..."
)
```

**Update the agent.py file:**

```python
from google.adk.agents.llm_agent import LlmAgent
from .tools import connector_tool

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='connector_agent',
    instruction="Help user, leverage the tools you have access to",
    tools=[connector_tool],
)
```

### Use Application Integration Workflows

**Create a tool:**

```python
integration_tool = ApplicationIntegrationToolset(
    project="test-project",
    location="us-central1",
    integration="test-integration",
    triggers=["api_trigger/test_trigger"],
    service_account_json='{...}',
    tool_name_prefix="tool_prefix1",
    tool_instructions="..."
)
```

**Add the tool to your agent:**

```python
from google.adk.agents.llm_agent import LlmAgent
from .tools import integration_tool, connector_tool

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='integration_agent',
    instruction="Help user, leverage the tools you have access to",
    tools=[integration_tool],
)
```
