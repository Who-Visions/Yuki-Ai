# Compress Agent Context for Performance (Context Compaction)

**Supported in ADK:** Python v1.16.0

The ADK Context Compaction feature reduces the size of context as an agent runs by summarizing older parts of the agent workflow event history using a sliding window approach.

## Configure context compaction

Add `EventsCompactionConfig` to the App object.

```python
from google.adk.apps.app import App
from google.adk.apps.app import EventsCompactionConfig

app = App(
    name='my-agent',
    root_agent=root_agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,  # Trigger compaction every 3 new invocations.
        overlap_size=1          # Include last invocation from the previous window.
    ),
)
```

## Example

With `compaction_interval=3` and `overlap_size=1`:
1.  **Event 3 completes:** Events 1-3 compressed.
2.  **Event 6 completes:** Events 3-6 compressed (including overlap).
3.  **Event 9 completes:** Events 6-9 compressed.

## Configuration settings

*   `compaction_interval`: Number of completed events that triggers compaction.
*   `overlap_size`: Number of previously compacted events to include in the new set.
*   `compactor`: (Optional) Define a custom compactor object.

## Define a Summarizer

Customize compaction by defining a `LlmEventSummarizer`.

```python
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.models import Gemini

# Define the AI model to be used for summarization:
summarization_llm = Gemini(model="gemini-2.5-flash")

# Create the summarizer with the custom model:
my_summarizer = LlmEventSummarizer(llm=summarization_llm)

# Configure the App with the custom summarizer and compaction settings:
app = App(
    name='my-agent',
    root_agent=root_agent,
    events_compaction_config=EventsCompactionConfig(
        summarizer=my_summarizer,
        compaction_interval=3,
        overlap_size=1
    ),
)
```
