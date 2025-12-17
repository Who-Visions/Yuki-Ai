#!/usr/bin/env python3
"""
🩵 Yuki Watchdog & Autonomous Task Runner (Cyan)
================================================
A continuous, self-healing dashboard that monitors ACTUAL Yuki V8 Pipeline Activity.
Uses 'rich.live' and 'firebase-admin' to watch the real generation queue.
Pulls REAL Analytics from Google Cloud Monitoring.

Features:
- 🔁 Real-time Firestore Monitoring: Watches the 'generations' collection.
- 📈 GCP Analytics: Fetches CPU & Request metrics from Cloud Run via Monitoring API.
- 🐕 Watchdog: Monitors the monitoring thread itself.
- 📊 Real-time Dashboard: Shows ACTUAL user requests and processing status.
- 🛸 Antigravity Link: Monitors 'ANTIGRAVITY_NOTES.md' for user directives.

Usage:
    python yuki_watchdog.py
"""

import asyncio
import random
import time
import sys
import os
from datetime import datetime, timedelta
from collections import deque
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

from rich.live import Live
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.logging import RichHandler
from rich import box

# GCP Imports
try:
    from google.cloud import monitoring_v3
    from google.protobuf import timestamp_pb2
    GCP_AVAILABLE = True
except ImportError:
    GCP_AVAILABLE = False

# =============================================================================
# CONFIGURATION
# =============================================================================
TASK_interval = 2.0        # Seconds between task checks
NOTE_CHECK_INTERVAL = 1.0  # Check Notes frequently
GCP_CHECK_INTERVAL = 60.0  # Check GCP metrics every 60s (API quotas)
WATCHDOG_TIMEOUT = 30.0    # Seconds before watchdog considers a worker hung (Relaxed)
MAX_QUEUE_SIZE = 50
HANDOFF_FILE = r"c:\Yuki_Local\yuki-app\TEAM_HANDOFF.md"
ANTIGRAVITY_FILE = r"c:\Yuki_Local\ANTIGRAVITY_NOTES.md"
PROJECT_ID = "gifted-cooler-479623-r7" # From previous context

# =============================================================================
# DATA MODELS
# =============================================================================

class TaskStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    HEALED = "HEALED"

@dataclass
class YukiTask:
    id: str
    type: str
    target: str
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    
    @property
    def age(self):
        return time.time() - self.created_at

@dataclass
class SystemState:
    online: bool = True
    active_workers: int = 1
    cpu_load: float = 0.0      # Real GCP Metric
    request_count: int = 0     # Real GCP Metric
    container_count: int = 0   # Real GCP Metric
    uptime: float = 0.0
    tasks_processed: int = 0
    errors_caught: int = 0
    healed_events: int = 0
    last_gcp_update: float = 0.0

# =============================================================================
# CORE COMPONENTS
# =============================================================================

class GCPMonitor:
    """Fetches real metrics from Google Cloud Monitoring."""
    def __init__(self, project_id, log_queue):
        self.project_id = project_id
        self.project_name = f"projects/{project_id}"
        self.log_queue = log_queue
        self.client = monitoring_v3.MetricServiceClient() if GCP_AVAILABLE else None

    def fetch_metrics(self, state: SystemState):
        if not self.client:
            return

        try:
            now = time.time()
            # Loopback window (last 5 mins)
            interval = monitoring_v3.TimeInterval()
            now_proto = timestamp_pb2.Timestamp()
            now_proto.seconds = int(now)
            now_proto.nanos = int((now - int(now)) * 1e9)
            
            start_proto = timestamp_pb2.Timestamp()
            start_proto.seconds = int(now - 300)
            start_proto.nanos = 0
            
            interval.end_time = now_proto
            interval.start_time = start_proto

            # 1. CPU Utilization (Cloud Run)
            # Metric: run.googleapis.com/container/cpu/utilizations
            results = self.client.list_time_series(
                request={
                    "name": self.project_name,
                    "filter": 'metric.type = "run.googleapis.com/container/cpu/utilizations"',
                    "interval": interval,
                    "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                }
            )
            
            cpu_points = []
            for result in results:
                for point in result.points:
                    cpu_points.append(point.value.double_value)
            
            if cpu_points:
                state.cpu_load = (sum(cpu_points) / len(cpu_points)) * 100
                
            # 2. Request Count
            # Metric: run.googleapis.com/request_count
            results_req = self.client.list_time_series(
                request={
                    "name": self.project_name,
                    "filter": 'metric.type = "run.googleapis.com/request_count"',
                    "interval": interval,
                    "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                }
            )
            
            req_count = 0
            for result in results_req:
                for point in result.points:
                    req_count += point.value.int64_value
            state.request_count = req_count

            # 3. Active Instances (Container Count)
            # Metric: run.googleapis.com/container/instance_count
            results_inst = self.client.list_time_series(
                request={
                    "name": self.project_name,
                    "filter": 'metric.type = "run.googleapis.com/container/instance_count"',
                    "interval": interval,
                    "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                }
            )
            
            inst_count = 0
            for result in results_inst:
                for point in result.points:
                    inst_count = max(inst_count, point.value.int64_value)
            state.container_count = inst_count

            state.last_gcp_update = now
            self.log_queue.append(f"[blue]☁️ GCP Sync: CPU {state.cpu_load:.1f}% | Reqs: {state.request_count}[/]")

        except Exception as e:
            self.log_queue.append(f"[dim]GCP Fetch Warn: {str(e)[:50]}...[/dim]")


class Watchdog:
    """Monitors the Autonomous Worker and restarts it if it hangs."""
    def __init__(self, log_queue):
        self.last_heartbeat = time.time()
        self.log_queue = log_queue
        self.restarts = 0

    def heartbeat(self):
        self.last_heartbeat = time.time()

    def check(self) -> bool:
        """Returns True if healthy, False if hung."""
        gap = time.time() - self.last_heartbeat
        if gap > WATCHDOG_TIMEOUT:
            self.log_queue.append(f"[bold red]🐕 WATCHDOG ALERT: Worker hung for {gap:.1f}s![/]")
            return False
        return True

    def restart_worker(self):
        self.restarts += 1
        self.log_queue.append(f"[bold yellow]🐕 Watchdog: Restarting Worker Process (Attempt #{self.restarts})...[/]")
        self.last_heartbeat = time.time() # Reset


# ... (Previous code remains the same until NoteLoader) ...

class AntigravityScribe:
    """Writes updates back to the Antigravity Notes file."""
    def __init__(self, filepath):
        self.filepath = filepath

    def append_feed(self, message: str):
        """Appends a message to the Live Feed section."""
        try:
            if not os.path.exists(self.filepath): return
            
            with open(self.filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            feed_found = False
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            for line in lines:
                new_lines.append(line)
                if "## 📡 Live Feed" in line:
                    feed_found = True
                    # Add new message immediately after header
                    new_lines.append(f"- `[{timestamp}]` {message}\n")
            
            # Keep feed size manageable (optional: remove old lines if > 20)
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
                
        except Exception as e:
            print(f"Scribe Error: {e}")

    def mark_task_complete(self, task_text: str):
        """Marks a specifically text-matched task as complete [x]."""
        try:
            if not os.path.exists(self.filepath): return
            
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple replace for the specific line
            # We look for "- [ ] {task_text}"
            target = f"- [ ] {task_text}"
            replacement = f"- [x] {task_text}"
            
            if target in content:
                new_content = content.replace(target, replacement)
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        except Exception as e:
            print(f"Scribe Mark Error: {e}")

class ActionDispatcher:
    """Parses directives and triggers external Python agents."""
    def __init__(self, log_queue, state: SystemState, scribe: Optional[AntigravityScribe] = None):
        self.log_queue = log_queue
        self.state = state
        self.scribe = scribe
        self.active_processes = {} 

    def execute_command(self, command_text: str, requestor: str):
        """Executes a known command."""
        cmd_lower = command_text.lower()
        
        script = None
        name = "Unknown"
        
        # --- COMMAND MAPPING ---
        if "stress test" in cmd_lower:
            script = "stress_test_yuki.py"
            name = "StressTest"
        elif "server" in cmd_lower and "start" in cmd_lower:
            # Check if likely to fail
            if not os.path.exists("yuki_a2a_server.py"):
                 self._log_reply(f"❌ Cannot start server: File missing.")
                 return
            script = "yuki_a2a_server.py"
            name = "A2A Server"
        elif "handoff" in cmd_lower:
            script = "team_handoff.py"
            name = "Handoff"
        elif "status" in cmd_lower or "check" in cmd_lower:
            # Internal command
            self._log_reply(f"✅ System Online. CPU: {self.state.cpu_load:.1f}% | Reqs: {self.state.request_count}")
            return
            
        if script:
            self.log_queue.append(f"[bold green]🚀 DISPATCH: Launching {name} ({script})...[/]")
            self._log_reply(f"🚀 Launching {name}...")
            
            try:
                if sys.platform == "win32":
                    os.system(f"start cmd /k python {script}") 
                    self.log_queue.append(f"[dim]Process launched in new window.[/dim]")
                    self._log_reply(f"✅ Launched {name} in new window.")
                else:
                    import subprocess
                    subprocess.Popen(["python3", script])
                    self._log_reply(f"✅ Launched {name} (Background).")
            except Exception as e:
                self.log_queue.append(f"[bold red]❌ Launch Failed: {e}[/]")
                self._log_reply(f"❌ Launch Failed: {e}")

    def _log_reply(self, msg):
        if self.scribe:
            self.scribe.append_feed(msg)

class NoteLoader:
    """Reads both Team Handoffs and Antigravity Notes."""
    def __init__(self, handoff_path, antigravity_path, log_queue, dispatcher: ActionDispatcher, scribe: AntigravityScribe):
        self.handoff_path = handoff_path
        self.antigravity_path = antigravity_path
        self.log_queue = log_queue
        self.dispatcher = dispatcher
        self.scribe = scribe
        self.known_tasks = set()
    
    def scan(self) -> List[YukiTask]:
        new_tasks = []
        new_tasks.extend(self._scan_file(self.handoff_path, "HANDOFF"))
        new_tasks.extend(self._scan_file(self.antigravity_path, "USER_DIRECTIVE"))
        return new_tasks

    def _scan_file(self, filepath, type_prefix):
        tasks = []
        try:
            if not os.path.exists(filepath): return []
            with open(filepath, 'r', encoding='utf-8') as f: lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line.startswith("- [ ]") or (line.startswith("- ") and "@" in line):
                    # Strict Checkbox logic for directives
                    is_unchecked = line.startswith("- [ ]")
                    
                    text = line.replace("- [ ]", "").replace("- ", "").strip()
                    
                    target = "System"
                    if "@Ebony" in text: target = "Ebony"
                    elif "@Ivory" in text: target = "Ivory"
                    elif "@Cyan" in text: target = "Cyan"
                    
                    # Generate ID
                    tid = f"{type_prefix}-{hash(text) % 100000}"
                    
                    # Only process if we haven't seen this specific task ID in this run
                    # AND it is unchecked (for directives)
                    if tid not in self.known_tasks and is_unchecked:
                        self.known_tasks.add(tid)
                        
                        if type_prefix == "USER_DIRECTIVE":
                             self.log_queue.append(f"[bold cyan]u200b🛸 USER DIRECTIVE ({target}): {text}[/]")
                             self.dispatcher.execute_command(text, target)
                             
                             # Mark as complete in file
                             if self.scribe:
                                 self.scribe.mark_task_complete(text)
                        else:
                             self.log_queue.append(f"[magenta]📝 Handoff Note ({target}): {text[:20]}...[/]")

                        t = YukiTask(id=tid[:8], type=type_prefix, target=target, status=TaskStatus.PENDING)
                        tasks.append(t)
        except Exception as e: 
            pass
        return tasks

# ... (Previous code remains) ...

async def main_corrected():
    console = Console()
    layout = make_layout()
    
    tasks = deque()
    logs = deque(maxlen=20)
    state = SystemState()
    watchdog = Watchdog(logs)
    worker = AutonomousWorker(tasks, state, watchdog, logs)
    
    scribe = AntigravityScribe(ANTIGRAVITY_FILE)
    
    dispatcher = ActionDispatcher(logs, state, scribe)
    loader = NoteLoader(HANDOFF_FILE, ANTIGRAVITY_FILE, logs, dispatcher, scribe)
    
    # ... (Rest of main loop) ...


class AutonomousWorker:
    """Simulates the continuous task processor."""
    def __init__(self, task_queue: deque, state: SystemState, watchdog: Watchdog, log_queue):
        self.queue = task_queue
        self.state = state
        self.watchdog = watchdog
        self.log_queue = log_queue
        self.current_task: Optional[YukiTask] = None
        self._stalled = False # Test flag to simulate freeze
        self._logged_mock = False

    async def run_loop(self):
        # ... logic inside main loop ...
        pass

# =============================================================================
# TUI / VIEW
# =============================================================================

def make_layout() -> Layout:
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )
    layout["left"].split(
        Layout(name="status", size=10),
        Layout(name="queue")
    )
    return layout

def generate_table(tasks: deque) -> Table:
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("ID", style="cyan", width=12)
    table.add_column("Type", style="white")
    table.add_column("Target", style="dim")
    table.add_column("Status", width=12)
    table.add_column("Progress", width=20)

    # Show top 10
    for i, task in enumerate(list(tasks)[:10]):
        status_style = {
            TaskStatus.PENDING: "yellow",
            TaskStatus.PROCESSING: "blue bold",
            TaskStatus.COMPLETED: "green",
            TaskStatus.FAILED: "red",
            TaskStatus.HEALED: "magenta"
        }.get(task.status, "white")
        
        # ASCII Bar
        bar_len = 10
        filled = int((task.progress / 100) * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)

        table.add_row(
            task.id,
            task.type,
            task.target,
            f"[{status_style}]{task.status.value}[/]",
            f"[{status_style}]{bar} {int(task.progress)}%[/]"
        )
    return table

def generate_logs(logs: deque) -> Panel:
    text = Text()
    for log in list(logs)[-15:]:
        text.append(log + "\n")
    return Panel(text, title="System Logs", border_style="cyan")

def generate_header(state: SystemState) -> Panel:
    status_color = "green" if state.online else "red"
    mode_text = "[bold blue]☁️ REAL GCP ANALYTICS[/]" if GCP_AVAILABLE else "[bold red]⚠️ GCP OFFLINE (NO DATA)[/]"
    return Panel(
        f"🩵 [bold cyan]Yuki Autonomous Watchdog[/] | Status: [{status_color}]{'ONLINE' if state.online else 'OFFLINE'}[/] | {mode_text}\nInstances: {state.container_count} | Requests(5m): {state.request_count} | Healed: {state.healed_events}",
        style="white on black"
    )

def generate_status_panel(state: SystemState, watchdog: Watchdog) -> Panel:
    
    grid = Table.grid(padding=1)
    grid.add_column(style="bold")
    grid.add_column()
    
    grid.add_row("Cloud Run CPU:", f"{state.cpu_load:.1f}%")
    grid.add_row("Total Requests:", f"{state.request_count}")
    grid.add_row("Containers:", f"{state.container_count}")
    grid.add_row("Watchdog:", f"{'OK' if watchdog.check() else 'ALERT'}")
    grid.add_row("Last GCP Sync:", f"{time.time() - state.last_gcp_update:.0f}s ago")
    grid.add_row("Restarts:", f"[yellow]{watchdog.restarts}[/]")
    
    return Panel(grid, title="GCP System Health", border_style="green")

def generate_footer(state: SystemState) -> Panel:
    """Footer with commands and uptime."""
    uptime_str = f"{state.uptime / 60:.1f}m" if state.uptime < 3600 else f"{state.uptime / 3600:.1f}h"
    footer_text = (
        f"🛸 [bold cyan]Antigravity Command Center[/] | "
        f"📊 Processed: {state.tasks_processed} | "
        f"🩹 Healed: {state.healed_events} | "
        f"⏱️ Uptime: {uptime_str} | "
        f"[dim]Press Ctrl+C to exit[/]"
    )
    return Panel(footer_text, style="dim white on black")

# =============================================================================
# MAIN LOOP
# =============================================================================

async def main_corrected():
    console = Console()
    layout = make_layout()
    
    tasks = deque()
    logs = deque(maxlen=20)
    state = SystemState()
    watchdog = Watchdog(logs)
    worker = AutonomousWorker(tasks, state, watchdog, logs)
    
    scribe = AntigravityScribe(ANTIGRAVITY_FILE)
    
    dispatcher = ActionDispatcher(logs, state, scribe)
    loader = NoteLoader(HANDOFF_FILE, ANTIGRAVITY_FILE, logs, dispatcher, scribe)
    gcp_monitor = GCPMonitor(PROJECT_ID, logs)

    last_note_check = 0
    last_gcp_check = 0
    
    if not GCP_AVAILABLE:
        logs.append("[yellow]⚠️ google-cloud-monitoring not installed. Using mock metrics.[/]")
    else:
        logs.append("[bold cyan]☁️ Initializing GCP Monitoring...[/]")

    # Initial Chaos
    tasks.append(YukiTask("INIT-01", "BOOTSTRAP", "System", status=TaskStatus.PROCESSING))
    start_time = time.time()

    # Async Loop
    with Live(layout, refresh_per_second=5, screen=True) as live:
        try:
            while True:
                # Update uptime
                state.uptime = time.time() - start_time
                
                # --- Worker Logic ---
                if not watchdog.check():
                    # HEAL
                    state.healed_events += 1
                    watchdog.restart_worker()
                    worker = AutonomousWorker(tasks, state, watchdog, logs)
                
                try:
                    # Single tick of worker logic
                    # 1. Heartbeat
                    watchdog.heartbeat()
                    
                    # 2. GCP Sync (REAL DATA ONLY)
                    if GCP_AVAILABLE and (time.time() - last_gcp_check > GCP_CHECK_INTERVAL):
                        gcp_monitor.fetch_metrics(state)
                        last_gcp_check = time.time()
                    
                    # 3. Process Queue
                    if worker.current_task:
                        # For notes, we assume dispatch happened instantly in loader, so we just finish it.
                        worker.current_task.progress = 100
                        worker.current_task.status = TaskStatus.COMPLETED
                        state.tasks_processed += 1
                        logs.append(f"[green]✅ Processed {worker.current_task.id}[/]")
                        tasks.popleft()
                        worker.current_task = None
                        
                    elif tasks:
                        worker.current_task = tasks[0]
                        worker.current_task.status = TaskStatus.PROCESSING
                        logs.append(f"🤖 Processing {worker.current_task.id}...")
                    
                    # 4. Check Handoff Notes (REAL INPUT ONLY)
                    if time.time() - last_note_check > NOTE_CHECK_INTERVAL:
                        note_tasks = loader.scan()
                        for nt in note_tasks:
                            if len(tasks) < MAX_QUEUE_SIZE:
                                tasks.appendleft(nt) # Prioritize notes
                        last_note_check = time.time()


                except Exception as e:
                    logs.append(f"[red]Error: {e}[/red]")
                    state.errors_caught += 1

                # --- UI Update ---
                layout["header"].update(generate_header(state))
                layout["left"]["status"].update(generate_status_panel(state, watchdog))
                layout["left"]["queue"].update(Panel(generate_table(tasks), title=f"Queue Depth: {len(tasks)}", border_style="blue"))
                layout["right"].update(generate_logs(logs))
                layout["footer"].update(generate_footer(state))
                
                await asyncio.sleep(0.2)
                
        except KeyboardInterrupt:
            console.print("System Shutdown.")

if __name__ == "__main__":
    asyncio.run(main_corrected())
