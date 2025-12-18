"""
⚡ KAI TAYLOR V10 FULL FACIAL MOCAP ⚡
50+ Node Facial Geometry Extraction + 2-Pass Generation System
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
import json
import re

# Vertex AI - Gemini 2.5/3.0 (NEVER downgrade)
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"

# V10 2-Pass Models - GEMINI 3 ONLY
EXTRACTION_MODEL = "gemini-3-flash-preview"      # Pass 1
REFINEMENT_MODEL = "gemini-3-pro-preview"  # Pass 2 (Deep)
IMAGE_MODEL = "gemini-3-pro-image-preview" # Image generation

# 50+ Node Facial Mocap Schema
FACIAL_MOCAP_PROMPT = """Perform a DETAILED 50+ NODE FACIAL GEOMETRY MOCAP on this subject.

Output ONLY raw JSON. Analyze ALL uploaded photos to create a comprehensive facial skeleton.

{
  "subject_identity": {
    "name": "Kai Taylor",
    "ethnicity": "<precise ethnicity>",
    "fitzpatrick_scale": "<I-VI>",
    "age_estimate": "<range>"
  },
  
  "facial_skeleton_nodes": {
    "skull_landmarks": {
      "glabella": "<description - bone between eyebrows>",
      "nasion": "<bridge of nose root>",
      "supraorbital_ridge": "<brow bone prominence>",
      "frontal_eminence": "<forehead curvature>",
      "temporal_fossa": "<temple depth>"
    },
    
    "orbital_region": {
      "medial_canthus": "<inner eye corner position>",
      "lateral_canthus": "<outer eye corner position>",
      "canthal_tilt": "<positive/negative degrees>",
      "palpebral_fissure_height": "<eye opening height>",
      "orbital_rim": "<eye socket shape>",
      "supratarsal_crease": "<eyelid crease depth/visibility>"
    },
    
    "nasal_geometry": {
      "radix": "<nose root height/depth>",
      "rhinion": "<mid-nose bridge>",
      "supratip_break": "<present/absent/degree>",
      "tip_defining_points": "<tip shape nodes>",
      "alar_base_width": "<nostril width measurement>",
      "columella": "<nose base pillar shape>",
      "nasofrontal_angle": "<angle in degrees>",
      "nasolabial_angle": "<angle in degrees>"
    },
    
    "midface_nodes": {
      "malar_eminence": "<cheekbone prominence>",
      "infraorbital_hollow": "<under-eye shape>",
      "zygomatic_arch": "<cheekbone to ear line>",
      "nasojugal_groove": "<tear trough depth>",
      "midface_projection": "<forward projection amount>"
    },
    
    "oral_region": {
      "philtrum_nodes": {
        "philtral_columns": "<ridge definition>",
        "philtral_dimple": "<center depth>",
        "cupids_bow_peaks": "<height and sharpness>"
      },
      "vermilion_border": "<lip outline sharpness>",
      "upper_lip_ratio": "<percentage of total>",
      "lower_lip_ratio": "<percentage of total>",
      "oral_commissures": "<mouth corner position>",
      "labiomental_crease": "<chin-lip junction>"
    },
    
    "chin_jaw_nodes": {
      "pogonion": "<chin tip projection>",
      "gnathion": "<lowest chin point>",
      "mentolabial_sulcus": "<chin-lip valley depth>",
      "mandibular_angle": "<jaw corner angle in degrees>",
      "gonion": "<jaw angle point>",
      "mandibular_border": "<jawline curve type>",
      "bigonial_width": "<jaw width>"
    },
    
    "neck_nodes": {
      "cervicomental_angle": "<neck-chin angle>",
      "submental_area": "<under-chin shape>",
      "sternocleidomastoid": "<neck muscle visibility>",
      "thyroid_cartilage": "<Adam's apple if visible>"
    }
  },
  
  "critical_identity_markers": [
    "<TOP marker 1 - most recognizable feature>",
    "<TOP marker 2>",
    "<TOP marker 3>",
    "<TOP marker 4>",
    "<TOP marker 5>",
    "<TOP marker 6>",
    "<TOP marker 7>",
    "<TOP marker 8>",
    "<TOP marker 9>",
    "<TOP marker 10>"
  ],
  
  "generation_lock_rules": {
    "ABSOLUTE_PRESERVE": [
      "<list features that MUST NEVER change>"
    ],
    "SOFT_PRESERVE": [
      "<features important but can flex slightly>"
    ],
    "ALLOW_COSTUME_OVERRIDE": [
      "<features that can change for costume - e.g., hair color, makeup>"
    ]
  }
}

Analyze ALL photos from multiple angles. Be EXTREMELY precise with measurements and descriptions."""


async def extract_50_node_mocap():
    """Pass 1: Extract 50+ node facial geometry"""
    print("=" * 70)
    print("⚡ V10 PASS 1: 50+ NODE FACIAL MOCAP EXTRACTION ⚡")
    print("=" * 70)
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    # Load NEW clearer photos
    kai_dir = Path("c:/Yuki_Local/Cosplay_Lab/Subjects/Kai Taylor")
    kai_images = sorted(list(kai_dir.glob("kai_new_*.jpg")))
    
    print(f"📸 Loading {len(kai_images)} photos...")
    
    image_parts = []
    for img in kai_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        print(f"   ✓ {img.name}")
    
    # Pass 1: Initial extraction
    print(f"\n🔬 Extracting with {EXTRACTION_MODEL}...")
    
    response = await client.aio.models.generate_content(
        model=EXTRACTION_MODEL,
        contents=[FACIAL_MOCAP_PROMPT] + image_parts,
        config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=8000)
    )
    
    # Handle response properly
    if not response or not response.candidates:
        print("   ⚠️ No response from model, retrying...")
        await asyncio.sleep(5)
        response = await client.aio.models.generate_content(
            model=EXTRACTION_MODEL,
            contents=[FACIAL_MOCAP_PROMPT] + image_parts,
            config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=8000)
        )
    
    text = ""
    if response and response.candidates and response.candidates[0].content:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'text') and part.text:
                text = part.text.strip()
                break
    
    if not text:
        print("   ❌ No text extracted")
        return {"error": "no_response"}, image_parts
    
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    # Parse
    try:
        mocap_data = json.loads(text)
        print("   ✅ Pass 1 complete!")
    except json.JSONDecodeError:
        print("   ⚠️ Parsing, fixing...")
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            mocap_data = json.loads(text[start:end])
        else:
            mocap_data = {"raw": text}
    
    return mocap_data, image_parts


async def refine_mocap(mocap_data, image_parts):
    """Pass 2: Refine with stronger model"""
    print("\n" + "=" * 70)
    print("⚡ V10 PASS 2: DEEP REFINEMENT ⚡")
    print("=" * 70)
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    refine_prompt = f"""REFINE this facial mocap data. Add more precision to measurements and descriptions.

CURRENT MOCAP:
{json.dumps(mocap_data, indent=2)}

Review the photos again and:
1. Add numerical precision where possible (angles, ratios, percentages)
2. Add any missing distinguishing features
3. Strengthen the critical_identity_markers with more detail
4. Ensure generation_lock_rules are comprehensive

Output the ENHANCED JSON only (no markdown)."""

    print(f"🔬 Refining with {REFINEMENT_MODEL}...")
    
    response = await client.aio.models.generate_content(
        model=REFINEMENT_MODEL,
        contents=[refine_prompt] + image_parts,
        config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=10000)
    )
    
    text = response.text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        refined = json.loads(text)
        print("   ✅ Pass 2 refinement complete!")
        return refined
    except:
        print("   ⚠️ Using Pass 1 data")
        return mocap_data


async def generate_with_mocap(mocap_data, reference_path, kai_parts):
    """Generate using full mocap data"""
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    # Build identity lock prompt from mocap
    identity_markers = mocap_data.get("critical_identity_markers", [])
    absolute_preserve = mocap_data.get("generation_lock_rules", {}).get("ABSOLUTE_PRESERVE", [])
    
    nodes = mocap_data.get("facial_skeleton_nodes", {})
    
    generation_prompt = f"""COSPLAY GENERATION WITH FACIAL MOCAP LOCK

🔒 SUBJECT IDENTITY LOCK - 50+ NODE FACIAL GEOMETRY:

ORBITAL REGION:
- Canthal tilt: {nodes.get('orbital_region', {}).get('canthal_tilt', 'positive')}
- Eye shape: {nodes.get('orbital_region', {}).get('palpebral_fissure_height', 'N/A')}
- Lid crease: {nodes.get('orbital_region', {}).get('supratarsal_crease', 'N/A')}

NASAL GEOMETRY:
- Supratip break: {nodes.get('nasal_geometry', {}).get('supratip_break', 'present')}
- Tip shape: {nodes.get('nasal_geometry', {}).get('tip_defining_points', 'upturned')}
- Alar width: {nodes.get('nasal_geometry', {}).get('alar_base_width', 'medium')}

ORAL REGION:
- Cupid's bow: {nodes.get('oral_region', {}).get('philtrum_nodes', {}).get('cupids_bow_peaks', 'sharp')}
- Lip ratio: {nodes.get('oral_region', {}).get('upper_lip_ratio', '40%')} upper / {nodes.get('oral_region', {}).get('lower_lip_ratio', '60%')} lower

CHIN/JAW:
- Mandibular angle: {nodes.get('chin_jaw_nodes', {}).get('mandibular_angle', 'soft')}
- Chin shape: {nodes.get('chin_jaw_nodes', {}).get('pogonion', 'tapered')}

MIDFACE:
- Malar prominence: {nodes.get('midface_nodes', {}).get('malar_eminence', 'high but soft')}
- Cheek fullness: {nodes.get('midface_nodes', {}).get('midface_projection', 'N/A')}

🎯 CRITICAL IDENTITY MARKERS (TOP 10):
{chr(10).join(f'• {m}' for m in identity_markers[:10])}

🔐 ABSOLUTE PRESERVE:
{chr(10).join(f'• {p}' for p in absolute_preserve)}

TASK: Generate this exact person (Kai Taylor from subject photos) wearing the costume shown in the reference image.
- FACE = Kai Taylor (use subject photos for face)
- COSTUME = From reference image only
- DO NOT use the reference person's face"""

    # Load reference
    with open(reference_path, "rb") as f:
        mime = "image/jpeg" if str(reference_path).lower().endswith(('.jpg', '.jpeg')) else "image/png"
        ref_part = types.Part.from_bytes(data=f.read(), mime_type=mime)
    
    contents = kai_parts + [generation_prompt, "Reference (costume only):", ref_part]
    
    response = await client.aio.models.generate_content(
        model=IMAGE_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE', 'TEXT'],
            temperature=1.0
        )
    )
    
    return response


async def main():
    print("=" * 70)
    print("⚡ V10 FULL PIPELINE: 50+ NODE MOCAP + 2-PASS GENERATION ⚡")
    print("=" * 70)
    
    # Step 1: Extract 50+ node mocap
    mocap_data, image_parts = await extract_50_node_mocap()
    
    # Step 2: Refine with Pass 2
    refined_mocap = await refine_mocap(mocap_data, image_parts)
    
    # Save mocap
    output_dir = Path("c:/Yuki_Local/Cosplay_Lab/Subjects/Kai Taylor")
    mocap_path = output_dir / "kai_v10_50node_mocap.json"
    refined_mocap["_metadata"] = {
        "created": datetime.now().isoformat(),
        "version": "V10-50NODE",
        "pass1_model": EXTRACTION_MODEL,
        "pass2_model": REFINEMENT_MODEL
    }
    with open(mocap_path, "w", encoding="utf-8") as f:
        json.dump(refined_mocap, f, indent=2)
    print(f"\n✅ Saved mocap: {mocap_path}")
    
    # Step 3: Generate from references
    ref_dir = Path("c:/Yuki_Local/Cosplay_Lab/References")
    refs = [f for f in ref_dir.glob("*.jpg")][:3]
    
    render_dir = Path("c:/Yuki_Local/Cosplay_Lab/Renders/kai_bella_v10_50node")
    render_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert image_parts to kai_parts for generation
    kai_parts = image_parts[:3]  # Use first 3 for generation
    
    for i, ref in enumerate(refs, 1):
        print(f"\n{'='*70}")
        print(f"🎬 Generating {i}/{len(refs)}: {ref.name}")
        print("="*70)
        
        try:
            response = await generate_with_mocap(refined_mocap, ref, kai_parts)
            
            if response.candidates and response.candidates[0].content:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        out_path = render_dir / f"kai_bella_50node_{i:02d}.png"
                        with open(out_path, "wb") as f:
                            f.write(part.inline_data.data)
                        print(f"   ✅ {out_path.name}")
                        break
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        await asyncio.sleep(15)
    
    print("\n" + "=" * 70)
    print("✅ V10 50-NODE PIPELINE COMPLETE")
    print(f"📁 Renders: {render_dir}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
