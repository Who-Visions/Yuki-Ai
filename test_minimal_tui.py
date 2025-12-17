#!/usr/bin/env python3
"""Minimal TUI to verify all widgets render correctly."""
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Label, Button, SelectionList, Input, Log

class TestTui(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    
    #test-list {
        height: 10;
        border: solid green;
    }
    
    #test-input {
        height: 3;
    }
    
    #test-log {
        height: 1fr;
        border: solid cyan;
    }
    
    Button {
        height: 3;
        width: 100%;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("TEST: Can you see this label?")
        yield Input(placeholder="TEST: Search...", id="test-input")
        yield SelectionList[str]("Neo", "Trinity", "Storm", id="test-list")
        yield Label("TEST: Log output below")
        yield Log(id="test-log")
        yield Button("TEST: Click me", id="test-btn")
        yield Footer()
    
    def on_mount(self):
        self.query_one("#test-log").write_line("TEST: TUI mounted successfully")
        self.query_one("#test-log").write_line("If you see this, the layout works")
    
    def on_button_pressed(self):
        log = self.query_one("#test-log", Log)
        log.write_line("Button clicked!")
        selected = self.query_one("#test-list", SelectionList).selected
        log.write_line(f"Selected: {selected}")

if __name__ == "__main__":
    app = TestTui()
    app.run()
