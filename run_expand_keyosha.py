"""
Stage 2: Expand 34-node to 68-point schema with neck/jawline
Uses Gemini 3 Flash for semantic expansion
"""
import asyncio
import json
from pathlib import Path
from datetime import datetime

from google import genai
from google.genai import types

# Config
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
FLASH_MODEL = "gemini-3-flash-preview"

SUBJECT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Keyosha Pullman")

# Enhanced expansion prompt with neck/jawline
EXPANSION_PROMPT = """FACIAL LANDMARK EXPANSION: 34 → 68+ POINTS WITH NECK/JAWLINE

You have Cloud Vision API data with 34 landmarks:
{cv_data}

TASK: Expand to the FULL 68-POINT SCHEMA plus NECK/UPPER BODY nodes.

The 68 points follow dlib/iBUG standard:
- Points 0-16: Jawline (17 points) - CRITICAL for identity
- Points 17-21: Right eyebrow (5 points)
- Points 22-26: Left eyebrow (5 points)
- Points 27-30: Nose bridge (4 points)
- Points 31-35: Nose bottom (5 points)
- Points 36-41: Right eye (6 points)
- Points 42-47: Left eye (6 points)
- Points 48-59: Outer lip (12 points)
- Points 60-67: Inner lip (8 points)

ADDITIONAL NODES (beyond standard 68):
- Points 68-72: Neck contour (5 points) - follow from jawline
- Points 73-75: Collar/shoulder line (3 points)
- Point 76: Adam's apple / thyroid cartilage position
- Point 77: Chin-neck junction (cervicomental angle)

Using the Cloud Vision landmarks and face image, INFER missing points by:
1. Mapping existing landmarks to 68-point equivalents
2. Interpolating missing jawline points from face contour
3. Estimating neck nodes based on face geometry and visible neck

Output JSON ONLY:
{{
  "landmarks_68": [
    {{"index": 0, "region": "jawline", "x": <value>, "y": <value>}},
    ...all 68 standard points...
  ],
  "neck_nodes": [
    {{"index": 68, "region": "neck_left", "x": <value>, "y": <value>}},
    {{"index": 69, "region": "neck_center", "x": <value>, "y": <value>}},
    {{"index": 70, "region": "neck_right", "x": <value>, "y": <value>}},
    {{"index": 71, "region": "collar_left", "x": <value>, "y": <value>}},
    {{"index": 72, "region": "collar_right", "x": <value>, "y": <value>}}
  ],
  "jawline_detail": {{
    "jaw_angle_left": "<degrees>",
    "jaw_angle_right": "<degrees>",
    "chin_shape": "<pointed/rounded/square>",
    "mandible_width": "<narrow/medium/wide>",
    "jawline_definition": "<sharp/soft/undefined>"
  }},
  "neck_detail": {{
    "neck_length": "<short/medium/long>",
    "neck_width": "<narrow/medium/wide>",
    "cervicomental_angle": "<degrees estimate>",
    "visible_landmarks": ["<list visible neck features>"]
  }},
  "face_geometry": {{
    "face_shape": "<oval/heart/round/square/oblong>",
    "symmetry_score": <0.0-1.0>,
    "proportions": {{
      "forehead_to_chin": <ratio>,
      "bizygomatic_width": <ratio>,
      "jaw_to_cheek_ratio": <ratio>
    }}
  }},
  "confidence": {{
    "landmarks_68": <0.0-1.0>,
    "neck_nodes": <0.0-1.0>,
    "overall": <0.0-1.0>
  }}
}}"""


async def expand_landmarks():
    """Run 68-point expansion on Keyosha Pullman"""
    print("=" * 60)
    print("⚡ STAGE 2: 68-Point + Neck/Jawline Expansion")
    print("=" * 60)
    
    # Load 34-node facial IP
    ip_path = SUBJECT_DIR / "facial_ip_34node.json"
    if not ip_path.exists():
        print(f"❌ Missing: {ip_path}")
        return
    
    with open(ip_path, "r", encoding="utf-8") as f:
        facial_ip = json.load(f)
    
    print(f"📂 Loaded: {facial_ip['photos_analyzed']} faces")
    
    # Use best face (highest confidence)
    best_face = max(facial_ip["faces"], key=lambda x: x["data"]["detection_confidence"])
    cv_data = best_face["data"]
    
    print(f"🎯 Best face: {best_face['file']} (conf: {cv_data['detection_confidence']})")
    
    # Load image for Gemini
    img_path = SUBJECT_DIR / best_face["file"]
    with open(img_path, "rb") as f:
        img_part = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    # Initialize Gemini
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    prompt = EXPANSION_PROMPT.format(cv_data=json.dumps(cv_data, indent=2))
    
    print(f"\n🔬 Expanding with {FLASH_MODEL}...")
    
    try:
        response = await client.aio.models.generate_content(
            model=FLASH_MODEL,
            contents=[prompt, img_part],
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=8000
            )
        )
        
        text = response.text.strip()
        # Clean markdown
        import re
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        
        expansion = json.loads(text)
        
        # Save expanded facial IP
        expanded_ip = {
            "subject_name": "Keyosha Pullman",
            "version": "V11-68NODE-NECK",
            "source_file": best_face["file"],
            "created_at": datetime.now().isoformat(),
            "cv_34_data": cv_data,
            "expansion_68": expansion
        }
        
        output_path = SUBJECT_DIR / "facial_ip_68node_neck.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(expanded_ip, f, indent=2)
        
        print(f"\n✅ Expansion complete!")
        print(f"   68 landmarks: {len(expansion.get('landmarks_68', []))}")
        print(f"   Neck nodes: {len(expansion.get('neck_nodes', []))}")
        print(f"   Jawline: {expansion.get('jawline_detail', {}).get('chin_shape', 'N/A')}")
        print(f"   Face shape: {expansion.get('face_geometry', {}).get('face_shape', 'N/A')}")
        print(f"   Confidence: {expansion.get('confidence', {}).get('overall', 'N/A')}")
        print(f"\n💾 Saved: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(expand_landmarks())
