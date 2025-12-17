from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
import time

def make_layout():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body")
    )
    return layout

layout = make_layout()

# Populate info BEFORE live
layout["header"].update(Panel("Header"))
layout["body"].update(Panel("Body"))

print("Starting debug run...")

# Use screen=False to see output in scrollback for debugging
with Live(layout, refresh_per_second=4, screen=False) as live:
    for i in range(5):
        layout["body"].update(Panel(f"Count: {i}"))
        time.sleep(0.5)

print("Debug run complete.")
