# Deployment Plan: Yuki Agent (Gemini 3 Pro)

This plan outlines the steps to deploy the Yuki Agent using the new `gemini-3-pro-preview` model on Vertex AI Reasoning Engine.

## User Requirements
- **Model**: `gemini-3-pro-preview` (Confirmed via `GEMINI_3_PRO_GUIDE.md`)
- **Location**: User requested "Global".
    - *Technical Note*: While `gemini-3-pro-preview` is available globally, the **Reasoning Engine** service itself (where the agent code runs) requires a specific region (e.g., `us-central1`, `europe-west4`).
    - *Decision*: We will use `us-central1` for the `vertexai.init` location to ensure the Reasoning Engine resource can be created. The model will still be accessed globally.
- **Environment**: Google Cloud Shell.

## Files to Update (in Cloud Shell)

### 1. `deploy.py`
- **Model ID**: Update to `gemini-3-pro-preview`.
- **Location**: Set to `us-central1`.
- **Requirements**: Ensure `google-cloud-aiplatform` is up to date (>=1.70.0) to support the new model.

```python
from vertexai.preview import reasoning_engines
import vertexai
import logging
from agent import YukiAgent
from tools import get_current_time, add_numbers

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
STAGING_BUCKET = "gs://gifted-cooler-479623-r7-yuki-staging"
LOCATION = "us-central1"  # Reasoning Engine requires a specific region

def deploy():
    vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

    print(f"Deploying Yuki Agent to {LOCATION}...")

    # Instantiate the local agent
    agent = YukiAgent(
        model="gemini-3-pro-preview",
        tools=[get_current_time, add_numbers],
        project=PROJECT_ID,
        location=LOCATION,
    )
    
    # Deploy the agent
    remote_agent = reasoning_engines.ReasoningEngine.create(
        agent,
        requirements=[
            "cloudpickle",
            "langchain-core",
            "langchain",
            "langchain-google-vertexai>=2.0.0",
            "langgraph",
            "google-cloud-aiplatform>=1.70.0",
            "google-auth",
            "google-cloud-secret-manager",
            "google-cloud-vertexai"
        ],
        display_name="Yuki V.005",
        description="Custom agent Yuki V.005 with Nano Banana capabilities.",
    )

    print("Deployment complete!")
    print(f"Resource Name: {remote_agent.resource_name}")
    return remote_agent

if __name__ == "__main__":
    deploy()
```

### 2. `agent.py`
- Ensure it matches the local version exactly.

### 3. `tools.py`
- Ensure it matches the local version exactly.

## Execution Steps
1.  **Wait for User Login**: Confirm the user is logged into Google Cloud Console and Cloud Shell is active.
2.  **Overwrite Files**: Use `cat` commands in the Cloud Shell terminal to update `deploy.py`, `agent.py`, and `tools.py`.
3.  **Run Deployment**: Execute `python deploy.py`.
4.  **Verify**: Check for the "Deployment complete!" message and the Resource Name.
