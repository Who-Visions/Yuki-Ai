"""
⚡ FACIAL IP EXTRACTOR V5 - DEEP NODE MAPPING ⚡
Inspired by VFX mocap face tracking with 100+ landmark points
MORE anchor points, MORE topology detail, MORE precision

Goal: Create such precise facial data that the AI has no choice
but to preserve the real face and only change costume elements.
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
import json
import re

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
ANALYSIS_MODEL = "gemini-3-pro-preview"

async def extract_v5_deep_nodes(input_dir: Path, output_path: Path, subject_name: str = "Subject"):
    """
    V5 Deep Node Mapping - like VFX mocap face tracking
    100+ conceptual landmark points for maximum identity preservation
    """
    
    console.print(f"\n[bold magenta]🎬 FACIAL IP V5 - DEEP NODE MAPPING[/bold magenta]")
    console.print(f"[cyan]   Inspired by VFX mocap - maximum anchor points[/cyan]")
    console.print(f"[cyan]   Model: {ANALYSIS_MODEL}[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    if not input_images:
        input_images = sorted(input_dir.glob("*.JPG"))[:14]
    
    console.print(f"[cyan]   Loading {len(input_images)} photos for deep node analysis...[/cyan]")
    
    image_parts = []
    image_files = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        image_files.append(img.name)
    
    # V5 Deep extraction with MANY more points
    prompt = f"""You are a VFX facial capture technician creating a DEEP NODE MAP for face tracking.
Think: 100+ mocap markers, ARKit face tracking, MediaPipe landmarks.

Analyze ALL {len(image_parts)} photos. Create the most DETAILED facial topology ever.

⚠️ RULES:
1. ONLY describe what you CLEARLY see - no assumptions
2. Be EXTREMELY specific about shapes, proportions, ratios
3. Think in terms of 3D space - how would VFX software track this face?
4. This data will be used to preserve identity in AI image generation

Output ONLY raw JSON (no markdown):

{{
  "subject_id": "{subject_name}",
  "map_version": "V5_DEEP_NODES",
  "confidence": "HIGH/MEDIUM/LOW",
  
  "face_calibration": {{
    "overall_shape": "<oval/round/square/oblong/heart/diamond/triangle>",
    "face_width_mm_estimate": "<estimate in mm based on proportions>",
    "face_length_mm_estimate": "<estimate in mm>",
    "width_to_length_ratio": "<decimal ratio>",
    "depth_profile": "<flat/average/prominent features>",
    "symmetry_score": "<1-10, where 10 is perfectly symmetric>"
  }},
  
  "forehead_nodes": {{
    "F1_hairline_center": "<position and shape>",
    "F2_temple_left": "<position>",
    "F3_temple_right": "<position>",
    "F4_brow_ridge_left": "<prominence>",
    "F5_brow_ridge_right": "<prominence>",
    "forehead_surface": "<flat/curved/sloped>",
    "forehead_height_ratio": "<ratio to total face>",
    "visible_veins_or_lines": "<none/subtle/visible>"
  }},
  
  "eyebrow_nodes": {{
    "EB1_left_inner": "<shape and position>",
    "EB2_left_arch_peak": "<position and height>",
    "EB3_left_outer": "<position and angle>",
    "EB4_right_inner": "<shape and position>",
    "EB5_right_arch_peak": "<position and height>",
    "EB6_right_outer": "<position and angle>",
    "brow_thickness": "<thin/medium/thick>",
    "brow_color": "<color>",
    "brow_texture": "<sparse/normal/thick/bushy>",
    "brow_symmetry": "<symmetric/left higher/right higher>",
    "distance_to_eyes": "<close/average/far>"
  }},
  
  "eye_nodes": {{
    "E1_left_inner_canthus": "<position>",
    "E2_left_pupil_center": "<position>",
    "E3_left_outer_canthus": "<position>",
    "E4_left_upper_lid_peak": "<position and curve>",
    "E5_left_lower_lid_lowest": "<position>",
    "E6_right_inner_canthus": "<position>",
    "E7_right_pupil_center": "<position>",
    "E8_right_outer_canthus": "<position>",
    "E9_right_upper_lid_peak": "<position and curve>",
    "E10_right_lower_lid_lowest": "<position>",
    "eye_shape": "<almond/round/hooded/monolid/deep-set/upturned/downturned>",
    "eye_size": "<small/medium/large relative to face>",
    "eye_color": "<specific color with detail>",
    "iris_pattern": "<solid/ring/multicolor>",
    "sclera_visibility": "<none/minimal/visible>",
    "eye_spacing": "<close-set/average/wide-set>",
    "eye_spacing_description": "<describe in terms of eye widths between eyes>",
    "upper_lid_crease": "<single/double/hooded/none>",
    "under_eye_area": "<smooth/slight shadow/dark circles/puffy>",
    "lash_density": "<sparse/average/thick>",
    "eye_cant": "<neutral/upturned/downturned - describe angle>"
  }},
  
  "nose_nodes": {{
    "N1_nasion": "<bridge top, between brows>",
    "N2_bridge_midpoint": "<bridge middle>",
    "N3_tip": "<nasal tip shape and projection>",
    "N4_left_ala": "<nostril wing left>",
    "N5_right_ala": "<nostril wing right>",
    "N6_left_nostril_base": "<nostril base left>",
    "N7_right_nostril_base": "<nostril base right>",
    "N8_columella": "<center bottom of nose>",
    "bridge_shape": "<straight/curved/bumped/flat/concave>",
    "bridge_width_top": "<narrow/medium/wide>",
    "bridge_width_bottom": "<narrow/medium/wide>",
    "tip_shape": "<pointed/rounded/bulbous/upturned/downturned>",
    "tip_width": "<narrow/medium/wide>",
    "tip_projection": "<minimal/average/prominent>",
    "nostril_shape": "<round/oval/slit/flared>",
    "nostril_size": "<small/medium/large>",
    "nostril_visibility_front": "<not visible/slightly/clearly visible>",
    "nose_length_ratio": "<ratio to face length>",
    "nose_width_ratio": "<ratio to face width>",
    "piercings": "<none/septum/nostril left/nostril right with jewelry description>"
  }},
  
  "cheek_nodes": {{
    "C1_left_cheekbone_high": "<position and prominence>",
    "C2_left_cheek_hollow": "<depth>",
    "C3_left_nasolabial_start": "<fold start>",
    "C4_right_cheekbone_high": "<position and prominence>",
    "C5_right_cheek_hollow": "<depth>",
    "C6_right_nasolabial_start": "<fold start>",
    "cheekbone_prominence": "<flat/subtle/defined/high/very prominent>",
    "cheekbone_width_contribution": "<how much width they add>",
    "cheek_fullness": "<hollow/average/full/very full>",
    "nasolabial_depth": "<none/subtle/moderate/deep>"
  }},
  
  "lip_nodes": {{
    "L1_left_corner": "<position and angle>",
    "L2_cupids_bow_left": "<peak position>",
    "L3_cupids_bow_center": "<center dip>",
    "L4_cupids_bow_right": "<peak position>",
    "L5_right_corner": "<position and angle>",
    "L6_upper_lip_center": "<fullness at center>",
    "L7_lower_lip_center": "<fullness at center>",
    "L8_lower_lip_lowest": "<position>",
    "upper_lip_fullness": "<thin/medium/full/very full>",
    "lower_lip_fullness": "<thin/medium/full/very full>",
    "lip_ratio": "<upper to lower ratio>",
    "cupids_bow_definition": "<flat/subtle/defined/very defined>",
    "lip_width": "<narrow/average/wide>",
    "lip_color": "<natural color description>",
    "vermillion_border": "<defined/subtle>",
    "philtrum_depth": "<shallow/average/deep>",
    "philtrum_width": "<narrow/average/wide>",
    "mouth_corners": "<upturned/neutral/downturned>"
  }},
  
  "jaw_chin_nodes": {{
    "J1_left_angle": "<jaw angle position and sharpness>",
    "J2_left_body": "<jaw body curve>",
    "J3_chin_left": "<chin left side>",
    "J4_chin_center": "<chin center point>",
    "J5_chin_right": "<chin right side>",
    "J6_right_body": "<jaw body curve>",
    "J7_right_angle": "<jaw angle position and sharpness>",
    "jaw_shape": "<V-shaped/U-shaped/square/round/angular>",
    "jaw_width": "<narrow/average/wide>",
    "jaw_definition": "<soft/moderate/defined/very sharp>",
    "jaw_angle_degrees": "<estimate angle>",
    "chin_shape": "<pointed/rounded/square/cleft>",
    "chin_projection": "<recessed/average/prominent>",
    "chin_width": "<narrow/average/wide>",
    "chin_vertical_length": "<short/average/long>",
    "mental_crease": "<none/subtle/defined>"
  }},
  
  "skin_surface": {{
    "fitzpatrick": "<I/II/III/IV/V/VI>",
    "tone_hex_approximate": "<approximate hex color or RGB>",
    "tone_description": "<detailed description>",
    "undertone": "<cool pink/cool red/neutral/warm yellow/warm golden/warm olive>",
    "texture": "<smooth/normal/some texture/textured>",
    "pore_visibility": "<not visible/minimal/visible/prominent>",
    "shine_zones": "<matte/T-zone shine/all over shine>",
    "moles": ["<list moles with EXACT positions>"],
    "freckles": "<none/few/moderate/many>",
    "scars": ["<list any visible scars with positions>"],
    "hyperpigmentation": "<none/minimal/some/notable>",
    "tattoos_face_neck": ["<list any visible tattoos>"]
  }},
  
  "hair_frame": {{
    "color": "<color with highlights/lowlights>",
    "texture": "<straight/wavy/curly/coily/kinky>",
    "density": "<fine/medium/thick>",
    "length": "<length description>",
    "style": "<current style in detail>",
    "hairline_shape": "<straight/rounded/widows peak/M-shaped/receding>",
    "parting": "<left/right/center/none>",
    "hair_face_framing": "<how hair frames face - important for generation>"
  }},
  
  "piercings_jewelry": {{
    "nose": "<none or description with jewelry type>",
    "ears": "<description of piercings and jewelry>",
    "lip": "<none or description>",
    "eyebrow": "<none or description>",
    "other_face": "<any other facial piercings>"
  }},
  
  "critical_identity_lock": {{
    "unique_identifiers_ranked": [
      "1. <MOST unique feature that makes this person recognizable>",
      "2. <Second most unique>",
      "3. <Third>",
      "4. <Fourth>",
      "5. <Fifth>",
      "6. <Sixth>",
      "7. <Seventh>"
    ],
    "absolute_preservation": [
      "<list features that must NEVER change - these define identity>"
    ],
    "styling_allowed": [
      "hair color",
      "hair style",
      "makeup application",
      "expression",
      "costume/clothing"
    ],
    "never_modify": [
      "facial bone structure",
      "nose shape and proportions",
      "eye shape and spacing",
      "lip shape and proportions",
      "skin tone and undertone",
      "face shape",
      "jawline structure"
    ]
  }},
  
  "generation_instructions": {{
    "target_output": "REAL PHOTOGRAPH of a real person in cosplay costume",
    "NOT_wanted": "anime, illustration, cartoon, CGI, digital art, stylized",
    "camera_simulation": "Canon EOS R6 Mark II, RF 85mm f/1.2L @ f/2.0",
    "lighting": "Professional studio or cinematic lighting",
    "skin_rendering": "Natural skin texture, pores, imperfections - NOT smoothed",
    "realism_level": "Magazine cover quality photorealism"
  }}
}}

Extract EVERY detail. This is the most comprehensive facial map possible.
Think: if a VFX artist needed to rebuild this face in 3D, what would they need?"""

    console.print(f"[yellow]   Running V5 deep node extraction (this takes longer)...[/yellow]")
    
    with console.status("[cyan]   Mapping 100+ facial nodes...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=ANALYSIS_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=8000
            )
        )
    
    text = response.text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        profile = json.loads(text[start:end]) if start >= 0 else {"raw": text, "error": "Parse failed"}
    except Exception as e:
        profile = {"raw": text, "error": str(e)}
    
    profile["_metadata"] = {
        "created": datetime.now().isoformat(),
        "model": ANALYSIS_MODEL,
        "extraction_type": "V5_DEEP_NODES",
        "sources": image_files,
        "photo_count": len(image_files),
        "concept": "100+ landmark nodes like VFX mocap tracking"
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    char_count = len(json.dumps(profile))
    console.print(f"[green]   ✅ V5 Deep Node Map extracted ({char_count} chars)[/green]")
    console.print(f"[green]   💾 Saved to: {output_path}[/green]")
    
    return profile

async def main():
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   🎬 FACIAL IP V5 - DEEP NODE MAPPING[/bold cyan]")
    console.print("[bold cyan]   100+ anchor points like VFX mocap tracking[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/bold cyan]")
    
    input_dir = Path("c:/Yuki_Local/snow test 2")
    output_path = Path("c:/Yuki_Local/snow_v5_deep_nodes.json")
    
    profile = await extract_v5_deep_nodes(input_dir, output_path, "Snow_V5")
    
    console.print("\n[bold green]═══ V5 DEEP NODE MAP COMPLETE ═══[/bold green]")
    
    if "critical_identity_lock" in profile:
        console.print("[cyan]Unique Identifiers (Ranked):[/cyan]")
        for ident in profile.get("critical_identity_lock", {}).get("unique_identifiers_ranked", []):
            console.print(f"   • {ident}")

if __name__ == "__main__":
    asyncio.run(main())
