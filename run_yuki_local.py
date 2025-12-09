from yuki_local import YukiLocal
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.theme import Theme
from rich.layout import Layout
from rich.live import Live
import sys
import time

# ═══════════════════════════════════════════════════════════════════════════════
# VISUAL CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

yuki_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "user": "bold color(200)",  # Lilac/Purple
    "yuki": "bold color(51)",   # Ice Blue
    "tool": "color(208)",       # Orange
    "success": "bold green",
    "dim": "dim white"
})

console = Console(theme=yuki_theme)

BANNER_TEXT = """
                   ░ ██░                  
                 ░░██░█░                  
                 ░██ ░█░                  
               ░██░░░░░██                 
               ▒▓▓░░░░██░                 
  ▓▓░░░        ▓▒▓░   ░██▓                
░▓▒▒▓▓██░      ██░█   ░░██▓▓██▓▓██        
░██░░██░░██    ▓▓██░░░██  ░░██░░░▒░░▓▓    
░██░  ██░░████░░░░░░░██░░██░██░░░░░░░██   
░██░░   ██░░░░░░░░░░░░░░██░██░░░░░░░░████ 
 ░██░   ██░░░░░░░░░░░░░░░██░░░░░░░░░░░░██ 
 ░██    ██░░░░░░░░░░░░░░░░██░░░░░░░░░░░░░██
 ░██    ██░░░░░░░░░░░░░░░░████░░░░░░░░░░░░██
 ░██░  ▒▒░░░░░░░░░░░░░░░░░▒▒▓▓░░░░░░░░░░░░██
 ░██░░ ▒░░░░░░░░░░░░░░░░░░░░██░░░░░░▓▓░░░▒▒██
  ░██░░░░░░░░░░░░░░░░░░░░░  ██░░░████░░░░░░██
  ░████░░░░░░░░░░░░░░░░░░██   ██░░██▒▒░░░░░░██
  ░██░██░░░░░░░░░░░░░░░░██    ██████░░░░░░░░██
    ░▓▒▓░░░░░░░░░░░░░░░░██      ▓▒▒▓░░░░░░░░░▒▓
      ██░░██░░░░░░░░░░░░░░██    █ ░░░░░░░░░░░░░██
      ░████ ░░░░░░░░░░░░░░  █ ░ ░    ░░░░░░░░░░░██
        ▒██ ░░██▓▓██░░░░░░░░░ █ ░ ░   ░░░░░░░░▓▓▒▒
          ██░░░░░░▒░▓▓██▒▒░░░   █ ░     ░░░░░░░░██
          ░██           █  ████           ░░░██
              ██           ██░██           ░░██
              ░██████▓▓░▓▓▓▓▒░██          ░░▓░
                    ░██░   ██░░░░██         ██
                    ░██░░ ▓▒░░░████        ▓░
                    ░██░░░██░░░██░██      ████
                      ░████░░░██  ██    ████
                        ░▒▒▓▓▓░   ██▓ ▒▓░░
                                ░   ░███░
"""

def print_banner():
    console.print(Panel(
        f"[yuki]{BANNER_TEXT}[/yuki]",
        border_style="yuki",
        subtitle="[dim]v0.06-local[/dim]",
        expand=False
    ))

def main():
    print_banner()
    console.print("[yuki]🦊 Initializing Neural Interfaces...[/yuki]")
    
    # Initialize Agent
    try:
        agent = YukiLocal()
        console.print("[success]✓ Agent Loaded Successfully[/success]")
    except Exception as e:
        console.print(f"[error]✗ Failed to load agent: {e}[/error]")
        return

    console.print(Panel("[yuki]I am listening. Tell me about your cosplay dream.[/yuki]", border_style="yuki"))

    while True:
        try:
            # Stylized Input
            console.print("\n[user]USER INPUT >[/user] ", end="")
            user_input = input().strip()
            
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[yuki]🦊 Arigato! Closing session...[/yuki]")
                break
            if not user_input:
                continue
            
            # Show "Thinking" spinner (simulated since query is blocking)
            with console.status("[bold yuki]Fox spirits are communing...[/bold yuki]", spinner="dots"):
                response = agent.query(user_input)
            
            # Handle response
            if response['status'] == 'ok':
                # Render Output as Markdown
                console.print("\n")
                console.print(Panel(
                    Markdown(response['output']),
                    title=f"[yuki]🦊 Yuki ({response['model']})[/yuki]",
                    border_style="yuki",
                    expand=True
                ))
            else:
                console.print(Panel(
                    f"[error]{response['output']}[/error]",
                    title=f"[error]Error ({response['model']})[/error]",
                    border_style="error"
                ))
                
        except KeyboardInterrupt:
            console.print("\n[yuki]Session interrupted. Goodbye![/yuki]")
            break
        except Exception as e:
            console.print(f"\n[error]System Error: {e}[/error]")

if __name__ == "__main__":
    main()
