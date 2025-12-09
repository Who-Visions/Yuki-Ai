# Computer Use Toolset with Gemini

> **Preview**
>
> The Computer Use model and tool is a Preview release. For more information, see the launch stage descriptions.

The Computer Use Toolset allows an agent to operate a user interface of a computer, such as a browser, to complete tasks using a specific Gemini model and Playwright.

## Setup

You must install Playwright and its dependencies.

1.  **Install Python dependencies:**
    ```bash
    pip install termcolor==3.1.0
    pip install playwright==1.52.0
    pip install browserbase==1.3.0
    pip install rich
    ```
2.  **Install Playwright dependencies (including Chromium):**
    ```bash
    playwright install-deps chromium
    playwright install chromium
    ```

## Use the tool

Add the `ComputerUseToolset` as a tool to your agent, providing an implementation of the `BaseComputer` class (e.g., `PlaywrightComputer`).

```python
from google.adk import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools.computer_use.computer_use_toolset import ComputerUseToolset
from typing_extensions import override

# Assuming PlaywrightComputer is defined in a local module or available
# from .playwright import PlaywrightComputer

root_agent = Agent(
    model='gemini-2.5-computer-use-preview-10-2025',
    name='hello_world_agent',
    description=(
        'computer use agent that can operate a browser on a computer to finish'
        ' user tasks'
    ),
    instruction='you are a computer use agent',
    tools=[
        ComputerUseToolset(computer=PlaywrightComputer(screen_size=(1280, 936)))
    ],
)
```
