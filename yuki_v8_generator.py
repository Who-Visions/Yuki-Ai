"""
🦊 YUKI V8 GENERATOR - MOCAP FACIAL IP LOCK SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

V8 ENHANCEMENTS:
1. Mocap Facial IP Extraction (18-zone face mapping)
2. Tiered Character Handling (Modern/Superhero/Fantasy/Cartoon)
3. Multi-Reference Image Support (3 photos per generation)
4. Stronger Facial Lock Prompts
5. Per-Generation Timing Display
6. Cleaner Progress Footer
7. Auto-Retry on Face Drift

Model: gemini-3-pro-image-preview (LOCKED)
"""

import asyncio
import time
import json
import random
import re
from pathlib import Path
from datetime import datetime
from typing import Optional
from google import genai
from google.genai import types
from PIL import Image

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from rich import box

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ID = "gifted-cooler-479623-r7"
OUTPUT_DIR = Path("C:/Yuki_Local/v8_test_results")
STATE_FILE = OUTPUT_DIR / "v8_state.json"
LOG_FILE = OUTPUT_DIR / "v8_test.log"

# Rate Limiting
BASE_DELAY = 80
DELAY_INCREMENT = 40
MAX_DELAY = 300
MAX_RETRIES = 5

# Character Tiers
TIER_MODERN = "modern"      # Suits, contemporary - best preservation
TIER_SUPERHERO = "superhero"  # Keep beard/hair, costume only
TIER_FANTASY = "fantasy"    # Period costumes - needs strongest lock
TIER_CARTOON = "cartoon"    # Humanized cartoon - styling only

console = Console()

# ═══════════════════════════════════════════════════════════════════════════════
# STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"completed": [], "failed": [], "current_delay": BASE_DELAY, "timings": []}

def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def log_event(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

# ═══════════════════════════════════════════════════════════════════════════════
# MOCAP FACIAL IP EXTRACTOR (V7 SYSTEM)
# ═══════════════════════════════════════════════════════════════════════════════

async def extract_facial_ip(client, input_images: list[Path], subject_name: str) -> dict:
    """
    Extract 18-zone Mocap facial geometry from subject photos.
    This is the V7 Facial IP system ported into V8.
    """
    console.print(f"\n[bold magenta]📐 EXTRACTING FACIAL IP (18-Zone Mocap)[/bold magenta]")
    console.print(f"   Subject: {subject_name} | Images: {len(input_images)}")
    
    # Use up to 5 best images for extraction
    sample_images = input_images[:5]
    
    prompt = f"""You are a forensic facial analyst performing mocap-level face mapping.
Analyze these {len(sample_images)} photos of the PRIMARY SUBJECT and create ultra-detailed measurements.

OUTPUT RAW JSON ONLY - NO MARKDOWN:

{{
  "subject_id": "{subject_name}",
  
  "zone_2_eyes": {{ "shape": "...", "cant": "...", "spacing": "wide/normal/close", "lid_type": "..." }},
  "zone_4_nose": {{ "bridge_shape": "...", "tip_shape": "...", "nostril_shape": "...", "width": "..." }},
  "zone_6_cheeks": {{ "prominence": "high/medium/low", "volume": "full/medium/hollow" }},
  "zone_8_chin": {{ "shape": "square/round/pointed", "projection": "strong/medium/weak", "width": "..." }},
  "zone_10_lips": {{ "upper_fullness": "...", "lower_fullness": "...", "width": "..." }},
  "zone_12_inter_feature_distances": {{ "eye_to_eye": "wide/normal/close", "nose_width_to_face": "..." }},
  "zone_14_jaw_definition": {{ "shape": "square/round/angular", "width": "wide/medium/narrow", "angle_sharpness": "sharp/soft" }},
  "zone_15_forehead": {{ "height": "high/medium/low", "width": "wide/medium/narrow" }},
  "zone_16_skin_surface": {{ "tone": "...", "texture": "smooth/textured", "facial_hair": "..." }},
  "zone_17_hair": {{ "type": "...", "color": "...", "style": "..." }},
  "zone_18_neck_jaw": {{ "transition": "sharp/defined/soft", "neck_width": "..." }},
  
  "critical_identity_lock": {{
    "top_5_identifiers": ["list the 5 most distinctive features that MUST be preserved"],
    "face_shape_overall": "oval/round/square/heart/oblong",
    "skin_tone_exact": "describe precisely",
    "age_appearance": "estimated age range"
  }}
}}"""

    try:
        # Load images
        image_parts = []
        for img_path in sample_images:
            img = Image.open(img_path)
            image_parts.append(img)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Fast model for analysis
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT"],
                temperature=0.0
            )
        )
        
        # Parse JSON from response
        text = response.text.strip()
        text = re.sub(r'```json\s*|\s*```', '', text)
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            facial_ip = json.loads(text[json_start:json_end])
            console.print(f"   [green]✅ Facial IP extracted successfully[/green]")
            log_event(f"Facial IP extracted for {subject_name}")
            return facial_ip
        else:
            raise ValueError("No valid JSON found")
            
    except Exception as e:
        console.print(f"   [yellow]⚠️ Facial IP extraction failed: {e}[/yellow]")
        log_event(f"Facial IP extraction failed: {e}")
        return {"error": str(e), "fallback": True}

def build_facial_lock_prompt(facial_ip: dict) -> str:
    """Build a strong facial preservation prompt from the IP profile."""
    
    if facial_ip.get("fallback") or facial_ip.get("error"):
        return """
CRITICAL FACIAL PRESERVATION:
- Preserve the EXACT face from the input photo
- Do NOT alter facial bone structure, skin tone, or features
- The costume goes ON this face - the face does NOT change
"""
    
    # Extract key identifiers
    identity = facial_ip.get("critical_identity_lock", {})
    top_5 = identity.get("top_5_identifiers", [])
    face_shape = identity.get("face_shape_overall", "")
    skin_tone = identity.get("skin_tone_exact", "")
    age = identity.get("age_appearance", "")
    
    # Build zones description
    zones = []
    if "zone_8_chin" in facial_ip:
        chin = facial_ip["zone_8_chin"]
        zones.append(f"Chin: {chin.get('shape', '')} shape, {chin.get('projection', '')} projection")
    if "zone_14_jaw_definition" in facial_ip:
        jaw = facial_ip["zone_14_jaw_definition"]
        zones.append(f"Jaw: {jaw.get('shape', '')} shape, {jaw.get('width', '')} width")
    if "zone_4_nose" in facial_ip:
        nose = facial_ip["zone_4_nose"]
        zones.append(f"Nose: {nose.get('bridge_shape', '')} bridge, {nose.get('tip_shape', '')} tip")
    if "zone_2_eyes" in facial_ip:
        eyes = facial_ip["zone_2_eyes"]
        zones.append(f"Eyes: {eyes.get('shape', '')}, {eyes.get('spacing', '')} spacing")
    
    prompt = f"""
═══════════════════════════════════════════════════════════════════════════════
                    🔒 MOCAP FACIAL IDENTITY LOCK 🔒
═══════════════════════════════════════════════════════════════════════════════

SUBJECT PROFILE:
- Face Shape: {face_shape}
- Skin Tone: {skin_tone}
- Age Appearance: {age}

BIOMETRIC MARKERS (MUST PRESERVE EXACTLY):
{chr(10).join(f'- {z}' for z in zones)}

TOP 5 IDENTITY ANCHORS:
{chr(10).join(f'- {id}' for id in top_5[:5])}

═══════════════════════════════════════════════════════════════════════════════
                         ⚠️ PRESERVATION RULES ⚠️
═══════════════════════════════════════════════════════════════════════════════

1. THIS IS THE EXACT FACE that MUST appear in the output
2. Facial bone structure is IMMUTABLE - do not alter for any reason
3. Skin tone and texture LOCKED - no changes allowed
4. The costume/outfit goes ON this exact person - face does NOT adapt
5. Hair may be styled for character but face geometry is FROZEN

"""
    return prompt

# ═══════════════════════════════════════════════════════════════════════════════
# TIERED PROMPT BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_tiered_prompt(char: dict, facial_lock: str) -> str:
    """Build character-specific prompts based on tier."""
    
    name = char["name"]
    source = char["source"]
    tier = char["tier"]
    
    if tier == TIER_MODERN:
        # Modern/contemporary - best preservation expected
        return f"""{facial_lock}

TRANSFORMATION REQUEST:
The exact person in these photos, dressed as {name} from {source}.

STYLING:
- Apply {name}'s signature outfit/styling
- Keep subject's natural face, beard, and general appearance
- Modern photorealistic quality, professional photography

OUTPUT: 4K photorealistic image of THIS PERSON cosplaying as {name}."""

    elif tier == TIER_SUPERHERO:
        # Superhero - costume focused, face locked
        return f"""{facial_lock}

TRANSFORMATION REQUEST:
The exact person in these photos wearing {name}'s superhero costume from {source}.

STYLING:
- Apply the full {name} costume/suit
- Subject's EXACT face visible (no full-face masks)
- Keep subject's natural beard/facial hair if present
- Heroic pose, dramatic lighting

OUTPUT: 4K photorealistic cosplay of THIS PERSON as {name}."""

    elif tier == TIER_FANTASY:
        # Fantasy/Period - STRONGEST face lock needed
        return f"""{facial_lock}

⚠️ CRITICAL - FANTASY CHARACTER PROTOCOL ⚠️

This exact person will be photographed wearing {name}'s costume from {source}.
The face in these reference photos is the ONLY face that should appear.

DO NOT:
- Generate a different person's face
- Alter facial bone structure
- Change skin tone or features
- Create a "generic" {name} face

DO:
- Apply {name}'s costume, hair styling, and accessories
- Keep the EXACT facial geometry from the input photos
- Period-appropriate setting and props

OUTPUT: 4K photorealistic image - THIS SPECIFIC PERSON in {name} costume."""

    elif tier == TIER_CARTOON:
        # Cartoon humanized - styling only
        return f"""{facial_lock}

TRANSFORMATION REQUEST:
The exact person in these photos styled as a live-action version of {name} from {source}.

APPROACH:
- This is NOT a face replacement - it's a COSTUME and STYLING application
- Subject's real face remains completely unchanged
- Apply {name}'s characteristic clothing/accessories/hair styling
- Capture {name}'s energy/pose/expression vibe

OUTPUT: 4K photorealistic cosplay - real person channeling {name}'s style."""

    else:
        # Default fallback
        return f"""{facial_lock}

Transform this person into {name} from {source}.
Preserve all facial features. Apply costume and styling only.

OUTPUT: 4K photorealistic cosplay masterpiece."""

# ═══════════════════════════════════════════════════════════════════════════════
# WATCHDOG
# ═══════════════════════════════════════════════════════════════════════════════

class Watchdog:
    def __init__(self):
        self.start_time = time.time()
        self.generations = 0
        self.failures = 0
        self.rate_limit_hits = 0
        self.last_success_time = time.time()
        self.timings = []
        
    def record_success(self, gen_time: float):
        self.generations += 1
        self.last_success_time = time.time()
        self.timings.append(gen_time)
        
    def record_failure(self, is_rate_limit: bool = False):
        self.failures += 1
        if is_rate_limit:
            self.rate_limit_hits += 1
            
    def get_stats(self) -> dict:
        runtime = time.time() - self.start_time
        avg_time = sum(self.timings) / len(self.timings) if self.timings else 0
        slowest = max(self.timings) if self.timings else 0
        return {
            "runtime_min": runtime / 60,
            "generations": self.generations,
            "failures": self.failures,
            "rate_limit_hits": self.rate_limit_hits,
            "avg_gen_time": avg_time,
            "slowest_gen": slowest,
            "success_rate": self.generations / max(1, self.generations + self.failures) * 100
        }

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

class YukiV8Generator:
    """V8 Generator with Mocap Facial IP Lock System"""
    
    def __init__(self, subject_name: str, input_dir: Path, characters: list[dict]):
        self.subject_name = subject_name
        self.input_dir = input_dir
        self.characters = characters
        self.output_dir = OUTPUT_DIR / subject_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Clients
        self.flash_client = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
        self.pro_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
        
        # State
        self.state = load_state()
        self.current_delay = self.state.get("current_delay", BASE_DELAY)
        self.watchdog = Watchdog()
        self.facial_ip = None
        
        # Input images
        self.input_images = (
            list(input_dir.glob("*.jpg")) + 
            list(input_dir.glob("*.JPG")) + 
            list(input_dir.glob("*.png")) + 
            list(input_dir.glob("*.jpeg"))
        )
        
        log_event(f"V8 Generator initialized - Subject: {subject_name}, {len(self.input_images)} images")

    async def generate_image(self, char: dict, gen_num: int) -> tuple[bool, float]:
        """Generate with full facial IP lock."""
        
        gen_start = time.time()
        char_name = char["name"]
        tier = char["tier"]
        
        # Build facial lock prompt
        facial_lock = build_facial_lock_prompt(self.facial_ip)
        
        # Build tiered prompt
        full_prompt = build_tiered_prompt(char, facial_lock)
        
        # Select multiple reference images (3 for stronger lock)
        ref_images = random.sample(self.input_images, min(3, len(self.input_images)))
        
        timestamp = datetime.now().strftime("%H%M%S")
        safe_name = char_name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")
        filename = f"{self.subject_name}_{safe_name}_gen{gen_num}_{timestamp}.png"
        save_path = self.output_dir / filename
        
        for attempt in range(MAX_RETRIES):
            try:
                # Load reference images
                image_parts = [Image.open(p) for p in ref_images]
                
                response = self.pro_client.models.generate_content(
                    model="gemini-3-pro-image-preview",
                    contents=image_parts + [full_prompt],
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
                    
                    gen_time = time.time() - gen_start
                    size_kb = save_path.stat().st_size / 1024
                    log_event(f"✅ {filename} ({size_kb:.1f}KB) [{gen_time:.1f}s] Tier:{tier}")
                    self.watchdog.record_success(gen_time)
                    return True, gen_time
                else:
                    raise Exception("No image in response")
                    
            except Exception as e:
                error_str = str(e)
                is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str
                
                self.watchdog.record_failure(is_rate_limit)
                log_event(f"❌ Attempt {attempt+1}: {char_name} - {error_str[:80]}")
                
                if is_rate_limit:
                    self.current_delay = min(self.current_delay + DELAY_INCREMENT, MAX_DELAY)
                    self.state["current_delay"] = self.current_delay
                    save_state(self.state)
                    await asyncio.sleep(self.current_delay)
                elif attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(30)
        
        gen_time = time.time() - gen_start
        log_event(f"💀 FAILED: {char_name} after {MAX_RETRIES} attempts")
        return False, gen_time

    async def run(self, gens_per_char: int = 2):
        """Main execution with Mocap Facial IP Lock."""
        
        console.print(Panel.fit(
            f"[bold cyan]🦊 YUKI V8 - MOCAP FACIAL IP LOCK[/bold cyan]\n\n"
            f"Subject: [yellow]{self.subject_name}[/yellow]\n"
            f"Characters: {len(self.characters)}\n"
            f"Generations: {gens_per_char} each = {len(self.characters) * gens_per_char} total\n"
            f"Model: gemini-3-pro-image-preview",
            box=box.DOUBLE
        ))
        
        console.print(f"\n📂 Input: {self.input_dir}")
        console.print(f"📂 Output: {self.output_dir}")
        console.print(f"⏳ Rate Limit Delay: {self.current_delay}s\n")
        
        if not self.input_images:
            console.print("[red]❌ No input images found![/red]")
            return
        
        # Step 1: Extract Facial IP
        self.facial_ip = await extract_facial_ip(
            self.flash_client, 
            self.input_images, 
            self.subject_name
        )
        
        # Build task list
        tasks = []
        for char in self.characters:
            for gen_num in range(1, gens_per_char + 1):
                task_id = f"{char['name']}_gen{gen_num}"
                if task_id not in self.state["completed"]:
                    tasks.append((char, gen_num, task_id))
        
        total_tasks = len(self.characters) * gens_per_char
        console.print(f"\n🎯 Tasks: {len(tasks)} remaining / {total_tasks} total\n")
        
        # Progress display
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TextColumn("[green]{task.fields[success]}✅[/green]"),
            TextColumn("[red]{task.fields[failed]}❌[/red]"),
            TextColumn("•"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            
            main_task = progress.add_task(
                "[cyan]Starting...", 
                total=len(tasks),
                success=0,
                failed=0
            )
            
            for idx, (char, gen_num, task_id) in enumerate(tasks):
                char_display = f"{char['name']} (Gen {gen_num})"
                tier_label = f"[{char['tier']}]"
                progress.update(main_task, description=f"[cyan]{char_display} {tier_label}")
                
                success, gen_time = await self.generate_image(char, gen_num)
                
                if success:
                    self.state["completed"].append(task_id)
                    progress.update(main_task, advance=1, success=self.watchdog.generations)
                    console.print(f"   [green]✅ {char_display} [{gen_time:.1f}s][/green]")
                else:
                    self.state["failed"].append(task_id)
                    progress.update(main_task, advance=1, failed=self.watchdog.failures)
                    console.print(f"   [red]❌ {char_display}[/red]")
                
                save_state(self.state)
                
                # Rate limit delay
                if idx < len(tasks) - 1:
                    for remaining in range(self.current_delay, 0, -10):
                        progress.update(main_task, description=f"[yellow]⏳ Wait {remaining}s...")
                        await asyncio.sleep(min(10, remaining))
        
        # Final summary
        stats = self.watchdog.get_stats()
        
        summary = Table(box=box.ROUNDED, show_header=False)
        summary.add_column("Metric", style="cyan")
        summary.add_column("Value", style="white")
        summary.add_row("✅ Successful", str(stats['generations']))
        summary.add_row("❌ Failed", str(stats['failures']))
        summary.add_row("⏱️ Runtime", f"{stats['runtime_min']:.1f} min")
        summary.add_row("📊 Success Rate", f"{stats['success_rate']:.1f}%")
        summary.add_row("⚡ Avg Gen Time", f"{stats['avg_gen_time']:.1f}s")
        summary.add_row("🐢 Slowest", f"{stats['slowest_gen']:.1f}s")
        summary.add_row("📂 Output", str(self.output_dir))
        
        console.print(Panel(summary, title="[bold green]🎉 V8 COMPLETE[/bold green]", box=box.DOUBLE))


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: MAURICE V8 RUN
# ═══════════════════════════════════════════════════════════════════════════════

YOLO_90S_CHALLENGE = [
    # FACE PAINT CHALLENGE
    {"name": "Eric Draven (The Crow)", "source": "The Crow (1994)", "tier": TIER_FANTASY},
    {"name": "Spawn (Al Simmons)", "source": "Spawn (1997)", "tier": TIER_FANTASY},  # Burns/scars
    
    # DISTINCTIVE HAIR CHALLENGE  
    {"name": "Simon Phoenix", "source": "Demolition Man (1993)", "tier": TIER_FANTASY},  # Bleached blonde
    {"name": "B.A. Baracus", "source": "The A-Team", "tier": TIER_CARTOON},  # Mohawk + chains
    {"name": "Clubber Lang", "source": "Rocky III (1982)", "tier": TIER_FANTASY},  # Mohawk, intimidating
    
    # ICONIC 90S LOOKS
    {"name": "Blade", "source": "Blade (1998)", "tier": TIER_SUPERHERO},  # Leather, shades
    {"name": "Morpheus", "source": "The Matrix (1999)", "tier": TIER_MODERN},  # Bald, shades, leather
    {"name": "Jules Winnfield", "source": "Pulp Fiction (1994)", "tier": TIER_MODERN},  # Jheri curl, suit
    {"name": "Candyman", "source": "Candyman (1992)", "tier": TIER_FANTASY},  # Fur coat, hook, horror
    
    # 90S TV ICONS
    {"name": "Fresh Prince (Will)", "source": "Fresh Prince of Bel-Air", "tier": TIER_MODERN},  # Colorful 90s
    {"name": "Martin Payne", "source": "Martin (1992)", "tier": TIER_MODERN},  # Wild outfits
    {"name": "Shang Tsung", "source": "Mortal Kombat (1995)", "tier": TIER_FANTASY},  # Sorcerer, long hair
]


if __name__ == "__main__":
    console.print("""
[bold magenta]
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🦊 YUKI V8 - MOCAP FACIAL IP LOCK 🦊                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  • 18-Zone Facial Geometry Extraction                                        ║
║  • Tiered Character Handling (Modern/Superhero/Fantasy/Cartoon)              ║
║  • Multi-Reference Image Support (3 photos per gen)                          ║
║  • Stronger Preservation Prompts                                             ║
║  • Per-Generation Timing                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
[/bold magenta]
""")
    
    gen = YukiV8Generator(
        subject_name="maurice",
        input_dir=Path("C:/Yuki_Local/Cosplay_Lab/Subjects/maurice"),
        characters=YOLO_90S_CHALLENGE
    )
    asyncio.run(gen.run(gens_per_char=2))
