# Evaluate agents using the GenAI Client in Vertex AI SDK

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

You can use the Gen AI evaluation service to evaluate the agent's ability to complete tasks and goals for a given use case.

## Before you begin

1.  Select or create a Google Cloud project.
2.  Verify billing is enabled.
3.  Install the Vertex AI SDK:
    ```bash
    %pip install google-cloud-aiplatform[adk,agent_engines]
    %pip install --upgrade --force-reinstall -q google-cloud-aiplatform[evaluation]
    ```
4.  Initialize the GenAI Client:
    ```python
    import vertexai
    from vertexai import Client
    from google.genai import types as genai_types

    vertexai.init(project=PROJECT_ID, location=LOCATION)
    client = Client(
        project=PROJECT_ID,
        location=LOCATION,
        http_options=genai_types.HttpOptions(api_version="v1beta1"),
    )
    ```

## Develop an agent

```python
from google.adk import Agent

# Define Agent Tools (e.g., search_products, get_product_details, add_to_cart)
# ...

# Define Agent
my_agent = Agent(
    model="gemini-2.5-flash",
    name='ecommerce_agent',
    instruction='You are an ecommerce expert',
    tools=[search_products, get_product_details, add_to_cart],
)
```

## Deploy agent

```python
def deploy_adk_agent(root_agent):
  app = vertexai.agent_engines.AdkApp(agent=root_agent)
  remote_app = client.agent_engines.create(
      agent=app,
      config = {
          "staging_bucket": gs://BUCKET_NAME,
          "requirements": ['google-cloud-aiplatform[adk,agent_engines]'],
          "env_vars": {"GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY": "true"}
      }
  )
  return remote_app

agent_engine = deploy_adk_agent(my_agent)
agent_engine_resource_name = agent_engine.api_resource.name
```

## Generate responses

1.  **Prepare your dataset:**
    ```python
    import pandas as pd
    from vertexai import types

    session_inputs = types.evals.SessionInput(user_id="user_123", state={})
    agent_prompts = ["Search for 'noise-cancelling headphones'.", ...]
    agent_dataset = pd.DataFrame({
        "prompt": agent_prompts,
        "session_inputs": [session_inputs] * len(agent_prompts),
    })
    ```
2.  **Run inference:**
    ```python
    agent_dataset_with_inference = client.evals.run_inference(
        agent=agent_engine_resource_name,
        src=agent_dataset,
    )
    ```

## Run the agent evaluation

1.  **Retrieve agent info:**
    ```python
    agent_info = types.evals.AgentInfo.load_from_agent(
        my_agent,
        agent_engine_resource_name
    )
    ```
2.  **Create evaluation run:**
    ```python
    evaluation_run = client.evals.create_evaluation_run(
        dataset=agent_dataset_with_inference,
        agent_info=agent_info,
        metrics=[
            types.RubricMetric.FINAL_RESPONSE_QUALITY,
            types.RubricMetric.TOOL_USE_QUALITY,
            types.RubricMetric.HALLUCINATION,
            types.RubricMetric.SAFETY,
        ],
        dest=GCS_DEST,
    )
    ```

## View the agent evaluation results

```python
evaluation_run = client.evals.get_evaluation_run(
    name=evaluation_run.name,
    include_evaluation_items=True
)

evaluation_run.show()
```
