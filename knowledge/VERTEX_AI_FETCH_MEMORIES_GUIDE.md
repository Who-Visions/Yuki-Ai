# Fetch memories

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

This page describes how to fetch generated and uploaded memories from Memory Bank.

## Get memory

Use `GetMemories` to get the full content of a single memory:

```python
memory = client.agent_engines.memories.get(
    name="MEMORY_NAME")
```
*   `MEMORY_NAME`: `projects/.../locations/.../reasoningEngines/.../memories...`.

## List memories

### Console

1.  Go to the **Vertex AI Agent Engine** page.
2.  Click the name of your Agent Engine instance.
3.  Click the **Memories** tab.

## Fetch memories using scope-based retrieval

Use `RetrieveMemories` to retrieve memories for a particular scope.

### Retrieve memories using similarity search

Retrieve only the most similar memories by providing similarity search parameters.

```python
results = client.agent_engines.memories.retrieve(
    name=agent_engine.api_resource.name,
    scope=SCOPE,
    similarity_search_params={
        "search_query": "QUERY",
        # Optional. Defaults to 3.
        "top_k": 3
    }
)
# RetrieveMemories returns a pager. You can use `list` to retrieve all memories.
list(results)
```

### Retrieve all memories

If no similarity search parameters are provided, `RetrieveMemories` returns all memories that have the provided scope.

```python
results = client.agent_engines.memories.retrieve(
    name=agent_engine.api_resource.name,
    scope=SCOPE
)
# RetrieveMemories returns a pager. You can use `list` to retrieve all pages' memories.
list(results)
```
