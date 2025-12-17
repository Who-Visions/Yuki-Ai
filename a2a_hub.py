#!/usr/bin/env python3
"""
🔗 A2A Hub - Official SDK Agent-to-Agent Communication
=======================================================
True bidirectional A2A protocol using official a2a-sdk

Uses:
- a2a.client.A2AClient for reliable agent communication
- a2a.client.A2ACardResolver for agent discovery
- Rich.live for real-time streaming display

Agents:
- Yuki: https://yuki-ai-914641083224.us-central1.run.app
- Dav1d: https://dav1d-322812104986.us-central1.run.app
"""

import asyncio
import logging
from uuid import uuid4
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

import httpx
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.spinner import Spinner

# A2A SDK imports
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
    Part,
    Message,
    Role,
)
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

# =============================================================================
# CONFIGURATION
# =============================================================================

# Agent Registry
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
logging.basicConfig(level=logging.WARNING)  # Quiet by default


# =============================================================================
# A2A AGENT WRAPPER
# =============================================================================

@dataclass
class AgentConnection:
    """Wrapper for an A2A agent connection."""
    key: str
    info: Dict[str, str]
    card: Optional[AgentCard] = None
    client: Optional[A2AClient] = None
    httpx_client: Optional[httpx.AsyncClient] = None
    
    @property
    def is_connected(self) -> bool:
        return self.client is not None
    
    @property
    def supports_streaming(self) -> bool:
        if self.card and self.card.capabilities:
            return getattr(self.card.capabilities, 'streaming', False)
        return False


class A2AHub:
    """
    Central hub for A2A agent-to-agent communication.
    Uses official a2a-sdk for protocol compliance.
    """
    
    def __init__(self):
        self.connections: Dict[str, AgentConnection] = {}
        self.active_agent: str = "dav1d"
        self.conversation_history: List[Dict[str, Any]] = []
        self.context_ids: Dict[str, str] = {}  # Per-agent context
    
    async def connect_all(self):
        """Connect to all registered agents."""
        for agent_key, agent_info in AGENTS.items():
            conn = AgentConnection(key=agent_key, info=agent_info)
            
            try:
                # Create persistent HTTP client
                conn.httpx_client = httpx.AsyncClient(timeout=120.0)
                
                # Try A2A discovery first
                try:
                    resolver = A2ACardResolver(
                        httpx_client=conn.httpx_client,
                        base_url=agent_info["url"]
                    )
                    conn.card = await resolver.get_agent_card()
                    conn.client = A2AClient(
                        httpx_client=conn.httpx_client,
                        agent_card=conn.card
                    )
                    console.print(f"  {agent_info['emoji']} {agent_info['name']}: [green]🟢 A2A Connected[/green]")
                    
                except Exception as e:
                    # Fallback: Create minimal card for OpenAI-compatible endpoints
                    conn.card = AgentCard(
                        name=agent_info["name"],
                        description=agent_info["description"],
                        url=agent_info["url"],
                        version="1.0.0"
                    )
                    console.print(f"  {agent_info['emoji']} {agent_info['name']}: [yellow]🟡 OpenAI Compat Mode[/yellow]")
                    
            except Exception as e:
                console.print(f"  {agent_info['emoji']} {agent_info['name']}: [red]❌ Failed ({e})[/red]")
            
            self.connections[agent_key] = conn
    
    async def close_all(self):
        """Close all connections."""
        for conn in self.connections.values():
            if conn.httpx_client:
                await conn.httpx_client.aclose()
    
    def switch_agent(self, agent_key: str) -> bool:
        """Switch active target agent."""
        if agent_key in self.connections:
            self.active_agent = agent_key
            return True
        return False
    
    async def send_message_a2a(self, conn: AgentConnection, text: str) -> Optional[str]:
        """Send message using official A2A protocol."""
        if not conn.client:
            return None
        
        # Get or create context ID for this agent
        context_id = self.context_ids.get(conn.key, str(uuid4()))
        self.context_ids[conn.key] = context_id
        
        message_payload = {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": text}],
                "messageId": str(uuid4()),
                "contextId": context_id
            }
        }
        
        try:
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(**message_payload)
            )
            response = await conn.client.send_message(request)
            
            # Extract text from response
            if hasattr(response, 'result') and response.result:
                result = response.result
                # Handle Task response
                if hasattr(result, 'artifacts') and result.artifacts:
                    texts = []
                    for artifact in result.artifacts:
                        if hasattr(artifact, 'parts'):
                            for part in artifact.parts:
                                if hasattr(part, 'text') and part.text:
                                    texts.append(part.text)
                    return "\n".join(texts)
                # Handle direct Message response
                elif hasattr(result, 'parts'):
                    texts = []
                    for part in result.parts:
                        if hasattr(part, 'text') and part.text:
                            texts.append(part.text)
                    return "\n".join(texts)
                    
        except Exception as e:
            console.print(f"[dim]A2A error: {e}[/dim]")
        
        return None
    
    async def send_message_a2a_streaming(self, conn: AgentConnection, text: str):
        """Send message with A2A streaming. Yields partial responses."""
        if not conn.client:
            return
        
        context_id = self.context_ids.get(conn.key, str(uuid4()))
        self.context_ids[conn.key] = context_id
        
        message_payload = {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": text}],
                "messageId": str(uuid4()),
                "contextId": context_id
            }
        }
        
        full_response = ""
        
        try:
            request = SendStreamingMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(**message_payload)
            )
            
            async for chunk in conn.client.send_message_streaming(request):
                if hasattr(chunk, 'result') and chunk.result:
                    result = chunk.result
                    if hasattr(result, 'artifacts'):
                        for artifact in result.artifacts:
                            if hasattr(artifact, 'parts'):
                                for part in artifact.parts:
                                    if hasattr(part, 'text') and part.text:
                                        full_response += part.text
                                        yield full_response
                                        
        except Exception as e:
            console.print(f"[dim]Streaming error: {e}[/dim]")

    
    async def send_message_openai(self, conn: AgentConnection, text: str) -> Optional[str]:
        """Fallback: Send via OpenAI-compatible endpoint."""
        if not conn.httpx_client:
            return None
        
        try:
            response = await conn.httpx_client.post(
                f"{conn.info['url']}/v1/chat/completions",
                json={
                    "model": conn.info["name"].lower(),
                    "messages": [{"role": "user", "content": text}],
                    "temperature": 0.7
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
        except Exception as e:
            console.print(f"[dim]OpenAI fallback error: {e}[/dim]")
        
        return None
    
    async def talk(self, message: str, target: Optional[str] = None) -> Optional[str]:
        """
        Send message to an agent with Rich.live display.
        """
        agent_key = target or self.active_agent
        
        if agent_key not in self.connections:
            console.print(f"[red]Unknown agent: {agent_key}[/red]")
            return None
        
        conn = self.connections[agent_key]
        agent_info = conn.info
        
        # Record in history
        self.conversation_history.append({
            "role": "user",
            "content": message,
            "target": agent_key
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
            
            # Try A2A first
            if conn.client:
                if conn.supports_streaming:
                    # Streaming A2A
                    async for partial in self.send_message_a2a_streaming(conn, message):
                        response_text = partial
                        live.update(Panel(
                            Markdown(response_text + "▌"),
                            title=f"{agent_info['emoji']} {agent_info['name']}",
                            border_style=agent_info["color"]
                        ))
                else:
                    # Sync A2A
                    response_text = await self.send_message_a2a(conn, message) or ""
            
            # Fallback to OpenAI-compat
            if not response_text:
                response_text = await self.send_message_openai(conn, message) or ""
            
            # Final display
            if response_text:
                live.update(Panel(
                    Markdown(response_text),
                    title=f"{agent_info['emoji']} {agent_info['name']}",
                    border_style=agent_info["color"]
                ))
        
        # Record response
        if response_text:
            self.conversation_history.append({
                "role": "agent",
                "agent": agent_key,
                "content": response_text
            })
        
        return response_text
    
    async def relay(self, message: str, from_agent: str = "yuki", to_agent: str = "dav1d") -> Optional[str]:
        """
        Relay message from one agent to another.
        True A2A agent-to-agent communication.
        """
        from_info = AGENTS.get(from_agent, {})
        to_info = AGENTS.get(to_agent, {})
        
        console.print(f"\n[dim]🔗 Relay: {from_info.get('emoji', '🤖')} → {to_info.get('emoji', '🤖')}[/dim]")
        
        # Get response from first agent
        response1 = await self.talk(message, from_agent)
        
        if response1:
            # Forward to second agent
            relay_msg = f"[Message from {from_info.get('name', from_agent)}]:\n{response1}"
            response2 = await self.talk(relay_msg, to_agent)
            return response2
        
        return None


# =============================================================================
# CLI INTERFACE
# =============================================================================

def print_banner():
    """Print the hub banner."""
    banner = """
[bold magenta]╔══════════════════════════════════════════════════════════════════╗
║         🔗 A2A HUB - Official SDK Agent Communication            ║
╠══════════════════════════════════════════════════════════════════╣
║  Commands:                                                       ║
║    @yuki <msg>     - Talk to Yuki                               ║
║    @dav1d <msg>    - Talk to Dav1d                              ║
║    /relay <msg>    - Yuki → Dav1d relay                         ║
║    /switch <agent> - Switch default target                       ║
║    /status         - Show connection status                      ║
║    /history        - Show conversation history                   ║
║    /clear          - Clear history                               ║
║    /exit           - Exit hub                                    ║
╚══════════════════════════════════════════════════════════════════╝[/bold magenta]
"""
    console.print(banner)


async def show_status(hub: A2AHub):
    """Display agent status table."""
    table = Table(title="🔗 Agent Network", border_style="magenta")
    table.add_column("Agent", style="bold")
    table.add_column("Status")
    table.add_column("Protocol")
    table.add_column("Streaming")
    
    for key, conn in hub.connections.items():
        info = conn.info
        active = " ← ACTIVE" if key == hub.active_agent else ""
        
        if conn.client:
            status = "[green]🟢 Connected[/green]"
            protocol = "A2A"
        elif conn.httpx_client:
            status = "[yellow]🟡 Fallback[/yellow]"
            protocol = "OpenAI"
        else:
            status = "[red]❌ Offline[/red]"
            protocol = "N/A"
        
        streaming = "✅" if conn.supports_streaming else "❌"
        
        table.add_row(
            f"{info['emoji']} {info['name']}{active}",
            status,
            protocol,
            streaming
        )
    
    console.print(table)


def show_history(hub: A2AHub):
    """Show recent conversation history."""
    if not hub.conversation_history:
        console.print("[dim]No history yet.[/dim]")
        return
    
    console.print("\n[bold]📜 Recent History[/bold]")
    for entry in hub.conversation_history[-10:]:
        content = entry["content"][:80] + "..." if len(entry["content"]) > 80 else entry["content"]
        
        if entry["role"] == "user":
            target = entry.get("target", "")
            console.print(f"  [green]You → @{target}[/green]: {content}")
        else:
            agent = entry.get("agent", "agent")
            emoji = AGENTS.get(agent, {}).get("emoji", "🤖")
            console.print(f"  [{agent}]{emoji}[/{agent}]: {content}")
    console.print()


async def main():
    """Main CLI loop."""
    print_banner()
    
    hub = A2AHub()
    
    console.print("\n[cyan]Connecting to agents...[/cyan]")
    await hub.connect_all()
    console.print()
    
    try:
        while True:
            try:
                active = hub.connections.get(hub.active_agent)
                if active:
                    prompt_emoji = active.info["emoji"]
                    prompt_color = active.info["color"]
                else:
                    prompt_emoji = "🤖"
                    prompt_color = "white"
                
                user_input = Prompt.ask(f"[{prompt_color}]{prompt_emoji}[/{prompt_color}] You").strip()
                
                if not user_input:
                    continue
                
                # Commands
                if user_input.startswith("/"):
                    parts = user_input.split(maxsplit=1)
                    cmd = parts[0].lower()
                    arg = parts[1] if len(parts) > 1 else ""
                    
                    if cmd in ("/exit", "/quit"):
                        console.print("\n[magenta]🔗 Disconnecting...[/magenta]\n")
                        break
                    elif cmd == "/status":
                        await show_status(hub)
                    elif cmd == "/history":
                        show_history(hub)
                    elif cmd == "/clear":
                        hub.conversation_history = []
                        hub.context_ids = {}
                        console.print("[green]✅ Cleared[/green]")
                    elif cmd == "/switch":
                        if arg and hub.switch_agent(arg.lower()):
                            new_info = AGENTS[arg.lower()]
                            console.print(f"[green]✅ Switched to {new_info['emoji']} {new_info['name']}[/green]")
                        else:
                            console.print(f"[yellow]Agents: {', '.join(AGENTS.keys())}[/yellow]")
                    elif cmd == "/relay":
                        if arg:
                            await hub.relay(arg)
                        else:
                            console.print("[yellow]Usage: /relay <message>[/yellow]")
                    elif cmd == "/help":
                        print_banner()
                    else:
                        console.print(f"[yellow]Unknown: {cmd}[/yellow]")
                    continue
                
                # Direct agent targeting
                elif user_input.startswith("@"):
                    parts = user_input.split(maxsplit=1)
                    target = parts[0][1:].lower()
                    msg = parts[1] if len(parts) > 1 else ""
                    
                    if target in AGENTS and msg:
                        await hub.talk(msg, target)
                    else:
                        console.print(f"[yellow]Usage: @{target} <message>[/yellow]")
                    continue
                
                # Message to active agent
                else:
                    await hub.talk(user_input)
                
                console.print()
                
            except KeyboardInterrupt:
                console.print("\n[cyan]Ctrl+C - /exit to quit[/cyan]")
            except EOFError:
                break
    
    finally:
        await hub.close_all()


if __name__ == "__main__":
    asyncio.run(main())
