# Vertex AI Agent Engine Memory Bank overview

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

Vertex AI Agent Engine Memory Bank lets you dynamically generate long-term memories based on users' conversations with your agent. Long-term memories are personalized information that can be accessed across multiple sessions for a particular user. The agent can use the memories to personalize responses to the user and create cross-session continuity.

## Overview

Memory Bank helps you manage memories, so that you can personalize how your agent interacts with users and manage the context window. For each scope, Memory Bank maintains an isolated collection of memories. Each memory is an independent, self-contained piece of information that can be used to expand the context available to your agent.

Example memory structure:
```json
{
  "name": "projects/.../locations/.../reasoningEngines/.../memories/...",
  "scope": {
    "agent_name": "My agent",
    "user": "my user ID"
  },
  "fact": "I use Memory Bank to manage my memories."
}
```

### Features

*   **Memory generation:** Create, refine, and manage memories using a large language model (LLM).
*   **Memory Extraction:** Extract only the most meaningful information from source data to persist as memories.
*   **Memory Consolidation:** Consolidate newly extracted information with existing memories, allowing memories to evolve as new information is ingested.
*   **Asynchronous Generation:** Generate memories in the background.
*   **Customizable Extraction:** Configure what information Memory Bank considers meaningful by providing specific topics and few-shot examples.
*   **Multimodal Understanding:** Process multimodal information to generate and persist textual insights.
*   **Managed Storage and Retrieval:** Benefit from a fully managed, persistent, and accessible memory store.
*   **Data isolation across identities:** Memory consolidation and retrieval is isolated to a specific identity.
*   **Persistent and Accessible Storage:** Store memories that can be accessed from multiple environments.
*   **Similarity Search:** Retrieve memories using similarity search that is scoped to a specific identity.
*   **Automatic Expiration:** Set a time to live (TTL) on memories.
*   **Memory Revisions:** Automatically create and maintain memory revisions.
*   **Agent integration:** Connect Memory Bank to your agent.
*   **Agent Development Kit (ADK) Integration:** Orchestrate calls from your ADK-based agent.

## Use cases

You can use Memory Bank to transform stateless agent interactions into stateful, contextual experiences where the agent remembers, learns, and adapts over time.

*   **Long-Term Personalization:** Build experiences that are tailored to individual users.
    *   *Example:* A customer service agent that remembers key information from a user's past support tickets and product preferences.
*   **LLM-driven Knowledge Extraction:** Automatically identify and persist the most important information from conversations or multimodal content.
    *   *Example:* A research agent that reads a series of technical papers and builds a consolidated memory of key findings.
*   **Dynamic & Evolving Context:** Use Memory Bank when you need a knowledge source that isn't static. Memory Bank evolves based on context provided by the agent.

## Example usage

You can use Memory Bank with Vertex AI Agent Engine Sessions to generate memories from stored sessions using the following process:

1.  **(Sessions) CreateSession:** Create a new session at the start of each conversation.
2.  **(Sessions) AppendEvent:** Upload events (user messages, agent responses) to Sessions as the user interacts.
3.  **(Sessions) ListEvents:** Agent retrieves conversation history.
4.  **(Memory Bank) Generate or create memories:**
    *   **GenerateMemories:** Trigger memory generation using conversation history at specified intervals.
    *   **CreateMemory:** Agent writes memories directly to Memory Bank (memory-as-a-tool).
5.  **(Memory Bank) RetrieveMemories:** Agent retrieves memories saved about the user (simple retrieval or similarity search) and inserts them into the prompt.

## Security risks of prompt injection

In addition to the security responsibilities outlined in Vertex AI shared responsibility, consider the risk of prompt injection and memory poisoning. Memory poisoning occurs when false information is stored in Memory Bank.

**Mitigation strategies:**
*   **Model Armor:** Use Model Armor to inspect prompts.
*   **Adversarial testing:** Proactively test for prompt injection vulnerabilities ("red teaming").
*   **Sandbox execution:** Perform actions in a sandboxed environment with strict access control if the agent interacts with external/critical systems.

## Resources
*   [Google's Approach for Secure AI Agents](https://cloud.google.com/security/ai-agents)
