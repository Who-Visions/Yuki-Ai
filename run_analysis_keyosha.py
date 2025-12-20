"""
Stage 3: Deep Analysis & Identity Lock with Gemini 3 Pro
Uses CV data + 68-point expansion to create comprehensive identity lock
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
PRO_MODEL = "gemini-3-pro-preview"

SUBJECT_DIR = Path("C:/Yuki_Local/Cosplay_Lab/Subjects/Keyosha Pullman")
SUBJECT_NAME = "Keyosha Pullman"

# Deep analysis prompt
ANALYSIS_PROMPT = """DEEP IDENTITY ANALYSIS FOR HIGH-FIDELITY IMAGE GENERATION

You are analyzing {subject_name} to create a COMPREHENSIVE IDENTITY LOCK.

CLOUD VISION DATA (34 landmarks + angles):
{cv_data}

68-POINT EXPANSION + NECK/JAWLINE:
{expansion_data}

SUBJECT PHOTOS: Analyze the attached images carefully.

TASK: Create an IDENTITY LOCK that will be used for image generation.
The lock must capture EVERYTHING that makes this person uniquely identifiable.

Output JSON:
{{
  "identity_lock": {{
    "subject_info": {{
      "name": "{subject_name}",
      "ethnicity": "<precise ethnic background>",
      "skin_tone": "<Fitzpatrick I-VI + hex color + description>",
      "age_range": "<years>",
      "gender_presentation": "<description>"
    }},
    
    "geometric_signatures": {{
      "face_shape": "<shape with precise description>",
      "face_angles": {{"roll": <deg>, "pan": <deg>, "tilt": <deg>}},
      "facial_thirds": {{
        "upper": "<forehead description>",
        "middle": "<eyes to nose description>",
        "lower": "<nose to chin description>"
      }},
      "key_ratios": {{
        "eye_width_to_face": <ratio>,
        "nose_length_to_face": <ratio>,
        "mouth_width_to_face": <ratio>,
        "interocular_distance": <normalized>,
        "nose_to_lip_ratio": <ratio>,
        "jaw_width_to_cheek": <ratio>
      }}
    }},
    
    "feature_signatures": {{
      "eyes": {{
        "shape": "<detailed shape description>",
        "canthal_tilt": "<positive/negative/neutral with degrees>",
        "lid_type": "<monolid/double lid/hooded>",
        "color": "<iris color>",
        "unique_traits": ["<specific distinguishing features>"]
      }},
      "eyebrows": {{
        "shape": "<arch type>",
        "thickness": "<thin/medium/thick>",
        "spacing": "<description>",
        "unique_traits": ["<list>"]
      }},
      "nose": {{
        "bridge_profile": "<straight/curved/aquiline>",
        "bridge_width": "<narrow/medium/wide>",
        "tip_shape": "<bulbous/pointed/upturned/drooping>",
        "nostril_shape": "<round/oval/flared>",
        "unique_traits": ["<list>"]
      }},
      "lips": {{
        "shape": "<detailed shape>",
        "cupids_bow": "<sharp/rounded/flat>",
        "fullness": {{
          "upper": "<thin/medium/full>",
          "lower": "<thin/medium/full>",
          "ratio": <upper_to_lower>
        }},
        "unique_traits": ["<list>"]
      }},
      "bone_structure": {{
        "cheekbones": "<prominence and position>",
        "jawline": "<sharp/soft/square/rounded>",
        "mandible_angle": "<degrees>",
        "chin": "<shape and prominence>",
        "forehead": "<shape and height>"
      }},
      "neck": {{
        "length": "<short/medium/long>",
        "width": "<narrow/medium/wide>",
        "cervicomental_angle": "<degrees>",
        "notable_features": ["<list>"]
      }}
    }},
    
    "skin_characteristics": {{
      "base_tone": "<hex color>",
      "undertone": "<warm/cool/neutral>",
      "texture": "<smooth/textured>",
      "notable_features": ["<moles, freckles, marks with locations>"]
    }},
    
    "expression_baseline": {{
      "resting_expression": "<description>",
      "smile_type": "<description if visible>",
      "eye_openness": "<narrow/medium/wide>"
    }},
    
    "absolute_preserve": [
      "<TOP 10 features that DEFINE this person - be EXTREMELY SPECIFIC>"
    ],
    
    "generation_guidance": "<detailed paragraph on exactly how to recreate this face>"
  }},
  
  "confidence_score": <0.0-1.0>,
  "analysis_notes": "<any important observations>"
}}

Be EXTREMELY precise. This identity lock controls image generation fidelity."""


async def deep_analysis():
    """Run Stage 3 Deep Analysis on Keyosha Pullman"""
    print("=" * 60)
    print(f"🧠 STAGE 3: Deep Analysis with Gemini 3 Pro")
    print(f"   Subject: {SUBJECT_NAME}")
    print("=" * 60)
    
    # Load CV 34-node data
    cv_path = SUBJECT_DIR / "facial_ip_34node.json"
    if not cv_path.exists():
        print(f"❌ Missing: {cv_path}")
        return
    
    with open(cv_path, "r", encoding="utf-8") as f:
        cv_data = json.load(f)
    
    # Load 68-node expansion
    expansion_path = SUBJECT_DIR / "facial_ip_68node_neck.json"
    if not expansion_path.exists():
        print(f"❌ Missing: {expansion_path}")
        return
    
    with open(expansion_path, "r", encoding="utf-8") as f:
        expansion_data = json.load(f)
    
    print(f"✅ Loaded CV data: {cv_data['photos_analyzed']} faces")
    print(f"✅ Loaded 68-node expansion")
    
    # Get best CV face
    best_cv = max(cv_data["faces"], key=lambda x: x["data"]["detection_confidence"])
    
    # Load multiple subject photos for analysis
    photos = sorted(SUBJECT_DIR.glob("*.jpg"), key=lambda p: p.stat().st_size, reverse=True)[:4]
    print(f"📸 Loading {len(photos)} photos for analysis...")
    
    image_parts = []
    for p in photos:
        with open(p, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        print(f"   ✓ {p.name}")
    
    # Initialize Gemini
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    prompt = ANALYSIS_PROMPT.format(
        subject_name=SUBJECT_NAME,
        cv_data=json.dumps(best_cv["data"], indent=2),
        expansion_data=json.dumps(expansion_data["expansion_68"], indent=2)
    )
    
    print(f"\n🔬 Analyzing with {PRO_MODEL}...")
    
    try:
        response = await client.aio.models.generate_content(
            model=PRO_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=10000
            )
        )
        
        text = response.text.strip()
        
        # Clean markdown
        import re
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        
        # Parse JSON
        try:
            analysis = json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                analysis = json.loads(text[start:end])
            else:
                print(f"❌ Failed to parse JSON response")
                print(f"Raw response:\n{text[:500]}...")
                return
        
        # Create complete identity lock file
        identity_lock = {
            "subject_name": SUBJECT_NAME,
            "version": "V11-IDENTITY-LOCK",
            "created_at": datetime.now().isoformat(),
            "pipeline_stages": {
                "stage1": "Cloud Vision API (34 landmarks)",
                "stage2": "Gemini 3 Flash (68-point + neck expansion)",
                "stage3": f"{PRO_MODEL} (deep analysis)"
            },
            "source_photos": [p.name for p in photos],
            "cv_summary": {
                "best_photo": best_cv["file"],
                "confidence": best_cv["data"]["detection_confidence"],
                "face_angles": best_cv["data"]["face_angles"]
            },
            "expansion_summary": {
                "landmarks_68_count": len(expansion_data["expansion_68"].get("landmarks_68", [])),
                "neck_nodes_count": len(expansion_data["expansion_68"].get("neck_nodes", [])),
                "face_shape": expansion_data["expansion_68"].get("face_geometry", {}).get("face_shape"),
                "jawline": expansion_data["expansion_68"].get("jawline_detail", {})
            },
            "deep_analysis": analysis
        }
        
        # Save
        output_path = SUBJECT_DIR / "identity_lock_v11.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(identity_lock, f, indent=2)
        
        # Extract key info for display
        lock = analysis.get("identity_lock", analysis)
        subject_info = lock.get("subject_info", {})
        features = lock.get("feature_signatures", {})
        preserve = lock.get("absolute_preserve", [])
        
        print(f"\n{'='*60}")
        print(f"✅ STAGE 3 COMPLETE: Identity Lock Created")
        print(f"{'='*60}")
        print(f"   Subject: {subject_info.get('name', SUBJECT_NAME)}")
        print(f"   Ethnicity: {subject_info.get('ethnicity', 'N/A')}")
        print(f"   Skin tone: {subject_info.get('skin_tone', 'N/A')}")
        print(f"   Face shape: {lock.get('geometric_signatures', {}).get('face_shape', 'N/A')}")
        print(f"   Confidence: {analysis.get('confidence_score', 'N/A')}")
        print(f"\n   TOP PRESERVE FEATURES:")
        for i, feat in enumerate(preserve[:5], 1):
            print(f"   {i}. {feat}")
        print(f"\n💾 Saved: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(deep_analysis())
