#!/usr/bin/env python3
"""
🦊 Yuki Chat CLI - Real-time Streaming Chat Interface
=====================================================
Instance mode + Session mode with Rich.live streaming output

Features:
- /instance - One-shot query mode (no memory)
- /session  - Persistent conversation mode  
- /listen   - Audio input (voice-to-text via Gemini)
- /analyze  - Image/file analysis
- /exit     - Quit the session

Usage:
  python yuki_chat.py                    # Interactive session mode
  python yuki_chat.py --instance "query" # One-shot instance mode
  python yuki_chat.py --endpoint URL     # Custom Yuki API endpoint
"""

import os
import sys
import json
import argparse
import httpx
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.spinner import Spinner
from rich.table import Table
from google import genai
from google.genai import types

# =============================================================================
# CONFIGURATION
# =============================================================================

# Default Yuki endpoints
YUKI_LOCAL = "http://localhost:8080"
YUKI_CLOUD = "https://yuki-api-XXXXX.run.app"  # Update with actual Cloud Run URL
DAV1D_ENDPOINT = "https://dav1d-322812104986.us-central1.run.app"

# Colors
class Colors:
    ICE_BLUE = "#00D9FF"
    SAKURA_PINK = "#FF69B4"
    FOX_FIRE = "#FF6B35"
    SNOW_WHITE = "#F0F8FF"
    SHADOW = "#2D2D2D"
    NEON_PINK = "#FF1493"
    AURORA = "#7B68EE"

console = Console()

# =============================================================================
# SESSION MANAGER
# =============================================================================

class SessionManager:
    """Manages conversation sessions with memory."""
    
    def __init__(self):
        self.session_id: Optional[str] = None
        self.messages: List[Dict[str, Any]] = []
        self.created_at: Optional[datetime] = None
        self.mode: str = "session"  # "session" or "instance"
        
    def start_session(self):
        """Start a new session."""
        self.session_id = f"yuki-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.messages = []
        self.created_at = datetime.now()
        self.mode = "session"
        return self.session_id
    
    def start_instance(self):
        """Start instance mode (no memory)."""
        self.session_id = None
        self.messages = []
        self.mode = "instance"
    
    def add_message(self, role: str, content: str):
        """Add message to history (only in session mode)."""
        if self.mode == "session":
            self.messages.append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
    
    def get_openai_messages(self) -> List[Dict[str, str]]:
        """Get messages in OpenAI format."""
        return [{"role": m["role"], "content": m["content"]} for m in self.messages]
    
    def clear(self):
        """Clear session history."""
        self.messages = []

# =============================================================================
# YUKI CLIENT
# =============================================================================

class YukiClient:
    """Client for interacting with Yuki API."""
    
    def __init__(self, endpoint: str = YUKI_LOCAL):
        self.endpoint = endpoint.rstrip("/")
        self.session = SessionManager()
        self.http_client = httpx.Client(timeout=120.0)
        
        # Initialize Gemini client for local processing
        try:
            self.genai_client = genai.Client(
                vertexai=True,
                project="gifted-cooler-479623-r7",
                location="global"
            )
        except Exception:
            self.genai_client = None
    
    def check_health(self) -> bool:
        """Check if Yuki API is healthy."""
        try:
            response = self.http_client.get(f"{self.endpoint}/health")
            return response.status_code == 200
        except Exception:
            return False
    
    def chat(self, message: str, model: str = "yuki") -> str:
        """Send chat message and get response."""
        # Add user message
        self.session.add_message("user", message)
        
        # Prepare request
        payload = {
            "model": model,
            "messages": self.session.get_openai_messages(),
            "temperature": 0.7,
            "stream": False
        }
        
        try:
            response = self.http_client.post(
                f"{self.endpoint}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            data = response.json()
            assistant_message = data["choices"][0]["message"]["content"]
            
            # Add assistant response to session
            self.session.add_message("assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def analyze_image(self, image_path: str, prompt: str = "Analyze this image") -> str:
        """Analyze an image using Gemini."""
        if not self.genai_client:
            return "❌ Gemini client not available"
        
        try:
            # Read and encode image
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            ext = Path(image_path).suffix.lower()
            mime_types = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg", 
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp"
            }
            mime_type = mime_types.get(ext, "image/jpeg")
            
            # Call Gemini
            response = self.genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(text=prompt),
                            types.Part(inline_data=types.Blob(
                                mime_type=mime_type,
                                data=image_data
                            ))
                        ]
                    )
                ]
            )
            
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            return "No analysis available"
            
        except Exception as e:
            return f"❌ Analysis error: {str(e)}"
    
    def listen_audio(self, audio_path: str) -> str:
        """Transcribe and analyze audio."""
        if not self.genai_client:
            return "❌ Gemini client not available"
        
        try:
            with open(audio_path, "rb") as f:
                audio_data = f.read()
            
            ext = Path(audio_path).suffix.lower()
            mime_types = {
                ".mp3": "audio/mp3",
                ".wav": "audio/wav",
                ".m4a": "audio/mp4",
                ".ogg": "audio/ogg",
                ".flac": "audio/flac"
            }
            mime_type = mime_types.get(ext, "audio/mp3")
            
            response = self.genai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(text="Transcribe and summarize this audio:"),
                            types.Part(inline_data=types.Blob(
                                mime_type=mime_type,
                                data=audio_data
                            ))
                        ]
                    )
                ]
            )
            
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            return "No transcription available"
            
        except Exception as e:
            return f"❌ Audio error: {str(e)}"

# =============================================================================
# RICH UI COMPONENTS
# =============================================================================

def print_banner():
    """Print Yuki banner."""
    banner = """
[bold cyan]╔══════════════════════════════════════════════════════════════╗
║       🦊 YUKI CHAT - Nine-Tailed Snow Fox Interface 🦊        ║
╠══════════════════════════════════════════════════════════════╣
║  Commands:                                                   ║
║    /session  - Start persistent session mode                 ║
║    /instance - Switch to one-shot mode (no memory)           ║
║    /analyze <path> - Analyze image/file                      ║
║    /listen <path>  - Transcribe audio                        ║
║    /clear   - Clear conversation history                     ║
║    /status  - Show session status                            ║
║    /exit    - Exit Yuki Chat                                 ║
╚══════════════════════════════════════════════════════════════╝[/bold cyan]
"""
    console.print(banner)

def stream_response(client: YukiClient, message: str) -> str:
    """Stream response with Rich.live display."""
    
    with Live(
        Panel(Spinner("dots", text="[cyan]Yuki is thinking...[/cyan]"), 
              title="🦊 Yuki", border_style="cyan"),
        console=console,
        refresh_per_second=10
    ) as live:
        # Get response
        response = client.chat(message)
        
        # Animate typing effect
        displayed = ""
        for i, char in enumerate(response):
            displayed += char
            
            # Update display every few characters for performance
            if i % 3 == 0 or i == len(response) - 1:
                live.update(Panel(
                    Markdown(displayed + "▌" if i < len(response) - 1 else displayed),
                    title="🦊 Yuki",
                    border_style="cyan"
                ))
    
    return response

def show_status(client: YukiClient):
    """Show session status."""
    session = client.session
    
    table = Table(title="📊 Session Status", border_style="cyan")
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Mode", session.mode.upper())
    table.add_row("Session ID", session.session_id or "N/A (instance mode)")
    table.add_row("Messages", str(len(session.messages)))
    table.add_row("Created", session.created_at.strftime("%H:%M:%S") if session.created_at else "N/A")
    table.add_row("Endpoint", client.endpoint)
    table.add_row("Health", "✅ Online" if client.check_health() else "❌ Offline")
    
    console.print(table)

# =============================================================================
# MAIN CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="🦊 Yuki Chat CLI")
    parser.add_argument("--instance", "-i", type=str, help="One-shot query (instance mode)")
    parser.add_argument("--endpoint", "-e", type=str, default=YUKI_LOCAL, 
                        help=f"Yuki API endpoint (default: {YUKI_LOCAL})")
    parser.add_argument("--model", "-m", type=str, default="yuki",
                        help="Model to use (default: yuki)")
    parser.add_argument("--dav1d", action="store_true", help="Use Dav1d endpoint instead")
    args = parser.parse_args()
    
    # Select endpoint
    endpoint = DAV1D_ENDPOINT if args.dav1d else args.endpoint
    client = YukiClient(endpoint)
    
    # Instance mode - one-shot
    if args.instance:
        client.session.start_instance()
        console.print(f"\n[bold cyan]🦊 Yuki (Instance Mode)[/bold cyan]")
        response = stream_response(client, args.instance)
        console.print()
        sys.exit(0)
    
    # Interactive session mode
    print_banner()
    
    # Check health
    with console.status("[cyan]Connecting to Yuki...[/cyan]"):
        if client.check_health():
            console.print(f"[green]✅ Connected to {endpoint}[/green]\n")
        else:
            console.print(f"[yellow]⚠️  Warning: Cannot reach {endpoint}[/yellow]")
            console.print("[yellow]   Falling back to local Gemini processing[/yellow]\n")
    
    # Start session
    session_id = client.session.start_session()
    console.print(f"[dim]Session: {session_id}[/dim]\n")
    
    # Main loop
    while True:
        try:
            user_input = Prompt.ask("[bold magenta]You[/bold magenta]").strip()
            
            if not user_input:
                continue
            
            # Command handling
            if user_input.startswith("/"):
                cmd_parts = user_input.split(maxsplit=1)
                cmd = cmd_parts[0].lower()
                cmd_arg = cmd_parts[1] if len(cmd_parts) > 1 else ""
                
                if cmd == "/exit" or cmd == "/quit":
                    console.print("\n[cyan]🦊 Sayonara! - Yuki out 💫[/cyan]\n")
                    break
                
                elif cmd == "/session":
                    client.session.start_session()
                    console.print(f"[green]✅ New session started: {client.session.session_id}[/green]")
                    continue
                
                elif cmd == "/instance":
                    client.session.start_instance()
                    console.print("[green]✅ Switched to instance mode (no memory)[/green]")
                    continue
                
                elif cmd == "/clear":
                    client.session.clear()
                    console.print("[green]✅ Conversation cleared[/green]")
                    continue
                
                elif cmd == "/status":
                    show_status(client)
                    continue
                
                elif cmd == "/analyze":
                    if not cmd_arg:
                        console.print("[yellow]Usage: /analyze <image_path>[/yellow]")
                        continue
                    with console.status("[cyan]Analyzing image...[/cyan]"):
                        result = client.analyze_image(cmd_arg.strip())
                    console.print(Panel(Markdown(result), title="🔍 Analysis", border_style="green"))
                    continue
                
                elif cmd == "/listen":
                    if not cmd_arg:
                        console.print("[yellow]Usage: /listen <audio_path>[/yellow]")
                        continue
                    with console.status("[cyan]Processing audio...[/cyan]"):
                        result = client.listen_audio(cmd_arg.strip())
                    console.print(Panel(Markdown(result), title="🎤 Transcription", border_style="purple"))
                    continue
                
                elif cmd == "/help":
                    print_banner()
                    continue
                
                else:
                    console.print(f"[yellow]Unknown command: {cmd}[/yellow]")
                    continue
            
            # Regular chat
            stream_response(client, user_input)
            console.print()  # Spacing
            
        except KeyboardInterrupt:
            console.print("\n[cyan]🦊 Interrupted - Type /exit to quit[/cyan]")
        except EOFError:
            break

if __name__ == "__main__":
    main()
