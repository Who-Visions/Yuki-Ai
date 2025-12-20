# Gemini 3.0 Project Standards (Dec 2025)

## Overview

This project adheres to the **Gemini 3.0** ecosystem standards. All new tools and agents must use the following configurations to ensure compatibility, speed, and availability.

## Model Family

| Tier | Model ID | Use Case |
| :--- | :--- | :--- |
| **Standard** | `gemini-3-flash-preview` | Default for tools, grounding, and general logic. Replaces 2.5 Flash. |
| **Complex** | `gemini-3-pro-preview` | Deep reasoning tasks. |
| **Vision** | `gemini-3-pro-image-preview` | High-fidelity image generation and editing. |

## Critical Configurations

### 1. Global Endpoint

**Requirement**: ALWAYS use `location='global'` to minimize `429 RESOURCE_EXHAUSTED` errors.
`us-central1` should be avoided for high-throughput batch operations.

```python
client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
```

### 2. Thinking Configuration

**Requirement**: Use `ThinkingConfig` for all Gemini 3 requests.

- **Low Latency / Tools**: `thinking_level="LOW"`
- **Reasoning**: `thinking_level="HIGH"` (Default)

```python
from google.genai.types import GenerateContentConfig, ThinkingConfig

config = GenerateContentConfig(
    thinking_config=ThinkingConfig(thinking_level="LOW")
)
```

### 3. Grounding

**Requirement**: Use `GoogleSearch` tool for web access.
**Enablement**: Project must have "Vertex AI Grounding with Google Search" enabled in Console.

## Migration Notes (from 2.5/1.5)

- **Deprecated**: `gemini-1.5-flash`, `gemini-1.5-pro` (End of Life: Sept 2025).
- **Thinking**: `thinking_budget` is replaced by `thinking_level`.
- **Media**: Use `media_resolution` parameter (`LOW`, `MEDIUM`, `HIGH`) instead of implicit defaults for better token management.
