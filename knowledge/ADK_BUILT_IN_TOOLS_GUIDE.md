# Built-in tools

These built-in tools provide ready-to-use functionality such as Google Search or code executors that provide agents with common capabilities.

## How to Use

1.  **Import:** Import the desired tool from the tools module.
2.  **Configure:** Initialize the tool, providing required parameters if any.
3.  **Register:** Add the initialized tool to the `tools` list of your Agent.

## Available Built-in tools

### Google Search

The `google_search` tool allows the agent to perform web searches using Google Search. Compatible with Gemini 2 models.

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

root_agent = Agent(
    name="basic_search_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions using Google Search.",
    instruction="I can answer your questions by searching the internet. Just ask me anything!",
    tools=[google_search]
)
```

### Code Execution

The `built_in_code_execution` tool enables the agent to execute code, specifically when using Gemini 2 models.

```python
from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor

code_agent = LlmAgent(
    name="calculator_agent",
    model="gemini-2.0-flash",
    code_executor=BuiltInCodeExecutor(),
    instruction="You are a calculator agent...",
    description="Executes Python code to perform calculations.",
)
```

### GKE Code Executor

The GKE Code Executor (`GkeCodeExecutor`) provides a secure and scalable method for running LLM-generated code by leveraging the GKE Sandbox environment.

```python
from google.adk.agents import LlmAgent
from google.adk.code_executors import GkeCodeExecutor

gke_executor = GkeCodeExecutor(
    namespace="agent-sandbox",
    timeout_seconds=600,
    cpu_limit="1000m",
    mem_limit="1Gi",
)

gke_agent = LlmAgent(
    name="gke_coding_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful AI agent that writes and executes Python code.",
    code_executor=gke_executor,
)
```

### Vertex AI RAG Engine

The `vertex_ai_rag_retrieval` tool allows the agent to perform private data retrieval using Vertex AI RAG Engine.

```python
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

ask_vertex_retrieval = VertexAiRagRetrieval(
    name='retrieve_rag_documentation',
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ.get("RAG_CORPUS")
        )
    ],
)
```

### Vertex AI Search

The `vertex_ai_search_tool` uses Google Cloud Vertex AI Search.

```python
from google.adk.tools import VertexAiSearchTool

vertex_search_tool = VertexAiSearchTool(data_store_id="DATASTORE_PATH_HERE")

doc_qa_agent = LlmAgent(
    name="doc_qa_agent",
    model="gemini-2.0-flash",
    tools=[vertex_search_tool],
    # ...
)
```

### BigQuery

Tools for BigQuery integration: `list_dataset_ids`, `get_dataset_info`, `list_table_ids`, `get_table_info`, `execute_sql`, `forecast`, `ask_data_insights`.

```python
from google.adk.tools.bigquery import BigQueryToolset

bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config, bigquery_tool_config=tool_config
)

bigquery_agent = Agent(
    model="gemini-2.0-flash",
    tools=[bigquery_toolset],
    # ...
)
```

### Spanner

Tools for Spanner integration: `list_table_names`, `list_table_indexes`, `list_table_index_columns`, `list_named_schemas`, `get_table_schema`, `execute_sql`, `similarity_search`.

```python
from google.adk.tools.spanner.spanner_toolset import SpannerToolset

spanner_toolset = SpannerToolset(
    credentials_config=credentials_config, spanner_tool_settings=tool_settings
)

spanner_agent = Agent(
    model="gemini-2.5-flash",
    tools=[spanner_toolset],
    # ...
)
```

### Bigtable

Tools for Bigtable integration: `list_instances`, `get_instance_info`, `list_tables`, `get_table_info`, `execute_sql`.

```python
from google.adk.tools.bigtable.bigtable_toolset import BigtableToolset

bigtable_toolset = BigtableToolset(
    credentials_config=credentials_config, bigtable_tool_settings=tool_settings
)

bigtable_agent = Agent(
    model="gemini-2.5-flash",
    tools=[bigtable_toolset],
    # ...
)
```

## Use Built-in tools with other tools

Demonstrates how to use multiple built-in tools or how to use built-in tools with other tools by using multiple agents.

```python
from google.adk.tools.agent_tool import AgentTool

root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    tools=[AgentTool(agent=search_agent), AgentTool(agent=coding_agent)],
)
```

## Limitations

*   Currently, for each root agent or single agent, only one built-in tool is supported.
*   Built-in tools cannot be used within a sub-agent (with exceptions for GoogleSearchTool and VertexAiSearchTool in ADK Python).
