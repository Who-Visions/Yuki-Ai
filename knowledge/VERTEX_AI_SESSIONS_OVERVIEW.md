# Vertex AI Agent Engine Sessions overview

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

Vertex AI Agent Engine Sessions maintains the history of interactions between a user and agents. Sessions provide definitive sources for long-term memory and conversation context.

## Core concepts

*   **Session:** A session represents the chronological sequence of messages and actions (events) for a single, ongoing interaction between a user and your agent system.
*   **Event:** An event stores the content of the conversation, as well as the actions taken by the agents such as function calls.
*   **State:** A state holds temporary data relevant only during the current conversation.
*   **Memory:** Memory is personalized information that can be accessed across multiple sessions for a particular user.

## Core functionalities

*   **Starting new conversations:** Create new sessions when a user begins an interaction with an agent.
*   **Resuming existing conversations:** Retrieving a specific session so the agent can resume a conversation that has been paused.
*   **Saving progress:** Append new interactions (events) to a session's history to update the session.
*   **Listing conversations:** Find the active session threads for a particular user and application.
*   **Cleaning up:** Delete session objects and their associated data when conversations are finished or no longer needed.
