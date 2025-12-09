"""
⚡ DAVE FACIAL IP EXTRACTION V2 ⚡
Create permanent JSON face profile - improved JSON parsing
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
TEXT_MODEL = "gemini-2.5-flash"

async def extract_facial_ip():
    print("=" * 70)
    print("⚡ DAVE FACIAL IP EXTRACTION V2 ⚡")
    print("=" * 70)
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    input_dir = Path("c:/Yuki_Local/Dav3 test")
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    
    print(f"\n📸 Loading {len(input_images)} photos...")
    
    image_parts = []
    image_files = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        image_files.append(img.name)
    
    prompt = """Analyze ALL 14 photos of this Black male subject. Create a comprehensive facial geometry JSON.

Output ONLY raw JSON (no markdown, no code blocks, no backticks). Start directly with { and end with }.

{
  "profile": {
    "name": "Dave",
    "role": "Default Black Male Template",
    "platform": "Yuki DNA-Authentic Cosplay"
  },
  "demographics": {
    "ethnicity": "Black/African American",
    "gender": "Male",
    "age_range": "<estimate>",
    "fitzpatrick": "<IV-VI>",
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
    "piercings": "<septum/nostril/none>"
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
    "eyelids": "<type>"
  },
  "eyebrows": {
    "shape": "<shape>",
    "thickness": "<level>",
    "arch": "<position>"
  },
  "hair": {
    "texture": "<type>",
    "style": "<current>",
    "hairline": "<shape>",
    "facial_hair": "<description>"
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

Fill in ALL fields with precise observations from the 14 photos. Be thorough and specific."""

    print("\n🔬 Analyzing facial geometry...")
    
    response = await client.aio.models.generate_content(
        model=TEXT_MODEL,
        contents=[prompt] + image_parts,
        config=types.GenerateContentConfig(temperature=0.2, max_output_tokens=4000)
    )
    
    text = response.text.strip()
    
    # Remove any markdown code blocks
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    
    # Parse JSON
    try:
        profile = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"   ⚠️ Parse issue, attempting fix...")
        # Try to find JSON in text
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            profile = json.loads(text[start:end])
        else:
            profile = {"raw": text}
    
    # Add metadata
    profile["_metadata"] = {
        "created": datetime.now().isoformat(),
        "model": TEXT_MODEL,
        "sources": image_files,
        "version": "2.0.0"
    }
    
    # Save
    output_path = Path("c:/Yuki_Local/dave_facial_ip.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ DAVE FACIAL IP SAVED!")
    print(f"📁 {output_path}")
    print(f"📊 {len(json.dumps(profile))} chars")
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 SUMMARY")
    print("=" * 70)
    if "demographics" in profile:
        d = profile["demographics"]
        print(f"   Ethnicity: {d.get('ethnicity', 'N/A')}")
        print(f"   Fitzpatrick: {d.get('fitzpatrick', 'N/A')}")
    if "bone_structure" in profile:
        print(f"   Face Shape: {profile['bone_structure'].get('face_shape', 'N/A')}")
    if "nose" in profile:
        print(f"   Piercings: {profile['nose'].get('piercings', 'N/A')}")
    if "distinctive_features" in profile:
        print(f"   Unique Features: {len(profile['distinctive_features'])}")
    
    print("\n🎯 Dave = DEFAULT BLACK MALE TEMPLATE")
    print("=" * 70)
    
    return profile

if __name__ == "__main__":
    asyncio.run(extract_facial_ip())
