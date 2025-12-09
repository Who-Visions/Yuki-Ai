# BigQuery Agent Analytics Plugin

> **Preview**
>
> The BigQuery Agent Analytics Plugin is in Preview release. For more information, see the launch stage descriptions.

The BigQuery Agent Analytics Plugin enhances the ADK by providing a robust solution for in-depth agent behavior analysis using the BigQuery Storage Write API.

## Use cases

*   **Agent workflow debugging and analysis:** Capture lifecycle events (LLM calls, tool usage, etc.).
*   **High-volume analysis and debugging:** Asynchronous logging to avoid blocking execution.

## Prerequisites

1.  **Google Cloud Project** with BigQuery API enabled.
2.  **BigQuery Dataset:** Create a dataset (e.g., `agent_events` table created automatically).
3.  **Authentication:** `gcloud auth application-default login` or service account.

## IAM permissions

*   `roles/bigquery.jobUser` (Project Level)
*   `roles/bigquery.dataEditor` (Table/Dataset Level)

## Use with agent

```python
import os
import google.auth
from google.adk.apps import App
from google.adk.plugins.bigquery_agent_analytics_plugin import BigQueryAgentAnalyticsPlugin
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig

# ... (Configuration and Env Vars) ...

# --- Initialize the Plugin ---
bq_logging_plugin = BigQueryAgentAnalyticsPlugin(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    table_id="agent_events"
)

# ... (Initialize Tools and Model) ...

# --- Create the App ---
app = App(
    name="my_bq_agent",
    root_agent=root_agent,
    plugins=[bq_logging_plugin], # Register the plugin here
)
```

## Configuration options

Customize using `BigQueryLoggerConfig`:

```python
from google.adk.plugins.bigquery_agent_analytics_plugin import BigQueryLoggerConfig

config = BigQueryLoggerConfig(
    enabled=True,
    event_allowlist=["LLM_REQUEST", "LLM_RESPONSE"],
    shutdown_timeout=10.0,
    client_close_timeout=2.0,
    max_content_length=500,
    content_formatter=redact_dollar_amounts,
)

plugin = BigQueryAgentAnalyticsPlugin(..., config=config)
```

## Schema and production setup

Recommended DDL for production:

```sql
CREATE TABLE `your-gcp-project-id.adk_agent_logs.agent_events`
(
  timestamp TIMESTAMP NOT NULL OPTIONS(description="The UTC time at which the event was logged."),
  event_type STRING OPTIONS(description="Indicates the type of event being logged (e.g., 'LLM_REQUEST', 'TOOL_COMPLETED')."),
  agent STRING OPTIONS(description="The name of the ADK agent or author associated with the event."),
  session_id STRING OPTIONS(description="A unique identifier to group events within a single conversation or user session."),
  invocation_id STRING OPTIONS(description="A unique identifier for each individual agent execution or turn within a session."),
  user_id STRING OPTIONS(description="The identifier of the user associated with the current session."),
  content STRING OPTIONS(description="The event-specific data (payload). Format varies by event_type."),
  error_message STRING OPTIONS(description="Populated if an error occurs during the processing of the event."),
  is_truncated BOOLEAN OPTIONS(description="Boolean flag indicates if the content field was truncated due to size limits.")
)
PARTITION BY DATE(timestamp)
CLUSTER BY event_type, agent, user_id;
```

## Event types

*   **LLM interactions:** `LLM_REQUEST`, `LLM_RESPONSE`, `LLM_ERROR`
*   **Tool usage:** `TOOL_STARTING`, `TOOL_COMPLETED`, `TOOL_ERROR`
*   **Agent lifecycle:** `INVOCATION_STARTING`, `INVOCATION_COMPLETED`, `AGENT_STARTING`, `AGENT_COMPLETED`
*   **User and generic events:** `USER_MESSAGE_RECEIVED`, `TOOL_CALL`, `TOOL_RESULT`, `MODEL_RESPONSE`

## Advanced analysis queries

**Trace a specific conversation turn:**
```sql
SELECT timestamp, event_type, agent, content
FROM `your-gcp-project-id.your-dataset-id.agent_events`
WHERE invocation_id = 'your-invocation-id'
ORDER BY timestamp ASC;
```

**Daily invocation volume:**
```sql
SELECT DATE(timestamp) as log_date, COUNT(DISTINCT invocation_id) as count
FROM `your-gcp-project-id.your-dataset-id.agent_events`
WHERE event_type = 'INVOCATION_STARTING'
GROUP BY log_date ORDER BY log_date DESC;
```
