import sys
import time
import subprocess
import threading
import shutil
from collections import deque
from datetime import datetime

# Check and install rich if missing
try:
    from rich.live import Live
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.align import Align
    from rich.text import Text
    from rich.table import Table
    from rich.spinner import Spinner
    from rich.console import Console, Group
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.syntax import Syntax
    from rich import box
except ImportError:
    print("Installing 'rich' library for UI...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    from rich.live import Live
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.align import Align
    from rich.text import Text
    from rich.table import Table
    from rich.spinner import Spinner
    from rich.console import Console, Group
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.syntax import Syntax
    from rich import box

console = Console()

# Configuration
SERVICES = [
    {
        "name": "Backend API",
        "icon": "🧠",
        "command": ["python", "yuki_openai_server.py"],
        "cwd": "C:\\Yuki_Local",
        "color": "yellow"
    },
    {
        "name": "Mobile App (Web)",
        "icon": "🦊",
        "command": ["npm.cmd", "run", "web"],
        "cwd": "C:\\Yuki_Local\\yuki-app",
        "color": "cyan"
    },
    {
        "name": "iOS Simulator",
        "icon": "📱",
        "command": ["npm.cmd", "run", "ios"],
        "cwd": "C:\\Yuki_Local\\yuki-app",
        "color": "magenta"
    }
]

# State
service_logs = {s["name"]: deque(maxlen=8) for s in SERVICES}
service_status = {s["name"]: "STARTING" for s in SERVICES}
start_time = datetime.now()

def capture_output(service):
    """Reads stdout/stderr from a service and appends to logs."""
    name = service["name"]
    cwd = service["cwd"]
    cmd = service["command"]
    
    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            bufsize=1,
            creationflags=subprocess.CREATE_NEW_CONSOLE  # Prevent signal propogation issues
        )
        
        service_status[name] = "RUNNING"
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                service_logs[name].append(line.strip())
                
        service_status[name] = "STOPPED"
    except Exception as e:
        service_status[name] = "ERROR"
        service_logs[name].append(f"Error: {str(e)}")

def make_layout():
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    
    layout["body"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=2)
    )
    
    # Split left column for 3 services
    layout["left"].split(
        Layout(name="service_0"),
        Layout(name="service_1"),
        Layout(name="service_2")
    )
    
    return layout

def generate_header():
    grid = Table.grid(expand=True)
    grid.add_column(justify="center", ratio=1)
    grid.add_row(
        Text(f"❄️ YUKI AI CONTROL CENTER ❄️  |  {datetime.now().strftime('%H:%M:%S')}", style="bold white on blue", justify="center")
    )
    return grid

def generate_service_panel(index):
    service = SERVICES[index]
    name = service["name"]
    status = service_status[name]
    logs = service_logs[name]
    color = service["color"]
    icon = service["icon"]
    
    # Status Spinner
    if status == "RUNNING":
        status_icon = Spinner("dots", style=f"bold {color}")
        status_text = Text(f" ONLINE", style=f"bold {color}")
    elif status == "STARTING":
        status_icon = Spinner("bouncingBall", style="yellow")
        status_text = Text(" BOOTING", style="yellow")
    elif status == "ERROR":
        status_icon = "❌"
        status_text = Text(" ERROR", style="bold red")
    else:
        status_icon = "🛑"
        status_text = Text(" STOPPED", style="dim")
    
    # Log Content
    log_text = Text()
    for line in logs:
        # Clean up some common clutter logs
        if "bit" in line or "npm" in line:
            log_text.append(f"› {line[:50]}...\n", style="dim white")
        else:
            log_text.append(f"› {line}\n", style="white")

    # Status Display (Inside Body)
    status_display = Table.grid(expand=True)
    status_display.add_column()
    status_display.add_column(justify="right")
    
    status_content = Table.grid()
    status_content.add_row(status_icon, status_text)
    
    # Assemble content
    content_group = Align.left(
        Group(
            status_content,
            Text("─" * 30, style="dim"),
            log_text
        ),
        vertical="bottom"
    )

    return Panel(
        content_group,
        title=f"{icon} {name}",
        border_style=color,
        box=box.ROUNDED
    )

def generate_main_dashboard():
    # Just a placeholder for the right side - maybe system stats or global log?
    # For "All in One", let's make it a consolidated "Master Log" or "Performance"
    # Actually, let's just make it a big visual graphic or instructions.
    
    welcome_text = Text.from_markup(
        """
[bold cyan]SYSTEM READY[/bold cyan]

[white]Press [bold yellow]Ctrl+C[/bold yellow] to Halt System[/white]

[dim]
- Web Interface: http://localhost:8081
- API Endpoint:  http://localhost:8000
- Launcher:      v2.0 (Rich)[/dim]
        """
    )
    
    return Panel(
        Align.center(welcome_text, vertical="middle"),
        title="[bold white]Dashboard[/bold white]",
        border_style="blue"
    )

def run():
    # 1. Start Services in Threads
    threads = []
    for service in SERVICES:
        t = threading.Thread(target=capture_output, args=(service,), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.5) # Stagger start
        
    layout = make_layout()
    
    # 2. Main UI Loop
    
    # Initialize layout content to prevent "Tree View" flash
    layout["header"].update(generate_header())
    for i in range(3):
        layout[f"service_{i}"].update(generate_service_panel(i))
    layout["right"].update(generate_main_dashboard())
    layout["footer"].update(Panel(Text("  Yuki AI System Online  ", style="black on green", justify="center"), box=box.HEAVY))

    with Live(layout, refresh_per_second=4, screen=True) as live:
        try:
            while True:
                layout["header"].update(generate_header())
                
                # Update Service Panels
                for i in range(3):
                    layout[f"service_{i}"].update(generate_service_panel(i))
                
                # Update Right Panel
                layout["right"].update(generate_main_dashboard())
                
                # Footer
                layout["footer"].update(Panel(Text("  Yuki AI System Online  ", style="black on green", justify="center"), box=box.HEAVY))
                
                time.sleep(0.25)
        except KeyboardInterrupt:
            pass
            
    print("Shutting down...")
    # Cleanup (subprocess.Popen in threads might need manual kill if not daemon)

if __name__ == "__main__":
    run()
