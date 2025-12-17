import sys
import os
import subprocess
import threading
from datetime import datetime
from textual.app import App, ComposeResult
from textual.containers import Container, Grid, Vertical
from textual.widgets import Header, Footer, Log, Static, Label, Button
from textual.reactive import reactive
from textual.worker import Worker, WorkerState

# Ensure Textual is installed
try:
    import textual
except ImportError:
    print("Installing 'textual' library for UI...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "textual"])
    import textual

# Service Configuration
SERVICES = [
    {
        "id": "backend",
        "name": "Backend API",
        "icon": "🧠",
        "command": [sys.executable, "-u", "yuki_openai_server.py"],
        "cwd": "C:\\Yuki_Local",
        "color": "#ffff00" # yellow
    },
    {
        "id": "mobile",
        "name": "Mobile App (Web)",
        "icon": "🦊",
        "command": ["npm.cmd", "run", "web"],
        "cwd": "C:\\Yuki_Local\\yuki-app",
        "color": "#00ffff" # cyan
    },
    {
        "id": "ios",
        "name": "Expo Bundler (iOS/Android)",
        "icon": "📱",
        "command": ["npx.cmd", "expo", "start", "--port", "8082"],
        "cwd": "C:\\Yuki_Local\\yuki-app",
        "color": "#ff00ff" # magenta
    }
]

class ServiceLog(Log):
    """Specialized Log widget for services."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border_title = "Logs"

class ServicePane(Vertical):
    """A widget to display a single service's status and logs."""
    
    status = reactive("STOPPED")
    
    def __init__(self, service_config, **kwargs):
        super().__init__(**kwargs)
        self.service_config = service_config
        self.process = None
        self.id = f"service-{service_config['id']}"
        self.border_title = f"{service_config['icon']} {service_config['name']}"
        self.styles.border = ("round", service_config["color"])

    def compose(self) -> ComposeResult:
        yield Label(f"Status: {self.status}", id=f"status-{self.service_config['id']}")
        yield ServiceLog(id=f"log-{self.service_config['id']}")

    def on_mount(self) -> None:
        # Trigger an update now that we are mounted
        self.watch_status(self.status, self.status)

    def watch_status(self, old_status: str, new_status: str) -> None:
        try:
            lbl = self.query_one(f"#status-{self.service_config['id']}", Label)
            lbl.update(f"Status: {new_status}")
            if new_status == "RUNNING":
                lbl.styles.color = "lightgreen"
            elif new_status == "ERROR":
                lbl.styles.color = "red"
            else:
                lbl.styles.color = "white"
        except Exception:
            # Widget might not be ready yet. 
            # The on_mount will sync it up.
            pass

    def write_log(self, line: str):
        if not self.is_mounted:
            return
        log_widget = self.query_one(f"#log-{self.service_config['id']}", Log)
        log_widget.write_line(line.strip())

class Dashboard(Static):
    """Right-side dashboard."""
    def compose(self) -> ComposeResult:
        yield Label("[bold cyan]YUKI AI CONTROL CENTER[/]", id="dash-title")
        yield Label("System Ready.", id="dash-status")
        yield Label("\nActive Ports:\n• API: 8000\n• Web: 8081\n", classes="info-text")

class YukiLauncherApp(App):
    """The main TUI Application."""
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 1fr 1fr;
    }

    #left-col {
        row-span: 1;
        layout: grid;
        grid-size: 1 3;
        grid-rows: 1fr 1fr 1fr;
    }

    ServicePane {
        border: round white;
        padding: 0 1;
        margin: 0 0 1 0;
        height: 100%;
    }

    #right-col {
        height: 100%;
        border: round blue;
        padding: 1 2;
        content-align: center middle;
    }

    #dash-title {
        text-align: center;
        text-style: bold;
        color: cyan;
        margin-bottom: 2;
    }
    
    .info-text {
        color: lightgrey;
    }
    """

    BINDINGS = [("q", "quit", "Quit"), ("r", "restart_all", "Restart All")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        # Left Column (Services)
        with Container(id="left-col"):
            for svc in SERVICES:
                yield ServicePane(svc)
        
        # Right Column (Dashboard)
        with Container(id="right-col"):
            yield Dashboard()

        yield Footer()

    def on_mount(self) -> None:
        self.call_later(self.start_services)

    def start_services(self):
        for svc in SERVICES:
            self.run_worker(self.service_worker(svc), group="services")

    async def service_worker(self, service_config):
        pane = self.query_one(f"#service-{service_config['id']}", ServicePane)
        pane.status = "STARTING"
        
        cmd = service_config["command"][0]
        args = service_config["command"][1:]
        cwd = service_config["cwd"]
        
        try:
            # Async subprocess to avoid blocking the main loop
            import asyncio
            # Prepare environment with UTF-8 encoding
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["FORCE_COLOR"] = "1" # Force color output for Rich/Textual compatibility

            process = await asyncio.create_subprocess_exec(
                cmd, *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT, # Merge stderr into stdout
                cwd=service_config["cwd"],
                env=env
                # text=True is not available in create_subprocess_exec, we decode manually
                # creationflags=subprocess.CREATE_NEW_CONSOLE # Removed to ensure pipe capture works
            )
            
            pane.process = process
            pane.status = "RUNNING"
            
            # Streaming logs
            while True:
                line_bytes = await process.stdout.readline()
                if not line_bytes:
                    break
                
                # Decode explicitly
                line = line_bytes.decode('utf-8', errors='replace')
                if line:
                    pane.write_log(line)
                    with open("debug_services.log", "a", encoding="utf-8") as f:
                        f.write(f"[{service_config['id']}] {line}")
            
            await process.wait()
            pane.status = "STOPPED"
            
        except Exception as e:
            pane.status = "ERROR"
            error_msg = f"Error starting service: {e}\nType: {type(e)}"
            pane.write_log(error_msg)
            with open("debug_services.log", "a", encoding="utf-8") as f:
                f.write(f"[{service_config['id']}] CRITICAL ERROR: {error_msg}\n")

    def on_unmount(self) -> None:
        # Cleanup processes on exit
        # Note: subprocess.CREATE_NEW_CONSOLE means they are detached, 
        # so we might need to rely on the OS or manual cleanup if we want them to die with the app.
        # For a development launcher, typically we want to kill them.
        pass

if __name__ == "__main__":
    app = YukiLauncherApp()
    app.run()
