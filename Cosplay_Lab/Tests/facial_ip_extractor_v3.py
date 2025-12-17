"""
⚡ FACIAL IP EXTRACTOR V3 ⚡
Uses gemini-3-pro-preview for accurate facial analysis (less hallucination)
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
ANALYSIS_MODEL = "gemini-3-pro-preview"  # Better vision accuracy!

async def extract_facial_ip(input_dir: Path, output_path: Path, subject_name: str = "Subject"):
    """Extract facial IP using Gemini 3 Pro Preview for accuracy"""
    
    console.print(f"\n[bold magenta]🔬 FACIAL IP EXTRACTION V3[/bold magenta]")
    console.print(f"[cyan]   Using: {ANALYSIS_MODEL} (better vision accuracy)[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    # Load all photos
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    if not input_images:
        input_images = sorted(input_dir.glob("*.JPG"))[:14]
    
    console.print(f"[cyan]   Loading {len(input_images)} photos...[/cyan]")
    
    image_parts = []
    image_files = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        image_files.append(img.name)
    
    # Extraction prompt with anti-hallucination instructions
    prompt = f"""You are a forensic facial analyst. Analyze ALL {len(image_parts)} photos.

⚠️ CRITICAL RULES:
1. ONLY describe what you can CLEARLY and DEFINITIVELY see
2. Do NOT infer, assume, or guess about:
   - Dental work (braces, retainers, veneers, dental implants)
   - Medical conditions or modifications
   - Features you cannot clearly verify across multiple photos
3. If uncertain, write "unclear" or omit the detail
4. Cross-reference features across ALL photos before including

Output ONLY raw JSON (no markdown, no backticks):

{{
  "subject_id": "{subject_name}",
  "extraction_confidence": "HIGH/MEDIUM/LOW",
  
  "face_structure": {{
    "shape": "<oval/round/square/oblong/heart/diamond>",
    "length": "<short/average/long>",
    "width": "<narrow/average/wide>",
    "symmetry": "<symmetrical/slight asymmetry/notable asymmetry>",
    "jawline": "<soft/moderate/angular/strong>",
    "chin": "<pointed/rounded/square/receding/prominent>"
  }},
  
  "forehead": {{
    "height": "<low/medium/high>",
    "width": "<narrow/average/wide>",
    "hairline": "<straight/rounded/widows peak/M-shaped/receding>"
  }},
  
  "eyes": {{
    "shape": "<almond/round/hooded/monolid/deep-set/downturned/upturned>",
    "size": "<small/medium/large>",
    "color": "<specific color>",
    "spacing": "<close-set/average/wide-set>",
    "characteristics": "<any notable features>"
  }},
  
  "eyebrows": {{
    "shape": "<straight/arched/S-curved>",
    "thickness": "<thin/medium/thick>",
    "color": "<color>"
  }},
  
  "nose": {{
    "size": "<small/medium/large>",
    "bridge": "<straight/curved/bumped/flat>",
    "tip": "<pointed/rounded/bulbous/upturned>",
    "width": "<narrow/medium/wide>",
    "nostrils": "<small/medium/large/flared>",
    "piercings": "<none/septum/nostril left/nostril right - ONLY if clearly visible>"
  }},
  
  "lips": {{
    "fullness": "<thin/medium/full/very full>",
    "upper_lip": "<description>",
    "lower_lip": "<description>",
    "cupids_bow": "<flat/subtle/defined/very defined>",
    "width": "<narrow/average/wide>"
  }},
  
  "teeth": {{
    "visibility_when_smiling": "<not visible/slightly/clearly visible>",
    "characteristics": "<natural/straight/gap/other - ONLY what is clearly visible, NO assumptions about dental work>"
  }},
  
  "cheeks": {{
    "cheekbones": "<flat/subtle/defined/prominent>",
    "fullness": "<hollow/average/full>"
  }},
  
  "skin": {{
    "fitzpatrick": "<I/II/III/IV/V/VI>",
    "tone": "<very fair/fair/light/medium/tan/brown/dark brown/deep>",
    "undertone": "<cool/neutral/warm>",
    "texture": "<smooth/some texture/textured>",
    "notable_marks": "<moles/scars/birthmarks with locations - ONLY if clearly visible>"
  }},
  
  "hair": {{
    "color": "<color>",
    "texture": "<straight/wavy/curly/coily/kinky>",
    "length": "<short/medium/long/very long>",
    "style": "<current style description>",
    "thickness": "<fine/medium/thick>"
  }},
  
  "ears": {{
    "size": "<small/medium/large>",
    "piercings": "<none/lobes/cartilage/multiple - describe what is clearly visible>"
  }},
  
  "distinctive_features": [
    "<list 3-5 features that make this person instantly recognizable>",
    "<ONLY include features you are 100% certain about>"
  ],
  
  "identity_lock_priorities": [
    "1. <most critical feature to preserve>",
    "2. <second most critical>",
    "3. <third>",
    "4. <fourth>",
    "5. <fifth>"
  ],
  
  "generation_rules": {{
    "MUST_PRESERVE": [
      "<list features that must stay identical>"
    ],
    "CAN_MODIFY": [
      "<hair color/style>",
      "<makeup>",
      "<expression>"
    ],
    "NEVER_CHANGE": [
      "<bone structure>",
      "<skin tone>",
      "<facial proportions>"
    ]
  }}
}}

Analyze ALL photos carefully. Be ACCURATE, not creative."""

    console.print(f"[yellow]   Analyzing with {ANALYSIS_MODEL} (this may take 30-60s)...[/yellow]")
    
    with console.status("[cyan]   Deep facial analysis in progress...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=ANALYSIS_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                temperature=0.1,  # Very low for accuracy
                max_output_tokens=4000
            )
        )
    
    text = response.text.strip()
    
    # Clean up response
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        profile = json.loads(text[start:end]) if start >= 0 else {"raw": text, "error": "Failed to parse JSON"}
    except Exception as e:
        profile = {"raw": text, "error": str(e)}
    
    # Add metadata
    profile["_metadata"] = {
        "created": datetime.now().isoformat(),
        "model": ANALYSIS_MODEL,
        "sources": image_files,
        "version": "3.0-GEMINI3PRO",
        "photo_count": len(image_files)
    }
    
    # Save
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    char_count = len(json.dumps(profile))
    console.print(f"[green]   ✅ Facial IP extracted ({char_count} chars)[/green]")
    console.print(f"[green]   💾 Saved to: {output_path}[/green]")
    
    return profile

async def main():
    # Extract for Snow Test 2
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   FACIAL IP EXTRACTOR V3 - Using Gemini 3 Pro Preview[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/bold cyan]")
    
    input_dir = Path("c:/Yuki_Local/snow test 2")
    output_path = Path("c:/Yuki_Local/snow_test2_enhanced_results/snow2_v3_facial_ip.json")
    
    profile = await extract_facial_ip(input_dir, output_path, "Snow2")
    
    # Print summary
    console.print("\n[bold green]═══ EXTRACTION COMPLETE ═══[/bold green]")
    if "distinctive_features" in profile:
        console.print("[cyan]Distinctive Features:[/cyan]")
        for feat in profile.get("distinctive_features", []):
            console.print(f"   • {feat}")

if __name__ == "__main__":
    asyncio.run(main())
