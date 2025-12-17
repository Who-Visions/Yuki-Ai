"""
⚡ FACIAL IP EXTRACTOR V7 - NECK & JAW SPECIALIST ⚡
V6 Zones + Zone 18 (Neck/Jaw) + Quantified Math
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
MODEL = "gemini-3-pro-preview"

async def extract_v7_complete(input_dir: Path, output_path: Path, subject_name: str):
    console.print(f"\n[bold magenta]📐 FACIAL IP V7 - NECK & JAW ARCHITECTURE[/bold magenta]")
    console.print(f"[cyan]   Subject: {subject_name} | Sources: {input_dir.name}[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    
    input_images = sorted(input_dir.glob("*.jpg"))[:10] # Top 10 clarity
    if not input_images: 
        input_images = sorted(input_dir.glob("*.JPG"))[:10]
        
    prompt = f"""You are a forensic facial analyst. Analyze {len(input_images)} photos of the PRIMARY SUBJECT.
Create ultra-detailed measurements across 18 zones, placing special emphasis on the NECK and JAWLINE architecture for portrait accuracy.

OUTPUT RAW JSON ONLY.

{{
  "subject_id": "{subject_name}",
  
  "zone_1_ears": {{ "shape": "...", "attachment": "...", "size": "..." }},
  "zone_2_eyes": {{ "shape": "...", "cant": "...", "spacing": "...", "lid_type": "..." }},
  "zone_3_mouth": {{ "width": "...", "corner_angle": "...", "lip_line": "..." }},
  "zone_4_nose": {{ "bridge_shape": "...", "tip_shape": "...", "nostril_shape": "..." }},
  "zone_5_eyebrows": {{ "arch_type": "...", "thickness": "...", "spacing": "..." }},
  "zone_6_cheeks": {{ "prominence": "...", "volume": "..." }},
  "zone_7_dimples": {{ "cheek": "...", "chin_cleft": "..." }},
  "zone_8_chin": {{ "shape": "...", "projection": "...", "width": "..." }},
  
  "zone_9_ear_nose_ratio": {{ "vertical_alignment": "..." }},
  
  "zone_10_lips": {{ 
    "upper_fullness": "...", "lower_fullness": "...", 
    "cupids_bow": "...", "philtrum_depth": "..." 
  }},
  
  "zone_11_hairline": {{ "shape": "...", "temporal_recession": "..." }},
  
  "zone_12_inter_feature_distances": {{ 
    "eye_to_eye": "...", "nose_width_to_eye_spacing": "...", "nose_to_lip": "..." 
  }},
  
  "zone_13_face_angles": {{ "profile_convexity": "...", "jaw_angle": "..." }},
  
  "zone_14_jaw_definition": {{ 
    "shape": "...", "width": "...", 
    "angle_sharpness": "...", "mandible_visibility": "..." 
  }},
  
  "zone_15_forehead": {{ "height": "...", "width": "...", "slope": "..." }},
  
  "zone_16_skin_surface": {{ 
    "tone": "...", "texture": "...", 
    "moles": ["list locations"], "tattoos": ["list locations"] 
  }},

  "zone_17_hair_texture": {{ "type": "...", "color": "..." }},

  "zone_18_neck_jaw_architecture": {{
    "jaw_to_neck_transition": "<sharp/soft/defined/fleshy>",
    "submental_region": "<taut/soft/full/double>",
    "neck_width_ratio": "<narrow/equal/wide relative to face>",
    "neck_length_appearance": "<short/average/long/swan-like>",
    "adam_apple_visibility": "<none/subtle/prominent>",
    "sternocleidomastoid_definition": "<hidden/subtle/defined/prominent>",
    "trapezius_slope": "<square/sloped/steep>",
    "skin_texture_neck": "<smooth/bands/lines>"
  }},

  "critical_identity_lock": {{
    "top_identifiers": ["list top 5"],
    "must_preserve": ["list"]
  }}
}}"""

    with console.status(f"[cyan]   Mapping {subject_name} V7 Topology...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=MODEL, contents=[prompt] + [types.Part.from_bytes(data=open(i,"rb").read(), mime_type="image/jpeg") for i in input_images],
            config=types.GenerateContentConfig(temperature=0.0)
        )
        
    text = re.sub(r'```json\s*|\s*```', '', response.text.strip())
    extracted = json.loads(text[text.find('{'):text.rfind('}')+1])
    
    with open(output_path, "w") as f: json.dump(extracted, f, indent=2)
    console.print(f"[green]   ✅ Saved V7 Map: {output_path.name}[/green]")
    return extracted

if __name__ == "__main__":
    pass
