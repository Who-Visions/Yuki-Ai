"""
⚡ V12.5 PIPELINE: Streamlined (Flash Expansion -> Generation) ⚡

Drops Stage 3 (Gemini Pro Deep Analysis) to test speed and 
identity preservation using only Stage 2 (Flash 68-point) 
structural landmarks.

3-Stage Architecture:
1. Cloud Vision API → 34 landmarks
2. Gemini 3 Flash → 68-point expansion (Structured Structural Lock)
3. Gemini 3 Pro Image → Final Generation
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

# Model Assignments
FLASH_MODEL = "gemini-3-flash-preview"      # Stage 2: 68-point expansion
IMAGE_MODEL = "gemini-3-pro-image-preview"  # Stage 4: Generation

# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================

class LandmarkPoint(BaseModel):
    index: int
    region: str
    x: float
    y: float
    source: str

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

# =============================================================================
# STAGE 1: CLOUD VISION API
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
    
    def _get_file_hash(self, image_path: Path) -> str:
        import hashlib
        with open(image_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def detect_face(self, image_path: Path) -> Dict[str, Any]:
        file_hash = self._get_file_hash(image_path)
        cache_path = self.cache_dir / f"{file_hash}.json"
        
        if cache_path.exists():
            print(f"   💾 CACHE HIT: {image_path.name}")
            with open(cache_path, "r") as f:
                return json.load(f)
        
        print(f"   🔍 Cloud Vision API: Analyzing {image_path.name}...")
        with open(image_path, "rb") as f:
            content = f.read()
        
        image = vision.Image(content=content)
        response = self.client.face_detection(image=image)
        
        if not response.face_annotations:
            return {"error": "no_face"}
        
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
            "face_angles": {"roll": face.roll_angle, "pan": face.pan_angle, "tilt": face.tilt_angle},
            "detection_confidence": face.detection_confidence
        }
        
        with open(cache_path, "w") as f:
            json.dump(result, f, indent=2)
            
        return result

# =============================================================================
# STAGE 2: GEMINI 3 FLASH (Structured Expansion)
# =============================================================================

async def expand_to_68_points(
    client: genai.Client, 
    cv_data: Dict,
    image_parts: List[types.Part]
) -> Dict:
    print(f"\n{'='*60}")
    print(f"⚡ STAGE 2: Gemini 3 Flash - Structural Expansion (V12.5)")
    print(f"{'='*60}")
    
    prompt = f"""FACIAL LANDMARK EXPANSION TASK
    Cloud Vision 34-point data: {json.dumps(cv_data, indent=2)}
    TASK: Expand to 68-point schema. Focus on precision for V12.5 generation bypass.
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
        result = LandmarkExpansionResponse.model_validate_json(response.text)
        print(f"   ✅ Structural Lock ready (precision: {result.mapping_confidence.overall})")
        return result.model_dump()
    except Exception as e:
        print(f"   ❌ Stage 2 Failed: {e}")
        return {}

# =============================================================================
# STAGE 4: GENERATION (Direct from Structural Lock)
# =============================================================================

async def generate_image(
    client: genai.Client,
    subject_name: str,
    target_character: str,
    structural_lock: Dict,
    reference_path: Path,
    subject_parts: List[types.Part]
) -> Optional[bytes]:
    print(f"\n{'='*60}")
    print(f"🎨 STAGE 4: Gemini 3 Pro Image - Generation (V12.5 Streamlined)")
    print(f"Target: {target_character}")
    print(f"{'='*60}")
    
    # We use Face Geometry and Landmark stats for the prompt
    geom = structural_lock.get("face_geometry", {})
    props = geom.get("key_proportions", {})
    
    generation_prompt = f"""COSPLAY GENERATION (V12.5 STREAMLINED)
    
    🔒 SUBJECT: {subject_name}
    📐 STRUCTURAL SPECS:
    - Face Shape: {geom.get('face_shape')}
    - Eye Spacing Ratio: {props.get('eye_spacing_ratio')}
    - Nose to Chin Ratio: {props.get('nose_to_chin_ratio')}
    - Symmetry Score: {geom.get('symmetry_score')}

    🎬 TASK:
    Generate a full-body cinematic shot of {subject_name} as "{target_character}".
    Preserve the subject's exact facial structure and identity based on the attached 
    photos and the structural specs provided.
    
    SPECS:
    - Framing: Full Body, Vertical 9:16.
    - Style: Hyper-photorealistic, RED V-Raptor 8K.
    - Lighting: Dramatic, high-contrast cinematic.
    """
    
    with open(reference_path, "rb") as f:
        data = f.read()
        
    suffix = reference_path.suffix.lower()
    if suffix in ['.jpg', '.jpeg']: mime = "image/jpeg"
    elif suffix == '.png': mime = "image/png"
    elif suffix == '.webp': mime = "image/webp"
    else: mime = "image/jpeg" 

    ref_part = types.Part.from_bytes(data=data, mime_type=mime)
    
    contents = [*subject_parts, ref_part, generation_prompt]
    
    print(f"   🚀 Generating with {IMAGE_MODEL}...")
    try:
        response = await client.aio.models.generate_content(
            model=IMAGE_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
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
# PIPELINE CLASS
# =============================================================================

class V12_5Pipeline:
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
        lock_path = output_dir / f"v12_5_struct_{safe_name}.json"
        
        # Load Images (Simplified for V12.5)
        subject_images = sorted(list(subject_dir.glob("*.jpg")))[:4]
        if not subject_images:
            subject_images = sorted(list(subject_dir.glob("*.png")))[:4]
            if not subject_images:
                subject_images = sorted(list(subject_dir.glob("*.webp")))[:4]
                if not subject_images:
                    subject_images = sorted(list(subject_dir.glob("*.avif")))[:4]
        
        subject_parts = []
        for img in subject_images:
            suffix = img.suffix.lower()
            if suffix in ['.jpg', '.jpeg']: mime = "image/jpeg"
            elif suffix == '.png': mime = "image/png"
            elif suffix == '.webp': mime = "image/webp"
            else: mime = "image/jpeg" # Fallback
            
            with open(img, "rb") as f:
                subject_parts.append(types.Part.from_bytes(data=f.read(), mime_type=mime))

        # Structural Lock
        structural_lock = None
        if bypass_lock and lock_path.exists():
            print(f"   🔓 BYPASS: Loading structural lock: {lock_path}")
            with open(lock_path, "r") as f:
                structural_lock = json.load(f)
        
        if not structural_lock:
            cv_data = self.cv_analyzer.detect_face(subject_images[0])
            structural_lock = await expand_to_68_points(self.client, cv_data, subject_parts)
            with open(lock_path, "w") as f:
                json.dump(structural_lock, f, indent=2)

        # Generation
        image_data = await generate_image(self.client, subject_name, target_character, structural_lock, reference_path, subject_parts)
        
        if image_data:
            char_safe = re.sub(r'[^a-zA-Z0-9]', '_', target_character).lower()
            timestamp = datetime.now().strftime("%H%M%S")
            out_path = output_dir / f"v12_5_{safe_name}_as_{char_safe}_{timestamp}.png"
            with open(out_path, "wb") as f:
                f.write(image_data)
            print(f"\n🎉 V12.5 Success: {out_path}")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--subject_dir", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--character", default="character")
    parser.add_argument("--output", default="Renders_V12_5")
    args = parser.parse_args()
    
    pipeline = V12_5Pipeline()
    await pipeline.run(args.name, args.character, Path(args.subject_dir), Path(args.ref), Path(args.output))

if __name__ == "__main__":
    asyncio.run(main())
