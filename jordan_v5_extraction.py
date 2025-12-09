"""
⚡ JORDAN V5 DEEP NODE EXTRACTION ⚡
Full V5 mocap treatment + Primary Subject Detection
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
import json, re

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
MODEL = "gemini-3-pro-preview"

async def extract_v5_primary_subject(input_dir: Path, output_path: Path):
    """V5 Deep Nodes + Primary Subject Detection combined"""
    
    console.print(f"\n[bold magenta]🎯 JORDAN V5 DEEP NODE EXTRACTION[/bold magenta]")
    console.print(f"[cyan]   Primary Subject Detection + Full V5 Mocap[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    input_images = sorted(input_dir.glob("*.jpg"))
    console.print(f"[cyan]   Loading {len(input_images)} photos...[/cyan]")
    
    image_parts = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        console.print(f"   ✓ {img.name}")
    
    prompt = f"""You are analyzing {len(image_parts)} photos. Some have MULTIPLE PEOPLE.

STEP 1: Identify the PRIMARY SUBJECT - the person appearing MOST OFTEN.
STEP 2: Create a DEEP V5 FACIAL MAP for ONLY that person (like VFX mocap with 100+ nodes).

⚠️ RULES:
- Ignore background people and secondary subjects
- ONLY describe what you CLEARLY see - no assumptions
- Be EXTREMELY specific about the PRIMARY SUBJECT's face

Output ONLY raw JSON:

{{
  "primary_subject_detection": {{
    "appears_in": "<X of {len(image_parts)} photos>",
    "description": "<brief description>",
    "confidence": "HIGH/MEDIUM/LOW"
  }},
  
  "face_calibration": {{
    "overall_shape": "<oval/round/square/oblong/heart/diamond/triangle>",
    "width_to_length_ratio": "<decimal estimate>",
    "symmetry_score": "<1-10>"
  }},
  
  "forehead_nodes": {{
    "height": "<low/medium/high>",
    "width": "<narrow/average/wide>",
    "shape": "<flat/curved/sloped>",
    "hairline": "<straight/rounded/widows peak/M-shaped>"
  }},
  
  "eyebrow_nodes": {{
    "shape": "<straight/soft arch/high arch>",
    "thickness": "<thin/medium/thick>",
    "color": "<color>",
    "spacing_from_eyes": "<close/average/far>"
  }},
  
  "eye_nodes": {{
    "shape": "<almond/round/hooded/monolid/deep-set/upturned/downturned>",
    "size": "<small/medium/large>",
    "color": "<specific color>",
    "spacing": "<close-set/average/wide-set>",
    "lid_visible": "<yes/hooded/partial>",
    "lash_density": "<sparse/average/thick>",
    "eye_cant": "<neutral/upturned/downturned - describe angle>",
    "under_eye": "<smooth/slight shadow/dark circles>"
  }},
  
  "nose_nodes": {{
    "bridge_shape": "<straight/curved/bumped/flat/concave>",
    "bridge_width": "<narrow/medium/wide>",
    "tip_shape": "<pointed/rounded/bulbous/upturned/downturned>",
    "tip_width": "<narrow/medium/wide>",
    "nostril_shape": "<round/oval/slit/flared>",
    "nostril_size": "<small/medium/large>",
    "nose_length_ratio": "<short/average/long relative to face>",
    "piercings": "<none/septum/nostril with details>"
  }},
  
  "cheek_nodes": {{
    "cheekbone_prominence": "<flat/subtle/defined/high/very prominent>",
    "cheek_fullness": "<hollow/average/full>",
    "nasolabial_depth": "<none/subtle/moderate/deep>"
  }},
  
  "lip_nodes": {{
    "upper_fullness": "<thin/medium/full/very full>",
    "lower_fullness": "<thin/medium/full/very full>",
    "lip_ratio": "<upper to lower ratio>",
    "cupids_bow": "<flat/subtle/defined/very defined>",
    "lip_width": "<narrow/average/wide>",
    "corners": "<upturned/neutral/downturned>",
    "philtrum_depth": "<shallow/average/deep>"
  }},
  
  "jaw_chin_nodes": {{
    "jaw_shape": "<V-shaped/U-shaped/square/round/angular>",
    "jaw_width": "<narrow/average/wide>",
    "jaw_definition": "<soft/moderate/defined/very sharp>",
    "chin_shape": "<pointed/rounded/square/cleft>",
    "chin_projection": "<recessed/average/prominent>",
    "chin_vertical_length": "<short/average/long>"
  }},
  
  "skin_surface": {{
    "fitzpatrick": "<I/II/III/IV/V/VI>",
    "tone": "<detailed description>",
    "undertone": "<cool/neutral/warm>",
    "texture": "<smooth/normal/textured>",
    "notable_marks": ["<moles, scars, tattoos with positions>"]
  }},
  
  "hair_frame": {{
    "color": "<color>",
    "texture": "<straight/wavy/curly/coily/kinky/braided>",
    "length": "<short/medium/long>",
    "style": "<current style in detail>",
    "hairline_shape": "<description>"
  }},
  
  "teeth_if_visible": {{
    "visibility": "<not visible/some/clearly visible>",
    "characteristics": "<only what you CLEARLY SEE - do NOT assume>"
  }},
  
  "piercings_jewelry": {{
    "nose": "<none or description>",
    "ears": "<description>",
    "lip": "<none or description>",
    "other": "<any other visible>"
  }},
  
  "tattoos_visible": ["<list any visible tattoos with EXACT locations>"],
  
  "critical_identity_lock": {{
    "unique_identifiers_ranked": [
      "1. <MOST unique feature>",
      "2. <second>",
      "3. <third>",
      "4. <fourth>",
      "5. <fifth>",
      "6. <sixth>",
      "7. <seventh>"
    ],
    "absolute_preservation": ["<features that define identity>"],
    "never_modify": ["bone structure", "skin tone", "facial proportions", "eye spacing"]
  }},
  
  "secondary_subjects_ignored": ["<brief list of other people found>"]
}}"""

    console.print(f"[yellow]   Running V5 deep extraction on primary subject...[/yellow]")
    
    with console.status("[cyan]   Mapping 100+ facial nodes...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=6000)
        )
    
    text = response.text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        profile = json.loads(text[start:end])
    except:
        profile = {"raw": text, "error": "Parse failed"}
    
    profile["_metadata"] = {
        "created": datetime.now().isoformat(),
        "model": MODEL,
        "extraction_type": "V5_DEEP_NODES_PRIMARY_SUBJECT",
        "photo_count": len(input_images)
    }
    
    with open(output_path, "w") as f:
        json.dump(profile, f, indent=2)
    
    char_count = len(json.dumps(profile))
    console.print(f"[green]   ✅ V5 Deep Map: {char_count} chars[/green]")
    console.print(f"[green]   💾 Saved: {output_path}[/green]")
    
    if "critical_identity_lock" in profile:
        console.print(f"\n[cyan]Top Unique Identifiers:[/cyan]")
        for ident in profile.get("critical_identity_lock", {}).get("unique_identifiers_ranked", [])[:5]:
            console.print(f"   • {ident}")
    
    return profile

async def main():
    console.print("[bold cyan]═══ JORDAN V5 DEEP NODE EXTRACTION ═══[/bold cyan]")
    
    input_dir = Path("c:/Yuki_Local/jordan test")
    output_path = Path("c:/Yuki_Local/jordan_test_results/jordan_v5_deep_nodes.json")
    
    await extract_v5_primary_subject(input_dir, output_path)
    console.print("\n[bold green]✨ V5 EXTRACTION COMPLETE![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
