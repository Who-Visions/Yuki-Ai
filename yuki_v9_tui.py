import sys
import os
import asyncio
import re
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Log, Button, Label, Input, ListItem, ListView, Select, RadioSet, RadioButton, SelectionList
from textual.binding import Binding
from textual.reactive import reactive

# Character Data
V9_CHARACTERS = [
    {"name": "Neo", "sex": "male"}, {"name": "John Wick", "sex": "male"},
    {"name": "Trinity", "sex": "female"}, {"name": "Mia Wallace", "sex": "female"},
    {"name": "Black Panther", "sex": "male"}, {"name": "Blade", "sex": "male"},
    {"name": "Storm", "sex": "female"}, {"name": "Gamora", "sex": "female"},
    {"name": "Geralt of Rivia", "sex": "male"}, {"name": "Morpheus", "sex": "male"},
    {"name": "Daenerys Targaryen", "sex": "female"}, {"name": "Princess Leia", "sex": "female"},
    {"name": "The Doctor", "sex": "non-binary"}, {"name": "Desire", "sex": "non-binary"},
    {"name": "Angel", "sex": "male"}, {"name": "Loki", "sex": "non-binary"},
]

potential_roots = [Path("C:/Yuki_Local"), Path("/mnt/c/Yuki_Local")]
YUKI_ROOT = next((p for p in potential_roots if p.exists()), Path("C:/Yuki_Local"))
SUBJECTS_DIR = YUKI_ROOT / "Cosplay_Lab" / "Subjects"

class YukiGeneratorTui(App):
    BINDINGS = [Binding("q", "quit", "Quit")]
    current_subject = reactive("")
    is_running = reactive(False)
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal():
            # Left: Subjects
            with Vertical(id="left-panel"):
                yield Label("📁 SUBJECTS")
                yield ListView(id="subject-list")
                yield Button("🔄 Refresh", id="btn-refresh")
            
            # Right: Settings + Output
            with ScrollableContainer(id="right-panel"):
                yield Label("⚙️ SETTINGS")
                
                with Horizontal():
                    yield Label("Variations:")
                    yield RadioSet("1", "2", "4", id="variations")
                
                with Horizontal():
                    yield Label("Shot:")
                    yield Select([("Default", "default"), ("Portrait", "portrait"), ("Closeup", "closeup")], value="default", id="shot")
                
                with Horizontal():
                    yield Label("Filter:")
                    yield Select([("All", "all"), ("Male", "male"), ("Female", "female"), ("Non-Binary", "non-binary")], value="all", id="filter")
                
                yield Label("🎭 CHARACTERS")
                yield Input(placeholder="Search...", id="search")
                yield SelectionList[str](id="chars")
                
                yield Label("🦊 OUTPUT")
                yield Log(id="log")
                yield Button("🚀 RUN", id="btn-run", disabled=True)
        
        yield Footer()
    
    def on_mount(self):
        self.load_subjects()
        self.populate_chars()
        self.query_one("#log").write_line("Ready. Select subject + characters.")
    
    def load_subjects(self):
        if not SUBJECTS_DIR.exists():
            return
        
        listview = self.query_one("#subject-list", ListView)
        listview.clear()
        
        for item in sorted(SUBJECTS_DIR.iterdir()):
            if item.is_dir():
                clean_id = re.sub(r'[^a-zA-Z0-9_-]', '_', item.name)
                list_item = ListItem(Label(item.name), id=f"subj-{clean_id}")
                list_item.subject_name = item.name
                listview.append(list_item)
    
    def populate_chars(self, sex_filter="all", search=""):
        chars_list = self.query_one("#chars", SelectionList)
        old_selected = set(chars_list.selected)
        chars_list.clear_options()
        
        for char in V9_CHARACTERS:
            if sex_filter != "all" and char["sex"] != sex_filter:
                continue
            if search and search.lower() not in char["name"].lower():
                continue
            
            is_selected = char["name"] in old_selected
            chars_list.add_option((f"{char['name']} ({char['sex']})", char["name"], is_selected))
    
    def on_list_view_selected(self, event: ListView.Selected):
        if hasattr(event.item, "subject_name"):
            self.current_subject = event.item.subject_name
            self.query_one("#btn-run").disabled = False
            self.query_one("#log").write_line(f"Selected: {self.current_subject}")
    
    def on_select_changed(self, event: Select.Changed):
        if event.select.id == "filter":
            self.populate_chars(sex_filter=event.value, search=self.query_one("#search").value)
    
    def on_input_changed(self, event: Input.Changed):
        if event.input.id == "search":
            sex_filter = self.query_one("#filter", Select).value
            self.populate_chars(sex_filter=sex_filter, search=event.value)
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-refresh":
            self.load_subjects()
        elif event.button.id == "btn-run" and not self.is_running:
            self.run_generator()
    
    async def run_generator(self):
        if not self.current_subject:
            return
        
        variations = 2  # Default
        variations_radio = self.query_one("#variations", RadioSet)
        if variations_radio.pressed_button:
            variations = int(str(variations_radio.pressed_button.label))
        
        shot_type = self.query_one("#shot", Select).value
        selected_chars = self.query_one("#chars", SelectionList).selected
        
        if not selected_chars:
            self.query_one("#log").write_line("❌ No characters selected!")
            return
        
        self.is_running = True
        self.query_one("#btn-run").disabled = True
        log = self.query_one("#log", Log)
        log.clear()
        
        cmd = [
            "python3", "-u", "yuki_v9_generator.py",
            self.current_subject,
            "--variations", str(variations),
            "--shot-type", shot_type,
            "--characters"
        ] + selected_chars
        
        log.write_line(f"🚀 Starting...")
        log.write_line(f"Subject: {self.current_subject}")
        log.write_line(f"Variations: {variations}, Shot: {shot_type}")
        log.write_line(f"Characters: {', '.join(selected_chars)}")
        
        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["FORCE_COLOR"] = "1"
            
            self.process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=str(YUKI_ROOT),
                env=env
            )
            
            while True:
                line = await self.process.stdout.readline()
                if not line:
                    break
                log.write_line(line.decode('utf-8', errors='replace').rstrip())
            
            await self.process.wait()
            log.write_line(f"\n🏁 Exit code: {self.process.returncode}")
        except Exception as e:
            log.write_line(f"❌ Error: {e}")
        
        self.is_running = False
        self.query_one("#btn-run").disabled = False

if __name__ == "__main__":
    app = YukiGeneratorTui()
    app.run()
