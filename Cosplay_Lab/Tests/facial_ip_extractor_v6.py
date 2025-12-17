"""
⚡ FACIAL IP EXTRACTOR V6 - 15+ MEASUREMENT ZONES ⚡
Ultra-comprehensive facial topology with quantifiable measurements
Inspired by forensic facial analysis and VFX mocap

15+ ZONES:
1. Ears - shape, size, attachment, lobe
2. Eyes - shape, size, spacing, color, lid, cant, lashes
3. Mouth - width, corners, lip line
4. Nose - bridge, tip, width, depth, nostrils
5. Eyebrows - arch, thickness, spacing
6. Cheeks - prominence, hollowness
7. Dimples - presence, location
8. Chin - shape, projection, cleft
9. Ear-to-nose distance ratio
10. Lip measurements - upper/lower ratio, width
11. Hairline - shape, height
12. Inter-feature distances
13. Face angles/perspectives
14. Jaw definition
15. Forehead proportions
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

async def extract_v6_full_zones(input_dir: Path, output_path: Path, subject_name: str = "Subject"):
    """V6 extraction with 15+ measurement zones"""
    
    console.print(f"\n[bold magenta]📐 FACIAL IP V6 - 15+ MEASUREMENT ZONES[/bold magenta]")
    console.print(f"[cyan]   Ultra-comprehensive facial topology[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    if not input_images:
        input_images = sorted(input_dir.glob("*.JPG"))[:14]
    
    console.print(f"[cyan]   Loading {len(input_images)} photos...[/cyan]")
    
    image_parts = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
    
    prompt = f"""You are a forensic facial analyst. Analyze ALL {len(image_parts)} photos.
Create ultra-detailed measurements across 15+ facial zones.

If photos have MULTIPLE PEOPLE, identify and analyze ONLY the PRIMARY SUBJECT (most common face).

⚠️ RULES:
- ONLY describe what you CLEARLY see
- Estimate ratios and proportions where possible
- No assumptions about things not visible

Output ONLY raw JSON:

{{
  "subject_id": "{subject_name}",
  "primary_subject": {{
    "appears_in": "<X of {len(image_parts)} photos>",
    "confidence": "HIGH/MEDIUM/LOW"
  }},
  
  "zone_1_ears": {{
    "shape": "<round/oval/rectangular/pointed/square>",
    "size": "<small/medium/large relative to face>",
    "attachment": "<attached/detached lobes>",
    "lobe_type": "<free/attached/absent>",
    "protrusion": "<flat/moderate/prominent>",
    "piercings": ["<list all ear piercings>"]
  }},
  
  "zone_2_eyes": {{
    "shape": "<almond/round/hooded/monolid/deep-set/downturned/upturned/wide-set/close-set>",
    "size": "<small/medium/large>",
    "color_iris": "<specific color with patterns>",
    "color_sclera": "<white/slightly off-white/yellow tinge>",
    "spacing_intercanthal": "<narrow/average/wide - describe in eye-width units>",
    "lid_type": "<single/double/hooded/epicanthic fold>",
    "lid_exposure": "<minimal/moderate/full crease visible>",
    "eye_cant": "<positive (upturned)/neutral/negative (downturned)>",
    "lash_density": "<sparse/average/thick>",
    "lash_length": "<short/medium/long>",
    "under_eye": "<smooth/slight shadow/dark circles/puffiness>",
    "brow_to_eye_distance": "<close/average/high>"
  }},
  
  "zone_3_mouth": {{
    "width": "<narrow/average/wide relative to nose>",
    "corner_angle": "<upturned/neutral/downturned>",
    "lip_line_shape": "<straight/curved up/curved down>",
    "commissures": "<defined/soft/indistinct>",
    "teeth_visible_at_rest": "<yes/no>"
  }},
  
  "zone_4_nose": {{
    "overall_size": "<small/medium/large>",
    "bridge_height": "<low/medium/high>",
    "bridge_width_top": "<narrow/medium/wide>",
    "bridge_width_bottom": "<narrow/medium/wide>",
    "bridge_shape_profile": "<straight/convex (roman)/concave/wavy/bumped>",
    "tip_shape": "<pointed/rounded/bulbous/bifid>",
    "tip_angle": "<upturned/straight/downturned>",
    "tip_width": "<narrow/medium/wide>",
    "tip_projection": "<short/average/prominent>",
    "nostril_shape": "<round/oval/slit/flared>",
    "nostril_size": "<small/medium/large>",
    "nostril_visibility_front": "<not visible/partial/clearly visible>",
    "columella_show": "<hidden/average/hanging>",
    "nasal_base_width": "<narrow/medium/wide - compare to intercanthal>",
    "piercings": "<none/septum/nostril L/nostril R with jewelry>"
  }},
  
  "zone_5_eyebrows": {{
    "arch_type": "<flat/soft arch/high arch/rounded/angular/S-shaped>",
    "arch_position": "<inner third/middle/outer third>",
    "thickness_inner": "<thin/medium/thick>",
    "thickness_middle": "<thin/medium/thick>",
    "thickness_outer": "<thin/medium/thick (taper)>",
    "length": "<short/medium/long>",
    "color": "<color>",
    "density": "<sparse/average/thick/bushy>",
    "grooming": "<natural/shaped/filled>",
    "spacing_glabella": "<close/average/wide apart>",
    "height_above_eye": "<close/average/high>"
  }},
  
  "zone_6_cheeks": {{
    "cheekbone_prominence": "<flat/subtle/moderate/high/very prominent>",
    "cheekbone_width": "<narrow/average/wide - face width contribution>",
    "cheekbone_position": "<low/middle/high on face>",
    "cheek_volume": "<hollow/flat/average/full/round>",
    "dimples_when_smiling": "<none/subtle/prominent>",
    "buccal_fat": "<minimal/average/full>",
    "nasolabial_fold_depth": "<none/subtle/moderate/deep>"
  }},
  
  "zone_7_dimples": {{
    "cheek_dimples": "<none/single left/single right/both>",
    "cheek_dimple_depth": "<shallow/moderate/deep>",
    "chin_dimple": "<none/subtle/prominent cleft>",
    "back_dimples": "<not visible/visible in photos>"
  }},
  
  "zone_8_chin": {{
    "shape_front": "<pointed/rounded/square/heart>",
    "shape_profile": "<receding/neutral/prominent/jutting>",
    "width": "<narrow/average/wide>",
    "vertical_height": "<short/average/long>",
    "cleft": "<none/subtle/prominent>",
    "mental_crease": "<none/subtle/defined>",
    "texture": "<smooth/dimpled when tensed>"
  }},
  
  "zone_9_ear_nose_ratio": {{
    "ear_length_estimate": "<small/medium/large>",
    "nose_length_estimate": "<small/medium/large>",
    "ratio_comparison": "<ears longer/equal/nose longer>",
    "ear_top_alignment": "<above/at/below eyebrow level>",
    "ear_bottom_alignment": "<above/at/below nose tip>"
  }},
  
  "zone_10_lips": {{
    "upper_lip_fullness": "<very thin/thin/medium/full/very full>",
    "lower_lip_fullness": "<very thin/thin/medium/full/very full>",
    "upper_to_lower_ratio": "<top heavier/equal/bottom heavier - estimate ratio>",
    "lip_width": "<narrow/average/wide>",
    "cupids_bow": "<flat/subtle/defined/very defined/heart-shaped>",
    "philtrum_width": "<narrow/average/wide>",
    "philtrum_depth": "<flat/shallow/moderate/deep>",
    "vermillion_border": "<indistinct/subtle/defined/very defined>",
    "lip_color": "<describe natural color>",
    "lip_texture": "<smooth/lines visible>"
  }},
  
  "zone_11_hairline": {{
    "shape": "<straight/rounded/M-shaped/widows peak/receding>",
    "height": "<low/average/high forehead>",
    "temporal_recession": "<none/slight/moderate/significant>",
    "baby_hairs": "<none/some/prominent>",
    "cowlicks": "<none/one/multiple with locations>"
  }},
  
  "zone_12_inter_feature_distances": {{
    "eye_to_eye_inner": "<1 eye width/less/more - intercanthal>",
    "eye_to_eye_outer": "<describe biocular width>",
    "nose_width_to_eye_spacing": "<narrower/equal/wider than intercanthal>",
    "nose_to_upper_lip": "<short/average/long philtrum>",
    "upper_lip_to_lower_lip_center": "<describe>",
    "lower_lip_to_chin": "<short/average/long>",
    "thirds_proportion": "<equal/forehead dominant/middle dominant/lower dominant>",
    "facial_index": "<wide face/oval/narrow face>"
  }},
  
  "zone_13_face_angles": {{
    "front_view_symmetry": "<highly symmetric/slight asymmetry/notable asymmetry>",
    "asymmetry_details": "<describe which side is different>",
    "profile_angle_forehead": "<sloped back/vertical/slightly forward>",
    "profile_angle_nose": "<describe projection>",
    "profile_angle_lips": "<recessed/in line/protrusive>",
    "profile_angle_chin": "<recessed/in line/prominent>",
    "facial_convexity": "<concave/straight/convex profile>"
  }},
  
  "zone_14_jaw": {{
    "jaw_shape": "<V-shaped/U-shaped/square/round/angular/heart>",
    "jaw_width": "<narrow/average/wide>",
    "jaw_angle_sharpness": "<soft/moderate/defined/very sharp>",
    "jaw_angle_position": "<high/average/low on face>",
    "mandible_definition": "<soft/visible/chiseled>",
    "jowls": "<none/minimal/visible>"
  }},
  
  "zone_15_forehead": {{
    "height": "<low/average/high>",
    "width": "<narrow/average/wide>",
    "shape": "<flat/slightly curved/rounded/sloped back>",
    "brow_bone_prominence": "<flat/subtle/moderate/prominent>",
    "forehead_to_face_ratio": "<small/average/dominant>",
    "texture": "<smooth/lines visible>",
    "veins_visible": "<no/subtle/visible>"
  }},
  
  "zone_16_skin_surface": {{
    "fitzpatrick_scale": "<I/II/III/IV/V/VI>",
    "tone_description": "<detailed color description>",
    "undertone": "<cool pink/cool red/neutral/warm yellow/warm golden/warm olive>",
    "texture": "<poreless-smooth/smooth/normal/visible pores/textured>",
    "moles": ["<list with exact face locations>"],
    "freckles": "<none/few/moderate/many with distribution>",
    "scars": ["<list with locations>"],
    "birthmarks": ["<list>"],
    "tattoos_face_neck": ["<list with exact positions and descriptions>"]
  }},
  
  "zone_17_hair": {{
    "color": "<color with highlights/roots if applicable>",
    "texture": "<straight/wavy/curly/coily/kinky>",
    "density": "<fine/medium/thick>",
    "length": "<description>",
    "current_style": "<detailed style description>",
    "parting": "<left/center/right/none>",
    "volume": "<flat/average/voluminous>"
  }},
  
  "critical_identity_lock": {{
    "top_7_unique_identifiers": [
      "1. <MOST unique/identifying feature>",
      "2. <second>",
      "3. <third>",
      "4. <fourth>",
      "5. <fifth>",
      "6. <sixth>",
      "7. <seventh>"
    ],
    "absolute_must_preserve": [
      "<critical identity features>"
    ],
    "can_modify_for_cosplay": [
      "hair color/style",
      "makeup",
      "expression",
      "costume"
    ],
    "never_change": [
      "bone structure",
      "skin tone",
      "facial proportions",
      "eye shape/spacing",
      "nose structure",
      "lip proportions"
    ]
  }}
}}

Analyze like a forensic artist building a reconstruction. Be as specific as possible."""

    console.print(f"[yellow]   Running V6 15+ zone extraction...[/yellow]")
    
    with console.status("[cyan]   Mapping 17 facial zones...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=8000)
        )
    
    text = response.text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        profile = json.loads(text[start:end])
    except Exception as e:
        profile = {"raw": text, "error": str(e)}
    
    profile["_metadata"] = {
        "created": datetime.now().isoformat(),
        "model": MODEL,
        "extraction_type": "V6_15_PLUS_ZONES",
        "zones_count": 17,
        "photo_count": len(input_images)
    }
    
    with open(output_path, "w") as f:
        json.dump(profile, f, indent=2)
    
    char_count = len(json.dumps(profile))
    console.print(f"[green]   ✅ V6 Map: {char_count} chars (17 zones)[/green]")
    console.print(f"[green]   💾 Saved: {output_path}[/green]")
    
    # Print zone summary
    zones_found = sum(1 for k in profile.keys() if k.startswith("zone_"))
    console.print(f"\n[cyan]Zones Mapped: {zones_found}/17[/cyan]")
    
    if "critical_identity_lock" in profile:
        console.print(f"\n[cyan]Top Identifiers:[/cyan]")
        for ident in profile.get("critical_identity_lock", {}).get("top_7_unique_identifiers", [])[:5]:
            console.print(f"   • {ident}")
    
    return profile

async def main():
    console.print("[bold cyan]═══ FACIAL IP V6 - 15+ MEASUREMENT ZONES ═══[/bold cyan]")
    
    # Run on Jordan photos
    input_dir = Path("c:/Yuki_Local/jordan test")
    output_path = Path("c:/Yuki_Local/jordan_test_results/jordan_v6_full_zones.json")
    
    await extract_v6_full_zones(input_dir, output_path, "Jordan_V6")
    console.print("\n[bold green]✨ V6 EXTRACTION COMPLETE![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
