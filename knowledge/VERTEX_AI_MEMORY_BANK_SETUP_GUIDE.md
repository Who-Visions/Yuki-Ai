# Set up Memory Bank

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

To use Vertex AI Agent Engine Memory Bank, you need an Vertex AI Agent Engine instance. This page demonstrates how to set up your environment and create an Vertex AI Agent Engine instance.

## Getting started

Before you work with Vertex AI Agent Engine Memory Bank, you must set up your environment.

### Set up your Google Cloud project

1.  **Select or create a Google Cloud project:** In the Google Cloud console, on the project selector page, select or create a Google Cloud project.
2.  **Verify billing:** Verify that billing is enabled for your Google Cloud project.
3.  **Enable the Vertex AI API:** Enable the Vertex AI API.

### Get the required roles

Ask your administrator to grant you the **Vertex AI User (`roles/aiplatform.user`)** IAM role on your project.

If you're making requests to Memory Bank from an agent deployed on Google Kubernetes Engine or Cloud Run, make sure that your service account has the necessary permissions. The Reasoning Engine Service Agent already has the necessary permissions to read and write memories.

### Install libraries

Install the Vertex AI SDK:

```bash
pip install google-cloud-aiplatform>=1.111.0
```

### Authentication

*   **Not using Express Mode:** Follow the instructions at Authenticate to Vertex AI.
*   **Using Express Mode:** Set up authentication by setting the API key in the environment:
    ```python
    os.environ["GOOGLE_API_KEY"] = "API_KEY"
    ```

### Set up a Vertex AI SDK client

```python
import vertexai

client = vertexai.Client(
    project="PROJECT_ID",
    location="LOCATION",
)
```
*   `PROJECT_ID`: Your Google Cloud project ID.
*   `LOCATION`: One of the supported regions for Memory Bank.

## Create or update an Agent Engine instance

To get started with Memory Bank, you first need an Agent Engine instance.

```python
agent_engine = client.agent_engines.create()

# Optionally, print out the Agent Engine resource name.
print(agent_engine.api_resource.name)
```

Once you have an Agent Engine instance, you can use the name of the instance to read or write memories.

```python
# Generate memories using your Memory Bank instance.
client.agent_engines.memories.generate(
  # `name` should have the format `projects/.../locations/.../reasoningEngines/...`.
  name=agent_engine.api_resource.name,
  ...
)
```

## Use with Vertex AI Agent Engine Runtime

You can use Memory Bank with Agent Engine Runtime to read and write memories from your deployed agent.

### AdkApp

If you're using the Agent Engine Agent Development Kit template, the agent uses the `VertexAiMemoryBankService` by default when deployed to Agent Engine Runtime.

```python
from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp

# Develop an agent using the ADK template.
agent = Agent(...)

adk_app = AdkApp(
      agent=adk_agent,
      ...
)

# Deploy the agent to Agent Engine Runtime.
agent_engine = client.agent_engines.create(
      agent_engine=adk_app,
      config={
            "staging_bucket": "STAGING_BUCKET",
            "requirements": ["google-cloud-aiplatform[agent_engines,adk]"],
            # Optional.
            **context_spec
      }
)
```

## Use in all other runtimes

If you want to use Memory Bank in a different environment, like Cloud Run or Colab, create an Agent Engine without providing an agent.

```python
agent_engine = client.agent_engines.create()
```

If you want to configure behavior, provide a Memory Bank configuration:

```python
agent_engine = client.agent_engines.create(
  config={
    "context_spec": {
      "memory_bank_config": ...
    }
  }
)
```

## Configure your Agent Engine instance for Memory Bank

You can configure your Memory Bank to customize how memories are generated and managed.

```python
client.agent_engines.create(
      ...,
      config={
            "context_spec": {
                  "memory_bank_config": memory_bank_config
            }
      }
)
```

You can configure the following settings:

*   **Customization configuration:** Configures how memories should be extracted.
*   **Similarity search configuration:** Configures which embedding model is used. Defaults to `text-embedding-005`.
*   **Generation configuration:** Configures which LLM is used. Defaults to `gemini-2.5-flash`.
*   **TTL configuration:** Configures how TTL is automatically set. Defaults to no TTL.

### Customization configuration

Customize how memories are extracted using **Memory topics** and **Few-shot examples**.

#### Configuring memory topics

*   **Managed topics:** Label and instructions are defined by Memory Bank (e.g., `USER_PERSONAL_INFO`, `USER_PREFERENCES`, `KEY_CONVERSATION_DETAILS`, `EXPLICIT_INSTRUCTIONS`).
*   **Custom topics:** Label and instructions are defined by you.

Example using managed and custom topics:

```python
customization_config = {
  "memory_topics": [
    { "managed_memory_topic": { "managed_topic_enum": "USER_PERSONAL_INFO" } },
    {
      "custom_memory_topic": {
        "label": "business_feedback",
        "description": "Specific user feedback about their experience..."
        }
    }
  ]
}
```

#### Few-shot examples

Demonstrate expected memory extraction behavior.

```python
example = {
    "conversationSource": {
      "events": [
        { "content": { "role": "model", "parts": [{ "text": "Welcome..." }] } },
        { "content": { "role": "user", "parts": [{ "text": "The coffee was lukewarm..." }] } }
      ]
    },
    "generatedMemories": [
      { "fact": "The user reported that the drip coffee was lukewarm." }
    ]
}
```

### Similarity search configuration

```python
memory_bank_config = {
    "similarity_search_config": {
        "embedding_model": "EMBEDDING_MODEL",
    }
}
```

### Generation configuration

```python
memory_bank_config = {
      "generation_config": {
            "model": "LLM_MODEL",
      }
}
```

### Time to live (TTL) configuration

*   **Default TTL:** Applied to all operations.
    ```python
    memory_bank_config = {
        "ttl_config": {
            "default_ttl": f"TTLs"
        }
    }
    ```
*   **Granular (per-operation) TTL:** Calculated based on the operation.
    ```python
    memory_bank_config = {
        "ttl_config": {
            "granular_ttl": {
                "create_ttl": f"CREATE_TTLs",
                "generate_created_ttl": f"GENERATE_CREATED_TTLs",
                "generate_updated_ttl": f"GENERATE_UPDATED_TTLs"
            }
        }
    }
    ```
