from vertexai.preview import reasoning_engines
import vertexai
from typing import Callable, Sequence, Iterable, Dict, Any
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent
from langchain_core.load import dumpd
import datetime

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
STAGING_BUCKET = "gs://gifted-cooler-479623-r7-yuki-staging"
LOCATION = "us-central1"

# Tools (inlined)
def get_current_time() -> str:
    """Returns the current time in UTC."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b

# Agent class (inlined)
class YukiAgent:
    def __init__(
        self,
        model: str,
        tools: Sequence[Callable],
        project: str,
        location: str,
    ):
        self.model_name = model
        self.tools = tools
        self.project = project
        self.location = location
        self.graph = None

    def set_up(self):
        """
        Initialize the agent, setting up Vertex AI and the LangGraph agent.
        """
        vertexai.init(project=self.project, location=self.location)
        model = ChatVertexAI(model_name=self.model_name)
        self.graph = create_react_agent(model, tools=self.tools)

    def query(self, **kwargs) -> Dict[str, Any]:
        """
        Synchronous query method.
        """
        if self.graph is None:
            self.set_up()
        return self.graph.invoke(**kwargs)

    def stream_query(self, **kwargs) -> Iterable:
        """
        Streaming query method.
        """
        if self.graph is None:
            self.set_up()
        for chunk in self.graph.stream(**kwargs):
            yield dumpd(chunk)

    async def async_query(self, **kwargs) -> Dict[str, Any]:
        """
        Asynchronous query method.
        """
        if self.graph is None:
            self.set_up()
        return await self.graph.ainvoke(**kwargs)

    async def async_stream_query(self, **kwargs):
        """
        Asynchronous streaming query method.
        """
        if self.graph is None:
            self.set_up()
        async for chunk in self.graph.astream(**kwargs):
            yield dumpd(chunk)

    def register_operations(self):
        """
        Register operations for the deployed agent.
        """
        return {
            "": ["query"],
            "stream": ["stream_query"],
        }

def deploy():
    vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

    print(f"Deploying Yuki Agent to {LOCATION}...")

    # Instantiate the local agent (WITHOUT calling set_up - let it lazy initialize)
    agent = YukiAgent(
        model="gemini-2.0-flash-exp",
        tools=[get_current_time, add_numbers],
        project=PROJECT_ID,
        location=LOCATION,
    )
    
    # Deploy the agent
    remote_agent = reasoning_engines.ReasoningEngine.create(
        agent,
        requirements=[
            "cloudpickle",
            "langchain-core",
            "langchain",
            "langchain-google-vertexai>=2.0.0",
            "langgraph",
            "google-cloud-aiplatform>=1.70.0",
            "google-auth",
            "google-cloud-secret-manager",
            "google-cloud-vertexai"
        ],
        display_name="Yuki V.005",
        description="Custom agent Yuki V.005 with Nano Banana capabilities.",
    )

    print("Deployment complete!")
    print(f"Resource Name: {remote_agent.resource_name}")
    return remote_agent

if __name__ == "__main__":
    deploy()
