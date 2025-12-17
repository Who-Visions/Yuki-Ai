# Rich Live Display Guide

**Reference**: [Rich Live Documentation](https://rich.readthedocs.io/en/latest/live.html)

The `Live` class from `rich.live` allows for dynamic, auto-refreshing terminal displays. It is essential for dashboards, progress trackers, and monitoring tools.

## 1. Basic Usage
Wrap your renderable (Table, Panel, Layout, etc.) in a `Live` context manager. It automatically refreshes the screen.

```python
from rich.live import Live
from rich.panel import Panel
import time

with Live(Panel("Hello, World!"), refresh_per_second=4) as live:
    for _ in range(10):
        time.sleep(1)
        # You can update the renderable in real-time
        live.update(Panel(f"Time: {time.time()}"))
```

## 2. Key Configuration Options

### `screen=True` (Alternate Screen)
Opens the display in a separate full-screen buffer (like `vim` or `htop`). Restores the previous terminal state upon exit.
```python
with Live(layout, screen=True) as live:
    ...
```

### `transient=True`
Clears the live display from the terminal after the context manager exits. Useful for progress bars that shouldn't clutter logs.
```python
with Live(panel, transient=True):
    ...
```

### `refresh_per_second` (Default: 4)
Controls how often the TUI redraws.
- **Low (e.g., 1-4)**: Good for static text, saves CPU.
- **High (e.g., 10-20)**: Necessary for smooth animations or spinners.

### `vertical_overflow`
Controls behavior when content exceeds terminal height.
- `"ellipsis"` (Default): Abbreviates content with `...`
- `"crop"`: Cuts off extra content.
- `"visible"`: Forces full rendering (can break clearing capability).

## 3. Updating Content

### Method A: Internal Mutation (Preferred for complex objects)
Pass a mutable object (like `Table` or `Layout`) to `Live`. Modify the object directly; `Live` picks up changes on the next refresh.
```python
table = Table()
with Live(table):
    table.add_row("New Data") # Automatically shows up next frame
```

### Method B: `live.update()` (Swapping Renderables)
Completely replace the displayed object.
```python
with Live(generate_view()) as live:
    while True:
        live.update(generate_view()) # Replaces entire view
```

## 4. Handling Output (Stdout/Stderr)
Rich automatically redirects `print()` calls so they don't break the TUI layout. Printed text appears **above** the live display.

```python
with Live(panel) as live:
    live.console.print("Log message") # Appears above
    print("Standard print")           # Also appears above
```

## 5. Layouts
Use `rich.layout.Layout` to build grid systems (dashboards).

```python
from rich.layout import Layout

layout = Layout()
layout.split(
    Layout(name="header", size=3),
    Layout(name="body"),
    Layout(name="footer", size=3)
)
layout["body"].split_row(
    Layout(name="left"),
    Layout(name="right")
)

with Live(layout, screen=True):
    # Update specific sections
    layout["header"].update(Panel("Header"))
```

## 6. Common Pitfalls

- **Blocking Loops**: Ensure your main loop calls `time.sleep()` or `drains` events so the UI has time to refresh.
- **Deep Nesting**: Updating deep variables in a `Live` loop is fine, but ensure the *root* object passed to `Live` is what connects to them.
- **Exceptions**: Always wrap the `Live` context in a `try...except` block to ensure `screen=True` mode exits cleanly and restores the terminal.

## 7. Advanced: Nesting
As of Rich v14, you can nest `Live` instances. The inner `Live` renders below the outer one.

---
*Created by Antigravity for the Yuki Project*
