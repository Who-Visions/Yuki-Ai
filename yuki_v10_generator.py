"""
🦊 YUKI V9 GENERATOR - CLOUD VISION + MOCAP FACIAL IP LOCK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

V9 ENHANCEMENTS (on top of V8):
1. Cloud Vision API face detection (precise landmarks + emotions)
2. Quality validation before generation (rejects bad photos)
3. Smart reference selection (best pose angles)
4. Hybrid facial IP (Cloud Vision coords + Gemini semantics)
5. Optional SafeSearch content moderation

V8 Features Retained:
- 18-Zone Mocap Facial IP Extraction
- Tiered Character Handling (Modern/Superhero/Fantasy/Cartoon)
- Multi-Reference Image Support (3 photos per generation)
- Rate Limiting with exponential backoff

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
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TaskProgressColumn

# Import V9 Cloud Vision
from cloud_vision_analyzer import CloudVisionAnalyzer

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ID = "gifted-cooler-479623-r7"  # Cloud Vision project (using same as Vertex)

VERTEX_PROJECT_ID = "gifted-cooler-479623-r7"  # Vertex AI / Gemini project
FALLBACK_API_KEY = "AIzaSyDuyXnNc0BS4SKbtzxUBXNnP3KZ5OK-8YM"  # Google AI Studio API key

OUTPUT_DIR = Path(__file__).parent / "v9_results"
STATE_FILE = OUTPUT_DIR / "v9_state.json"
LOG_FILE = OUTPUT_DIR / "v9_test.log"

# Rate Limiting (minimal for API key mode)
BASE_DELAY = 10          # API key has higher limits
DELAY_INCREMENT = 5      # Minimal increase
MAX_DELAY = 30           # Lower max
MAX_RETRIES = 5

# Character Tiers (same as V8)
TIER_MODERN = "modern"
TIER_SUPERHERO = "superhero"
TIER_FANTASY = "fantasy"
TIER_CARTOON = "cartoon"

# Cloud Vision Settings
ENABLE_CLOUD_VISION = True  # Toggle V9 features
MIN_QUALITY_SCORE = 50      # Minimum quality to proceed
USE_FALLBACK = False        # Will be set True if Vertex AI exhausted

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
# V9 CLOUD VISION PRE-PROCESSING
# ═══════════════════════════════════════════════════════════════════════════════

def validate_images_with_cloud_vision(
    analyzer: CloudVisionAnalyzer, 
    image_paths: list[Path]
) -> tuple[list[Path], dict]:
    """
    V9: Pre-process all input images with Cloud Vision.
    
    Returns:
        (valid_images, facial_ip_data)
    """
    console.print("\n[bold magenta]🔍 V9 CLOUD VISION PRE-PROCESSING[/bold magenta]")
    
    valid_images = []
    best_image = None
    best_score = 0
    all_faces = []
    
    for img_path in image_paths:
        try:
            # Analyze with Cloud Vision (face detection only = FREE tier)
            result = analyzer.analyze_image(str(img_path), features=["face"])
            validation = analyzer.validate_for_generation(result)
            
            status = "✅" if validation["valid"] else "❌"
            score = validation["quality_score"]
            
            console.print(f"   {status} {img_path.name}: {score}/100")
            
            if validation["valid"] and score >= MIN_QUALITY_SCORE:
                valid_images.append(img_path)
                
                if result.get("faces"):
                    all_faces.append(result["faces"][0])
                
                # Track best image
                if score > best_score:
                    best_score = score
                    best_image = img_path
            
            if validation["issues"]:
                for issue in validation["issues"]:
                    console.print(f"      [dim]{issue}[/dim]")
                    
        except Exception as e:
            console.print(f"   [red]⚠️ {img_path.name}: {e}[/red]")
    
    # Build Cloud Vision facial IP data
    cv_facial_ip = {}
    if all_faces:
        best_face = min(all_faces, key=lambda f: abs(f["pan_angle"]) + abs(f["tilt_angle"]))
        cv_facial_ip = {
            "analyzed_count": len(all_faces),
            "best_confidence": max(f["confidence"] for f in all_faces),
            "avg_pose": {
                "roll": sum(f["roll_angle"] for f in all_faces) / len(all_faces),
                "pan": sum(f["pan_angle"] for f in all_faces) / len(all_faces),
                "tilt": sum(f["tilt_angle"] for f in all_faces) / len(all_faces),
            },
            "dominant_emotion": _get_dominant_emotion(all_faces),
            "best_face_bounds": best_face["bounds"],
        }
    
    console.print(f"   [green]Valid: {len(valid_images)}/{len(image_paths)} images[/green]\n")
    
    return valid_images, cv_facial_ip

def _get_dominant_emotion(faces: list[dict]) -> str:
    """Determine dominant emotion across all faces."""
    emotions = {"joy": 0, "neutral": 0, "serious": 0}
    for face in faces:
        if face["joy"] in ["LIKELY", "VERY_LIKELY"]:
            emotions["joy"] += 1
        elif face["anger"] in ["LIKELY", "VERY_LIKELY"] or face["sorrow"] in ["LIKELY", "VERY_LIKELY"]:
            emotions["serious"] += 1
        else:
            emotions["neutral"] += 1
    return max(emotions, key=emotions.get)

def select_optimal_references(
    valid_images: list[Path], 
    cv_facial_ip: dict, 
    analyzer: CloudVisionAnalyzer,
    count: int = 3
) -> list[Path]:
    """
    V9: Select best reference images based on Cloud Vision pose data.
    Prefers front-facing photos with high confidence.
    """
    if len(valid_images) <= count:
        return valid_images
    
    # Score each image by pose deviation from frontal
    scored = []
    for img_path in valid_images:
        result = analyzer.analyze_image(str(img_path), features=["face"])
        faces = result.get("faces", [])
        if faces:
            face = faces[0]
            # Lower deviation = better
            deviation = abs(face["pan_angle"]) + abs(face["tilt_angle"])
            score = face["confidence"] * 100 - deviation
            scored.append((img_path, score))
    
    # Sort by score (higher = better)
    scored.sort(key=lambda x: x[1], reverse=True)
    
    return [img for img, _ in scored[:count]]

# ═══════════════════════════════════════════════════════════════════════════════
# V8 MOCAP FACIAL IP EXTRACTOR (GEMINI-BASED)
# ═══════════════════════════════════════════════════════════════════════════════

async def extract_facial_ip_v10(client, input_images: list[Path], subject_name: str) -> dict:
    """
    V10: Extract 50-zone Mocap facial geometry using 2-Pass Logic.
    Pass 1: Low-latency extraction (gemini-3-pro, thinking=low)
    Pass 2: High-reasoning refinement (gemini-3-pro, thinking=high)
    """
    console.print(f"\n[bold cyan]🧬 EXTRACTING 50-ZONE FACIAL IP (V10 2-Pass)[/bold cyan]")
    
    sample_images = input_images[:5]
    
    prompt = f"""You are a forensic facial analyst performing mocap-level face mapping.
Analyze these {len(sample_images)} photos of the PRIMARY SUBJECT and create ultra-detailed 35-zone measurements.

OUTPUT RAW JSON ONLY - NO MARKDOWN:

{{
  "subject_id": "{subject_name}",
  
  "zone_01_forehead": {{ "height": "tall/medium/short", "width": "wide/medium/narrow", "shape": "flat/rounded/sloped" }},
  "zone_02_brow_ridge": {{ "prominence": "strong/medium/subtle", "shape": "straight/arched/angled" }},
  "zone_03_eyebrows": {{ "thickness": "thick/medium/thin", "shape": "straight/arched/angled", "spacing": "wide/close" }},
  "zone_04_upper_eyelid": {{ "crease": "visible/hooded/monolid", "depth": "deep/medium/shallow" }},
  "zone_05_eye_shape": {{ "shape": "almond/round/hooded/upturned/downturned", "cant": "positive/neutral/negative" }},
  "zone_06_eye_color": {{ "iris_color": "...", "limbal_ring": "present/absent" }},
  "zone_07_eye_spacing": {{ "ratio": "wide-set/average/close-set", "distance_mm_estimate": "..." }},
  "zone_08_under_eye": {{ "fullness": "full/medium/hollow", "darkness": "none/mild/prominent" }},
  "zone_09_nose_bridge": {{ "width": "wide/medium/narrow", "height": "high/medium/low", "shape": "straight/curved/bumped" }},
  "zone_10_nose_tip": {{ "shape": "bulbous/round/pointed/upturned", "width": "wide/medium/narrow" }},
  "zone_11_nostrils": {{ "shape": "flared/medium/narrow", "visibility": "visible/hidden" }},
  "zone_12_nasal_base": {{ "width": "wide/medium/narrow", "angle": "acute/right/obtuse" }},
  "zone_13_cheekbones": {{ "prominence": "high/medium/low", "width": "wide/medium/narrow", "position": "high/mid/low" }},
  "zone_14_cheek_hollow": {{ "depth": "prominent/subtle/none" }},
  "zone_15_nasolabial_folds": {{ "depth": "deep/medium/shallow/none" }},
  "zone_16_philtrum": {{ "definition": "defined/subtle/flat", "length": "long/medium/short" }},
  "zone_17_upper_lip": {{ "fullness": "full/medium/thin", "shape": "cupid_bow/straight/undefined", "vermillion_border": "defined/subtle" }},
  "zone_18_lower_lip": {{ "fullness": "full/medium/thin", "projection": "forward/neutral/recessed" }},
  "zone_19_lip_corners": {{ "angle": "upturned/neutral/downturned" }},
  "zone_20_mouth_width": {{ "ratio": "wide/medium/narrow" }},
  "zone_21_chin_front": {{ "shape": "square/round/pointed/cleft", "projection": "strong/medium/recessed" }},
  "zone_22_chin_width": {{ "width": "wide/medium/narrow" }},
  "zone_23_jawline": {{ "definition": "sharp/medium/soft", "angle": "angular/curved" }},
  "zone_24_jaw_width": {{ "width": "wide/medium/narrow" }},
  "zone_25_mandible_angle": {{ "angle": "defined/subtle/rounded" }},
  "zone_26_ear_position": {{ "height": "high/medium/low", "protrusion": "flat/normal/prominent" }},
  "zone_27_ear_shape": {{ "size": "large/medium/small", "lobe": "attached/detached" }},
  "zone_28_temple": {{ "fullness": "full/hollow" }},
  "zone_29_hairline": {{ "shape": "straight/widow_peak/rounded/receding", "height": "high/medium/low" }},
  "zone_30_hair_texture": {{ "type": "straight/wavy/curly/coily", "thickness": "thick/medium/fine" }},
  "zone_31_hair_color": {{ "base": "...", "highlights": "...", "gray_percentage": "..." }},
  "zone_32_skin_tone": {{ "undertone": "warm/cool/neutral", "depth": "fair/light/medium/tan/deep/dark" }},
  "zone_33_skin_texture": {{ "type": "smooth/textured/pores_visible", "imperfections": "..." }},
  "zone_34_facial_hair": {{ "presence": "none/stubble/beard/mustache", "pattern": "..." }},
  "zone_35_face_shape": {{ "overall": "oval/round/square/heart/oblong/diamond", "symmetry": "symmetrical/slight_asymmetry/notable_asymmetry" }},
  
  "zone_36_chin_cleft": {{ "presence": "yes/no", "depth": "deep/subtle/dimple", "shape": "vertical/horizontal" }},
  "zone_37_chin_dimple": {{ "presence": "yes/no", "position": "center/off_center" }},
  "zone_38_cheek_dimples": {{ "presence": "yes/no", "visibility": "always/when_smiling", "position": "high/low" }},
  "zone_39_neck_front": {{ "length": "long/medium/short", "width": "wide/medium/narrow", "adams_apple": "prominent/visible/subtle/none" }},
  "zone_40_neck_side": {{ "muscle_definition": "defined/subtle/soft", "veins": "visible/subtle/hidden" }},
  "zone_41_jaw_neck_transition": {{ "definition": "sharp/gradual/soft", "angle": "defined/smooth" }},
  "zone_42_facial_indentations": {{ "temple_hollows": "deep/subtle/none", "under_cheekbone": "prominent/subtle/none", "mentolabial_fold": "deep/medium/shallow" }},
  
  "critical_identity_lock": {{
    "top_10_identifiers": ["list the 10 most distinctive features that MUST be preserved"],
    "skin_tone_exact": "describe precisely with hex-like specificity",
    "bone_structure_summary": "describe underlying bone structure",
    "age_appearance": "estimated age range",
    "ethnicity_markers": "observable ethnic characteristics for accurate representation",
    "unique_indentations": "describe any dimples, clefts, hollows that define this face"
  }}
}}"""

    try:
        image_parts = [Image.open(p) for p in sample_images]
        
        # PASS 1: thinking=LOW for fast initial extraction
        console.print(f"   [cyan]Pass 1: Structuring (thinking=LOW)...[/cyan]")
        response_low = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT"],
                temperature=0.0,
                thinking_config=types.ThinkingConfig(thinking_level="low")
            )
        )
        
        text_low = response_low.text.strip()
        text_low = re.sub(r'```json\s*|\s*```', '', text_low)
        json_start = text_low.find('{')
        json_end = text_low.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            facial_ip_low = json.loads(text_low[json_start:json_end])
            console.print(f"   [green]✅ Pass 1 complete[/green]")
        else:
            raise ValueError("No valid JSON in Pass 1")
        
        # PASS 2: thinking=HIGH for deep refinement
        console.print(f"   [cyan]Pass 2: Refining (thinking=HIGH)...[/cyan]")
        
        refine_prompt = f"""You are refining a facial IP analysis. Here is the initial analysis:

{json.dumps(facial_ip_low, indent=2)}

Review the reference photos again and ENHANCE this analysis with:
1. More precise measurements
2. Correct any errors you see
3. Add more detail to sparse zones
4. Ensure ethnicity markers are accurate

OUTPUT REFINED JSON ONLY - NO MARKDOWN:"""

        response_high = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=[refine_prompt] + image_parts,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT"],
                temperature=0.0,
                thinking_config=types.ThinkingConfig(thinking_level="high")
            )
        )
        
        text_high = response_high.text.strip()
        text_high = re.sub(r'```json\s*|\s*```', '', text_high)
        json_start = text_high.find('{')
        json_end = text_high.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            facial_ip = json.loads(text_high[json_start:json_end])
            console.print(f"   [green]✅ Pass 2 complete - 2-PASS FACIAL IP EXTRACTED[/green]")
            return facial_ip
        else:
            # Fall back to Pass 1 if Pass 2 fails
            console.print(f"   [yellow]⚠️ Pass 2 failed, using Pass 1 result[/yellow]")
            return facial_ip_low
            
    except Exception as e:
        console.print(f"   [yellow]⚠️ Facial IP extraction failed: {e}[/yellow]")
        return {"error": str(e), "fallback": True}

# ═══════════════════════════════════════════════════════════════════════════════
# V9 HYBRID FACIAL LOCK PROMPT
# ═══════════════════════════════════════════════════════════════════════════════

def build_v9_facial_lock(gemini_ip: dict, cloud_vision_ip: dict) -> str:
    """
    V9: Combine Cloud Vision precise data with Gemini semantic analysis.
    """
    
    if gemini_ip.get("fallback"):
        # Fallback if Gemini failed
        cv_data = cloud_vision_ip or {}
        return f"""
CRITICAL FACIAL PRESERVATION:
- Preserve the EXACT face from the input photos
- Face Detection Confidence: {cv_data.get('best_confidence', 'N/A')}
- Do NOT alter facial bone structure or features
"""
    
    # Extract Gemini data
    identity = gemini_ip.get("critical_identity_lock", {})
    top_5 = identity.get("top_5_identifiers", [])
    face_shape = identity.get("face_shape_overall", "")
    skin_tone = identity.get("skin_tone_exact", "")
    
    # Extract Cloud Vision data
    cv = cloud_vision_ip or {}
    avg_pose = cv.get("avg_pose", {})
    confidence = cv.get("best_confidence", 0)
    
    prompt = f"""
═══════════════════════════════════════════════════════════════════════════════
                    🔒 V9 HYBRID FACIAL IDENTITY LOCK 🔒
═══════════════════════════════════════════════════════════════════════════════

SUBJECT PROFILE:
- Face Shape: {face_shape}
- Skin Tone: {skin_tone}
- Cloud Vision Confidence: {confidence:.1%}
- Average Pose: Roll={avg_pose.get('roll', 0):.1f}° Pan={avg_pose.get('pan', 0):.1f}°

TOP 5 IDENTITY ANCHORS:
{chr(10).join(f'- {id}' for id in top_5[:5])}

═══════════════════════════════════════════════════════════════════════════════
                         ⚠️ PRESERVATION RULES ⚠️
═══════════════════════════════════════════════════════════════════════════════

1. THIS IS THE EXACT FACE that MUST appear in the output
2. Facial bone structure is IMMUTABLE
3. Skin tone and texture LOCKED
4. The costume goes ON this exact person
5. Hair may be styled but face geometry is FROZEN
"""
    return prompt

# ═══════════════════════════════════════════════════════════════════════════════
# TIERED PROMPT BUILDER (SAME AS V8)
# ═══════════════════════════════════════════════════════════════════════════════

# ... existing code ...

def build_tiered_prompt(char: dict, facial_lock: str, shot_type: str = "") -> str:
    """Build character-specific prompts based on tier."""
    
    name = char["name"]
    source = char["source"]
    tier = char["tier"]
    
    # Shot type modifier
    shot_instruction = ""
    if shot_type == "portrait":
        shot_instruction = "\nCOMPOSITION: Full body portrait, showing feet, head to toe."
    elif shot_type == "closeup":
        shot_instruction = "\nCOMPOSITION: Close-up bust shot, focus on face and shoulders."
    
    if tier == TIER_MODERN:
        return f"""{facial_lock}

TRANSFORMATION REQUEST:
The exact person in these photos, dressed as {name} from {source}.

STYLING:
- Apply {name}'s signature outfit/styling
- Keep subject's natural face, beard, and appearance
- Modern photorealistic quality{shot_instruction}

OUTPUT: 4K photorealistic image of THIS PERSON as {name}."""

    elif tier == TIER_SUPERHERO:
        return f"""{facial_lock}

TRANSFORMATION REQUEST:
The exact person wearing {name}'s superhero costume from {source}.

STYLING:
- Apply the full {name} costume/suit
- Subject's EXACT face visible (no full-face masks)
- Heroic pose, dramatic lighting{shot_instruction}

OUTPUT: 4K photorealistic cosplay of THIS PERSON as {name}."""

    elif tier == TIER_FANTASY:
        return f"""{facial_lock}

⚠️ CRITICAL - FANTASY CHARACTER PROTOCOL ⚠️

This exact person in {name}'s costume from {source}.
The face in these reference photos is the ONLY face that should appear.

DO NOT:
- Generate a different person's face
- Alter facial bone structure
- Change skin tone or features

DO:
- Apply {name}'s costume, hair styling, and accessories
- Keep EXACT facial geometry from input photos{shot_instruction}

OUTPUT: 4K photorealistic - THIS SPECIFIC PERSON in {name} costume."""

    elif tier == TIER_CARTOON:
        return f"""{facial_lock}

TRANSFORMATION REQUEST:
The exact person styled as a live-action version of {name} from {source}.

APPROACH:
- This is COSTUME and STYLING application, not face replacement
- Subject's real face remains unchanged
- Apply {name}'s characteristic clothing/accessories{shot_instruction}

OUTPUT: 4K photorealistic cosplay - real person channeling {name}'s style."""

    else:
        return f"""{facial_lock}

Transform this person into {name} from {source}.
Preserve all facial features. Apply costume and styling only.{shot_instruction}

OUTPUT: 4K photorealistic cosplay masterpiece."""

# ═══════════════════════════════════════════════════════════════════════════════
# V9 MAIN GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

class YukiV10Generator:
    """V10 Generator: V8 + Cloud Vision + 2-Pass Refinement"""
    
    def __init__(self, subject_name: str, input_dir: Path, characters: list[dict], shot_type: str = ""):
        self.subject_name = subject_name
        self.input_dir = input_dir
        self.characters = characters
        self.shot_type = shot_type
        self.output_dir = OUTPUT_DIR / subject_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Clients - API-only mode (skip Vertex AI rate limits)
        self.flash_client = genai.Client(vertexai=True, project=VERTEX_PROJECT_ID, location="global")
        self.pro_client = genai.Client(api_key=FALLBACK_API_KEY)  # Direct API key - no Vertex
        
        # Cloud Vision (V9) - uses PROJECT_ID with caching enabled
        self.cv_analyzer = CloudVisionAnalyzer(project_id=PROJECT_ID, enable_cache=True)
        
        # State
        self.state = load_state()
        self.current_delay = self.state.get("current_delay", BASE_DELAY)
        self.using_fallback = False  # Track if we switched to fallback API key
        
        # Input images
        self.input_images = (
            list(input_dir.glob("*.jpg")) + 
            list(input_dir.glob("*.JPG")) + 
            list(input_dir.glob("*.png")) + 
            list(input_dir.glob("*.jpeg"))
        )
        
        # V9 data
        self.cloud_vision_ip = {}
        self.gemini_ip = {}
        
        log_event(f"V9 Generator initialized - Subject: {subject_name}, {len(self.input_images)} images")

    async def run(self, gens_per_char: int = 2):
        """Main execution with Cloud Vision + Mocap Facial IP Lock."""
        
        console.print(Panel.fit(
            f"[bold cyan]🦊 YUKI V9 - CLOUD VISION + MOCAP[/bold cyan]\n\n"
            f"Subject: [yellow]{self.subject_name}[/yellow]\n"
            f"Characters: {len(self.characters)}\n"
            f"Generations: {gens_per_char} each = {len(self.characters) * gens_per_char} total\n"
            f"Shot Type: {self.shot_type if self.shot_type else 'Default'}\n"
            f"Cloud Vision: {'✅ Enabled' if ENABLE_CLOUD_VISION else '❌ Disabled'}",
            box=box.DOUBLE
        ))
        
        if not self.input_images:
            console.print("[red]❌ No input images found![/red]")
            return
        
        # ═══ V9 Step 1: Cloud Vision Pre-Processing ═══
        if ENABLE_CLOUD_VISION:
            valid_images, self.cloud_vision_ip = validate_images_with_cloud_vision(
                self.cv_analyzer, 
                self.input_images
            )
            
            if not valid_images:
                console.print("[red]❌ No valid images after Cloud Vision validation![/red]")
                return
            
            # Select optimal references
            self.input_images = select_optimal_references(
                valid_images, 
                self.cloud_vision_ip, 
                self.cv_analyzer,
                count=5
            )
            console.print(f"[green]📷 Using {len(self.input_images)} best references[/green]\n")
        
        # ═══ V10 Step 2: Gemini 2-Pass Extraction ═══
        self.gemini_ip = await extract_facial_ip_v10(
            self.flash_client,
            self.input_images,
            self.subject_name
        )
        
        # ═══ V9 Step 3: Build Hybrid Facial Lock ═══
        facial_lock = build_v9_facial_lock(self.gemini_ip, self.cloud_vision_ip)
        
        # ═══ Step 4: Generate ═══
        total_tasks = len(self.characters) * gens_per_char
        success_count = 0
        fail_count = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=False,
            refresh_per_second=4
        ) as progress:
            gen_task = progress.add_task("[cyan]🎨 Generating...", total=total_tasks)
            results = []  # Collect results to print after
            
            for char in self.characters:
                for gen_num in range(1, gens_per_char + 1):
                    task_id = f"{char['name']}_gen{gen_num}"
                    if task_id in self.state["completed"]:
                        progress.advance(gen_task)
                        continue
                    
                    progress.update(gen_task, description=f"[cyan]🎨 {char['name']}...")
                    success, gen_time = await self._generate_image(char, gen_num, facial_lock)
                    
                    if success:
                        self.state["completed"].append(task_id)
                        success_count += 1
                        results.append(f"   [green]✅ {char['name']} ({gen_num}) [{gen_time:.1f}s][/green]")
                    else:
                        self.state["failed"].append(task_id)
                        fail_count += 1
                        results.append(f"   [red]❌ {char['name']} ({gen_num})[/red]")
                    
                    save_state(self.state)
                    progress.advance(gen_task)
                    await asyncio.sleep(self.current_delay)
        
        # Print results after progress bar is done
        for result in results:
            console.print(result)
        console.print(f"\n[bold green]✅ Complete: {success_count} success, {fail_count} failed[/bold green]")

    async def _generate_image(self, char: dict, gen_num: int, facial_lock: str) -> tuple[bool, float]:
        """Generate single image with V9 pipeline."""
        
        gen_start = time.time()
        
        # Build prompt
        full_prompt = build_tiered_prompt(char, facial_lock, self.shot_type)
        
        # Select reference images
        ref_images = random.sample(self.input_images, min(3, len(self.input_images)))
        
        # Output filename
        timestamp = datetime.now().strftime("%H%M%S")
        safe_name = char["name"].replace(" ", "_").replace("/", "-")
        filename = f"{self.subject_name}_{safe_name}_v10_gen{gen_num}_{timestamp}.png"  # v10 = Official 2-Pass
        save_path = self.output_dir / filename
        
        for attempt in range(MAX_RETRIES):
            try:
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
                    log_event(f"✅ {filename} [{gen_time:.1f}s]")
                    return True, gen_time
                else:
                    raise Exception("No image in response")
                    
            except Exception as e:
                error_str = str(e)
                is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str
                
                log_event(f"❌ Attempt {attempt+1}: {char['name']} - {error_str[:80]}")
                
                if is_rate_limit:
                    # Switch to fallback API key after first rate limit
                    if attempt >= 1 and not self.using_fallback:
                        console.print(f"[yellow]⚠️ Switching to fallback API key...[/yellow]")
                        log_event("Switching to fallback API key")
                        self.pro_client = genai.Client(api_key=FALLBACK_API_KEY)
                        self.using_fallback = True
                        await asyncio.sleep(5)  # Brief pause before retry
                    else:
                        self.current_delay = min(self.current_delay + DELAY_INCREMENT, MAX_DELAY)
                        await asyncio.sleep(self.current_delay)
                elif attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(30)
        
        return False, time.time() - gen_start


# ═══════════════════════════════════════════════════════════════════════════════
# TEST CONFIG - 30 WAIFU CHARACTERS (15 Winter, 15 Original)
# ═══════════════════════════════════════════════════════════════════════════════

V9_TEST_CHARACTERS = [
    # ════════════════════════════════════════════════════════════════════════════
    # WINTER THEMED (15) - Cozy sweaters, snow, holiday vibes
    # ════════════════════════════════════════════════════════════════════════════
    {"name": "Mikasa Ackerman (Winter)", "source": "Attack on Titan", "tier": TIER_MODERN, "sex": "female", "theme": "winter"},
    {"name": "Zero Two (Christmas)", "source": "Darling in the Franxx", "tier": TIER_MODERN, "sex": "female", "theme": "winter"},
    {"name": "Hinata Hyuga (Snow)", "source": "Naruto", "tier": TIER_FANTASY, "sex": "female", "theme": "winter"},
    {"name": "Yor Forger (Holiday)", "source": "Spy x Family", "tier": TIER_MODERN, "sex": "female", "theme": "winter"},
    {"name": "Marin Kitagawa (Cozy)", "source": "My Dress-Up Darling", "tier": TIER_MODERN, "sex": "female", "theme": "winter"},
    {"name": "Nezuko (Winter Kimono)", "source": "Demon Slayer", "tier": TIER_FANTASY, "sex": "female", "theme": "winter"},
    {"name": "Rem (Christmas Maid)", "source": "Re:Zero", "tier": TIER_FANTASY, "sex": "female", "theme": "winter"},
    {"name": "Asuna (Snow Queen)", "source": "Sword Art Online", "tier": TIER_FANTASY, "sex": "female", "theme": "winter"},
    {"name": "Makima (Winter Coat)", "source": "Chainsaw Man", "tier": TIER_MODERN, "sex": "female", "theme": "winter"},
    {"name": "Power (Santa)", "source": "Chainsaw Man", "tier": TIER_MODERN, "sex": "female", "theme": "winter"},
    {"name": "Boa Hancock (Fur Coat)", "source": "One Piece", "tier": TIER_FANTASY, "sex": "female", "theme": "winter"},
    {"name": "Android 18 (Winter)", "source": "Dragon Ball Z", "tier": TIER_SUPERHERO, "sex": "female", "theme": "winter"},
    {"name": "Sailor Moon (Ice Princess)", "source": "Sailor Moon", "tier": TIER_FANTASY, "sex": "female", "theme": "winter"},
    {"name": "Tohru (Dragon Maid Christmas)", "source": "Miss Kobayashi", "tier": TIER_FANTASY, "sex": "female", "theme": "winter"},
    {"name": "Ochaco Uraraka (Snow Hero)", "source": "My Hero Academia", "tier": TIER_SUPERHERO, "sex": "female", "theme": "winter"},
    
    # ════════════════════════════════════════════════════════════════════════════
    # ORIGINAL COSTUMES (15) - Classic iconic looks
    # ════════════════════════════════════════════════════════════════════════════
    {"name": "Mikasa Ackerman", "source": "Attack on Titan", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Zero Two", "source": "Darling in the Franxx", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Hinata Hyuga", "source": "Naruto", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Yor Forger", "source": "Spy x Family", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Marin Kitagawa", "source": "My Dress-Up Darling", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Nezuko Kamado", "source": "Demon Slayer", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Rem", "source": "Re:Zero", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Asuna Yuuki", "source": "Sword Art Online", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Makima", "source": "Chainsaw Man", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Power", "source": "Chainsaw Man", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Boa Hancock", "source": "One Piece", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Android 18", "source": "Dragon Ball Z", "tier": TIER_SUPERHERO, "sex": "female", "theme": "original"},
    {"name": "Sailor Moon", "source": "Sailor Moon", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Tohru", "source": "Miss Kobayashi's Dragon Maid", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Ochaco Uraraka", "source": "My Hero Academia", "tier": TIER_SUPERHERO, "sex": "female", "theme": "original"},
    
    # ════════════════════════════════════════════════════════════════════════════
    # ADDITIONAL WAIFUS (20 more to reach 50)
    # ════════════════════════════════════════════════════════════════════════════
    # Classics
    {"name": "Bulma", "source": "Dragon Ball", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Erza Scarlet", "source": "Fairy Tail", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Lucy Heartfilia", "source": "Fairy Tail", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Nami", "source": "One Piece", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Robin", "source": "One Piece", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    
    # Modern Hits
    {"name": "Nobara Kugisaki", "source": "Jujutsu Kaisen", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Maki Zenin", "source": "Jujutsu Kaisen", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Nico Robin (Winter)", "source": "One Piece", "tier": TIER_FANTASY, "sex": "female", "theme": "winter"},
    {"name": "Momo Yaoyorozu", "source": "My Hero Academia", "tier": TIER_SUPERHERO, "sex": "female", "theme": "original"},
    {"name": "Tsuyu Asui", "source": "My Hero Academia", "tier": TIER_SUPERHERO, "sex": "female", "theme": "original"},
    
    # Iconic
    {"name": "Rei Ayanami", "source": "Neon Genesis Evangelion", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Asuka Langley", "source": "Neon Genesis Evangelion", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Misato Katsuragi", "source": "Neon Genesis Evangelion", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Rukia Kuchiki", "source": "Bleach", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    {"name": "Yoruichi Shihoin", "source": "Bleach", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    
    # Seasonal
    {"name": "Shoko Komi (Winter)", "source": "Komi Can't Communicate", "tier": TIER_MODERN, "sex": "female", "theme": "winter"},
    {"name": "Kaguya Shinomiya", "source": "Kaguya-sama", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Chika Fujiwara", "source": "Kaguya-sama", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Mai Sakurajima", "source": "Bunny Girl Senpai", "tier": TIER_MODERN, "sex": "female", "theme": "original"},
    {"name": "Aqua", "source": "Konosuba", "tier": TIER_FANTASY, "sex": "female", "theme": "original"},
    
    # ════════════════════════════════════════════════════════════════════════════
    # 90s BLACK TV SHOW LEADS (Jordan Remix) - Female leads with refactored titles
    # ════════════════════════════════════════════════════════════════════════════
    {"name": "Khadijah (Living Jordan)", "source": "Living Single", "tier": TIER_MODERN, "sex": "female", "theme": "90s_tv"},
    {"name": "Jordan as Moesha", "source": "Moesha", "tier": TIER_MODERN, "sex": "female", "theme": "90s_tv"},
    {"name": "Joan (Jordan's Girlfriends)", "source": "Girlfriends", "tier": TIER_MODERN, "sex": "female", "theme": "90s_tv"},
    {"name": "Nikki (The Jordans)", "source": "The Parkers", "tier": TIER_MODERN, "sex": "female", "theme": "90s_tv"},
    {"name": "Tia and Tamera (Jordan Jordan)", "source": "Sister Sister", "tier": TIER_MODERN, "sex": "female", "theme": "90s_tv"},
    {"name": "Whitley (Jordan's World)", "source": "A Different World", "tier": TIER_MODERN, "sex": "female", "theme": "90s_tv"},
    {"name": "Dee Dee (Jordan and Half)", "source": "Half and Half", "tier": TIER_MODERN, "sex": "female", "theme": "90s_tv"},
    {"name": "Hilary Banks (Jordan of Bel-Air)", "source": "Fresh Prince of Bel-Air", "tier": TIER_MODERN, "sex": "female", "theme": "90s_tv"},
    {"name": "Gina (Jordan's Martin)", "source": "Martin", "tier": TIER_MODERN, "sex": "female", "theme": "90s_tv"},
    {"name": "Laura Winslow (Jordan Matters)", "source": "Family Matters", "tier": TIER_MODERN, "sex": "female", "theme": "90s_tv"},

    # ════════════════════════════════════════════════════════════════════════════
    # 90s HORROR MOVIE LEADS - For 4-model A/B test
    # ════════════════════════════════════════════════════════════════════════════
    {"name": "Sidney Prescott", "source": "Scream (1996)", "tier": TIER_MODERN, "sex": "female", "theme": "90s_horror"},
    {"name": "Julie James", "source": "I Know What You Did Last Summer", "tier": TIER_MODERN, "sex": "female", "theme": "90s_horror"},
    {"name": "Sarah Bailey", "source": "The Craft (1996)", "tier": TIER_FANTASY, "sex": "female", "theme": "90s_horror"},
    {"name": "Maureen Evans", "source": "Scream 2 (1997)", "tier": TIER_MODERN, "sex": "female", "theme": "90s_horror"},
    {"name": "Karla Wilson", "source": "I Still Know What You Did (1998)", "tier": TIER_MODERN, "sex": "female", "theme": "90s_horror"},

    # ════════════════════════════════════════════════════════════════════════════
    # 2000s NICKELODEON - Cartoons and TV Shows
    # ════════════════════════════════════════════════════════════════════════════
    {"name": "Sam Puckett", "source": "iCarly", "tier": TIER_MODERN, "sex": "female", "theme": "nick_2000s"},
    {"name": "Carly Shay", "source": "iCarly", "tier": TIER_MODERN, "sex": "female", "theme": "nick_2000s"},
    {"name": "Zoey Brooks", "source": "Zoey 101", "tier": TIER_MODERN, "sex": "female", "theme": "nick_2000s"},
    {"name": "Lola Martinez", "source": "Zoey 101", "tier": TIER_MODERN, "sex": "female", "theme": "nick_2000s"},
    {"name": "Tori Vega", "source": "Victorious", "tier": TIER_MODERN, "sex": "female", "theme": "nick_2000s"},
    {"name": "Jade West", "source": "Victorious", "tier": TIER_MODERN, "sex": "female", "theme": "nick_2000s"},
    {"name": "Trina Vega", "source": "Victorious", "tier": TIER_MODERN, "sex": "female", "theme": "nick_2000s"},
    {"name": "Kim Possible", "source": "Kim Possible", "tier": TIER_CARTOON, "sex": "female", "theme": "nick_2000s"},
    {"name": "Shego", "source": "Kim Possible", "tier": TIER_CARTOON, "sex": "female", "theme": "nick_2000s"},
    {"name": "Danny Phantom Girl", "source": "Danny Phantom", "tier": TIER_CARTOON, "sex": "female", "theme": "nick_2000s"},

    # ════════════════════════════════════════════════════════════════════════════
    # COMIC BOOK HEROINES (Marvel & DC) - 2-Pass Stress Test
    # ════════════════════════════════════════════════════════════════════════════
    {"name": "Storm", "source": "X-Men", "tier": TIER_FANTASY, "sex": "female", "theme": "comics"},
    {"name": "Wonder Woman", "source": "DC Comics", "tier": TIER_FANTASY, "sex": "female", "theme": "comics"},
    {"name": "Black Widow", "source": "Marvel Comics", "tier": TIER_MODERN, "sex": "female", "theme": "comics"},
    {"name": "Harley Quinn", "source": "DC Comics", "tier": TIER_MODERN, "sex": "female", "theme": "comics"},
    {"name": "Scarlet Witch", "source": "Marvel Comics", "tier": TIER_FANTASY, "sex": "female", "theme": "comics"},
    {"name": "Catwoman", "source": "DC Comics", "tier": TIER_MODERN, "sex": "female", "theme": "comics"},
    {"name": "Rogue", "source": "X-Men", "tier": TIER_FANTASY, "sex": "female", "theme": "comics"},
    {"name": "Supergirl", "source": "DC Comics", "tier": TIER_FANTASY, "sex": "female", "theme": "comics"},
    {"name": "Jean Grey", "source": "X-Men", "tier": TIER_FANTASY, "sex": "female", "theme": "comics"},
    {"name": "Starfire", "source": "Teen Titans", "tier": TIER_FANTASY, "sex": "female", "theme": "comics"},
]





if __name__ == "__main__":
    import sys
    import argparse
    
    console.print("""
[bold cyan]
╔══════════════════════════════════════════════════════════════════════════════╗
║                   🧬 YUKI V10 - 2-PASS FACIAL CORE 🧬                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  • Cloud Vision Face Detection (precise landmarks)                           ║
║  • 2-Pass Gemini Analysis (Low Latency → High Reasoning Refinement)          ║
║  • Quality Validation (rejects bad photos)                                   ║
║  • Smart Reference Selection (optimal poses)                                 ║
║  • 50-Zone Hybrid Facial Lock                                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
[/bold cyan]
""")
    
    parser = argparse.ArgumentParser(description="Yuki V10 Generator")
    parser.add_argument("subject", help="Subject name (folder name)")
    parser.add_argument("--variations", type=int, default=2, help="Number of variations per character")
    parser.add_argument("--characters", nargs="+", help="Specific characters to generate (by name)")
    parser.add_argument("--sex", choices=["all", "male", "female", "non-binary"], default="all", help="Filter by sex")
    parser.add_argument("--shot-type", choices=["default", "portrait", "closeup"], default="default", help="Shot type modifier")
    
    args = parser.parse_args()
    
    subject = args.subject
    base_dir = Path(__file__).parent
    input_dir = base_dir / "Cosplay_Lab/Subjects" / subject
    
    if not input_dir.exists():
        subject_underscores = subject.replace(" ", "_")
        input_dir_underscores = base_dir / "Cosplay_Lab/Subjects" / subject_underscores
        if input_dir_underscores.exists():
            console.print(f"[yellow]Redirecting to folder with underscores: {subject_underscores}[/yellow]")
            input_dir = input_dir_underscores
            subject = subject_underscores
        else:
            console.print(f"[red]Subject folder not found: {input_dir}[/red]")
            sys.exit(1)
            
    # Filter characters
    selected_chars = V9_TEST_CHARACTERS
    
    # 1. Filter by specific names if provided
    if args.characters and "all" not in args.characters:
        # Case insensitive matching
        target_names = [n.lower() for n in args.characters]
        selected_chars = [c for c in selected_chars if c["name"].lower() in target_names]
        
    # 2. Filter by sex
    if args.sex != "all":
        selected_chars = [c for c in selected_chars if c.get("sex") == args.sex]
        
    if not selected_chars:
        # If filters result in empty list, maybe user picked characters that don't match the sex filter?
        # Or just picked invalid names.
        console.print("[red]❌ No characters matched the criteria![/red]")
        sys.exit(1)
    
    gen = YukiV10Generator(
        subject_name=subject,
        input_dir=input_dir,
        characters=selected_chars,
        shot_type=args.shot_type
    )
    asyncio.run(gen.run(gens_per_char=args.variations))
