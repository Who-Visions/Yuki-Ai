# Yuki Agent Deployment Guide  
Cosplay Preview Architect on Vertex AI Reasoning Engine (Gemini 3 Pro)

## Overview

Yuki is a custom Reasoning Engine agent that uses the `gemini-3-pro-preview` model to handle cosplay preview logic.

Key traits:

1. Runs on Vertex AI Reasoning Engine in region `us-central1`.  
2. Uses Gemini 3 Pro globally through the new `google genai` client with `vertexai=True`.  
3. Exposes a single public method named `query` for all frontend calls.  
4. Supports tools such as `get_current_time` and `add_numbers` as a template for future tools.

---

## Architecture

High level:

1. Reasoning Engine resource lives in `us-central1`.  
2. Gemini 3 Pro is accessed using location `global` inside the agent, since Gemini 3 models require the global endpoint.  
3. Yuki lazy-initializes the Gen AI client inside `query`.  
4. Operations are registered through `register_operations`, which is required for Reasoning Engine to expose the `query` method.

---

## Configuration

Project and runtime constants in `deploy_yuki.py`:

```python
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"  # Reasoning Engine region
MODEL = "gemini-3-pro-preview"
STAGING_BUCKET = f"gs://yuki-{PROJECT_ID}"
```

Requirements passed to the Reasoning Engine:

```python
requirements = [
    "cloudpickle==3",
    "google-genai>=1.51.0"
]
```

You also need the regular Vertex AI SDK in your Cloud Shell environment:

```bash
pip install --upgrade google-cloud-aiplatform google-genai
```

---

## Yuki Class Responsibilities

Yuki is defined inside `deploy_yuki.py` (or `agent.py` if you split it).

### Core fields

```python
class Yuki:
    def __init__(self):
        self.name = "Yuki"
        self.version = "0.05"
        self.role = "Cosplay Preview Architect"
        self.model_name = MODEL
        self.client = None
        self.tools = [get_current_time, add_numbers]
```

### set_up

Initializes the Gen AI client with the correct location logic.

```python
def set_up(self):
    """Initialize Gemini client with dynamic location routing."""
    from google import genai

    if "gemini-3" in self.model_name or "gemini-exp" in self.model_name:
        client_location = "global"
    else:
        client_location = LOCATION

    self.client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=client_location,
    )
```

**Notes:**
- Reasoning Engine is regional.
- Gemini 3 Pro is only reachable through the global location.
- This method bridges that mismatch by routing the client to the correct endpoint while the engine itself is in `us-central1`.

### query

Single public operation that the Reasoning Engine exposes.

```python
def query(self, user_instruction: str) -> dict:
    """Main entry point for Yuki."""
    from google.genai import types

    if self.client is None:
        self.set_up()

    if isinstance(user_instruction, dict):
        if "messages" in user_instruction:
            text = user_instruction["messages"][-1]["content"] if user_instruction["messages"] else ""
        elif "input" in user_instruction:
            text = user_instruction["input"]
        else:
            text = str(user_instruction)
    else:
        text = str(user_instruction)

    try:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction="You are Yuki, a helpful AI assistant.",
                tools=self.tools,
                temperature=1.0,
            ),
        )

        return {"output": response.text.strip()}

    except Exception as e:
        return {
            "output": f"Error: {str(e)}",
            "status": "error",
        }
```

**Key details:**
- Lazy init ensures `set_up` runs inside the deployed agent, not just locally.
- Handles both simple string input and dict payloads with `messages` or `input`.
- Always returns a JSON-serializable dict, both in success and error branches.

### register_operations

This is the piece that makes `agent.query` actually exist on the remote resource.

```python
def register_operations(self):
    """Register operations for the deployed agent."""
    return {
        "": ["query"]
    }
```

**Without this**, the Reasoning Engine resource will deploy but you will get an object with no `query` attribute.

---

## Deployment Script

Deployment happens from `deploy_yuki.py` inside Cloud Shell.

```python
from vertexai.preview import reasoning_engines
import vertexai

from tools import get_current_time, add_numbers
from yuki import Yuki  # if you split Yuki into its own module

def deploy():
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STAGING_BUCKET,
    )

    yuki = Yuki()
    yuki.set_up()
    test_result = yuki.query("Hello")
    print("Local test:", test_result)

    remote_yuki = reasoning_engines.ReasoningEngine.create(
        Yuki(),
        requirements=[
            "cloudpickle==3",
            "google-genai>=1.51.0",
        ],
        display_name="Yuki-v005",
        description="Cosplay Preview Architect | Nine-Tailed Snow Fox",
    )

    print("Deployment complete.")
    print("Resource name:", remote_yuki.resource_name)
    return remote_yuki

if __name__ == "__main__":
    deploy()
```

### Deployment Steps

From Cloud Shell:

1. **Confirm you are in the correct project:**
```bash
gcloud config set project gifted-cooler-479623-r7
```

2. **Ensure required libs are installed:**
```bash
pip install --upgrade google-cloud-aiplatform google-genai
```

3. **Upload or edit** `deploy_yuki.py`, `tools.py`, and any `yuki.py` or `agent.py` file so they match your working local versions.

4. **Run deployment:**
```bash
python deploy_yuki.py
```

5. **Copy the printed `resource_name`** and store it somewhere.

Example from the current deployment:
```
projects/914641083224/locations/us-central1/reasoningEngines/2780528567203659776
```

---

## Testing The Deployed Agent

Create `test_yuki_deployed.py` in Cloud Shell.

```python
import json
import vertexai
from vertexai.preview import reasoning_engines

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "us-central1"
RESOURCE_NAME = "projects/914641083224/locations/us-central1/reasoningEngines/2780528567203659776"

def main():
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    agent = reasoning_engines.ReasoningEngine(RESOURCE_NAME)

    response = agent.query(
        user_instruction="Hello Yuki, what time is it right now in UTC?"
    )

    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
```

Run:
```bash
python test_yuki_deployed.py
```

Expected output:
```json
{
  "output": "The current time is 2025-12-01 12:47:08 UTC."
}
```

---

## Troubleshooting Notes

Observed failure modes, their causes, and fixes:

### Query attribute missing on the remote agent
- **Cause:** `register_operations` not implemented or not exposing "query".
- **Fix:** Implement `register_operations` and map the default operation key to `["query"]`.

### Client not initialized inside Reasoning Engine
- **Cause:** `set_up` never called in the remote runtime.
- **Fix:** Lazy initialization inside `query` that calls `set_up` when `self.client is None`.

### Bucket location error when using GLOBAL
- **Error:** `Project may not create STANDARD buckets with locationConstraint GLOBAL`.
- **Fix:** Use a regional staging bucket in `us-central1` instead of global.

### Model not found for Gemini 3 Pro
- **Error:** `404 NOT_FOUND: gemini-3-pro-preview`.
- **Cause:** Gemini 3 models are only available at the global location for Gen AI.
- **Fix:** Route the Gen AI client to `location="global"` whenever the model name contains "gemini-3" or "gemini-exp".

### Query returns null
- **Cause:** Success path of `query` had no return.
- **Fix:** Ensure the final response is returned, e.g., `return {"output": response.text.strip()}`.

---

## Current Active Resource

As of 2025-12-01, the current Yuki Reasoning Engine resource is:

```
projects/914641083224/locations/us-central1/reasoningEngines/2780528567203659776
```

Use this value for all integration work until the next redeploy.
