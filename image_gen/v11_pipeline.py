"""
⚡ V11 PIPELINE: Cloud Vision + Gemini 3 Integration ⚡

4-Stage Architecture:
1. Cloud Vision API → 34 landmarks + face angles + emotions
2. Gemini 3 Flash → 68-point semantic expansion (AI-inferred)
3. Gemini 3 Pro → Deep analysis & identity lock
4. Gemini 3 Pro Image → Final generation

No MediaPipe dependency - Gemini handles landmark expansion.
"""

import asyncio
import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from google.cloud import vision

# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"

# Model Assignments (V11)
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
# STAGE 1: CLOUD VISION API - 34 Landmarks + Face Analysis (WITH CACHING)
# =============================================================================

class CloudVisionAnalyzer:
    """
    Google Cloud Vision API for face detection (34 landmarks)
    
    CACHING: Results are cached by file hash. Cache is ALWAYS checked
    first before any API call to avoid duplicate charges.
    """
    
    def __init__(self, cache_dir: Optional[Path] = None):
        # Use a local cache directory relative to the script if not provided
        base_dir = Path(__file__).resolve().parent.parent
        self.cache_dir = cache_dir or (base_dir / "cache/cloud_vision")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._client = None  # Lazy init
    
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
                    cached = json.load(f)
                print(f"   💾 CACHE HIT: {image_path.name}")
                return cached
            except (json.JSONDecodeError, IOError):
                pass
        return None
    
    def _save_to_cache(self, image_path: Path, result: Dict[str, Any]) -> None:
        cache_path = self._get_cache_path(image_path)
        try:
            result["_cache_metadata"] = {
                "source_file": str(image_path),
                "cached_at": datetime.now().isoformat(),
                "file_hash": self._get_file_hash(image_path)
            }
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
        except IOError as e:
            print(f"   ⚠️ Cache write error: {e}")
    
    def detect_face(self, image_path: Path, force_refresh: bool = False) -> Dict[str, Any]:
        if not force_refresh:
            cached = self._load_from_cache(image_path)
            if cached is not None:
                return cached
        
        print(f"   🔍 Cloud Vision API: Analyzing {image_path.name}...")
        
        with open(image_path, "rb") as f:
            content = f.read()
        
        image = vision.Image(content=content)
        response = self.client.face_detection(image=image)
        
        if not response.face_annotations:
            print("   ⚠️ No face detected")
            result = {"error": "no_face_detected", "confidence": 0.0}
            self._save_to_cache(image_path, result)
            return result
        
        face = response.face_annotations[0]
        
        # Bounding box
        vertices = face.bounding_poly.vertices
        bbox = {
            "x": vertices[0].x,
            "y": vertices[0].y,
            "width": vertices[2].x - vertices[0].x,
            "height": vertices[2].y - vertices[0].y
        }
        
        # 34 Landmarks
        landmarks = []
        for lm in face.landmarks:
            landmarks.append({
                "type": lm.type_.name,
                "x": lm.position.x,
                "y": lm.position.y,
                "z": lm.position.z
            })
        
        # Angles & Emotions
        angles = {
            "roll": round(face.roll_angle, 2),
            "pan": round(face.pan_angle, 2),
            "tilt": round(face.tilt_angle, 2)
        }
        
        emotions = {
            "joy": face.joy_likelihood.name,
            "sorrow": face.sorrow_likelihood.name,
            "anger": face.anger_likelihood.name,
            "surprise": face.surprise_likelihood.name
        }
        
        result = {
            "landmarks_34": landmarks,
            "landmark_count": len(landmarks),
            "bounding_box": bbox,
            "face_angles": angles,
            "emotions": emotions,
            "detection_confidence": round(face.detection_confidence, 3)
        }
        
        print(f"   ✅ Detected {len(landmarks)} landmarks (conf: {face.detection_confidence:.2f})")
        self._save_to_cache(image_path, result)
        return result


# =============================================================================
# STAGE 2: GEMINI 3 FLASH - 68-Point Semantic Expansion
# =============================================================================

EXPANSION_PROMPT = """FACIAL LANDMARK EXPANSION TASK

You have Cloud Vision API data with 34 landmarks:
{cv_data}

TASK: Expand this to the STANDARD 68-POINT FACIAL SCHEMA used in facial recognition.

The 68 points follow the dlib/iBUG standard:
- Points 0-16: Jawline (17 points)
- Points 17-21: Right eyebrow (5 points)
- Points 22-26: Left eyebrow (5 points)  
- Points 27-30: Nose bridge (4 points)
- Points 31-35: Nose bottom (5 points)
- Points 36-41: Right eye (6 points)
- Points 42-47: Left eye (6 points)
- Points 48-59: Outer lip (12 points)
- Points 60-67: Inner lip (8 points)

Using the Cloud Vision landmarks and the face image, INFER the missing points by:
1. Mapping existing landmarks to their 68-point equivalents
2. Interpolating missing points based on facial geometry
3. Using proportional estimation for unmapped regions

IMPORTANT: Round all coordinates to 2 decimal places to save space.

Output JSON ONLY:
{{
  "landmarks_68": [
    {{"index": 0, "region": "jawline", "x": 123.45, "y": 678.90, "source": "interpolated"}},
    ...all 68 points...
  ],
  "mapping_confidence": {{
    "eyes": <0.0-1.0>,
    "nose": <0.0-1.0>,
    "mouth": <0.0-1.0>,
    "jawline": <0.0-1.0>,
    "overall": <0.0-1.0>
  }},
  "face_geometry": {{
    "face_shape": "<detected shape>",
    "symmetry_score": <0.0-1.0>,
    "key_proportions": {{
      "eye_spacing_ratio": <value>,
      "nose_to_chin_ratio": <value>,
      "face_width_height_ratio": <value>
    }}
  }}
}}"""

async def expand_to_68_points(
    client: genai.Client, 
    cv_data: Dict,
    image_parts: List[types.Part]
) -> Dict:
    """Stage 2: Expand Cloud Vision 34 points to 68-point schema using Gemini Flash"""
    print(f"\n{'='*60}")
    print(f"⚡ STAGE 2: Gemini 3 Flash - 68-Point Expansion")
    print(f"{'='*60}")
    
    prompt = EXPANSION_PROMPT.format(cv_data=json.dumps(cv_data, indent=2))
    
    try:
        response = await client.aio.models.generate_content(
            model=FLASH_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LandmarkExpansionResponse,
                temperature=0.1,
                max_output_tokens=6000
            )
        )
        
        result = LandmarkExpansionResponse.model_validate_json(response.text)
        print(f"   ✅ Expanded to 68 points (confidence: {result.mapping_confidence.overall})")
        return result.model_dump()
            
    except Exception as e:
        print(f"   ❌ Stage 2 Failed: {e}")
        return {}


# =============================================================================
# STAGE 3: GEMINI 3 PRO - Deep Analysis & Identity Lock
# =============================================================================

ANALYSIS_PROMPT = """DEEP IDENTITY ANALYSIS FOR IMAGE GENERATION

You have precise facial data:

CLOUD VISION (34 landmarks + angles):
{cv_data}

68-POINT EXPANSION:
{expansion_data}

SUBJECT PHOTOS: Analyze the attached images.

TASK: Create a COMPREHENSIVE IDENTITY LOCK for image generation.

Output JSON:
{{
  "identity_lock": {{
    "subject_info": {{
      "name": "{subject_name}",
      "ethnicity": "<precise>",
      "skin_tone": "<fitzpatrick I-VI + hex color>",
      "age_range": "<years>"
    }},
    
    "geometric_signatures": {{
      "face_shape": "<shape with measurements>",
      "face_angles": {{"roll": <deg>, "pan": <deg>, "tilt": <deg>}},
      "key_ratios": {{
        "eye_width_to_face": <ratio>,
        "nose_length_to_face": <ratio>,
        "mouth_width_to_face": <ratio>,
        "interocular_distance": <normalized>
      }}
    }},
    
    "feature_signatures": {{
      "eyes": {{
        "shape": "<detailed>",
        "canthal_tilt": "<degrees>",
        "color": "<color>",
        "unique_traits": ["<list>"]
      }},
      "nose": {{
        "bridge": "<profile>",
        "tip": "<shape>",
        "width": "<measurement>",
        "unique_traits": ["<list>"]
      }},
      "lips": {{
        "shape": "<detailed>",
        "cupids_bow": "<description>",
        "fullness": "<upper/lower ratio>",
        "unique_traits": ["<list>"]
      }},
      "bone_structure": {{
        "cheekbones": "<description>",
        "jawline": "<description>",
        "chin": "<description>"
      }}
    }},
    
    "absolute_preserve": [
      "<TOP 10 features that DEFINE this person's identity - be SPECIFIC>"
    ],
    
    "generation_guidance": "<detailed paragraph on how to generate this exact face>"
  }},
  
  "confidence_score": <0.0-1.0>
}}

Be EXTREMELY precise. This identity lock controls image generation fidelity."""

async def deep_analysis_pro(
    client: genai.Client,
    subject_name: str,
    cv_data: Dict,
    expansion_data: Dict,
    image_parts: List[types.Part]
) -> Dict:
    """Stage 3: Deep analysis with Gemini 3 Pro"""
    print(f"\n{'='*60}")
    print(f"🧠 STAGE 3: Gemini 3 Pro - Deep Analysis")
    print(f"{'='*60}")
    
    prompt = ANALYSIS_PROMPT.format(
        subject_name=subject_name,
        cv_data=json.dumps(cv_data, indent=2),
        expansion_data=json.dumps(expansion_data, indent=2)
    )
    
    try:
        response = await client.aio.models.generate_content(
            model=PRO_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=IdentityLockResponse,
                temperature=0.2,
                max_output_tokens=8000
            )
        )
        
        result = IdentityLockResponse.model_validate_json(response.text)
        print(f"   ✅ Identity Lock created (confidence: {result.confidence_score})")
        return result.model_dump()
        
    except Exception as e:
        print(f"   ❌ Stage 3 Failed: {e}")
        return {}


# =============================================================================
# STAGE 4: GEMINI 3 PRO IMAGE - Generation
# =============================================================================

async def generate_image(
    client: genai.Client,
    subject_name: str,
    identity_lock: Dict,
    reference_path: Path,
    subject_parts: List[types.Part],
    aspect_ratio: str = "9:16",
    full_body: bool = False
) -> Optional[bytes]:
    """Stage 4: Image generation with Gemini 3 Pro Image"""
    print(f"\n{'='*60}")
    print(f"🎨 STAGE 4: Gemini 3 Pro Image - Generation")
    print(f"{'='*60}")
    
    # Extract from identity lock
    lock = identity_lock.get("identity_lock", identity_lock)
    absolute_preserve = lock.get("absolute_preserve", [])
    features = lock.get("feature_signatures", {})
    guidance = lock.get("generation_guidance", "")
    
    framing = "FULL BODY SHOT (Head to Toe MUST be visible)" if full_body else "Cinematic Portrait"
    
    generation_prompt = f"""COSPLAY GENERATION WITH V11 IDENTITY LOCK
    
    🔒 IDENTITY LOCK ACTIVE FOR: {subject_name}
    
    ABSOLUTE PRESERVE (NEVER CHANGE):
    {chr(10).join(f'• {p}' for p in absolute_preserve[:10])}
    
    FEATURE SIGNATURES:
    • Eyes: {json.dumps(features.get('eyes', {}), indent=2)}
    • Nose: {json.dumps(features.get('nose', {}), indent=2)}
    • Lips: {json.dumps(features.get('lips', {}), indent=2)}
    • Bone Structure: {json.dumps(features.get('bone_structure', {}), indent=2)}
    
    GENERATION GUIDANCE:
    {guidance}
    
    🎬 TECHNICAL SPECS:
    - FRAMING: {framing}
    - ASPECT RATIO: {aspect_ratio}
    - STYLE: Photorealistic, professional photography, movie lighting.
    
    🎬 TASK:
    Generate {subject_name} (from subject photos) wearing the COSTUME from the reference.
    - FACE = Subject identity ({subject_name}) - MUST match subject photos exactly
    - POSE/BODY = Can adapt to reference
    - COSTUME/CLOTHES = From reference image only
    - DO NOT blend or use reference person's facial features
    
    Output a single high-quality photorealistic image."""

    # Load reference
    with open(reference_path, "rb") as f:
        ext = reference_path.suffix.lower()
        mime = "image/jpeg" if ext in ['.jpg', '.jpeg'] else "image/png"
        ref_part = types.Part.from_bytes(data=f.read(), mime_type=mime)
    
    contents = [
        "=== SUBJECT PHOTOS (THIS IS THE FACE TO USE) ===",
        *subject_parts,
        "=== REFERENCE IMAGE (COSTUME/POSE ONLY) ===",
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
    
    print(f"   ❌ Generation failed")
    return None


# =============================================================================
# V11 PIPELINE ORCHESTRATOR
# =============================================================================

class V11Pipeline:
    """V11 Pipeline: Cloud Vision + Gemini 3 (No MediaPipe)"""
    
    def __init__(self, project_id: str = PROJECT_ID):
        self.project_id = project_id
        self.client = genai.Client(vertexai=True, project=project_id, location=LOCATION)
        self.cv_analyzer = CloudVisionAnalyzer()
    
    async def run(
        self,
        subject_name: str,
        subject_dir: Path,
        reference_path: Path,
        output_dir: Path,
        aspect_ratio: str = "9:16",
        full_body: bool = False,
        bypass_lock: bool = False
    ) -> Optional[Path]:
        
        output_dir.mkdir(parents=True, exist_ok=True)
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', subject_name).lower()
        lock_path = output_dir / f"v11_lock_{safe_name}.json"
        
        print("=" * 70)
        print("⚡ V11 PIPELINE: Cloud Vision + Gemini 3 ⚡")
        print("=" * 70)
        print(f"   Subject Name: {subject_name}")
        print(f"   Subject Dir:  {subject_dir}")
        print(f"   Reference:    {reference_path}")
        print(f"   Output Dir:   {output_dir}")
        print(f"   Aspect Ratio: {aspect_ratio}")
        
        # Load subject images
        # Try finding images with the subject name first, else all jpgs
        subject_images = sorted(list(subject_dir.glob(f"*{subject_name.split()[0].lower()}*.jpg")))[:4]
        if not subject_images:
            subject_images = sorted(list(subject_dir.glob("*.jpg")))[:4]
            if not subject_images:
                subject_images = sorted(list(subject_dir.glob("*.png")))[:4]
        
        if not subject_images:
            print(f"❌ No suitable images found in {subject_dir}")
            return None
        
        print(f"\n📸 Loading {len(subject_images)} subject photos...")
        subject_parts = []
        for img in subject_images:
            mime = "image/jpeg" if img.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
            with open(img, "rb") as f:
                subject_parts.append(types.Part.from_bytes(data=f.read(), mime_type=mime))
            print(f"   ✓ {img.name}")
            
        # Identity Lock Handling
        identity_lock = None
        if bypass_lock and lock_path.exists():
            print(f"\n🔓 BYPASS: Loading existing identity lock: {lock_path}")
            with open(lock_path, "r", encoding="utf-8") as f:
                identity_lock = json.load(f)
        
        if not identity_lock:
            # ===== STAGE 1: Cloud Vision (34 landmarks) =====
            print(f"\n{'='*60}")
            print(f"👁️ STAGE 1: Cloud Vision API")  
            print(f"{'='*60}")
            cv_data = self.cv_analyzer.detect_face(subject_images[0])
            
            # ===== STAGE 2: Gemini Flash (68-point expansion) =====
            expansion_data = await expand_to_68_points(self.client, cv_data, subject_parts)
            
            # ===== STAGE 3: Gemini Pro (deep analysis) =====
            identity_lock = await deep_analysis_pro(
                self.client, subject_name, cv_data, expansion_data, subject_parts
            )
            
            # Save identity lock
            identity_lock["_metadata"] = {
                "created": datetime.now().isoformat(),
                "version": "V11",
                "subject": subject_name
            }
            with open(lock_path, "w", encoding="utf-8") as f:
                json.dump(identity_lock, f, indent=2)
            print(f"\n💾 Saved identity lock: {lock_path}")
        
        # ===== STAGE 4: Gemini Pro Image (generation) =====
        image_data = await generate_image(
            self.client, subject_name, identity_lock, reference_path, subject_parts,
            aspect_ratio=aspect_ratio, full_body=full_body
        )
        
        if image_data:
            ref_name = reference_path.stem[:20].replace(" ", "_")
            timestamp = datetime.now().strftime("%H%M%S")
            out_path = output_dir / f"v11_{safe_name}_as_{ref_name}_{timestamp}.png"
            with open(out_path, "wb") as f:
                f.write(image_data)
            print(f"\n✅ V11 PIPELINE COMPLETE")
            print(f"📁 Output: {out_path}")
            return out_path
        
        print(f"\n❌ Pipeline failed at generation stage")
        return None

# =============================================================================
# CLI
# =============================================================================

async def main():
    parser = argparse.ArgumentParser(description="V11 Cosplay Generator (Generic)")
    
    parser.add_argument("--name", type=str, required=True, help="Name of the subject (e.g., 'Kai Taylor')")
    parser.add_argument("--subject_dir", type=str, required=True, help="Directory containing subject photos")
    parser.add_argument("--ref", type=str, required=True, help="Path to reference/costume image")
    parser.add_argument("--output", type=str, default="Renders_V11", help="Output directory")
    parser.add_argument("--aspect_ratio", type=str, default="9:16", help="Target aspect ratio (e.g., '9:16', '1:1')")
    parser.add_argument("--full_body", action="store_true", help="Request a full body shot")
    parser.add_argument("--bypass_lock", action="store_true", help="Bypass analysis and use existing identity lock if available")
    parser.add_argument("--project_id", type=str, default=PROJECT_ID, help="Google Cloud Project ID")
    
    args = parser.parse_args()
    
    subject_path = Path(args.subject_dir)
    ref_path = Path(args.ref)
    out_path = Path(args.output)
    
    if not subject_path.exists():
        print(f"❌ Subject directory not found: {subject_path}")
        return
    if not ref_path.exists():
        print(f"❌ Reference image not found: {ref_path}")
        return

    pipeline = V11Pipeline(project_id=args.project_id)
    
    await pipeline.run(
        subject_name=args.name,
        subject_dir=subject_path,
        reference_path=ref_path,
        output_dir=out_path,
        aspect_ratio=args.aspect_ratio,
        full_body=args.full_body,
        bypass_lock=args.bypass_lock
    )

if __name__ == "__main__":
    asyncio.run(main())
