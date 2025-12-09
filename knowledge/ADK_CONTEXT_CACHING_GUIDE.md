# Context Caching with Gemini

**Supported in ADK:** Python v1.15.0

The ADK Context Caching feature allows you to cache request data with generative AI models that support it (Gemini 2.0+), speeding up responses and lowering token usage for repeated large contexts.

## Configure context caching

Configure at the ADK App object level using `ContextCacheConfig`.

```python
from google.adk import Agent
from google.adk.apps.app import App
from google.adk.agents.context_cache_config import ContextCacheConfig

root_agent = Agent(
  # configure an agent using Gemini 2.0 or higher
)

# Create the app with context caching configuration
app = App(
    name='my-caching-agent-app',
    root_agent=root_agent,
    context_cache_config=ContextCacheConfig(
        min_tokens=2048,    # Minimum tokens to trigger caching (Default: 0)
        ttl_seconds=600,    # Store for up to 10 minutes (Default: 1800/30 mins)
        cache_intervals=5,  # Refresh after 5 uses (Default: 10)
    ),
)
```

## Configuration settings

*   `min_tokens` (int): Minimum tokens required to enable caching.
*   `ttl_seconds` (int): Time-to-live for the cache in seconds.
*   `cache_intervals` (int): Maximum number of times cached content can be used before expiry.
