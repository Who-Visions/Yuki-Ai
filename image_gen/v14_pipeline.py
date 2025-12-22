"""
⚡ V12 PIPELINE: Structured Outputs + Pydantic + Gemini 3 ⚡

Upgrades from V11:
1.  **Structured Outputs:** Uses `response_json_schema` with Pydantic models.
2.  **Type Safety:** Eliminates manual JSON parsing and regex hacks.
3.  **Reliability:** Guarantees valid JSON response from Gemini.
4.  **CLI:** Fully generic CLI support.

4-Stage Architecture:
1. Cloud Vision API → 34 landmarks (Base Truth)
2. Gemini 3 Flash → 68-point expansion (Structured)
3. Gemini 3 Pro → Deep Identity Lock (Structured)
4. Gemini 3 Pro Image → Final Generation
"""

import asyncio
import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal

from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from google.cloud import vision

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"

# Model Assignments
FLASH_MODEL = "gemini-3-flash-preview"      # Stage 2: 68-point expansion
PRO_MODEL = "gemini-3-pro-preview"          # Stage 3: Deep analysis
IMAGE_MODEL = "gemini-3-pro-image-preview"  # Stage 4: Generation

# =============================================================================
# PYDANTIC SCHEMAS (STRUCTURED OUTPUTS)
# =============================================================================

class LandmarkPoint(BaseModel):
    index: int = Field(..., description="The 0-67 index of the landmark point.")
    region: str = Field(..., description="The facial region (e.g., 'jawline', 'eye_left').")
    x: float = Field(..., description="X coordinate (rounded to 2 decimal places).")
    y: float = Field(..., description="Y coordinate (rounded to 2 decimal places).")
    source: str = Field(..., description="How this point was derived (e.g., 'interpolated', 'mapped').")

class MappingConfidence(BaseModel):
    eyes: float
    nose: float
    mouth: float
    jawline: float
    overall: float

class KeyProportions(BaseModel):
    eye_spacing_ratio: float
    nose_to_chin_ratio: float
    face_width_height_ratio: float

class FaceGeometry(BaseModel):
    face_shape: str
    symmetry_score: float
    key_proportions: KeyProportions

class LandmarkExpansionResponse(BaseModel):
    landmarks_68: List[LandmarkPoint]
    mapping_confidence: MappingConfidence
    face_geometry: FaceGeometry

# --- Stage 3 Schemas ---

class SubjectInfo(BaseModel):
    name: str
    ethnicity: str
    skin_tone: str
    age_range: str

class FaceAngles(BaseModel):
    roll: float
    pan: float
    tilt: float

class KeyRatios(BaseModel):
    eye_width_to_face: float
    nose_length_to_face: float
    mouth_width_to_face: float
    interocular_distance: float

class GeometricSignatures(BaseModel):
    face_shape: str
    face_angles: FaceAngles
    key_ratios: KeyRatios

class FeatureDetails(BaseModel):
    shape: str
    description: Optional[str] = None
    color: Optional[str] = None
    unique_traits: List[str]

class FeatureSignatures(BaseModel):
    eyes: FeatureDetails
    nose: FeatureDetails
    lips: FeatureDetails
    bone_structure: Dict[str, str]

class IdentityLockData(BaseModel):
    subject_info: SubjectInfo
    geometric_signatures: GeometricSignatures
    feature_signatures: FeatureSignatures
    absolute_preserve: List[str] = Field(..., description="List of top 10 features to absolutely preserve.")
    generation_guidance: str = Field(..., description="Detailed paragraph on how to generate this exact face.")

class IdentityLockResponse(BaseModel):
    identity_lock: IdentityLockData
    confidence_score: float

# =============================================================================
# STAGE 1: CLOUD VISION API (Same as V11)
# =============================================================================

class CloudVisionAnalyzer:
    def __init__(self, cache_dir: Optional[Path] = None):
        base_dir = Path(__file__).resolve().parent.parent
        self.cache_dir = cache_dir or (base_dir / "cache/cloud_vision")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = vision.ImageAnnotatorClient()
        return self._client
    
    def _get_file_hash(self, file_path: Path) -> str:
        import hashlib
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _get_cache_path(self, image_path: Path) -> Path:
        file_hash = self._get_file_hash(image_path)
        return self.cache_dir / f"{file_hash}.json"
    
    def _load_from_cache(self, image_path: Path) -> Optional[Dict[str, Any]]:
        cache_path = self._get_cache_path(image_path)
        if cache_path.exists():
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: pass
        return None
    
    def _save_to_cache(self, image_path: Path, result: Dict[str, Any]) -> None:
        cache_path = self._get_cache_path(image_path)
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
        except: pass
    
    def detect_face(self, image_path: Path) -> Dict[str, Any]:
        cached = self._load_from_cache(image_path)
        if cached:
            print(f"   💾 CACHE HIT: {image_path.name}")
            return cached
        
        print(f"   🔍 Cloud Vision API: Analyzing {image_path.name}...")
        with open(image_path, "rb") as f:
            content = f.read()
        
        image = vision.Image(content=content)
        response = self.client.face_detection(image=image)
        
        if not response.face_annotations:
            print("   ⚠️ No face detected")
            return {"error": "no_face", "confidence": 0.0}
        
        face = response.face_annotations[0]
        
        landmarks = []
        for lm in face.landmarks:
            landmarks.append({
                "type": lm.type_.name,
                "x": lm.position.x,
                "y": lm.position.y,
                "z": lm.position.z
            })
        
        result = {
            "landmarks_34": landmarks,
            "face_angles": {
                "roll": face.roll_angle,
                "pan": face.pan_angle,
                "tilt": face.tilt_angle
            },
            "detection_confidence": face.detection_confidence
        }
        
        print(f"   ✅ Detected {len(landmarks)} landmarks")
        self._save_to_cache(image_path, result)
        return result

# =============================================================================
# STAGE 2: GEMINI 3 FLASH (Structured Output)
# =============================================================================

async def expand_to_68_points(
    client: genai.Client, 
    cv_data: Dict,
    image_parts: List[types.Part]
) -> Dict:
    print(f"\n{'='*60}")
    print(f"⚡ STAGE 2: Gemini 3 Flash - Structured Expansion")
    print(f"{ '='*60}")
    
    prompt = f"""FACIAL LANDMARK EXPANSION TASK

    You have Cloud Vision API data with 34 landmarks:
    {json.dumps(cv_data, indent=2)}

    TASK: Expand this to the STANDARD 68-POINT FACIAL SCHEMA (dlib/iBUG standard).
    
    INSTRUCTIONS:
    1. Map existing landmarks to their 68-point equivalents.
    2. Interpolate missing points based on facial geometry.
    3. Round ALL coordinates to 2 decimal places to be concise.
    """
    
    try:
        response = await client.aio.models.generate_content(
            model=FLASH_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LandmarkExpansionResponse,
                temperature=0.1
            )
        )
        
        # Pydantic validation handles parsing
        result = LandmarkExpansionResponse.model_validate_json(response.text)
        print(f"   ✅ Expanded to 68 points (confidence: {result.mapping_confidence.overall})")
        return result.model_dump()
        
    except Exception as e:
        print(f"   ❌ Stage 2 Failed: {e}")
        return {}

# =============================================================================
# STAGE 3: GEMINI 3 PRO (Structured Output)
# =============================================================================

async def deep_analysis_pro(
    client: genai.Client,
    subject_name: str,
    cv_data: Dict,
    expansion_data: Dict,
    image_parts: List[types.Part]
) -> Dict:
    print(f"\n{'='*60}")
    print(f"🧠 STAGE 3: Gemini 3 Pro - Structured Analysis")
    print(f"{ '='*60}")
    
    prompt = f"""DEEP IDENTITY ANALYSIS FOR: {subject_name}

    CLOUD VISION DATA:
    {json.dumps(cv_data, indent=2)}

    68-POINT EXPANSION:
    {json.dumps(expansion_data, indent=2)}

    TASK: Create a COMPREHENSIVE IDENTITY LOCK.
    Analyze the subject photos to extract precise geometric and feature signatures.
    """
    
    try:
        response = await client.aio.models.generate_content(
            model=PRO_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=IdentityLockResponse,
                temperature=0.2
            )
        )
        
        result = IdentityLockResponse.model_validate_json(response.text)
        print(f"   ✅ Identity Lock created (confidence: {result.confidence_score})")
        return result.model_dump()
        
    except Exception as e:
        print(f"   ❌ Stage 3 Failed: {e}")
        return {}

# =============================================================================
# STAGE 4: GENERATION (Same as V11)
# =============================================================================

async def generate_image(

    client: genai.Client,

    subject_name: str,

    target_character: str,

    identity_lock: Dict,

    reference_path: Path,

    subject_parts: List[types.Part]

) -> Optional[bytes]:

    print(f"\n{'='*60}")

    print(f"🎨 STAGE 4: Gemini 3 Pro Image - Generation (Target: {target_character})")

    print(f"{'='*60}")
    
    lock = identity_lock.get("identity_lock", {})
    absolute_preserve = lock.get("absolute_preserve", [])
    features = lock.get("feature_signatures", {})
    guidance = lock.get("generation_guidance", "")
    
    generation_prompt = f"""COSPLAY GENERATION WITH V12 STRUCTURAL LOCK

    🔒 IDENTITY LOCK ACTIVE FOR: {subject_name}

    ABSOLUTE PRESERVE (NEVER CHANGE):
    {chr(10).join(f'• {p}' for p in absolute_preserve[:10])}

    FEATURE SIGNATURES:
    {json.dumps(features, indent=2)}

    GENERATION GUIDANCE:
    {guidance}

    🎬 CINEMATIC & TECHNICAL SPECS (STRICT):
    - CAMERA: RED V-Raptor XL 8K VV.
    - COLOR: 10-bit color depth, raw output, cinematic color grading.
    - LENS: 35mm Anamorphic Prime (sharp subject, creamy bokeh).
    - RESOLUTION: 8K Ultra-HD, visible skin texture, microscopic details.
    - FRAMING: FULL BODY SHOT (Head to Toe MUST be visible).
    - ASPECT RATIO: Vertical 9:16.
    - STYLE: Hyper-photorealistic, Magazine Cover quality.

    🎬 TASK:
    Generate a FULL BODY shot of {subject_name} as the character "{target_character}".
    - FACE: Must match {subject_name} exactly (Use Identity Lock).
    - COSTUME: Must match the iconic outfit of "{target_character}" perfectly.
    - THEME: Unsettling, weird, and hyper-detailed anime aesthetic.
    - POSE: Standing, powerful full-body pose.
    
    Output a single high-quality 8K photorealistic vertical image.
    """
    
    with open(reference_path, "rb") as f:
        ref_part = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    contents = [
        "=== SUBJECT PHOTOS ===",
        *subject_parts,
        f"=== REFERENCE CHARACTER: {target_character} ===",
        ref_part,
        generation_prompt
    ]
    
    print(f"   🚀 Generating with {IMAGE_MODEL}...")
    try:
        response = await client.aio.models.generate_content(
            model=IMAGE_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE', 'TEXT'],
                temperature=1.0
            )
        )
        
        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    print(f"   ✅ Image generated successfully")
                    return part.inline_data.data
    except Exception as e:
        print(f"   ❌ Generation Error: {e}")
    
    return None

# =============================================================================
# MAIN PIPELINE
# =============================================================================

class V12Pipeline:
    def __init__(self, project_id: str = PROJECT_ID):
        self.client = genai.Client(vertexai=True, project=project_id, location=LOCATION)
        self.cv_analyzer = CloudVisionAnalyzer()
    
    async def run(
        self,
        subject_name: str,
        target_character: str,
        subject_dir: Path,
        reference_path: Path,
        output_dir: Path,
        bypass_lock: bool = False
    ):
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', subject_name).lower()
        lock_path = output_dir / f"v12_lock_{safe_name}.json"
        
        print(f"⚡ V12 PIPELINE START for {subject_name} as {target_character}")
        
        # Load Images
        subject_images = sorted(list(subject_dir.glob(f"*{subject_name.split()[0].lower()}*.jpg")))[:4]
        if not subject_images:
            subject_images = sorted(list(subject_dir.glob("*.jpg")))[:4]
            if not subject_images:
                 subject_images = sorted(list(subject_dir.glob("*.png")))[:4]
        
        if not subject_images:
            print(f"❌ No suitable images found in {subject_dir}")
            return
            
        subject_parts = []
        for img in subject_images:
            mime = "image/jpeg" if img.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
            with open(img, "rb") as f:
                subject_parts.append(types.Part.from_bytes(data=f.read(), mime_type=mime))
        
        # Identity Lock Handling
        identity_lock = None
        if bypass_lock and lock_path.exists():
            print(f"\n🔓 BYPASS: Loading existing identity lock: {lock_path}")
            with open(lock_path, "r", encoding="utf-8") as f:
                identity_lock = json.load(f)
        
        if not identity_lock:
            # Stage 1
            cv_data = self.cv_analyzer.detect_face(subject_images[0])
            
            # Stage 2
            expansion_data = await expand_to_68_points(self.client, cv_data, subject_parts)
            if not expansion_data: return
            
            # Stage 3
            identity_lock = await deep_analysis_pro(self.client, subject_name, cv_data, expansion_data, subject_parts)
            if not identity_lock: return
            
            # Save Lock
            with open(lock_path, "w", encoding="utf-8") as f:
                json.dump(identity_lock, f, indent=2)
            print(f"\n💾 Saved identity lock: {lock_path}")
            
        # Stage 4
        image_data = await generate_image(self.client, subject_name, target_character, identity_lock, reference_path, subject_parts)
        
        if image_data:
            # --- DB & SECURE FILENAME LOGGING ---
            try:
                import sqlite3
                import os
                
                email = os.environ.get("YUKI_USER_EMAIL")
                subject_id = None
                
                if email:
                    db_path = Path("C:/Yuki_Local/Cosplay_Lab/Brain/yuki_memory.db")
                    if db_path.exists():
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        
                        # Find Subject ID
                        cursor.execute("SELECT id FROM subjects WHERE email = ?", (email,))
                        row = cursor.fetchone()
                        if row:
                            subject_id = row[0]
                        else:
                            # Fallback to name
                            cursor.execute("SELECT id FROM subjects WHERE name LIKE ?", (f"%{subject_name}%",))
                            row = cursor.fetchone()
                            if row:
                                subject_id = row[0]
                        conn.close()

                # Secure Filename Logic
                char_slug = target_character.replace(" ", "_").lower()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                if subject_id:
                    filename = f"gen_u{subject_id}_{char_slug}_{timestamp}.png"
                else:
                    # Fallback if no user linked (shouldn't happen for auth'd users)
                    safe_subject = re.sub(r'[^a-zA-Z0-9]', '_', subject_name).lower()
                    filename = f"gen_{safe_subject}_{char_slug}_{timestamp}.png"

                out_path = output_dir / filename
                with open(out_path, "wb") as f:
                    f.write(image_data)
                print(f"\n🎉 V12 Success: {out_path}")

                # Log to DB
                if subject_id:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO generation_log (subject_id, filename, prompt, status, confidence_score, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        subject_id, 
                        filename, 
                        f"{subject_name} as {target_character}", 
                        "SUCCESS_V12_SECURE", 
                        identity_lock.get("confidence_score", 1.0) if identity_lock else 0.0,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ))
                    conn.commit()
                    print(f"   💾 Logged to DB for subject_id {subject_id}")
                    conn.close()
                    
            except Exception as e:
                print(f"   ❌ DB Logging/Saving Error: {e}")
                # Fallback save if DB failed but image exists
                if image_data and 'filename' not in locals():
                     with open(output_dir / f"fallback_{timestamp}.png", "wb") as f:
                        f.write(image_data)

async def main():
    parser = argparse.ArgumentParser(description="V12 Cosplay Generator (Structured)")
    parser.add_argument("--name", type=str, required=True)
    parser.add_argument("--character", type=str, default="the character in reference image")
    parser.add_argument("--subject_dir", type=str, required=True)
    parser.add_argument("--ref", type=str, required=True)
    parser.add_argument("--output", type=str, default="Renders_V12")
    args = parser.parse_args()
    
    pipeline = V12Pipeline()
    await pipeline.run(args.name, args.character, Path(args.subject_dir), Path(args.ref), Path(args.output))

if __name__ == "__main__":
    asyncio.run(main())
