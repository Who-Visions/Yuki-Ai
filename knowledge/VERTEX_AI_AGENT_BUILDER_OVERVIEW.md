# Vertex AI Agent Builder overview

Vertex AI Agent Builder is a suite of products that help developers build, scale, and govern AI agents in production. Vertex AI Agent Builder provides a full-stack, secure foundation that supports the entire agent lifecycle:

## Build
Build agents using frameworks such as Agent Development Kit (ADK) or any other open-source framework of your choice.

*   **Agent Development Kit (ADK):** An open-source framework that simplifies the process of building sophisticated multi-agent systems while maintaining precise control over agent behavior.
*   **Agent Garden (Supported in preview):** A library in the Google Cloud console where you can find and explore sample agents and tools that are designed to accelerate your development.
    *   **Agents:** Prebuilt, end-to-end solutions for specific use cases (e.g., customer service, data analysis). Only Google can publish agents to the Agent Garden.
    *   **Tools:** Individual components that you can add to your own agents (e.g., interacting with a database, calling an external API).

## Scale
Scale your agents into production with built-in testing, release management, and reliability at a global and secure scale.

*   **Vertex AI Agent Engine:** A set of services that enables developers to deploy, manage, and scale AI agents in production. Services include:
    *   Fully-managed runtime
    *   Evaluation
    *   Sessions
    *   Memory Bank
    *   Code Execution
    *   Observability with Google Cloud Trace, Cloud Monitoring, and Cloud Logging.
*   **Agent Tools:** Tools that you can equip your ADK agent to use, including:
    *   **Built-in tools:** Grounding with Google Search, Vertex AI Search, and Code Execution.
    *   **RAG Engine:** For retrieval-augmented generation (RAG).
    *   **Google Cloud tools:** Connect to APIs managed in Apigee API Hub, 100+ enterprise applications through Integration Connectors, and custom integrations with Application Integration.
    *   **Model Context Protocol (MCP) tools.**
    *   **Ecosystem tools:** LangChain tools, CrewAI tools, and GenAI Toolbox for Databases.

## Govern
Monitor what your agents are doing with an audit trail for end-to-end observability.

*   **Detect threats with Security Command Center:** Agent Engine Threat Detection (Preview) helps detect and investigate potential attacks on agents deployed to Vertex AI Agent Engine Runtime.
*   **Agent identity (Preview):** Use Identity Access Management (IAM) agent identity to provide security and access management features when using agents on Vertex AI Agent Engine Runtime.

## Resources
*   [Blog post on multi-agent systems with Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/build-multi-agent-systems-with-vertex-ai)
*   [What are AI Agents?](https://cloud.google.com/learn/what-are-ai-agents)
*   [Vertex AI Agent Builder](https://cloud.google.com/generative-ai-agent-builder)
