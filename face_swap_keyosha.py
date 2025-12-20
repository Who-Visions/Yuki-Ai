"""
V11 Face Swap Post-Processor
Swap Keyosha's face onto generated cosplay images using InsightFace

This approach:
1. Take the generated cosplay image (wrong face, right costume)
2. Detect the face in the cosplay image
3. Swap it with Keyosha's actual face from reference photos
4. Result: Keyosha's face + character costume

Requires: pip install insightface onnxruntime-gpu opencv-python
"""
import os
import sys
from pathlib import Path
from typing import Optional, List
import json

# Check for required packages
try:
    import cv2
    import numpy as np
    from insightface.app import FaceAnalysis
    from insightface.model_zoo import get_model
except ImportError:
    print("=" * 60)
    print("MISSING DEPENDENCIES - Run:")
    print("  pip install insightface onnxruntime-gpu opencv-python numpy")
    print("=" * 60)
    sys.exit(1)

# Config
SUBJECT_NAME = "Keyosha Pullman"
SUBJECT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Keyosha Pullman")
RENDERS_DIR = SUBJECT_DIR / "Renders"
OUTPUT_DIR = SUBJECT_DIR / "FaceSwapped"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# InsightFace models dir
MODELS_DIR = Path("C:/Yuki_Local/models/insightface")
MODELS_DIR.mkdir(parents=True, exist_ok=True)


class FaceSwapper:
    def __init__(self):
        print("🔧 Initializing InsightFace...")
        
        # Face analysis for detection
        self.app = FaceAnalysis(
            name='buffalo_l',
            root=str(MODELS_DIR),
            providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
        )
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        
        # Face swapper model (inswapper_128)
        model_path = MODELS_DIR / "models" / "inswapper_128.onnx"
        if not model_path.exists():
            print(f"❌ Missing: {model_path}")
            print("Download inswapper_128.onnx from:")
            print("  https://huggingface.co/deepinsight/inswapper/resolve/main/inswapper_128.onnx")
            print(f"Place in: {model_path.parent}")
            self.swapper = None
        else:
            self.swapper = get_model(str(model_path), providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
            print("✅ Face swapper loaded")
    
    def get_best_source_face(self) -> Optional[np.ndarray]:
        """Get the best face from subject reference photos"""
        photos = sorted(SUBJECT_DIR.glob("*.jpg"), key=lambda p: p.stat().st_size, reverse=True)[:4]
        
        best_face = None
        best_score = 0
        
        for photo in photos:
            img = cv2.imread(str(photo))
            if img is None:
                continue
            
            faces = self.app.get(img)
            if faces:
                for face in faces:
                    # Use detection score
                    score = face.det_score if hasattr(face, 'det_score') else 0.9
                    if score > best_score:
                        best_score = score
                        best_face = face
                        print(f"   ✓ Best face from {photo.name} (score: {score:.2f})")
        
        return best_face
    
    def swap_face(self, target_image_path: Path, source_face) -> Optional[Path]:
        """Swap source face onto target image"""
        if self.swapper is None:
            print("❌ Swapper not initialized")
            return None
        
        # Load target image
        target_img = cv2.imread(str(target_image_path))
        if target_img is None:
            print(f"❌ Cannot load: {target_image_path}")
            return None
        
        # Detect faces in target
        target_faces = self.app.get(target_img)
        if not target_faces:
            print(f"   ⚠️ No face detected in {target_image_path.name}")
            return None
        
        # Swap each face
        result = target_img.copy()
        for i, target_face in enumerate(target_faces):
            result = self.swapper.get(result, target_face, source_face, paste_back=True)
            print(f"   ✓ Swapped face {i+1}")
        
        # Save result
        output_name = f"swapped_{target_image_path.name}"
        output_path = OUTPUT_DIR / output_name
        cv2.imwrite(str(output_path), result)
        
        return output_path
    
    def process_all_renders(self):
        """Process all renders in the Renders folder"""
        print("=" * 60)
        print(f"🔄 FACE SWAP: {SUBJECT_NAME}")
        print("=" * 60)
        
        # Get source face
        print("\n📸 Finding best source face...")
        source_face = self.get_best_source_face()
        if source_face is None:
            print("❌ No source face found")
            return
        
        # Find all renders (exclude already swapped)
        renders = [f for f in RENDERS_DIR.glob("*.png") if not f.name.startswith("swapped_")]
        print(f"\n🎨 Processing {len(renders)} renders...")
        
        success = 0
        failed = 0
        
        for render in renders:
            print(f"\n→ {render.name}")
            result = self.swap_face(render, source_face)
            if result:
                print(f"   ✅ Saved: {result.name}")
                success += 1
            else:
                failed += 1
        
        print(f"\n{'='*60}")
        print(f"✅ COMPLETE: {success} swapped, {failed} failed")
        print(f"📁 Output: {OUTPUT_DIR}")
        print(f"{'='*60}")


def main():
    swapper = FaceSwapper()
    swapper.process_all_renders()


if __name__ == "__main__":
    main()
