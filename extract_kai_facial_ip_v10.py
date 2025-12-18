"""
⚡ KAI TAYLOR FACIAL IP EXTRACTION V10 ⚡
2-Pass method: Extract → Refine for Bella Swan (Twilight) cosplay
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
import json
import re

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
# V10 uses gemini-3-pro-preview with 2-pass method
TEXT_MODEL_PASS1 = "gemini-2.5-flash"  # Quick initial extraction
TEXT_MODEL_PASS2 = "gemini-3-pro-preview"  # Deep refinement

async def extract_facial_ip_v10():
    print("=" * 70)
    print("⚡ KAI TAYLOR FACIAL IP EXTRACTION V10 ⚡")
    print("🎭 Target Cosplay: Bella Swan (Twilight)")
    print("=" * 70)
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    # Load Kai Taylor's photos
    input_dir = Path("c:/Yuki_Local/Cosplay_Lab/Subjects/Kai Taylor")
    input_images = sorted(input_dir.glob("*.jpeg")) + sorted(input_dir.glob("*.jpg"))
    
    print(f"\n📸 Loading {len(input_images)} photos of Kai Taylor...")
    
    image_parts = []
    image_files = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        image_files.append(img.name)
        print(f"   ✓ {img.name}")
    
    # ============================================
    # PASS 1: Initial Facial Geometry Extraction
    # ============================================
    print("\n" + "=" * 70)
    print("🔬 PASS 1: Initial Facial Geometry Extraction")
    print("=" * 70)
    
    pass1_prompt = """Analyze ALL photos of this female subject. Create a comprehensive facial geometry JSON.

Output ONLY raw JSON (no markdown, no code blocks, no backticks). Start directly with { and end with }.

{
  "profile": {
    "name": "Kai Taylor",
    "role": "Primary Subject - Bella Swan Cosplay",
    "platform": "Yuki DNA-Authentic Cosplay V10"
  },
  "demographics": {
    "ethnicity": "<observe accurately>",
    "gender": "Female",
    "age_range": "<estimate>",
    "fitzpatrick": "<I-VI>",
    "undertone": "<warm/cool/neutral>"
  },
  "bone_structure": {
    "face_shape": "<shape>",
    "jawline": "<type, angle, definition>",
    "cheekbones": "<prominence, placement>",
    "chin": "<shape, projection>",
    "forehead": "<height, shape>"
  },
  "nose": {
    "bridge": "<shape, width, height>",
    "tip": "<shape>",
    "width": "<overall>",
    "nostrils": "<shape>",
    "profile": "<straight/curved/button>"
  },
  "lips": {
    "fullness": "<overall>",
    "upper": "<shape, fullness>",
    "lower": "<shape, fullness>",
    "width": "<relative>",
    "cupids_bow": "<defined/subtle/flat>"
  },
  "eyes": {
    "shape": "<shape>",
    "size": "<relative>",
    "spacing": "<close/average/wide>",
    "color": "<color>",
    "eyelids": "<type>",
    "lashes": "<natural description>"
  },
  "eyebrows": {
    "shape": "<shape>",
    "thickness": "<level>",
    "arch": "<position>",
    "color": "<color>"
  },
  "hair": {
    "texture": "<type>",
    "color": "<color>",
    "style": "<current>",
    "hairline": "<shape>",
    "length": "<length>"
  },
  "skin": {
    "tone": "<description>",
    "texture": "<description>",
    "notable_marks": "<any>"
  },
  "distinctive_features": [
    "<unique feature 1>",
    "<unique feature 2>",
    "<unique feature 3>"
  ],
  "identity_priorities": [
    "1. <most critical to preserve>",
    "2. <second critical>",
    "3. <third critical>",
    "4. <fourth>",
    "5. <fifth>"
  ],
  "generation_rules": {
    "must_preserve": ["<list>"],
    "can_modify": ["<list>"],
    "never_modify": ["<list>"]
  }
}

Fill in ALL fields with precise observations. Be thorough and specific."""

    response1 = await client.aio.models.generate_content(
        model=TEXT_MODEL_PASS1,
        contents=[pass1_prompt] + image_parts,
        config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=4000)
    )
    
    text1 = response1.text.strip()
    
    # Clean markdown artifacts
    text1 = re.sub(r'^```json\s*', '', text1)
    text1 = re.sub(r'^```\s*', '', text1)
    text1 = re.sub(r'\s*```$', '', text1)
    text1 = text1.strip()
    
    # Parse Pass 1 JSON
    try:
        profile_pass1 = json.loads(text1)
        print("   ✅ Pass 1 extraction complete!")
    except json.JSONDecodeError:
        print("   ⚠️ Parse issue, attempting fix...")
        start = text1.find('{')
        end = text1.rfind('}') + 1
        if start >= 0 and end > start:
            profile_pass1 = json.loads(text1[start:end])
        else:
            profile_pass1 = {"raw": text1}
    
    # ============================================
    # PASS 2: Deep Refinement with Gemini 3 Pro
    # ============================================
    print("\n" + "=" * 70)
    print("🔬 PASS 2: Deep Refinement (Gemini 3 Pro)")
    print("=" * 70)
    
    pass2_prompt = f"""You are refining a facial identity profile for cosplay generation.

PASS 1 EXTRACTION:
{json.dumps(profile_pass1, indent=2)}

Review ALL photos again and enhance this profile with:
1. More precise measurements and proportions
2. Subtle details that distinguish this person
3. Lighting-independent features
4. Key features for Bella Swan (Twilight) cosplay compatibility

Output ONLY the refined JSON (no markdown). Add these new sections:
- "bella_compatibility": analysis of which Kai features align with Bella Swan's look
- "transformation_notes": what makeup/styling would enhance Bella resemblance
- "critical_lock": top 3 features that MUST be preserved in any generation

Start directly with {{ and end with }}"""

    try:
        response2 = await client.aio.models.generate_content(
            model=TEXT_MODEL_PASS2,
            contents=[pass2_prompt] + image_parts,
            config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=6000)
        )
        
        text2 = response2.text.strip()
        text2 = re.sub(r'^```json\s*', '', text2)
        text2 = re.sub(r'^```\s*', '', text2)
        text2 = re.sub(r'\s*```$', '', text2)
        text2 = text2.strip()
        
        try:
            profile_final = json.loads(text2)
            print("   ✅ Pass 2 refinement complete!")
        except json.JSONDecodeError:
            print("   ⚠️ Using Pass 1 + enhancements...")
            start = text2.find('{')
            end = text2.rfind('}') + 1
            if start >= 0 and end > start:
                profile_final = json.loads(text2[start:end])
            else:
                profile_final = profile_pass1
                profile_final["_pass2_raw"] = text2
                
    except Exception as e:
        print(f"   ⚠️ Pass 2 failed ({e}), using Pass 1...")
        profile_final = profile_pass1
    
    # Add V10 metadata
    profile_final["_v10_metadata"] = {
        "created": datetime.now().isoformat(),
        "pass1_model": TEXT_MODEL_PASS1,
        "pass2_model": TEXT_MODEL_PASS2,
        "sources": image_files,
        "version": "10.0.0",
        "target_cosplay": "Bella Swan (Twilight)",
        "method": "2-pass extraction"
    }
    
    # Save
    output_path = Path("c:/Yuki_Local/Cosplay_Lab/Subjects/Kai Taylor/kai_taylor_facial_ip_v10.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile_final, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ KAI TAYLOR V10 FACIAL IP SAVED!")
    print(f"📁 {output_path}")
    print(f"📊 {len(json.dumps(profile_final))} chars")
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 V10 SUMMARY - KAI TAYLOR × BELLA SWAN")
    print("=" * 70)
    if "demographics" in profile_final:
        d = profile_final["demographics"]
        print(f"   Ethnicity: {d.get('ethnicity', 'N/A')}")
        print(f"   Fitzpatrick: {d.get('fitzpatrick', 'N/A')}")
    if "bone_structure" in profile_final:
        print(f"   Face Shape: {profile_final['bone_structure'].get('face_shape', 'N/A')}")
    if "distinctive_features" in profile_final:
        print(f"   Unique Features: {len(profile_final['distinctive_features'])}")
    if "bella_compatibility" in profile_final:
        print(f"\n🌙 BELLA COMPATIBILITY:")
        compat = profile_final["bella_compatibility"]
        if isinstance(compat, dict):
            for k, v in compat.items():
                print(f"   • {k}: {v}")
        else:
            print(f"   {compat}")
    if "critical_lock" in profile_final:
        print(f"\n🔒 CRITICAL IDENTITY LOCK:")
        for item in profile_final.get("critical_lock", []):
            print(f"   • {item}")
    
    print("\n🎯 Ready for Bella Swan (Twilight) generation!")
    print("=" * 70)
    
    return profile_final

if __name__ == "__main__":
    asyncio.run(extract_facial_ip_v10())
