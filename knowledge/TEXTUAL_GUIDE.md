# Textual TUI Guide

**Reference**: [Textual Tutorial](https://textual.textualize.io/tutorial/)

Textual is a TUI framework for Python inspired by modern web development. It uses a class-based architecture with CSS for styling.

## 1. The App Class
Every Textual app inherits from `App`. It manages the event loop and the root screen.

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

class MyApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle Dark Mode")]
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        yield Footer()
        
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

## 2. Widgets & Composition
- **`compose()`**: The primary method to define UI structure. Use `yield` to add child widgets.
- **Containers**: Use `Container`, `Vertical`, `Horizontal`, `Grid` to arrange widgets.
- **Built-ins**: `Button`, `Label`, `Input`, `Log`, `Static` (for text/panels).

```python
from textual.containers import Grid
from textual.widgets import Button, Label

class Calculator(Static):
    def compose(self) -> ComposeResult:
        yield Label("0", id="display")
        with Grid(id="buttons"):
            yield Button("1")
            yield Button("2")
```

## 3. Reactivity
Textual allows you to define `reactive` attributes. When these change, the UI updates automatically (via `watch_<attr>` methods or automatic re-rendering).

```python
from textual.reactive import reactive

class Counter(Static):
    count = reactive(0)

    def watch_count(self, old_value, new_value):
        self.update(f"Count: {new_value}")
```

## 4. CSS Styling
Textual uses a CSS-like syntax for layout and styling. You can define it in a `CSS` class attribute or an external file.

```python
class MyApp(App):
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
    }
    #sidebar {
        width: 20%;
        dock: left;
    }
    .error {
        color: red;
    }
    """
```

## 5. Async & Concurrency
Textual is built on `asyncio`.
- **Workers**: Use `@work` decorator or `self.run_worker()` for background tasks.
- **Thread Safety**: If running threads, use `self.call_from_thread(callback)` to update the UI.
- **Subprocesses**: Prefer `asyncio.create_subprocess_exec` within a worker function to keep the UI responsive.

## 6. Common Pitfalls
- **Blocking the Loop**: Never run long CPU tasks or `time.sleep()` in the main thread. Use Workers.
- **Mounting**: Widgets are not immediately available after `compose`. Use `on_mount` or `call_later` if you need to access DOM nodes right away.
- **Exceptions**: Use `textual run --dev my_app.py` to see detached tracebacks.

---
*Created by Antigravity for the Yuki Project*
