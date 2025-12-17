"""
⚡ JORDAN TEST - PRIMARY SUBJECT DETECTION ⚡
Challenge: Multiple people in photos - can Yuki identify the PRIMARY subject?

This tests the model's ability to:
1. Identify the MOST FREQUENTLY appearing face across photos
2. Filter out background people / other subjects
3. Lock onto the main subject's facial IP
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich import box
import subprocess
import time
import json
import re

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
ANALYSIS_MODEL = "gemini-3-pro-preview"
IMAGE_MODEL = "gemini-3-pro-image-preview"
BUFFER_SECONDS = 90

async def extract_primary_subject(client, input_dir: Path, output_path: Path):
    """
    Extract facial IP for the PRIMARY subject - the person appearing most often.
    Challenge: Photos may have multiple people in them.
    """
    
    console.print(f"\n[bold magenta]🎯 PRIMARY SUBJECT DETECTION TEST[/bold magenta]")
    console.print(f"[cyan]   Challenge: Multiple people in photos[/cyan]")
    console.print(f"[cyan]   Model must identify the MOST COMMON face[/cyan]")
    
    input_images = sorted(input_dir.glob("*.jpg"))
    if not input_images:
        input_images = sorted(input_dir.glob("*.JPG"))
    
    console.print(f"[cyan]   Loading {len(input_images)} photos...[/cyan]")
    
    image_parts = []
    image_files = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        image_files.append(img.name)
        console.print(f"   ✓ {img.name}")
    
    # CRITICAL: Primary Subject Detection Prompt
    prompt = f"""You are analyzing {len(image_parts)} photos to identify the PRIMARY SUBJECT.

⚠️ CRITICAL CHALLENGE: Some photos may have MULTIPLE PEOPLE in them.
Your job is to identify the SINGLE person who appears MOST FREQUENTLY across all photos.

STEP 1 - FACE COUNT ANALYSIS:
For each photo, list:
- How many faces are visible
- Brief description of each face (gender, apparent age, distinctive features)

STEP 2 - PRIMARY SUBJECT IDENTIFICATION:
Analyze which face appears MOST OFTEN across all photos.
This is your PRIMARY SUBJECT. Everyone else is background/secondary.

STEP 3 - FACIAL IP EXTRACTION (for PRIMARY SUBJECT only):
Create a facial profile for ONLY the most common face.

Output ONLY raw JSON (no markdown):

{{
  "analysis": {{
    "total_photos": {len(image_parts)},
    "photos_with_multiple_people": "<count>",
    "primary_subject_appears_in": "<count> of {len(image_parts)} photos",
    "confidence": "HIGH/MEDIUM/LOW"
  }},
  
  "primary_subject_identification": {{
    "description": "<brief description of who the primary subject is>",
    "gender": "<male/female>",
    "apparent_age": "<age range>",
    "distinctive_markers": ["<list 3-5 features that identify this specific person>"]
  }},
  
  "face_calibration": {{
    "overall_shape": "<oval/round/square/oblong/heart/diamond/triangle>",
    "face_width": "<narrow/average/wide>",
    "face_length": "<short/average/long>"
  }},
  
  "eye_nodes": {{
    "shape": "<almond/round/hooded/monolid/deep-set/upturned/downturned>",
    "size": "<small/medium/large>",
    "color": "<specific color>",
    "spacing": "<close-set/average/wide-set>"
  }},
  
  "nose_nodes": {{
    "bridge": "<straight/curved/bumped/flat>",
    "tip": "<pointed/rounded/bulbous/upturned>",
    "width": "<narrow/medium/wide>",
    "piercings": "<none/septum/nostril with description>"
  }},
  
  "lip_nodes": {{
    "fullness_upper": "<thin/medium/full>",
    "fullness_lower": "<thin/medium/full>",
    "cupids_bow": "<flat/subtle/defined>",
    "width": "<narrow/average/wide>"
  }},
  
  "jaw_chin": {{
    "jaw_shape": "<V-shaped/U-shaped/square/round/angular>",
    "chin_shape": "<pointed/rounded/square>"
  }},
  
  "skin": {{
    "fitzpatrick": "<I/II/III/IV/V/VI>",
    "tone": "<detailed description>",
    "undertone": "<cool/neutral/warm>"
  }},
  
  "hair": {{
    "color": "<color>",
    "texture": "<straight/wavy/curly/coily/kinky>",
    "length": "<short/medium/long>",
    "style": "<current style>"
  }},
  
  "facial_hair": {{
    "type": "<none/stubble/goatee/beard/mustache>",
    "coverage": "<description if applicable>"
  }},
  
  "critical_identity_lock": {{
    "unique_identifiers": [
      "1. <most unique feature>",
      "2. <second>",
      "3. <third>",
      "4. <fourth>",
      "5. <fifth>"
    ],
    "must_preserve": ["<list features that define identity>"],
    "never_modify": ["bone structure", "skin tone", "facial proportions"]
  }},
  
  "secondary_subjects_found": [
    "<list any other people found in photos - just brief descriptions>"
  ]
}}

CRITICAL: Focus ONLY on the PRIMARY SUBJECT (most common face).
Ignore background people, secondary subjects, or people who only appear once."""

    console.print(f"[yellow]   Analyzing photos for PRIMARY subject...[/yellow]")
    
    with console.status("[cyan]   Detecting most common face across all photos...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=ANALYSIS_MODEL,
            contents=[prompt] + image_parts,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=4000
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
        "test_type": "PRIMARY_SUBJECT_DETECTION",
        "sources": image_files,
        "photo_count": len(image_files)
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    console.print(f"[green]   ✅ Primary Subject IP extracted[/green]")
    console.print(f"[green]   💾 Saved to: {output_path}[/green]")
    
    # Print analysis results
    if "analysis" in profile:
        analysis = profile["analysis"]
        console.print(f"\n[cyan]📊 ANALYSIS RESULTS:[/cyan]")
        console.print(f"   Total photos: {analysis.get('total_photos', 'N/A')}")
        console.print(f"   Photos with multiple people: {analysis.get('photos_with_multiple_people', 'N/A')}")
        console.print(f"   Primary subject in: {analysis.get('primary_subject_appears_in', 'N/A')}")
        console.print(f"   Confidence: {analysis.get('confidence', 'N/A')}")
    
    if "primary_subject_identification" in profile:
        subj = profile["primary_subject_identification"]
        console.print(f"\n[cyan]👤 PRIMARY SUBJECT:[/cyan]")
        console.print(f"   {subj.get('description', 'N/A')}")
        console.print(f"   Gender: {subj.get('gender', 'N/A')}")
        console.print(f"   Age: {subj.get('apparent_age', 'N/A')}")
    
    if "secondary_subjects_found" in profile:
        secondary = profile["secondary_subjects_found"]
        if secondary:
            console.print(f"\n[yellow]👥 SECONDARY SUBJECTS (ignored):[/yellow]")
            for s in secondary[:3]:
                console.print(f"   - {s}")
    
    return profile

def get_lite_map(full_map: dict) -> str:
    """Extract essential nodes for V5-Lite generation"""
    lite = {
        "face_calibration": full_map.get("face_calibration", {}),
        "eye_nodes": full_map.get("eye_nodes", {}),
        "nose_nodes": full_map.get("nose_nodes", {}),
        "lip_nodes": full_map.get("lip_nodes", {}),
        "jaw_chin": full_map.get("jaw_chin", {}),
        "skin": full_map.get("skin", {}),
        "facial_hair": full_map.get("facial_hair", {}),
        "critical_identity_lock": full_map.get("critical_identity_lock", {})
    }
    return json.dumps(lite, indent=2)

async def generate_test(client, lite_map: str, photo, output_dir: Path):
    """Generate 3 test characters to verify primary subject detection"""
    
    characters = [
        {"name": "Spike_Spiegel", "show": "Cowboy Bebop", "desc": "Tall figure, navy blue suit, yellow shirt, green fuzzy hair (afro-ish), laid-back bounty hunter", "scene": "Spaceship interior, neon lights"},
        {"name": "Mugen", "show": "Samurai Champloo", "desc": "Wild spiky black hair, red jin-baori (sleeveless jacket), baggy shorts, hip-hop samurai style", "scene": "Edo period street, cherry blossoms"},
        {"name": "Goku", "show": "Dragon Ball", "desc": "Spiky black hair standing up, orange and blue gi martial arts uniform, muscular build, confident smile", "scene": "Training ground, dramatic sky"}
    ]
    
    console.print(f"\n[bold cyan]🎭 GENERATING 3 TEST CHARACTERS[/bold cyan]")
    
    prompt_template = """
📷 REAL PHOTOGRAPH - Canon EOS R6 Mark II, RF 85mm f/1.2L @ f/2.0, 4K 9:16

⚠️ OUTPUT: REAL COSPLAY PHOTO (not anime, not illustration, not CGI)

🔒 FACIAL IDENTITY (PRIMARY SUBJECT ONLY):
{lite_map}

CRITICAL: This is the PRIMARY SUBJECT detected across multiple photos.
Preserve this EXACT face. Ignore any other faces that may be in the reference.

📷 COSPLAY: {name} from {show}
{desc}
SCENE: {scene}

Generate ONE REAL cosplay photograph. Face must be INSTANTLY recognizable.
"""
    
    results = []
    for i, char in enumerate(characters, 1):
        console.print(f"\n[magenta]🎭 [{i}/3] {char['name']} ({char['show']})[/magenta]")
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = output_dir / f"JORDAN_{char['name']}_{ts}.png"
        
        prompt = prompt_template.format(
            lite_map=lite_map,
            name=char['name'],
            show=char['show'],
            desc=char['desc'],
            scene=char['scene']
        )
        
        with console.status(f"[cyan]⚡ Generating {char['name']}...", spinner="dots12"):
            try:
                response = await client.aio.models.generate_content(
                    model=IMAGE_MODEL,
                    contents=[prompt, photo],
                    config=types.GenerateContentConfig(
                        temperature=1.0,
                        response_modalities=["IMAGE", "TEXT"],
                        safety_settings=[
                            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
                            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
                            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_ONLY_HIGH"),
                            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"),
                        ]
                    )
                )
                
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        with open(path, "wb") as f:
                            f.write(part.inline_data.data)
                        kb = path.stat().st_size / 1024
                        console.print(f"[green]✅ {path.name} ({kb:.0f} KB)[/green]")
                        results.append((char['name'], kb))
                        break
            except Exception as e:
                console.print(f"[red]❌ {str(e)[:60]}[/red]")
        
        if i < len(characters):
            console.print(f"[cyan]⏳ 90s cooldown...[/cyan]")
            await asyncio.sleep(BUFFER_SECONDS)
    
    return results

async def main():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   🎯  JORDAN TEST - PRIMARY SUBJECT DETECTION  🎯                        ║
    ║                                                                           ║
    ║   Challenge: Photos with multiple people                                 ║
    ║   Can Yuki identify and lock onto the PRIMARY subject?                   ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", box=box.DOUBLE_EDGE))
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    console.print("[green]✅ Client ready[/green]")
    
    input_dir = Path("c:/Yuki_Local/jordan test")
    output_dir = Path("c:/Yuki_Local/jordan_test_results")
    output_dir.mkdir(exist_ok=True)
    
    # Step 1: Extract Primary Subject IP
    ip_path = output_dir / "jordan_primary_subject_ip.json"
    profile = await extract_primary_subject(client, input_dir, ip_path)
    
    # Step 2: Generate V5-Lite map
    lite_map = get_lite_map(profile)
    console.print(f"\n[green]✅ V5-Lite map: {len(lite_map)} chars[/green]")
    
    # Load best photo for generation
    input_images = sorted(input_dir.glob("*.jpg"))
    with open(input_images[0], "rb") as f:
        photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    # Step 3: Generate test characters
    results = await generate_test(client, lite_map, photo, output_dir)
    
    console.print(f"\n[cyan]⏱️ Generated: {len(results)}/3[/cyan]")
    console.print(f"[green]📂 Output: {output_dir}[/green]")
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    console.print("\n[bold green]✨ JORDAN TEST COMPLETE![/bold green]")
    console.print("[yellow]Review the images to verify PRIMARY subject was correctly identified.[/yellow]")

if __name__ == "__main__":
    asyncio.run(main())
