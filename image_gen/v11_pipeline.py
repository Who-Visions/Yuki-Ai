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
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

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

# Paths
BASE_DIR = Path("c:/Yuki_Local")
SUBJECT_DIR = BASE_DIR / "Cosplay_Lab/Subjects/Kai Taylor"
REF_DIR = BASE_DIR / "Cosplay_Lab/References"
RENDER_DIR = BASE_DIR / "Cosplay_Lab/Renders/kai_bella_v11"


# =============================================================================
# STAGE 1: CLOUD VISION API - 34 Landmarks + Face Analysis (WITH CACHING)
# =============================================================================

# Cache directory for Cloud Vision results
CV_CACHE_DIR = BASE_DIR / "cache/cloud_vision"
CV_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _get_file_hash(file_path: Path) -> str:
    """Generate hash of file content for cache key"""
    import hashlib
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


class CloudVisionAnalyzer:
    """
    Google Cloud Vision API for face detection (34 landmarks)
    
    CACHING: Results are cached by file hash. Cache is ALWAYS checked
    first before any API call to avoid duplicate charges.
    """
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or CV_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._client = None  # Lazy init to avoid API call on import
    
    @property
    def client(self):
        """Lazy-load Vision client only when needed"""
        if self._client is None:
            self._client = vision.ImageAnnotatorClient()
        return self._client
    
    def _get_cache_path(self, image_path: Path) -> Path:
        """Get cache file path for an image"""
        file_hash = _get_file_hash(image_path)
        return self.cache_dir / f"{file_hash}.json"
    
    def _load_from_cache(self, image_path: Path) -> Optional[Dict[str, Any]]:
        """Load cached result if exists - ALWAYS called first"""
        cache_path = self._get_cache_path(image_path)
        if cache_path.exists():
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                print(f"   💾 CACHE HIT: {image_path.name} (saved ${self._estimate_cost()} API cost)")
                return cached
            except (json.JSONDecodeError, IOError) as e:
                print(f"   ⚠️ Cache read error: {e}")
        return None
    
    def _save_to_cache(self, image_path: Path, result: Dict[str, Any]) -> None:
        """Save result to cache"""
        cache_path = self._get_cache_path(image_path)
        try:
            result["_cache_metadata"] = {
                "source_file": str(image_path),
                "cached_at": datetime.now().isoformat(),
                "file_hash": _get_file_hash(image_path)
            }
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            print(f"   💾 Cached result: {cache_path.name}")
        except IOError as e:
            print(f"   ⚠️ Cache write error: {e}")
    
    def _estimate_cost(self) -> str:
        """Estimate cost saved by cache hit"""
        # Cloud Vision Face Detection: ~$1.50 per 1000 images
        return "~$0.0015"
    
    def detect_face(self, image_path: Path, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Detect face using Cloud Vision API (WITH CACHING)
        
        FAILSAFE: Cache is ALWAYS checked first. API only called if:
        1. No cache exists for this image
        2. force_refresh=True is explicitly set
        
        Args:
            image_path: Path to image file
            force_refresh: If True, bypass cache and call API
            
        Returns:
            - landmarks_34: Cloud Vision's 34 facial landmarks
            - bounding_box: face region
            - face_angles: roll, pan, tilt
            - emotions: joy, sorrow, anger, surprise
            - confidence: detection confidence
        """
        # ===== FAILSAFE: ALWAYS CHECK CACHE FIRST =====
        if not force_refresh:
            cached = self._load_from_cache(image_path)
            if cached is not None:
                return cached
        
        # ===== CACHE MISS: Call Cloud Vision API =====
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
        
        # 34 Landmarks with types
        landmarks = []
        for lm in face.landmarks:
            landmarks.append({
                "type": lm.type_.name,
                "x": lm.position.x,
                "y": lm.position.y,
                "z": lm.position.z
            })
        
        # Face angles
        angles = {
            "roll": round(face.roll_angle, 2),
            "pan": round(face.pan_angle, 2),
            "tilt": round(face.tilt_angle, 2)
        }
        
        # Emotions
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
        
        # ===== SAVE TO CACHE =====
        self._save_to_cache(image_path, result)
        
        return result
    
    def clear_cache(self) -> int:
        """Clear all cached results. Returns number of files deleted."""
        import shutil
        count = len(list(self.cache_dir.glob("*.json")))
        if count > 0:
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        print(f"   🗑️ Cleared {count} cached entries")
        return count


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

Output JSON ONLY:
{{
  "landmarks_68": [
    {{"index": 0, "region": "jawline", "x": <estimated>, "y": <estimated>, "source": "interpolated/mapped"}},
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
    
    response = await client.aio.models.generate_content(
        model=FLASH_MODEL,
        contents=[prompt] + image_parts,
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=6000
        )
    )
    
    text = response.text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        expansion = json.loads(text)
        conf = expansion.get("mapping_confidence", {}).get("overall", "N/A")
        print(f"   ✅ Expanded to 68 points (confidence: {conf})")
        return expansion
    except json.JSONDecodeError:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            expansion = json.loads(text[start:end])
            print(f"   ✅ Expanded (with cleanup)")
            return expansion
        print(f"   ⚠️ Failed to parse")
        return {"raw": text}


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
      "name": "Kai Taylor",
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
    cv_data: Dict,
    expansion_data: Dict,
    image_parts: List[types.Part]
) -> Dict:
    """Stage 3: Deep analysis with Gemini 3 Pro"""
    print(f"\n{'='*60}")
    print(f"🧠 STAGE 3: Gemini 3 Pro - Deep Analysis")
    print(f"{'='*60}")
    
    prompt = ANALYSIS_PROMPT.format(
        cv_data=json.dumps(cv_data, indent=2),
        expansion_data=json.dumps(expansion_data, indent=2)
    )
    
    response = await client.aio.models.generate_content(
        model=PRO_MODEL,
        contents=[prompt] + image_parts,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=8000
        )
    )
    
    text = response.text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        analysis = json.loads(text)
        conf = analysis.get("confidence_score", "N/A")
        print(f"   ✅ Deep analysis complete (confidence: {conf})")
        return analysis
    except json.JSONDecodeError:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            analysis = json.loads(text[start:end])
            print(f"   ✅ Analysis complete (with cleanup)")
            return analysis
        print(f"   ⚠️ Failed to parse")
        return {"raw": text}


# =============================================================================
# STAGE 4: GEMINI 3 PRO IMAGE - Generation
# =============================================================================

async def generate_image(
    client: genai.Client,
    identity_lock: Dict,
    reference_path: Path,
    subject_parts: List[types.Part]
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
    
    generation_prompt = f"""COSPLAY GENERATION WITH V11 IDENTITY LOCK

🔒 IDENTITY LOCK ACTIVE

ABSOLUTE PRESERVE (NEVER CHANGE):
{chr(10).join(f'• {p}' for p in absolute_preserve[:10])}

FEATURE SIGNATURES:
• Eyes: {json.dumps(features.get('eyes', {}), indent=2)}
• Nose: {json.dumps(features.get('nose', {}), indent=2)}
• Lips: {json.dumps(features.get('lips', {}), indent=2)}
• Bone Structure: {json.dumps(features.get('bone_structure', {}), indent=2)}

GENERATION GUIDANCE:
{guidance}

🎬 TASK:
Generate the SUBJECT (from subject photos) wearing the COSTUME from the reference.
- FACE = Subject identity (Kai Taylor) - MUST match subject photos exactly
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
        subject_dir: Path,
        reference_path: Path,
        output_dir: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Run full V11 pipeline
        
        Args:
            subject_dir: Directory with subject photos
            reference_path: Path to reference/costume image
            output_dir: Where to save output
            
        Returns:
            Path to generated image or None
        """
        output_dir = output_dir or RENDER_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("=" * 70)
        print("⚡ V11 PIPELINE: Cloud Vision + Gemini 3 ⚡")
        print("=" * 70)
        print(f"   Subject: {subject_dir}")
        print(f"   Reference: {reference_path}")
        print(f"   Output: {output_dir}")
        
        # Load subject images
        subject_images = sorted(list(subject_dir.glob("kai_new_*.jpg")))[:4]
        if not subject_images:
            subject_images = sorted(list(subject_dir.glob("*.jpg")))[:4]
        
        print(f"\n📸 Loading {len(subject_images)} subject photos...")
        
        subject_parts = []
        for img in subject_images:
            with open(img, "rb") as f:
                subject_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
            print(f"   ✓ {img.name}")
        
        # ===== STAGE 1: Cloud Vision (34 landmarks) =====
        print(f"\n{'='*60}")
        print(f"👁️ STAGE 1: Cloud Vision API")  
        print(f"{'='*60}")
        cv_data = self.cv_analyzer.detect_face(subject_images[0])
        
        # ===== STAGE 2: Gemini Flash (68-point expansion) =====
        expansion_data = await expand_to_68_points(self.client, cv_data, subject_parts)
        
        # ===== STAGE 3: Gemini Pro (deep analysis) =====
        identity_lock = await deep_analysis_pro(
            self.client, cv_data, expansion_data, subject_parts
        )
        
        # Save identity lock
        lock_path = output_dir / "v11_identity_lock.json"
        identity_lock["_metadata"] = {
            "created": datetime.now().isoformat(),
            "version": "V11",
            "stages": {
                "stage1": "Cloud Vision API (34 landmarks)",
                "stage2": f"{FLASH_MODEL} (68-point expansion)",
                "stage3": f"{PRO_MODEL} (deep analysis)",
                "stage4": f"{IMAGE_MODEL} (generation)"
            }
        }
        with open(lock_path, "w", encoding="utf-8") as f:
            json.dump(identity_lock, f, indent=2)
        print(f"\n💾 Saved identity lock: {lock_path}")
        
        # ===== STAGE 4: Gemini Pro Image (generation) =====
        image_data = await generate_image(
            self.client, identity_lock, reference_path, subject_parts
        )
        
        if image_data:
            ref_name = reference_path.stem[:20].replace(" ", "_")
            timestamp = datetime.now().strftime("%H%M%S")
            out_path = output_dir / f"v11_{ref_name}_{timestamp}.png"
            with open(out_path, "wb") as f:
                f.write(image_data)
            print(f"\n✅ V11 PIPELINE COMPLETE")
            print(f"📁 Output: {out_path}")
            return out_path
        
        print(f"\n❌ Pipeline failed at generation stage")
        return None
    
    async def batch_run(
        self,
        subject_dir: Path,
        reference_paths: List[Path],
        output_dir: Optional[Path] = None,
        delay_seconds: int = 10
    ) -> List[Path]:
        """Run pipeline on multiple references"""
        output_dir = output_dir or RENDER_DIR
        results = []
        
        for i, ref in enumerate(reference_paths, 1):
            print(f"\n{'#'*70}")
            print(f"# BATCH {i}/{len(reference_paths)}: {ref.name}")
            print(f"{'#'*70}")
            
            try:
                result = await self.run(subject_dir, ref, output_dir)
                if result:
                    results.append(result)
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            if i < len(reference_paths):
                print(f"\n⏳ Waiting {delay_seconds}s...")
                await asyncio.sleep(delay_seconds)
        
        return results


# =============================================================================
# CLI
# =============================================================================

async def main():
    """Run V11 pipeline on Kai Taylor"""
    pipeline = V11Pipeline()
    
    # Get references
    refs = sorted(list(REF_DIR.glob("*.jpg")))[:3]
    
    if not refs:
        print("❌ No reference images found")
        return
    
    print(f"Found {len(refs)} references")
    
    # Run on first reference
    result = await pipeline.run(SUBJECT_DIR, refs[0])
    
    if result:
        print(f"\n🎉 Success! Check: {result}")


if __name__ == "__main__":
    asyncio.run(main())
