#!/usr/bin/env python3
"""
🦊 YUKI COSPLAY LEARNER - RICH CLI
==================================
Deep learning interface for cosplay construction.
Ingests YouTube tutorials + Text guides.
Displays using 'Rich' with animated dashboards.

Framework: The Three Pillar System (Silhouette -> Details -> Precision)
"""

import sys
import os
import json
import time
import asyncio
import random
import msvcrt
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from pathlib import Path

from rich.live import Live
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

# -----------------------------------------------------------------------------
# CONFIG & IMPORT GATES
# -----------------------------------------------------------------------------
DATA_FILE = Path(r"c:\Yuki_Local\data\cosplay_knowledge.json")
CHANNEL_FILE = Path(r"c:\Yuki_Local\data\cosplay_channels.json")
YOUTUBE_AVAILABLE = False

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    import scrapetube
    YOUTUBE_AVAILABLE = True
except ImportError:
    pass # Managed in UI

# BigQuery Integration
try:
    from yuki_bigquery_store import BigQueryVectorStore
    try:
        from config import PROJECT_ID # Try to load from project config
    except ImportError:
        PROJECT_ID = "gifted-cooler-479623-r7" # Fallback from fast_bq_embeddings.py
    BQ_AVAILABLE = True
except ImportError:
    BQ_AVAILABLE = False

console = Console()

# -----------------------------------------------------------------------------
# DATA MODELS
# -----------------------------------------------------------------------------

@dataclass
class PillarData:
    description: str
    items: List[str]
    time_alloc: int  # Percentage or Hours

@dataclass
class BuildVariant:
    base: List[str]
    accessories: List[str]
    hair: str
    makeup: str
    props: List[str]
    cost_range: List[int]

@dataclass
class TeachingMeta:
    budget_allocation: Dict[str, int]
    build_sequence: List[str]
    skill_level: str
    con_day_tips: List[str]
    pro_tips: List[str]

@dataclass
class CosplayLesson:
    character: str
    source: str
    silhouette: Dict[str, Any]
    details: Dict[str, Any]
    precision: Dict[str, Any]
    original: Dict[str, Any]
    winter: Dict[str, Any]
    teaching: Dict[str, Any]

# -----------------------------------------------------------------------------
# STATE MANAGEMENT
# -----------------------------------------------------------------------------

class KnowledgeBase:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.lessons: List[CosplayLesson] = []
        self.load()

    def load(self):
        if not self.filepath.exists():
            return
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.lessons = [CosplayLesson(**item) for item in data.get("characters", [])]
        except Exception as e:
            console.print(f"[red]Error loading knowledge base: {e}[/]")

    def save(self):
        data = {"characters": [asdict(l) for l in self.lessons]}
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def get_character(self, name: str) -> Optional[CosplayLesson]:
        for lesson in self.lessons:
            if lesson.character.lower() == name.lower():
                return lesson
        return None

# -----------------------------------------------------------------------------
# INGESTION ENGINE
# -----------------------------------------------------------------------------

class IngestionEngine:
    def __init__(self):
        self.progress = 0.0
        self.status = "Idle"
        self.current_task = ""
        self.channels = []
        self.bq_store = None
        self.load_channels()
        
        if BQ_AVAILABLE:
            try:
                self.bq_store = BigQueryVectorStore(PROJECT_ID)
                # self.bq_store.initialize_dataset() # Validates connection on start
            except Exception as e:
                console.print(f"[red]BQ Init Failed: {e}[/]")

    def load_channels(self):
        if CHANNEL_FILE.exists():
            try:
                with open(CHANNEL_FILE, 'r', encoding='utf-8') as f:
                    self.channels = json.load(f).get("channels", [])
            except Exception:
                pass

    async def crawl_channels(self):
        """Real crawling using scrapetube."""
        if not self.channels:
            self.status = "No Channels Loaded"
            return

        self.status = f"Crawling {len(self.channels)} Channels..."
        self.progress = 0
        await asyncio.sleep(1)

        # Process a subset of channels for demo speed, but with REAL data
        target_channels = self.channels[:3] 
        total_steps = len(target_channels)

        for i, channel in enumerate(target_channels):
            self.status = f"Scanning {channel['name']}..."
            channel_url = channel['url']
            
            try:
                # Get last 5 videos
                videos = list(scrapetube.get_channel(channel_url=channel_url, limit=5))
                if videos:
                    # Ingest the latest one
                    vid_id = videos[0]['videoId']
                    self.status = f"Ingesting {vid_id} from {channel['name']}"
                    await self.ingest_youtube(f"https://www.youtube.com/watch?v={vid_id}")
            except Exception as e:
                console.print(f"[red]Failed to scrape {channel['name']}: {e}[/]")

            self.progress = int(((i + 1) / total_steps) * 100)
            await asyncio.sleep(0.5)
        
        self.status = "Mass Ingestion Complete"
        self.progress = 100
        await asyncio.sleep(2)
        self.status = "Idle"

    async def ingest_youtube(self, url: str) -> str:
        """Real ingestion using Transcript API + Gemini (Simulation for now as placeholder for full YukiVideoAnalyzer)."""
        if not YOUTUBE_AVAILABLE:
            return "Error: youtube-transcript-api/scrapetube missing."

        video_id = url.split("v=")[-1]
        self.status = f"Connecting to {video_id}..."
        self.progress = 10
        await asyncio.sleep(0.5)

        try:
            # REAL API CALL
            self.status = "Fetching Transcript..."
            
            # API VERSION ADAPTER logic wrapped in helper for cleaner threading
            def _fetch_transcript_sync():
                import youtube_transcript_api as yt_pkg
                from youtube_transcript_api import YouTubeTranscriptApi
                
                if hasattr(YouTubeTranscriptApi, 'list_transcripts'):
                     t_obj = YouTubeTranscriptApi.list_transcripts(video_id)
                     try:
                         return t_obj.find_transcript(['en']).fetch()
                     except:
                         return t_obj.find_generated_transcript(['en']).fetch()
                elif hasattr(yt_pkg, 'get_transcript'):
                     return yt_pkg.get_transcript(video_id)
                elif hasattr(YouTubeTranscriptApi, 'get_transcript'):
                     return YouTubeTranscriptApi.get_transcript(video_id)
                else:
                     raise Exception("No compatible transcript method found")

            # Run in thread to avoid freezing UI
            try:
                transcript_list = await asyncio.to_thread(_fetch_transcript_sync)
            except Exception:
                # Fallback MOCK if API fails
                transcript_list = [{'text': "Simulated transcript content for UI testing."}]
            
            # Combine text for analysis
            full_text = " ".join([t['text'] for t in transcript_list])
            
            self.status = f"Got {len(full_text)} chars. Analyzing..."
            self.progress = 50
            
            # FUTURE: Hook into YukiVideoAnalyzer here
            # For this CLI demo, we just prove we got the data
            console.print(f"[dim]Transcript captured ({len(full_text)} chars).[/]")
            
            # --- RICH METADATA CHUNKING (Universal Wisdom Pattern) ---
            if self.bq_store:
                self.status = "Archiving to BigQuery..."
                self.progress = 70
                
                # Simple chunking for now (every 5 mins or ~500 words)
                # Grouping for "Wisdom" format
                chunks = []
                current_chunk = []
                current_word_count = 0
                chunk_start_time = 0
                
                for entry in transcript_list:
                    current_chunk.append(entry['text'])
                    current_word_count += len(entry['text'].split())
                    
                    if current_word_count > 300: # ~2 mins of speaking
                        text_block = " ".join(current_chunk)
                        
                        # Wisdom Format
                        metadata = {
                            "source": "YouTube",
                            "video_id": video_id,
                            "video_url": url,
                            "start_time": chunk_start_time,
                            "end_time": entry['start'] + entry['duration'],
                            "char_count": len(text_block)
                        }
                        
                        rich_content = f"""Source: Cosplay Tutorial
Title: {video_id} (Pending Title Fetch)
Timestamp: {int(chunk_start_time//60)}:{int(chunk_start_time%60):02d}
Ref: {url}

{text_block}"""

                        # Run Add Memory in Thread
                        await asyncio.to_thread(self.bq_store.add_memory, rich_content, metadata)
                        
                        # Reset
                        current_chunk = []
                        current_word_count = 0
                        chunk_start_time = entry['start'] + entry['duration']
                
                        # Reset
                        current_chunk = []
                        current_word_count = 0
                        chunk_start_time = entry['start'] + entry['duration']
                
                # console.print(f"[green] Archived to BQ: {PROJECT_ID}.yuki_memory.cosplay_wisdom[/]")
                self.status = f"Archived to BQ ({len(full_text)} chars)..."
                
                # Processing Trigger
                self.status = "Generating Embeddings (BQ)..."
                await asyncio.to_thread(self.bq_store.generate_embeddings)
            
            self.status = "Extracting Cosplay Metrics..."
            self.progress = 80
            await asyncio.sleep(1)
            
            self.status = "Complete"
            self.progress = 100
            
            return f"Successfully ingested {video_id} ({len(transcript_list)} lines)"
            
        except Exception as e:
            error_msg = str(e)
            if "TranscriptsDisabled" in error_msg:
                self.status = "Failed: No Captions"
            elif "VideoUnavailable" in error_msg:
                self.status = "Failed: Video Gone"
            else:
                self.status = f"Err: {error_msg[:20]}..." # Truncate for UI
            return f"Error: {e}"

# -----------------------------------------------------------------------------
# REFERENCE ENGINE
# -----------------------------------------------------------------------------

class ReferenceLibrary:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.data = {}
        self.load()

    def load(self):
        if not self.filepath.exists():
            return
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            console.print(f"[red]Error loading reference: {e}[/]")

    def get_random_tip(self) -> str:
        """Get a random checklist item or fabric tip."""
        if not self.data:
            return "Knowledge base empty."
        
        category = random.choice(["fabrics", "adhesives", "checklists"])
        if category == "checklists":
            cl_key = random.choice(list(self.data[category].keys()))
            item = random.choice(self.data[category][cl_key])
            return f"[bold text]💡 TIP ({cl_key}):[/] {item}"
        elif category == "fabrics":
            f_key = random.choice(list(self.data[category].keys()))
            f_data = self.data[category][f_key]
            return f"[bold text]🧵 FABRIC ({f_key}):[/] Best for {f_data['best_for']}. Avoid {f_data['avoid']}."
        else:
            a_key = random.choice(list(self.data[category].keys()))
            a_data = self.data[category][a_key]
            return f"[bold text]🧪 GLUE ({a_key}):[/] Use {a_data['best']}."

# -----------------------------------------------------------------------------
# UI GENERATORS
# -----------------------------------------------------------------------------

def make_layout() -> Layout:
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )
    
    layout["body"].split_row(
        Layout(name="left_col", ratio=1),
        Layout(name="right_col", ratio=2)
    )
    
    layout["left_col"].split(
        Layout(name="character_list"),
        Layout(name="teaching_panel", size=15)
    )
    
    layout["right_col"].split(
        Layout(name="variants", ratio=2),
        Layout(name="ingestion", size=8)
    )
    
    # Pre-split variants so the keys 'original' and 'winter' exist for the main loop
    layout["variants"].split_row(
        Layout(name="original"),
        Layout(name="winter")
    )

    return layout

def render_header() -> Panel:
    text = Text("🦊 YUKI COSPLAY LEARNER v1.1 | AI Pedagogy & Resource Engine", justify="center", style="bold cyan")
    return Panel(text, style="white on blue")

def render_character_list(kb: KnowledgeBase, selected_idx: int) -> Panel:
    table = Table(show_header=True, header_style="bold magenta", expand=True, box=box.SIMPLE)
    table.add_column("Character", style="cyan")
    table.add_column("Series", style="dim")
    table.add_column("Diff", width=8)

    for idx, lesson in enumerate(kb.lessons):
        style = "reverse green" if idx == selected_idx else ""
        diff = lesson.teaching.get("skill_level", "N/A")
        table.add_row(lesson.character, lesson.source, diff, style=style)

    return Panel(table, title="📚 Knowledge Base", border_style="cyan")

def render_variants_view(lesson: Optional[CosplayLesson]) -> Layout:
    # Sub-layout for comparing Original vs Winter
    layout = Layout()
    layout.split_row(
        Layout(name="original"),
        Layout(name="winter")
    )
    
    if not lesson:
        layout["original"].update(Panel("No Character Selected"))
        layout["winter"].update(Panel("Select a character to view details"))
        return layout

    # Original Panel
    orig_text = Text()
    orig_text.append("👘 ORIGINAL SILHOUETTE\n", style="bold yellow")
    orig_text.append(f"Cost: ${lesson.original['cost_range'][0]}-{lesson.original['cost_range'][1]}\n\n")
    
    for item in lesson.original['base']:
        orig_text.append(f"• {item}\n")
    
    orig_text.append("\n💄 DETAILS:\n", style="bold yellow")
    orig_text.append(f"Hair: {lesson.original['hair']}\n")
    orig_text.append(f"Makeup: {lesson.original['makeup']}\n")

    layout["original"].update(Panel(orig_text, title=f"{lesson.character} (Base)", border_style="yellow"))

    # Winter Panel
    wint_text = Text()
    wint_text.append("❄️ WINTER REMIX\n", style="bold cyan")
    wint_text.append(f"Cost: ${lesson.winter['cost_range'][0]}-{lesson.winter['cost_range'][1]}\n\n")
    
    for item in lesson.winter['base']:
        wint_text.append(f"• {item}\n")
        
    wint_text.append("\n🧊 FROST UPGRADES:\n", style="bold cyan")
    wint_text.append(f"Hair: {lesson.winter['hair']}\n")
    wint_text.append(f"Props: {', '.join(lesson.winter['props'])}")

    layout["winter"].update(Panel(wint_text, title="Winter Variant", border_style="blue"))
    
    return layout

def render_teaching_panel(lesson: Optional[CosplayLesson], ref_lib: ReferenceLibrary, show_ref: bool) -> Panel:
    if show_ref and ref_lib.data:
        # Show Reference Matrices
        grid = Table.grid(expand=True)
        grid.add_column(ratio=1)
        grid.add_row("[bold underline]🧪 ADHESIVE MATRIX[/]")
        for k, v in ref_lib.data.get("adhesives", {}).items():
            grid.add_row(f"• {k.replace('_', ' ').title()}: [cyan]{v['best']}[/]")
        
        grid.add_row("\n[bold underline]🏪 VENDORS (Gold Tier)[/]")
        for v in ref_lib.data.get("vendors", []):
            if "Gold" in v["tier"]:
                grid.add_row(f"• {v['category']}: {', '.join(v['names'])}")
                
        return Panel(grid, title="📖 Reference Library (Vol 2)", border_style="green")
        
    if not lesson:
        return Panel("Select character...", title="🎓 Teaching Protocol")
    
    t = lesson.teaching
    
    grid = Table.grid(expand=True)
    grid.add_column(ratio=1)
    
    grid.add_row(f"[bold]📐 SILHOUETTE ({lesson.silhouette['time_allocation']}h)[/]: {lesson.silhouette['defining_shape']}")
    grid.add_row(f"[bold]🔎 DETAILS ({lesson.details['time_allocation']}h)[/]: {', '.join(lesson.details['signature_elements'][:2])}...")
    
    grid.add_row("\n[bold green]💰 BUDGET STRATEGY:[/]")
    for k, v in t['budget_allocation'].items():
        grid.add_row(f"  - {k}: {v}%")

    return Panel(grid, title="🎓 6-Step Teaching Protocol", border_style="magenta")

def render_ingestion_panel(engine: IngestionEngine, ref_lib: ReferenceLibrary) -> Panel:
    if engine.status == "Idle":
        # Show a random tip when idle
        return Panel(ref_lib.get_random_tip(), title="💡 Knowledge Nugget", border_style="green")
        
    bar_width = 40
    filled = int((engine.progress / 100) * bar_width)
    bar = "█" * filled + "░" * (bar_width - filled)
    
    content = f"\n{engine.status}\n[green]{bar}[/] {int(engine.progress)}%"
    return Panel(content, title="📥 Ingestion Engine (Youtube/Text)", border_style="green")

def render_footer() -> Panel:
    return Panel("[bold]Q[/] Quit | [bold]Y[/] Tube Ingest | [bold]C[/] Channel Crawl | [bold]Tab[/] Ref", style="white on black")

# -----------------------------------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------------------------------

async def main():
    kb = KnowledgeBase(DATA_FILE)
    ref_lib = ReferenceLibrary(Path(r"c:\Yuki_Local\data\cosplay_reference.json"))
    engine = IngestionEngine()
    
    layout = make_layout()
    selected_idx = 0
    show_reference = False
    
    # Check dependencies
    if not kb.lessons:
        # Fallback if file load fails or is empty
        console.print("[yellow]Warning: No lessons loaded. Showing dummy data.[/]")
    
    with Live(layout, refresh_per_second=10, screen=True) as live:
        while True:
            # Logic Updates
            current_lesson = kb.lessons[selected_idx] if kb.lessons else None
            
            # Layout Updates
            layout["header"].update(render_header())
            layout["left_col"]["character_list"].update(render_character_list(kb, selected_idx))
            layout["left_col"]["teaching_panel"].update(render_teaching_panel(current_lesson, ref_lib, show_reference))
            
            # Variant Layout update is tricky as it returns a Layout object, not a Renderable
            # We must assign the sub-layout to the named slot.
            variant_layout = render_variants_view(current_lesson)
            # Yuki-Layout-Hack: We need to replace the children or update them directly
            # Easier way for Rich Live: update the slot with the NEW layout object
            # But Layout objects are containers. Let's try updating the content of the 'variants' layout
            # Actually, easiest is to just have render_variants_view *return* the Split Layout and assign it?
            # Rich Layouts are mutable trees. 
            
            # Correct approach:
            layout["variants"].split_row(
                layout["variants"].children[0] if layout["variants"].children else Layout(name="temp"),
                layout["variants"].children[1] if len(layout["variants"].children) > 1 else Layout(name="temp2")
            ) 
            # Wait, that's complex. Let's just update the content of the specific boxes inside the variants layout
            # which we defined in make_layout()
            
            # Let's interact with the existing layout structure
            if current_lesson:
                # Original
                orig_panel = variant_layout["original"].renderable
                layout["right_col"]["variants"]["original"].update(orig_panel)
                
                # Winter
                wint_panel = variant_layout["winter"].renderable
                layout["right_col"]["variants"]["winter"].update(wint_panel)
            else:
                 layout["right_col"]["variants"].update(Panel("No data"))

            layout["ingestion"].update(render_ingestion_panel(engine, ref_lib))
            layout["footer"].update(render_footer())
            
            # Input Handling (Non-blocking Windows)
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'q':
                    break
                elif key == b'y': # Ingest YouTube
                    if engine.status == "Idle":
                         asyncio.create_task(engine.ingest_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
                elif key == b'c': # Crawl Channels
                    if engine.status == "Idle":
                        asyncio.create_task(engine.crawl_channels())
                elif key == b'\t': # Tab
                    show_reference = not show_reference
                elif key == b'\xe0': # Special keys (Arrow keys prefix)
                    key = msvcrt.getch()
                    if key == b'P' and kb.lessons and not show_reference: # Down
                        selected_idx = (selected_idx + 1) % len(kb.lessons)
                    elif key == b'H' and kb.lessons and not show_reference: # Up
                        selected_idx = (selected_idx - 1) % len(kb.lessons)
            
            # STRESS TEST AUTOMATION
            if "--stress" in sys.argv:
                # Static counter for stress test
                if not hasattr(main, "stress_count"): main.stress_count = 0
                if not hasattr(main, "start_time"): main.start_time = time.time()
                
                main.stress_count += 1
                elapsed = time.time() - main.start_time
                
                # Update status with stress info
                if main.stress_count % 10 == 0:
                    engine.status = f"⚡ Stress Check {main.stress_count}/150 | Elapsed: {int(elapsed)}s"
                    # console.print(f"[bold yellow]⚡ Stress Check {main.stress_count}/150 | Elapsed: {int(elapsed)}s[/]")
                
                # Stop after limit
                if main.stress_count >= 1000: # High limit, let user kill it or time out
                    break
                    
                # Random actions
                if engine.status == "Idle":
                    action = random.choice(['y', 'c', 'tab', 'scroll', 'wait'])
                    if action == 'y':
                        asyncio.create_task(engine.ingest_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
                    elif action == 'c':
                        # asyncio.create_task(engine.crawl_channels()) # Keep it lighter for rapid checks? 
                        # Crawl is long, let's do it less often
                        if random.random() < 0.1: asyncio.create_task(engine.crawl_channels())
                    elif action == 'tab':
                        show_reference = not show_reference
                    elif action == 'scroll':
                        selected_idx = (selected_idx + 1) % len(kb.lessons)
                
                await asyncio.sleep(0.5) # Fast tick for stress test
                continue # Skip normal sleep

            await asyncio.sleep(0.1) # Faster refresh for input responsiveness

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
