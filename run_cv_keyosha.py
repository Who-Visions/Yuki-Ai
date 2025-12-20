"""Run Cloud Vision on Keyosha Pullman subject photos"""
from pathlib import Path
import json
from image_gen.v11_pipeline import CloudVisionAnalyzer

subject_dir = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Keyosha Pullman")
output_dir = subject_dir

cv = CloudVisionAnalyzer()

# Get best photos (largest JPGs)
photos = sorted(subject_dir.glob("*.jpg"), key=lambda p: p.stat().st_size, reverse=True)[:4]

print(f"Processing {len(photos)} photos for 34-node facial geometry...")

all_results = []
for p in photos:
    print(f"\n--- {p.name} ---")
    result = cv.detect_face(p)
    if "error" not in result:
        all_results.append({"file": p.name, "data": result})
        print(f"  Landmarks: {result['landmark_count']}")
        print(f"  Confidence: {result['detection_confidence']}")
        print(f"  Face Angles: roll={result['face_angles']['roll']}, pan={result['face_angles']['pan']}, tilt={result['face_angles']['tilt']}")
    else:
        print(f"  Error: {result['error']}")

# Save consolidated facial IP
facial_ip_path = output_dir / "facial_ip_34node.json"
facial_ip = {
    "subject_name": "Keyosha Pullman",
    "version": "V11-34NODE",
    "photos_analyzed": len(all_results),
    "faces": all_results
}

with open(facial_ip_path, "w", encoding="utf-8") as f:
    json.dump(facial_ip, f, indent=2)

print(f"\n✅ Saved facial IP: {facial_ip_path}")
print(f"   Photos processed: {len(all_results)}")
