# Memory revisions

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

This page describes how memory revision resources are created and managed for Vertex AI Agent Engine Memory Bank.

## Lifecycle of a memory and its revisions

Memories can be created, updated, or deleted either directly or dynamically. A new, immutable revision is automatically saved each time that the memory is created or modified.

*   **Memory resources:** Always reflect the current, consolidated state of the information.
*   **MemoryRevisions resources:** Represent the historical states of the parent memory.

### Memory creation

When a memory is created, a single Memory resource and a child MemoryRevision are created.

### Memory update

When a memory is updated, the existing Memory resource is updated, and a new child MemoryRevision is created.

### Memory deletion

When a memory is deleted, the existing Memory resource is deleted, and a new child MemoryRevision is created. The fact in the latest memory revision is empty.

## Memory revision operations

### List revisions

```python
list(client.agent_engines.memories.revisions.list(name=MEMORY_NAME))
```

### Get a revision

```python
client.agent_engines.memories.revisions.get(name=MEMORY_REVISION_NAME)
```

### Roll back a memory

Use `RollbackMemory` to roll a memory back to a previous revision.

```python
client.agent_engines.memories.rollback(
    name=name=MEMORY_NAME,
    target_revision_id=REVISION_ID
)
```

## Disabling memory revisions

You can disable memory revisions either for all requests to your Memory Bank instance or for each individual request.

**Instance level:**
```python
client.agent_engines.create(
  config={
    "context_spec": {
      "memory_bank_config": {
        "disable_memory_revisions": True
      }
    }
  }
)
```

**Request level:**
```python
client.agent_engines.memories.generate(
  ...,
  "config": {
    "disable_memory_revisions": True
  }
)
```

## Revision expiration

The default time to live (TTL) is 365 days.

**Instance level:**
```python
client.agent_engines.create(
  config={
    "context_spec": {
      "memory_bank_config": {
        "ttl_config": {
          "revision_ttl": f"{30 * 60 * 60 * 24}s"
        }
      }
    }
  }
)
```

**Request level:**
```python
config = {
    "revision_ttl": f"{30 * 60 * 60 * 24}s"
}

client.agent_engines.memories.create(
  ...,
  config=config
)
```
