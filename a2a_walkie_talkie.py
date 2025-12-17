#!/usr/bin/env python3
"""
🔗 A2A Walkie-Talkie - Agent-to-Agent Communication Hub
========================================================
True bidirectional A2A protocol implementation for Yuki <-> Dav1d comms

Based on A2A Protocol Specification v1.0
https://a2a-protocol.org/latest/specification/

Features:
- Agent Card discovery at /.well-known/agent.json
- SSE streaming for real-time responses
- Task lifecycle management
- Multi-turn conversations
- Rich.live terminal UI

Agents:
- Yuki: https://yuki-ai-914641083224.us-central1.run.app
- Dav1d: https://dav1d-322812104986.us-central1.run.app
"""

import os
import sys
import json
import uuid
import asyncio
import httpx
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, AsyncGenerator
from enum import Enum
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.spinner import Spinner
from rich.layout import Layout
from rich.text import Text

# =============================================================================
# CONFIGURATION
# =============================================================================

# Agent Endpoints
AGENTS = {
    "yuki": {
        "name": "Yuki",
        "url": "https://yuki-ai-914641083224.us-central1.run.app",
        "emoji": "🦊",
        "color": "cyan",
        "description": "Nine-Tailed Snow Fox - Cosplay Preview Architect"
    },
    "dav1d": {
        "name": "Dav1d", 
        "url": "https://dav1d-322812104986.us-central1.run.app",
        "emoji": "🧠",
        "color": "magenta",
        "description": "Neural Network Orchestrator"
    }
}

console = Console()

# =============================================================================
# A2A PROTOCOL DATA MODELS
# =============================================================================

class TaskState(str, Enum):
    UNSPECIFIED = "TASK_STATE_UNSPECIFIED"
    SUBMITTED = "TASK_STATE_SUBMITTED"
    WORKING = "TASK_STATE_WORKING"
    COMPLETED = "TASK_STATE_COMPLETED"
    FAILED = "TASK_STATE_FAILED"
    CANCELLED = "TASK_STATE_CANCELLED"
    INPUT_REQUIRED = "TASK_STATE_INPUT_REQUIRED"
    REJECTED = "TASK_STATE_REJECTED"
    AUTH_REQUIRED = "TASK_STATE_AUTH_REQUIRED"

class Role(str, Enum):
    UNSPECIFIED = "ROLE_UNSPECIFIED"
    USER = "ROLE_USER"
    AGENT = "ROLE_AGENT"

@dataclass
class Part:
    """A2A Part - contains text, file, or data."""
    text: Optional[str] = None
    file: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Message:
    """A2A Message - unit of communication."""
    messageId: str
    role: str
    parts: List[Part]
    contextId: Optional[str] = None
    taskId: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class TaskStatus:
    """A2A TaskStatus - current state of a task."""
    state: str
    message: Optional[Message] = None
    timestamp: Optional[str] = None

@dataclass
class Artifact:
    """A2A Artifact - output of a task."""
    artifactId: str
    name: Optional[str] = None
    parts: List[Part] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Task:
    """A2A Task - core unit of action."""
    id: str
    contextId: str
    status: TaskStatus
    artifacts: List[Artifact] = field(default_factory=list)
    history: List[Message] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class AgentCard:
    """A2A Agent Card - discovery metadata."""
    protocolVersion: str
    name: str
    description: str
    supportedInterfaces: List[Dict[str, str]]
    provider: Optional[Dict[str, str]] = None
    version: Optional[str] = None
    capabilities: Optional[Dict[str, bool]] = None
    skills: Optional[List[Dict[str, Any]]] = None

@dataclass
class SendMessageRequest:
    """A2A SendMessageRequest - request to send a message."""
    message: Message
    configuration: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

# =============================================================================
# A2A CLIENT
# =============================================================================

class A2AClient:
    """
    A2A Protocol Client for Agent-to-Agent communication.
    Implements HTTP+JSON/REST binding with SSE streaming.
    """
    
    def __init__(self, agent_key: str):
        if agent_key not in AGENTS:
            raise ValueError(f"Unknown agent: {agent_key}")
        
        self.agent_info = AGENTS[agent_key]
        self.base_url = self.agent_info["url"].rstrip("/")
        self.agent_card: Optional[AgentCard] = None
        self.current_context_id: Optional[str] = None
        self.http_client = httpx.AsyncClient(timeout=120.0)
    
    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose()
    
    async def discover(self) -> Optional[AgentCard]:
        """
        Discover agent capabilities via Agent Card.
        GET /.well-known/agent.json
        """
        try:
            # Try standard well-known path first
            response = await self.http_client.get(f"{self.base_url}/.well-known/agent.json")
            if response.status_code == 200:
                data = response.json()
                self.agent_card = AgentCard(**{k: v for k, v in data.items() if k in AgentCard.__annotations__})
                return self.agent_card
            
            # Fallback to root endpoint for basic info
            response = await self.http_client.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                # Create minimal agent card from root response
                self.agent_card = AgentCard(
                    protocolVersion="0.3.0",
                    name=data.get("service", self.agent_info["name"]),
                    description=self.agent_info["description"],
                    supportedInterfaces=[{"url": self.base_url, "protocolBinding": "HTTP+JSON"}],
                    version=data.get("version", "unknown"),
                    capabilities={"streaming": True}
                )
                return self.agent_card
                
        except Exception as e:
            console.print(f"[yellow]Discovery failed: {e}[/yellow]")
            return None
    
    async def send_message(self, text: str, context_id: Optional[str] = None) -> Optional[Task]:
        """
        Send a message to the agent.
        POST /v1/message:send (A2A)
        Fallback: POST /v1/chat/completions (OpenAI-compatible)
        """
        message_id = f"msg-{uuid.uuid4()}"
        ctx_id = context_id or self.current_context_id or f"ctx-{uuid.uuid4()}"
        
        # Try A2A endpoint first
        try:
            request_data = {
                "message": {
                    "messageId": message_id,
                    "role": "user",
                    "parts": [{"text": text}],
                    "contextId": ctx_id
                }
            }
            
            response = await self.http_client.post(
                f"{self.base_url}/v1/message:send",
                json=request_data,
                headers={"Content-Type": "application/a2a+json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "task" in data:
                    self.current_context_id = data["task"].get("contextId", ctx_id)
                    return self._parse_task(data["task"])
                    
        except Exception as e:
            # Fallback to OpenAI-compatible endpoint
            pass
        
        # Fallback to OpenAI /v1/chat/completions
        try:
            messages = [{"role": "user", "content": text}]
            
            response = await self.http_client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.agent_info["name"].lower(),
                    "messages": messages,
                    "temperature": 0.7
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Wrap in A2A Task format
                return Task(
                    id=f"task-{uuid.uuid4()}",
                    contextId=ctx_id,
                    status=TaskStatus(state=TaskState.COMPLETED.value),
                    artifacts=[Artifact(
                        artifactId=f"artifact-{uuid.uuid4()}",
                        name="Response",
                        parts=[Part(text=content)]
                    )]
                )
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return None
    
    async def send_streaming_message(self, text: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Send a message with SSE streaming.
        POST /v1/message:stream
        """
        message_id = f"msg-{uuid.uuid4()}"
        ctx_id = self.current_context_id or f"ctx-{uuid.uuid4()}"
        
        request_data = {
            "message": {
                "messageId": message_id,
                "role": "user",
                "parts": [{"text": text}],
                "contextId": ctx_id
            }
        }
        
        try:
            async with self.http_client.stream(
                "POST",
                f"{self.base_url}/v1/message:stream",
                json=request_data,
                headers={
                    "Content-Type": "application/a2a+json",
                    "Accept": "text/event-stream"
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data:"):
                        data_str = line[5:].strip()
                        if data_str:
                            try:
                                yield json.loads(data_str)
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            console.print(f"[yellow]Streaming not available, using sync: {e}[/yellow]")
            # Fallback to sync
            result = await self.send_message(text)
            if result:
                yield {"task": asdict(result) if hasattr(result, '__dataclass_fields__') else result}
    
    async def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get task status.
        GET /v1/tasks/{id}
        """
        try:
            response = await self.http_client.get(f"{self.base_url}/v1/tasks/{task_id}")
            if response.status_code == 200:
                return self._parse_task(response.json())
        except Exception as e:
            console.print(f"[red]Error getting task: {e}[/red]")
        return None
    
    def _parse_task(self, data: Dict[str, Any]) -> Task:
        """Parse task from JSON response."""
        status_data = data.get("status", {})
        status = TaskStatus(
            state=status_data.get("state", TaskState.UNSPECIFIED.value),
            timestamp=status_data.get("timestamp")
        )
        
        artifacts = []
        for art_data in data.get("artifacts", []):
            parts = [Part(text=p.get("text")) for p in art_data.get("parts", [])]
            artifacts.append(Artifact(
                artifactId=art_data.get("artifactId", f"artifact-{uuid.uuid4()}"),
                name=art_data.get("name"),
                parts=parts
            ))
        
        return Task(
            id=data.get("id", f"task-{uuid.uuid4()}"),
            contextId=data.get("contextId", ""),
            status=status,
            artifacts=artifacts
        )

# =============================================================================
# WALKIE-TALKIE HUB
# =============================================================================

class WalkieTalkieHub:
    """
    Two-way A2A communication hub between agents.
    Acts as a relay/translator for agent-to-agent messages.
    """
    
    def __init__(self):
        self.clients: Dict[str, A2AClient] = {}
        self.active_agent: str = "dav1d"  # Default target
        self.conversation_history: List[Dict[str, Any]] = []
    
    async def connect_all(self):
        """Connect to all known agents."""
        for agent_key in AGENTS:
            try:
                client = A2AClient(agent_key)
                card = await client.discover()
                self.clients[agent_key] = client
                
                emoji = AGENTS[agent_key]["emoji"]
                name = AGENTS[agent_key]["name"]
                status = "🟢 Online" if card else "🟡 Partial"
                console.print(f"  {emoji} {name}: {status}")
                
            except Exception as e:
                console.print(f"  ❌ {AGENTS[agent_key]['name']}: Offline ({e})")
    
    async def close_all(self):
        """Close all client connections."""
        for client in self.clients.values():
            await client.close()
    
    def switch_agent(self, agent_key: str) -> bool:
        """Switch the active target agent."""
        if agent_key in AGENTS:
            self.active_agent = agent_key
            return True
        return False
    
    async def talk(self, message: str) -> Optional[str]:
        """
        Send message to active agent with Rich.live streaming display.
        """
        if self.active_agent not in self.clients:
            console.print(f"[red]Agent {self.active_agent} not connected[/red]")
            return None
        
        client = self.clients[self.active_agent]
        agent_info = AGENTS[self.active_agent]
        
        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "target": self.active_agent
        })
        
        response_text = ""
        
        with Live(
            Panel(
                Spinner("dots", text=f"[{agent_info['color']}]{agent_info['emoji']} {agent_info['name']} is thinking...[/{agent_info['color']}]"),
                title=f"{agent_info['emoji']} {agent_info['name']}",
                border_style=agent_info["color"]
            ),
            console=console,
            refresh_per_second=10
        ) as live:
            
            # Try streaming first
            try:
                async for event in client.send_streaming_message(message):
                    if "task" in event:
                        task_data = event["task"]
                        for artifact in task_data.get("artifacts", []):
                            for part in artifact.get("parts", []):
                                if part.get("text"):
                                    response_text += part["text"]
                        
                        # Update display
                        live.update(Panel(
                            Markdown(response_text + "▌"),
                            title=f"{agent_info['emoji']} {agent_info['name']}",
                            border_style=agent_info["color"]
                        ))
                    
                    elif "artifactUpdate" in event:
                        artifact = event["artifactUpdate"].get("artifact", {})
                        for part in artifact.get("parts", []):
                            if part.get("text"):
                                response_text += part["text"]
                        
                        live.update(Panel(
                            Markdown(response_text + "▌"),
                            title=f"{agent_info['emoji']} {agent_info['name']}",
                            border_style=agent_info["color"]
                        ))
                    
                    elif "statusUpdate" in event:
                        status = event["statusUpdate"].get("status", {})
                        if status.get("state") == "completed":
                            break
                            
            except Exception as e:
                # Fallback to sync message
                result = await client.send_message(message)
                if result and result.artifacts:
                    for artifact in result.artifacts:
                        for part in artifact.parts:
                            if part.text:
                                response_text += part.text
            
            # Final display
            if response_text:
                live.update(Panel(
                    Markdown(response_text),
                    title=f"{agent_info['emoji']} {agent_info['name']}",
                    border_style=agent_info["color"]
                ))
        
        # Add response to history
        if response_text:
            self.conversation_history.append({
                "role": "agent",
                "agent": self.active_agent,
                "content": response_text,
                "timestamp": datetime.now().isoformat()
            })
        
        return response_text
    
    async def relay(self, from_agent: str, to_agent: str, message: str) -> Optional[str]:
        """
        Relay a message from one agent to another.
        True A2A communication.
        """
        if from_agent not in self.clients or to_agent not in self.clients:
            console.print("[red]Both agents must be connected[/red]")
            return None
        
        from_info = AGENTS[from_agent]
        to_info = AGENTS[to_agent]
        
        console.print(f"\n[dim]🔗 Relaying: {from_info['emoji']} {from_info['name']} → {to_info['emoji']} {to_info['name']}[/dim]")
        
        # Get response from source agent
        old_active = self.active_agent
        self.active_agent = from_agent
        source_response = await self.talk(message)
        
        if source_response:
            # Send to target agent
            self.active_agent = to_agent
            target_response = await self.talk(f"[From {from_info['name']}]: {source_response}")
            
            self.active_agent = old_active
            return target_response
        
        self.active_agent = old_active
        return None

# =============================================================================
# MAIN CLI
# =============================================================================

def print_banner():
    """Print walkie-talkie banner."""
    banner = """
[bold magenta]╔══════════════════════════════════════════════════════════════════╗
║          🔗 A2A WALKIE-TALKIE - Agent-to-Agent Comms Hub         ║
╠══════════════════════════════════════════════════════════════════╣
║  Commands:                                                       ║
║    @yuki <msg>   - Talk to Yuki (Cosplay Architect)             ║
║    @dav1d <msg>  - Talk to Dav1d (Neural Orchestrator)          ║
║    /relay <msg>  - Relay between agents (Yuki → Dav1d)          ║
║    /switch <agent> - Set default target agent                    ║
║    /status       - Show all agent statuses                       ║
║    /history      - Show conversation history                     ║
║    /clear        - Clear conversation history                    ║
║    /exit         - Exit the hub                                  ║
╚══════════════════════════════════════════════════════════════════╝[/bold magenta]
"""
    console.print(banner)

async def show_status(hub: WalkieTalkieHub):
    """Show all agent statuses."""
    table = Table(title="🔗 Agent Network Status", border_style="magenta")
    table.add_column("Agent", style="bold")
    table.add_column("Status", style="cyan")
    table.add_column("Version", style="dim")
    table.add_column("Capabilities", style="green")
    
    for agent_key, client in hub.clients.items():
        info = AGENTS[agent_key]
        icon = "🟢" if client.agent_card else "🟡"
        version = client.agent_card.version if client.agent_card else "unknown"
        caps = ""
        if client.agent_card and client.agent_card.capabilities:
            caps = ", ".join(k for k, v in client.agent_card.capabilities.items() if v)
        
        active = " ← ACTIVE" if agent_key == hub.active_agent else ""
        table.add_row(
            f"{info['emoji']} {info['name']}{active}",
            f"{icon} Connected",
            version,
            caps or "basic"
        )
    
    console.print(table)

def show_history(hub: WalkieTalkieHub):
    """Show conversation history."""
    if not hub.conversation_history:
        console.print("[dim]No conversation history yet.[/dim]")
        return
    
    console.print("\n[bold]📜 Conversation History[/bold]")
    for entry in hub.conversation_history[-10:]:  # Last 10 entries
        role = entry["role"]
        content = entry["content"][:100] + "..." if len(entry["content"]) > 100 else entry["content"]
        
        if role == "user":
            console.print(f"  [bold green]You →[/bold green] {content}")
        else:
            agent = entry.get("agent", "agent")
            emoji = AGENTS.get(agent, {}).get("emoji", "🤖")
            console.print(f"  [bold cyan]{emoji} {agent} →[/bold cyan] {content}")
    console.print()

async def main():
    """Main entry point."""
    print_banner()
    
    hub = WalkieTalkieHub()
    
    console.print("\n[bold cyan]Connecting to agent network...[/bold cyan]")
    await hub.connect_all()
    console.print()
    
    try:
        while True:
            try:
                # Get active agent info for prompt
                active_info = AGENTS[hub.active_agent]
                prompt_text = f"[{active_info['color']}]{active_info['emoji']}[/{active_info['color']}] You"
                
                user_input = Prompt.ask(prompt_text).strip()
                
                if not user_input:
                    continue
                
                # Command handling
                if user_input.startswith("/"):
                    cmd_parts = user_input.split(maxsplit=1)
                    cmd = cmd_parts[0].lower()
                    cmd_arg = cmd_parts[1] if len(cmd_parts) > 1 else ""
                    
                    if cmd == "/exit" or cmd == "/quit":
                        console.print("\n[magenta]🔗 Disconnecting from agent network...[/magenta]\n")
                        break
                    
                    elif cmd == "/status":
                        await show_status(hub)
                        continue
                    
                    elif cmd == "/history":
                        show_history(hub)
                        continue
                    
                    elif cmd == "/clear":
                        hub.conversation_history = []
                        console.print("[green]✅ History cleared[/green]")
                        continue
                    
                    elif cmd == "/switch":
                        if cmd_arg and hub.switch_agent(cmd_arg.lower()):
                            new_info = AGENTS[cmd_arg.lower()]
                            console.print(f"[green]✅ Switched to {new_info['emoji']} {new_info['name']}[/green]")
                        else:
                            console.print(f"[yellow]Available agents: {', '.join(AGENTS.keys())}[/yellow]")
                        continue
                    
                    elif cmd == "/relay":
                        if cmd_arg:
                            await hub.relay("yuki", "dav1d", cmd_arg)
                        else:
                            console.print("[yellow]Usage: /relay <message>[/yellow]")
                        continue
                    
                    elif cmd == "/help":
                        print_banner()
                        continue
                    
                    else:
                        console.print(f"[yellow]Unknown command: {cmd}[/yellow]")
                        continue
                
                # Direct agent targeting with @
                elif user_input.startswith("@"):
                    parts = user_input.split(maxsplit=1)
                    target = parts[0][1:].lower()  # Remove @
                    message = parts[1] if len(parts) > 1 else ""
                    
                    if target in AGENTS and message:
                        old_active = hub.active_agent
                        hub.active_agent = target
                        await hub.talk(message)
                        hub.active_agent = old_active
                    else:
                        console.print(f"[yellow]Usage: @{target} <message>[/yellow]")
                    continue
                
                # Regular message to active agent
                else:
                    await hub.talk(user_input)
                
                console.print()  # Spacing
                
            except KeyboardInterrupt:
                console.print("\n[cyan]Ctrl+C - Type /exit to quit[/cyan]")
            except EOFError:
                break
    
    finally:
        await hub.close_all()

if __name__ == "__main__":
    asyncio.run(main())
