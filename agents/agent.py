from typing import Callable, Sequence, Iterable, Dict, Any
import vertexai
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent
from langchain_core.load import dumpd

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
        return self.graph.invoke(**kwargs)

    def stream_query(self, **kwargs) -> Iterable:
        """
        Streaming query method.
        """
        for chunk in self.graph.stream(**kwargs):
            yield dumpd(chunk)

    async def async_query(self, **kwargs) -> Dict[str, Any]:
        """
        Asynchronous query method.
        """
        return await self.graph.ainvoke(**kwargs)

    async def async_stream_query(self, **kwargs):
        """
        Asynchronous streaming query method.
        """
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
