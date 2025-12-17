"""
⚡ FACIAL IP EXTRACTOR V4 - VFX DEEP MAP ⚡
Inspired by face projection mapping technology (photogrammetry, 3D morphology)
Uses gemini-3-pro-preview for accurate facial topology extraction

The face is treated as a 3D projection surface with:
- Bone structure planes
- Contour zones
- Light reflection areas
- Facial landmarks as anchor points
- Surface topology for digital skin mapping
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

async def extract_vfx_facial_map(input_dir: Path, output_path: Path, subject_name: str = "Subject"):
    """
    Extract deep facial topology like VFX face projection mapping.
    Think: photogrammetry, 3D morphology, digital skin overlay.
    """
    
    console.print(f"\n[bold magenta]🎬 FACIAL IP EXTRACTOR V4 - VFX DEEP MAP[/bold magenta]")
    console.print(f"[cyan]   Inspired by face projection mapping technology[/cyan]")
    console.print(f"[cyan]   Model: {ANALYSIS_MODEL}[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    # Load all photos
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    if not input_images:
        input_images = sorted(input_dir.glob("*.JPG"))[:14]
    
    console.print(f"[cyan]   Loading {len(input_images)} photos for 3D morphology analysis...[/cyan]")
    
    image_parts = []
    image_files = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        image_files.append(img.name)
    
    # VFX-inspired deep extraction prompt
    prompt = f"""You are a VFX facial topology analyst, like those who work on face projection mapping 
and photogrammetry for films. Analyze ALL {len(image_parts)} photos to create a DEEP FACIAL MAP.

Think like you're creating data for:
- Face projection mapping (projecting digital content onto a moving face)
- Photogrammetry (100 camera 3D face scan)
- Digital skin overlay for VFX
- 3D makeup application zones

⚠️ RULES:
1. ONLY describe what you can CLEARLY see across multiple photos
2. NO assumptions about dental work, medical conditions, or things not visible
3. Think in terms of 3D PLANES, ZONES, and ANCHOR POINTS

Output ONLY raw JSON (no markdown):

{{
  "subject_id": "{subject_name}",
  "vfx_confidence": "HIGH/MEDIUM/LOW",
  
  "3d_face_topology": {{
    "overall_shape": "<oval/round/square/oblong/heart/diamond/triangle>",
    "face_plane_angle": "<flat/slightly angled forward/angled back>",
    "depth_profile": "<flat/average depth/prominent features>",
    "symmetry_rating": "<highly symmetric/slight asymmetry/notable asymmetry>",
    "asymmetry_details": "<describe any asymmetries as they would affect projection>"
  }},
  
  "bone_structure_zones": {{
    "forehead_plane": {{
      "shape": "<flat/curved/sloped>",
      "prominence": "<recessed/flat/average/prominent>",
      "surface_area": "<small/medium/large>"
    }},
    "orbital_zones": {{
      "depth": "<shallow/average/deep set>",
      "brow_bone_prominence": "<minimal/moderate/prominent>",
      "under_eye_plane": "<flat/slightly hollow/hollow>"
    }},
    "cheekbone_planes": {{
      "prominence": "<flat/subtle/defined/high/very prominent>",
      "angle": "<description of cheekbone angle>",
      "width_contribution": "<how much they add to face width>"
    }},
    "nose_bridge_projection": {{
      "height": "<low/medium/high>",
      "angle_from_face": "<degrees estimate or description>",
      "tip_projection": "<minimal/average/prominent>"
    }},
    "maxilla_zone": {{
      "projection": "<recessed/flat/average/forward>",
      "nasolabial_depth": "<shallow/moderate/deep folds>"
    }},
    "mandible_zone": {{
      "jaw_angle": "<soft/moderate/sharp/very defined>",
      "width": "<narrow/average/wide>",
      "definition": "<soft/moderate/chiseled>"
    }},
    "chin_projection": {{
      "forward_projection": "<recessed/average/prominent>",
      "shape": "<pointed/rounded/square/cleft>",
      "vertical_length": "<short/average/long>"
    }}
  }},
  
  "facial_anchor_points": {{
    "description": "Key landmarks for tracking/projection alignment",
    "primary_anchors": [
      "inner eye corners (canthi)",
      "outer eye corners",
      "nose tip",
      "nostril edges",
      "lip corners",
      "chin point"
    ],
    "secondary_anchors": [
      "eyebrow peaks",
      "cheekbone high points",
      "jawline angles",
      "hairline center"
    ],
    "eye_spacing_ratio": "<close/average/wide - critical for alignment>",
    "nose_to_lip_ratio": "<short/average/long philtrum>",
    "lip_to_chin_ratio": "<short/average/long>"
  }},
  
  "surface_characteristics": {{
    "skin_type": {{
      "fitzpatrick": "<I-VI>",
      "tone": "<specific description>",
      "undertone": "<cool pink/cool red/neutral/warm yellow/warm golden/warm olive>",
      "reflectivity": "<matte/slightly dewy/dewy/oily shine zones>"
    }},
    "texture_zones": {{
      "forehead": "<smooth/some texture/textured>",
      "cheeks": "<smooth/some texture/pores visible>",
      "nose": "<smooth/pores/textured>",
      "chin": "<smooth/textured>"
    }},
    "shadow_catch_areas": [
      "<list areas that naturally catch shadow - important for projection>"
    ],
    "highlight_areas": [
      "<list areas that catch light - nose bridge, cheekbones, etc>"
    ]
  }},
  
  "feature_details": {{
    "eyes": {{
      "shape": "<almond/round/hooded/monolid/deep-set/downturned/upturned>",
      "size_relative": "<small/medium/large>",
      "color": "<specific>",
      "lid_visible": "<yes/hooded/partial>",
      "lash_prominence": "<sparse/average/thick>"
    }},
    "eyebrows": {{
      "shape": "<straight/soft arch/high arch>",
      "thickness": "<thin/medium/thick>",
      "color": "<color>",
      "grooming": "<natural/shaped>"
    }},
    "nose": {{
      "bridge_profile": "<straight/curved/bumped/flat>",
      "tip_type": "<pointed/rounded/bulbous/upturned>",
      "width": "<narrow/medium/wide>",
      "nostril_visibility": "<minimal/moderate/flared>",
      "piercings": "<none/location if visible>"
    }},
    "lips": {{
      "fullness": "<thin/medium/full/very full>",
      "shape": "<description>",
      "cupids_bow": "<flat/subtle/defined>",
      "color": "<natural color>"
    }},
    "jaw_chin": {{
      "jawline_definition": "<soft/moderate/defined/sharp>",
      "chin_shape": "<pointed/rounded/square>",
      "profile_angle": "<description>"
    }}
  }},
  
  "hair_framing": {{
    "texture": "<straight/wavy/curly/coily/kinky>",
    "density": "<fine/medium/thick>",
    "color": "<color description>",
    "length": "<length>",
    "style": "<current style>",
    "face_framing": "<how hair frames face - important for projection boundaries>",
    "hairline_shape": "<straight/rounded/widows peak/M-shaped>",
    "parting": "<left/right/center/none>"
  }},
  
  "piercings_and_marks": {{
    "facial_piercings": ["<list any visible piercings with exact locations>"],
    "ear_piercings": ["<list ear piercings>"],
    "notable_marks": ["<moles, scars, birthmarks with locations>"],
    "tattoos_visible": ["<any visible tattoos near face/neck>"]
  }},
  
  "expression_baseline": {{
    "resting_expression": "<neutral/slight smile/serious>",
    "eye_expression": "<alert/relaxed/intense>",
    "muscle_tension_areas": "<where face holds tension>"
  }},
  
  "projection_mapping_zones": {{
    "forehead_zone": "Zone 1 - largest flat surface for projection",
    "eye_mask_zone": "Zone 2 - orbital area, requires careful tracking",
    "cheek_zones": "Zone 3L/3R - angled surfaces, catch highlights",
    "nose_zone": "Zone 4 - central ridge, defines depth",
    "mouth_zone": "Zone 5 - mobile, requires expression tracking",
    "jaw_zones": "Zone 6L/6R - lower face framing",
    "chin_zone": "Zone 7 - forward projection point"
  }},
  
  "identity_lock_critical": {{
    "top_5_unique_identifiers": [
      "1. <most unique feature>",
      "2. <second most unique>",
      "3. <third>",
      "4. <fourth>",
      "5. <fifth>"
    ],
    "MUST_PRESERVE": [
      "<list features that define this person's identity>"
    ],
    "CAN_STYLE": [
      "hair color/style",
      "makeup",
      "expression",
      "accessories"
    ],
    "NEVER_MODIFY": [
      "bone structure",
      "facial proportions",
      "skin tone",
      "eye shape and spacing"
    ]
  }}
}}

Analyze like you're building a 3D face model for VFX projection. Be precise about planes, zones, and spatial relationships."""

    console.print(f"[yellow]   Running VFX-grade facial topology analysis...[/yellow]")
    
    with console.status("[cyan]   Deep 3D morphology extraction in progress...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=ANALYSIS_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=6000
            )
        )
    
    text = response.text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        profile = json.loads(text[start:end]) if start >= 0 else {"raw": text, "error": "Failed to parse"}
    except Exception as e:
        profile = {"raw": text, "error": str(e)}
    
    profile["_metadata"] = {
        "created": datetime.now().isoformat(),
        "model": ANALYSIS_MODEL,
        "extraction_type": "VFX_DEEP_MAP_V4",
        "sources": image_files,
        "photo_count": len(image_files),
        "inspiration": "Face projection mapping, photogrammetry, 3D morphology"
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    char_count = len(json.dumps(profile))
    console.print(f"[green]   ✅ VFX Deep Map extracted ({char_count} chars)[/green]")
    console.print(f"[green]   💾 Saved to: {output_path}[/green]")
    
    return profile

async def main():
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   🎬 FACIAL IP V4 - VFX DEEP MAP EXTRACTION[/bold cyan]")
    console.print("[bold cyan]   Inspired by face projection mapping & photogrammetry[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/bold cyan]")
    
    input_dir = Path("c:/Yuki_Local/snow test 2")
    output_path = Path("c:/Yuki_Local/snow_v4_vfx_facial_map.json")
    
    profile = await extract_vfx_facial_map(input_dir, output_path, "Snow_VFX")
    
    console.print("\n[bold green]═══ VFX DEEP MAP COMPLETE ═══[/bold green]")
    
    if "identity_lock_critical" in profile:
        console.print("[cyan]Top 5 Unique Identifiers:[/cyan]")
        for ident in profile.get("identity_lock_critical", {}).get("top_5_unique_identifiers", []):
            console.print(f"   • {ident}")
    
    if "projection_mapping_zones" in profile:
        console.print("\n[cyan]Projection Zones Mapped:[/cyan]")
        for zone, desc in profile.get("projection_mapping_zones", {}).items():
            console.print(f"   • {zone}: {desc[:50]}...")

if __name__ == "__main__":
    asyncio.run(main())
