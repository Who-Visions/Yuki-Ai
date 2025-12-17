"""
🦊 YUKI V7 MAURICE TEST GENERATOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Subject: Maurice
Model: gemini-3-pro-image-preview (LOCKED)
Generations: 2 per character
Rate Limiting: Start at 2/3 default, increase ONLY on 429 hits
Features: Rich Live CLI, Watchdog, Force Retry, DNA Preservation

Characters:
1. Homelander (The Boys)
2. Mighty Max (Mighty Max)
3. Ghost Rider (Marvel)
4. Dr. Robotnik (Sonic)
5. Dr. Doom (Marvel)
6. Robin Hood (Legend)
7. Darkwing Duck (Disney)
8. Nightwing (DC)
9. Chip (Chip 'n Dale Rescue Rangers)
10. Dale (Chip 'n Dale Rescue Rangers)
11. Jon Snow (Game of Thrones)
12. Ned Stark (Game of Thrones)
13. James St. Patrick "Ghost" (Power)
14. Mark Grayson / Invincible (Invincible)
15. Joey Tribbiani (Friends)
16. Cosmo Kramer (Seinfeld)
"""

import asyncio
import time
import json
import random
from pathlib import Path
from datetime import datetime
from typing import Optional
from google import genai
from google.genai import types
from PIL import Image

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ID = "gifted-cooler-479623-r7"
SUBJECT_NAME = "maurice"
INPUT_DIR = Path(f"C:/Yuki_Local/Cosplay_Lab/Subjects/{SUBJECT_NAME}")
OUTPUT_DIR = Path(f"C:/Yuki_Local/maurice_v7_test_results")
STATE_FILE = OUTPUT_DIR / "v7_state.json"
LOG_FILE = OUTPUT_DIR / "v7_maurice_test.log"

# Rate Limiting - Start conservative (2/3 of normal)
BASE_DELAY = 80  # Normal would be 120s, we start at 80s (2/3)
current_delay = BASE_DELAY
DELAY_INCREMENT = 40  # Add 40s on rate limit hit
MAX_DELAY = 300  # Cap at 5 minutes
MAX_RETRIES = 5

# Character Definitions
CHARACTERS = [
    {"name": "Homelander", "source": "The Boys", "genre": "superhero/antihero"},
    {"name": "Mighty Max", "source": "Mighty Max", "genre": "90s cartoon"},
    {"name": "Ghost Rider", "source": "Marvel Comics", "genre": "supernatural"},
    {"name": "Dr. Robotnik", "source": "Sonic the Hedgehog", "genre": "video game villain"},
    {"name": "Dr. Doom", "source": "Marvel Comics", "genre": "supervillain"},
    {"name": "Robin Hood", "source": "English Legend", "genre": "folklore hero"},
    {"name": "Darkwing Duck", "source": "Disney", "genre": "90s cartoon superhero"},
    {"name": "Nightwing", "source": "DC Comics", "genre": "superhero"},
    {"name": "Chip", "source": "Chip 'n Dale Rescue Rangers", "genre": "Disney adventure"},
    {"name": "Dale", "source": "Chip 'n Dale Rescue Rangers", "genre": "Disney adventure"},
    {"name": "Jon Snow", "source": "Game of Thrones", "genre": "fantasy"},
    {"name": "Ned Stark", "source": "Game of Thrones", "genre": "fantasy"},
    {"name": "James St. Patrick (Ghost)", "source": "Power", "genre": "crime drama"},
    {"name": "Mark Grayson / Invincible", "source": "Invincible", "genre": "superhero"},
    {"name": "Joey Tribbiani", "source": "Friends", "genre": "sitcom"},
    {"name": "Cosmo Kramer", "source": "Seinfeld", "genre": "sitcom"},
]

GENERATIONS_PER_CHAR = 2
console = Console()

# ═══════════════════════════════════════════════════════════════════════════════
# STATE MANAGEMENT (Resume Support)
# ═══════════════════════════════════════════════════════════════════════════════

def load_state() -> dict:
    """Load state from disk for resume capability"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"completed": [], "failed": [], "current_delay": BASE_DELAY}

def save_state(state: dict):
    """Save state to disk"""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def log_event(msg: str):
    """Append to log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

# ═══════════════════════════════════════════════════════════════════════════════
# WATCHDOG
# ═══════════════════════════════════════════════════════════════════════════════

class Watchdog:
    """Monitors generation health and triggers alerts"""
    
    def __init__(self):
        self.start_time = time.time()
        self.generations = 0
        self.failures = 0
        self.rate_limit_hits = 0
        self.last_success_time = time.time()
        self.stall_threshold = 600  # 10 minutes without success = stall
        
    def record_success(self):
        self.generations += 1
        self.last_success_time = time.time()
        
    def record_failure(self, is_rate_limit: bool = False):
        self.failures += 1
        if is_rate_limit:
            self.rate_limit_hits += 1
            
    def check_health(self) -> tuple[bool, str]:
        """Returns (healthy, message)"""
        time_since_success = time.time() - self.last_success_time
        
        if time_since_success > self.stall_threshold:
            return False, f"⚠️ STALL DETECTED: {time_since_success/60:.1f}min since last success"
        
        if self.failures > 10 and self.failures > self.generations:
            return False, f"⚠️ HIGH FAILURE RATE: {self.failures} failures vs {self.generations} successes"
            
        return True, "✅ System healthy"
    
    def get_stats(self) -> dict:
        runtime = time.time() - self.start_time
        return {
            "runtime_min": runtime / 60,
            "generations": self.generations,
            "failures": self.failures,
            "rate_limit_hits": self.rate_limit_hits,
            "success_rate": self.generations / max(1, self.generations + self.failures) * 100
        }

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

class YukiV7Generator:
    """V7 Generator with Rich Live CLI and Smart Rate Limiting"""
    
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize clients
        self.flash_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        self.pro_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
        
        # State
        self.state = load_state()
        self.current_delay = self.state.get("current_delay", BASE_DELAY)
        self.watchdog = Watchdog()
        
        # Get input images
        self.input_images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png")) + list(INPUT_DIR.glob("*.jpeg"))
        
        log_event(f"V7 Generator initialized - {len(self.input_images)} input images found")
        
    async def analyze_dna(self, image_path: Path) -> dict:
        """Fast DNA analysis with Gemini 2.5 Flash"""
        img = Image.open(image_path)
        
        prompt = """Analyze this person's features for authentic cosplay transformation:

**PHYSICAL TRAITS:**
- Age range, skin tone (Fitzpatrick scale), ethnic features
- Face shape, bone structure, facial proportions
- Hair: natural color, texture, type
- Eyes: color, shape, spacing
- Build type, height proportions

**PRESERVATION RULES:**
These features MUST be preserved in any transformation:
1. Exact skin tone and undertones
2. Facial bone structure and proportions
3. Age appearance
4. Body type and build

Respond in clear prose, be specific."""

        try:
            response = self.flash_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[img, prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT"],
                    temperature=0.1
                )
            )
            return {"analysis": response.text, "success": True}
        except Exception as e:
            log_event(f"DNA analysis failed: {e}")
            return {"analysis": "Preserve natural features, skin tone, age, and build.", "success": False}

    async def generate_image(self, char: dict, input_path: Path, analysis: dict, gen_num: int) -> bool:
        """Generate with gemini-3-pro-image-preview - LOCKED MODEL"""
        global current_delay
        
        char_name = char["name"]
        source = char["source"]
        genre = char["genre"]
        
        # Build rich prompt
        prompt = f"""Transform this person into {char_name} from {source}.

{analysis['analysis']}

=== CHARACTER TRANSFORMATION ===
Character: {char_name}
Source: {source} ({genre})
Style: Photorealistic cosplay with authentic costume details

=== PRESERVATION RULES ===
1. PRESERVE: Face structure, skin tone, age, body type, ethnic features
2. TRANSFORM: Hair style/color, outfit, accessories to match {char_name}
3. QUALITY: 4K resolution, professional photography, dramatic lighting
4. MAINTAIN: Natural bone structure, eye shape, facial geometry

=== CONTENT GUIDELINES ===
ALLOWED: Action poses, dramatic expressions, character-accurate costumes
PROHIBITED: Nudity, explicit content

OUTPUT: Photorealistic 4K cosplay masterpiece."""

        timestamp = datetime.now().strftime("%H%M%S")
        safe_name = char_name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")
        filename = f"{SUBJECT_NAME}_{safe_name}_gen{gen_num}_{timestamp}.png"
        save_path = self.output_dir / filename
        
        for attempt in range(MAX_RETRIES):
            try:
                input_img = Image.open(input_path)
                
                response = self.pro_client.models.generate_content(
                    model="gemini-3-pro-image-preview",  # LOCKED MODEL
                    contents=[input_img, prompt],
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        http_options=types.HttpOptions(timeout=15*60*1000)
                    )
                )
                
                # Extract image
                generated_data = None
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'image') and part.image:
                            generated_data = part.image.image_bytes
                            break
                        elif hasattr(part, 'inline_data') and part.inline_data:
                            generated_data = part.inline_data.data
                            break
                
                if generated_data:
                    with open(save_path, "wb") as f:
                        f.write(generated_data)
                    
                    if save_path.exists():
                        size_kb = save_path.stat().st_size / 1024
                        log_event(f"✅ SAVED: {filename} ({size_kb:.1f} KB)")
                        self.watchdog.record_success()
                        return True
                    else:
                        raise Exception("File write verification failed")
                else:
                    raise Exception("No image data in response")
                    
            except Exception as e:
                error_str = str(e)
                is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str
                
                self.watchdog.record_failure(is_rate_limit)
                log_event(f"❌ Attempt {attempt+1}/{MAX_RETRIES} failed for {char_name}: {error_str[:100]}")
                
                if is_rate_limit:
                    # Increase delay on rate limit
                    self.current_delay = min(self.current_delay + DELAY_INCREMENT, MAX_DELAY)
                    self.state["current_delay"] = self.current_delay
                    save_state(self.state)
                    log_event(f"⚠️ Rate limit hit! Delay increased to {self.current_delay}s")
                    await asyncio.sleep(self.current_delay)
                elif attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(30)  # Brief retry delay
                    
        log_event(f"💀 FAILED after {MAX_RETRIES} attempts: {char_name}")
        return False

    async def run(self):
        """Main execution with Rich Progress bars"""
        
        # Build task list
        tasks = []
        for char in CHARACTERS:
            for gen_num in range(1, GENERATIONS_PER_CHAR + 1):
                task_id = f"{char['name']}_gen{gen_num}"
                if task_id not in self.state["completed"]:
                    tasks.append((char, gen_num, task_id))
        
        total_tasks = len(CHARACTERS) * GENERATIONS_PER_CHAR
        completed = len(self.state["completed"])
        
        log_event(f"Starting V7 test: {len(tasks)} remaining tasks, {completed} already completed")
        console.print(f"\n[bold blue]🦊 YUKI V7 MAURICE TEST[/bold blue]")
        console.print(f"   📂 Input: {INPUT_DIR}")
        console.print(f"   📂 Output: {OUTPUT_DIR}")
        console.print(f"   🎯 Tasks: {len(tasks)} remaining / {total_tasks} total")
        console.print(f"   ⏳ Initial Delay: {self.current_delay}s\n")
        
        if not self.input_images:
            console.print("[red]❌ No input images found![/red]")
            return
        
        # Analyze DNA once
        console.print("[cyan]🔬 Analyzing DNA features...[/cyan]")
        input_img = random.choice(self.input_images)
        analysis = await self.analyze_dna(input_img)
        console.print("[green]✅ DNA analysis complete[/green]\n")
        
        # Create progress display
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TextColumn("[green]{task.fields[success]}[/green] ✅"),
            TextColumn("[red]{task.fields[failed]}[/red] ❌"),
            TextColumn("•"),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        )
        
        with progress:
            # Main progress bar
            main_task = progress.add_task(
                "[cyan]Generating...", 
                total=len(tasks),
                success=0,
                failed=0
            )
            
            for idx, (char, gen_num, task_id) in enumerate(tasks):
                char_display = f"{char['name']} (Gen {gen_num})"
                progress.update(main_task, description=f"[cyan]{char_display}")
                
                # Generate
                input_img = self.input_images[idx % len(self.input_images)]
                success = await self.generate_image(char, input_img, analysis, gen_num)
                
                if success:
                    self.state["completed"].append(task_id)
                    progress.update(main_task, advance=1, success=self.watchdog.generations)
                    console.print(f"   [green]✅ {char_display}[/green]")
                else:
                    self.state["failed"].append(task_id)
                    progress.update(main_task, advance=1, failed=self.watchdog.failures)
                    console.print(f"   [red]❌ {char_display}[/red]")
                
                save_state(self.state)
                
                # Check watchdog health
                healthy, msg = self.watchdog.check_health()
                if not healthy:
                    log_event(f"WATCHDOG ALERT: {msg}")
                    console.print(f"   [yellow]⚠️ {msg}[/yellow]")
                
                # Rate limit delay (only if more tasks)
                if idx < len(tasks) - 1:
                    # Show countdown
                    for remaining in range(self.current_delay, 0, -10):
                        progress.update(main_task, description=f"[yellow]⏳ Wait {remaining}s...")
                        await asyncio.sleep(min(10, remaining))
        
        # Final summary
        stats = self.watchdog.get_stats()
        console.print("\n" + "="*60)
        console.print("[bold green]🎉 V7 MAURICE TEST COMPLETE[/bold green]")
        console.print(f"   ✅ Successful: {stats['generations']}")
        console.print(f"   ❌ Failed: {stats['failures']}")
        console.print(f"   ⏱️ Runtime: {stats['runtime_min']:.1f} minutes")
        console.print(f"   📊 Success Rate: {stats['success_rate']:.1f}%")
        console.print(f"   📂 Output: {OUTPUT_DIR}")
        console.print("="*60 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    console.print("""
[bold blue]
╔══════════════════════════════════════════════════════════════╗
║           🦊 YUKI V7 MAURICE TEST GENERATOR 🦊              ║
╠══════════════════════════════════════════════════════════════╣
║  Model: gemini-3-pro-image-preview (LOCKED)                  ║
║  Subject: Maurice                                            ║
║  Characters: 16 | Generations: 2 each = 32 total            ║
║  Features: Progress Bar, Watchdog, Smart Rate Limiting       ║
╚══════════════════════════════════════════════════════════════╝
[/bold blue]
""")
    
    gen = YukiV7Generator()
    asyncio.run(gen.run())
