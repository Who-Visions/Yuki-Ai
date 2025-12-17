"""
⚡ SNOW TEST 2 RETRY - ENHANCED FACE MATH ⚡
STRONGER facial mapping + 4-gen batches + 240s mega-buffer
"""

import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from rich import box
import subprocess
import time
import json
import re

console = Console()

# Configuration - UPDATED TIMING
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
MODEL = "gemini-3-pro-image-preview"
TEXT_MODEL = "gemini-2.5-flash"
BUFFER_SECONDS = 90  # Between each gen
MEGA_BUFFER_SECONDS = 240  # 4 minutes between batches
MEGA_BUFFER_EVERY = 4  # After every 4 generations

CAMERA_SPEC = """
CAMERA: Canon EOS R6 Mark II
LENS: RF 85mm f/1.2L USM @ f/2.0
RESOLUTION: 4K (9:16 vertical portrait)
LIGHTING: Professional cinematic lighting
QUALITY: Magazine cover, natural skin texture
"""

# Characters for retry
CHARACTERS = [
    {
        "name": "Satsuki_Kiryuin",
        "show": "Kill la Kill",
        "description": """
        Satsuki Kiryuin from Kill la Kill.
        
        APPEARANCE:
        - Very long, straight BLACK hair (extremely long)
        - Sharp blue eyes
        - Regal, commanding presence
        - Tall, elegant figure
        - Thick dramatic eyebrows
        
        COSTUME:
        - WHITE Honnouji Academy uniform (modified, regal)
        - Bakuzan sword at side optional
        
        STYLE: Empress, dominant ruler
        EXPRESSION: Cold superiority
        """,
        "scene": "Top of Honnouji Academy stairs, dramatic sunset"
    },
    {
        "name": "Winry_Rockbell",
        "show": "Fullmetal Alchemist",
        "description": """
        Winry Rockbell from Fullmetal Alchemist.
        
        APPEARANCE:
        - Long BLONDE hair in high ponytail
        - Blue eyes
        - Soft, kind face
        - Warm, friendly expression
        
        COSTUME:
        - Mechanic outfit (tank top)
        - Work apron, tool belt
        - Bandana in hair
        
        STYLE: Skilled automail mechanic
        EXPRESSION: Friendly smile
        """,
        "scene": "Rockbell automail workshop, warm golden light"
    },
    {
        "name": "Olivier_Armstrong",
        "show": "Fullmetal Alchemist Brotherhood",
        "description": """
        Olivier Mira Armstrong from FMAB.
        
        APPEARANCE:
        - Long BLONDE wavy hair
        - Icy blue eyes
        - Sharp, severe features
        - Cold, intimidating expression
        
        COSTUME:
        - Amestris military uniform (blue)
        - Long military coat with fur collar
        - Sword at hip
        
        STYLE: Ice Queen commander
        EXPRESSION: Icy stare
        """,
        "scene": "Briggs Fortress snow backdrop, cold blue lighting"
    },
    {
        "name": "Asuna_Yuuki",
        "show": "Sword Art Online",
        "description": """
        Asuna Yuuki from Sword Art Online.
        
        APPEARANCE:
        - Long chestnut/orange-brown hair
        - Amber/hazel eyes
        - Beautiful, elegant features
        - Gentle but determined expression
        
        COSTUME:
        - Knights of Blood Oath uniform
        - White and red leather armor dress
        - Rapier sword at side
        
        STYLE: Lightning Flash
        EXPRESSION: Kind but battle-ready
        """,
        "scene": "Aincrad floating castle, golden fantasy lighting"
    },
    {
        "name": "Sinon",
        "show": "Sword Art Online",
        "description": """
        Sinon (Shino Asada) from SAO.
        
        APPEARANCE:
        - Short AQUA/light blue hair (bob cut)
        - Teal/blue eyes
        - Slim, athletic figure
        - Calm, focused expression
        
        COSTUME:
        - GGO sniper outfit (futuristic)
        - Green/teal combat gear
        - Sniper rifle optional
        
        STYLE: Ice-cold sniper
        EXPRESSION: Focused, calculating
        """,
        "scene": "Futuristic battlefield, blue/teal sci-fi lighting"
    },
    {
        "name": "Revy",
        "show": "Black Lagoon",
        "description": """
        Revy (Rebecca Lee) from Black Lagoon.
        
        APPEARANCE:
        - TAN/brown skin (Chinese-American)
        - Long dark purple/maroon hair in ponytail
        - Brown eyes
        - Athletic, muscular build
        - Aggressive, wild expression
        
        COSTUME:
        - Black crop top (midriff showing)
        - Daisy duke shorts
        - Combat boots
        - TWIN Beretta pistols in holsters
        - Tribal tattoo on right arm
        
        STYLE: Chaotic gunfighter
        EXPRESSION: Wild grin, dangerous
        """,
        "scene": "Roanapur docks at night, neon signs"
    }
]

async def animated_countdown(seconds: int, desc: str, mega: bool = False):
    color = "bold yellow" if mega else "cyan"
    emoji = "🔥" if mega else "⏳"
    
    with Progress(
        SpinnerColumn("dots12"),
        TextColumn(f"[{color}]{emoji} {desc}"),
        BarColumn(bar_width=50, complete_style="green" if not mega else "yellow"),
        TextColumn("[bold cyan]{task.fields[remaining]}s"),
        TimeElapsedColumn(),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("", total=seconds, remaining=seconds)
        for i in range(seconds, 0, -1):
            progress.update(task, advance=1, remaining=i-1)
            await asyncio.sleep(1)

async def extract_enhanced_facial_ip(client, image_parts: list, image_files: list) -> dict:
    """ENHANCED facial extraction - much more detailed for identity lock"""
    
    console.print("\n[bold magenta]🔬 ENHANCED FACIAL IP EXTRACTION...[/bold magenta]")
    console.print("[yellow]   Using comprehensive multi-angle analysis...[/yellow]")
    
    # MUCH more detailed extraction prompt
    prompt = """You are a forensic facial analyst creating an IDENTITY LOCK profile.
    
Analyze ALL photos of this person from EVERY angle. This profile will be used to 
PERFECTLY recreate this exact face in AI-generated images. Any drift from these 
measurements = identity loss = failure.

Output ONLY raw JSON (no markdown). Be EXTREMELY specific with measurements and descriptions.

{
  "identity_lock": {
    "subject_id": "Snow2",
    "confidence": "HIGH",
    "analysis_quality": "COMPREHENSIVE"
  },
  
  "critical_identifiers": {
    "most_distinctive_feature_1": "<the #1 thing that makes this face unique>",
    "most_distinctive_feature_2": "<#2 unique identifier>",
    "most_distinctive_feature_3": "<#3 unique identifier>",
    "instant_recognition_markers": ["<list features that enable instant recognition>"]
  },
  
  "precise_measurements": {
    "face_length_category": "<short/average/long - BE SPECIFIC>",
    "face_width_category": "<narrow/average/wide>",
    "face_shape_exact": "<oval/round/square/oblong/heart/diamond/triangle>",
    "facial_thirds": {
      "upper_third": "<forehead proportion - short/average/long>",
      "middle_third": "<eyes to nose base - short/average/long>", 
      "lower_third": "<nose to chin - short/average/long>"
    },
    "facial_symmetry": "<symmetrical/slight left bias/slight right bias/notable asymmetry>"
  },
  
  "forehead": {
    "height": "<low/medium/high - cm estimate if possible>",
    "width": "<narrow/average/wide>",
    "shape": "<flat/rounded/sloped backward>",
    "hairline_shape": "<straight/widows peak/M-shaped/rounded>",
    "visible_lines": "<none/faint horizontal/prominent>"
  },
  
  "eyebrows": {
    "shape": "<straight/soft arch/high arch/S-curved>",
    "thickness": "<thin/medium/thick/very thick>",
    "length": "<short/medium/long>",
    "color": "<color>",
    "spacing_from_eyes": "<close/average/far>",
    "inner_corner_position": "<where do they start relative to eye>",
    "arch_peak_position": "<where is highest point>",
    "grooming": "<natural/shaped/filled>"
  },
  
  "eyes": {
    "shape": "<almond/round/hooded/monolid/deep-set/protruding/downturned/upturned>",
    "size_relative": "<small/medium/large for face>",
    "color_exact": "<be very specific - dark brown/light brown/hazel/green/blue/grey>",
    "color_pattern": "<solid/ring around pupil/multicolor>",
    "spacing": "<close-set/average/wide-set>",
    "eye_opening": "<narrow/average/wide>",
    "upper_lid_visible": "<yes amount/no/hooded>",
    "lower_lid": "<tight/average/visible white below>",
    "eye_corners_inner": "<rounded/pointed>",
    "eye_corners_outer": "<upturned/straight/downturned>",
    "lashes": "<sparse/average/thick/very thick>",
    "under_eye_area": "<smooth/slight shadow/dark circles/puffy>"
  },
  
  "nose": {
    "overall_size": "<small/medium/large for face>",
    "bridge_shape": "<straight/curved/bumped/flat/concave>",
    "bridge_width": "<narrow/medium/wide>",
    "bridge_height": "<low/medium/high>",
    "tip_shape": "<pointed/rounded/bulbous/upturned/downturned>",
    "tip_width": "<narrow/medium/wide>",
    "nostril_shape": "<round/oval/flared>",
    "nostril_size": "<small/medium/large>",
    "nostril_visibility_front": "<not visible/slightly/clearly visible>",
    "nose_length": "<short/medium/long>",
    "nose_angle": "<upturned/straight/downturned>",
    "any_piercings": "<septum/nostril left/nostril right/none>"
  },
  
  "lips_mouth": {
    "overall_fullness": "<thin/medium/full/very full>",
    "upper_lip_shape": "<straight/M-shaped/hearts bow>",
    "upper_lip_fullness": "<thin/medium/full>",
    "cupids_bow": "<flat/subtle/defined/very defined>",
    "lower_lip_fullness": "<thin/medium/full/fuller than upper>",
    "lip_width": "<narrow/average/wide>",
    "lip_color_natural": "<pink/rose/brown/dark>",
    "mouth_corners": "<upturned/straight/downturned>",
    "teeth_visible_smile": "<yes/no>",
    "philtrum": "<short/medium/long>"
  },
  
  "cheeks": {
    "cheekbone_prominence": "<flat/subtle/defined/very prominent>",
    "cheekbone_width": "<narrow/average/wide>",
    "cheekbone_height": "<low/medium/high>",
    "cheek_fullness": "<hollow/average/full/very full>",
    "dimples": "<none/one side/both sides>"
  },
  
  "jaw_chin": {
    "jaw_shape": "<narrow/square/round/V-shaped/angular>",
    "jaw_width": "<narrow/average/wide>",
    "jaw_definition": "<soft/moderate/strong/very defined>",
    "jaw_angle": "<description of angle>",
    "chin_shape": "<pointed/rounded/square/cleft>",
    "chin_projection": "<receding/average/prominent>",
    "chin_width": "<narrow/average/wide>",
    "chin_length": "<short/medium/long>"
  },
  
  "skin": {
    "fitzpatrick_scale": "<I/II/III/IV/V/VI - be accurate>",
    "tone_description": "<very fair/fair/light/medium/tan/brown/dark brown/deep>",
    "undertone": "<cool pink/cool red/neutral/warm yellow/warm olive/warm golden>",
    "texture": "<smooth/some texture/textured>",
    "visible_pores": "<minimal/some/noticeable>",
    "any_marks": "<moles/scars/birthmarks - describe locations>",
    "freckles": "<none/few/moderate/many>"
  },
  
  "hair": {
    "natural_color": "<black/dark brown/brown/light brown/blonde/red/grey>",
    "current_color": "<if different from natural>",
    "texture": "<straight/wavy/curly/coily/kinky>",
    "thickness": "<fine/medium/thick>",
    "current_length": "<short/medium/long/very long>",
    "current_style": "<description>",
    "parting": "<left/right/center/none>",
    "volume": "<flat/average/voluminous>"
  },
  
  "ears": {
    "size": "<small/medium/large>",
    "shape": "<round/pointed/square>",
    "attachment": "<attached/detached lobes>",
    "piercings": "<none/lobes/cartilage/multiple - describe>"
  },
  
  "expression_tendencies": {
    "resting_expression": "<neutral/slight smile/serious/soft>",
    "eye_expression": "<warm/intense/tired/alert/dreamy>",
    "overall_vibe": "<approachable/reserved/confident/gentle/fierce>"
  },
  
  "generation_rules": {
    "MUST_PRESERVE_EXACTLY": [
      "<list the 5-7 features that MUST stay identical>",
      "<these are non-negotiable for identity>"
    ],
    "CAN_STYLE": [
      "<hair color/style>",
      "<makeup>",
      "<expression intensity>"
    ],
    "NEVER_CHANGE": [
      "<bone structure>",
      "<nose shape>",
      "<eye shape and spacing>",
      "<skin tone>",
      "<lip proportions>"
    ]
  }
}

Analyze ALL 14 angles. Cross-reference features across photos. Be forensically precise.
This person must be INSTANTLY recognizable in any generated image."""

    with console.status("[cyan]   Deep analysis across all angles (this takes longer)...", spinner="dots12"):
        response = await client.aio.models.generate_content(
            model=TEXT_MODEL,
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
        profile = json.loads(text[start:end]) if start >= 0 else {"raw": text}
    except:
        profile = {"raw": text}
    
    profile["_metadata"] = {
        "created": datetime.now().isoformat(),
        "sources": image_files,
        "version": "2.0-ENHANCED",
        "extraction_type": "forensic_detail"
    }
    
    char_count = len(json.dumps(profile))
    console.print(f"[green]   ✅ ENHANCED Facial IP extracted ({char_count} chars)[/green]")
    
    if char_count < 3000:
        console.print("[yellow]   ⚠️ Profile seems short, may need re-extraction[/yellow]")
    
    return profile

async def generate_image(client, prompt: str, photo, output_path: Path) -> bool:
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=[prompt, photo],
        config=types.GenerateContentConfig(
            temperature=1.0, top_p=0.95, top_k=40,
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
            with open(output_path, "wb") as f:
                f.write(part.inline_data.data)
            return True
    return False

def build_prompt(character: dict, geometry: str) -> str:
    return f"""
═══════════════════════════════════════════════════════════════════════════════
PROFESSIONAL COSPLAY - {character['name'].replace('_', ' ')} from {character['show']}
═══════════════════════════════════════════════════════════════════════════════

TRANSFORM this person into {character['name'].replace('_', ' ')}.

═══════════════════════════════════════════════════════════════════════════════
🔒🔒🔒 FORENSIC FACIAL IDENTITY LOCK 🔒🔒🔒
═══════════════════════════════════════════════════════════════════════════════

{geometry}

⚠️ CRITICAL: Use the MUST_PRESERVE_EXACTLY fields as absolute constraints.
The bone structure, nose, eyes, lips, and skin tone are NON-NEGOTIABLE.
This face must be INSTANTLY recognizable as the reference person.

═══════════════════════════════════════════════════════════════════════════════
CHARACTER COSTUME & STYLING ONLY:
═══════════════════════════════════════════════════════════════════════════════

{character['description']}

Apply costume and styling. DO NOT alter facial geometry.

═══════════════════════════════════════════════════════════════════════════════
📷 {CAMERA_SPEC}
═══════════════════════════════════════════════════════════════════════════════

SCENE: {character['scene']}
COMPOSITION: 9:16 vertical portrait

Generate ONE photo where the person is INSTANTLY recognizable but in character costume.
═══════════════════════════════════════════════════════════════════════════════
"""

async def main():
    banner = """
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   ❄️  SNOW TEST 2 RETRY - ENHANCED FACE MATH  ❄️                        ║
    ║                                                                           ║
    ║   STRONGER facial mapping | 4-gen batches | 240s mega-buffer             ║
    ║                                                                           ║
    ║   Satsuki • Winry • Olivier • Asuna • Sinon • Revy                       ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan", box=box.DOUBLE_EDGE))
    
    with console.status("[bold cyan]⚡ Initializing...", spinner="dots12"):
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    console.print("[green]✅ Client ready![/green]")
    
    input_dir = Path("c:/Yuki_Local/snow test 2")
    output_dir = Path("c:/Yuki_Local/snow_test2_enhanced_results")
    output_dir.mkdir(exist_ok=True)
    
    input_images = sorted(input_dir.glob("*.jpg"))[:14]
    console.print(f"\n[cyan]📸 Loading {len(input_images)} photos...[/cyan]")
    
    image_parts = []
    image_files = []
    for img in input_images:
        with open(img, "rb") as f:
            image_parts.append(types.Part.from_bytes(data=f.read(), mime_type="image/jpeg"))
        image_files.append(img.name)
    
    best_photo = image_parts[0]
    console.print(f"[green]✅ Loaded {len(image_parts)} photos[/green]")
    
    # ENHANCED extraction
    facial_ip = await extract_enhanced_facial_ip(client, image_parts, image_files)
    
    ip_path = output_dir / "snow2_enhanced_facial_ip.json"
    with open(ip_path, "w", encoding="utf-8") as f:
        json.dump(facial_ip, f, indent=2, ensure_ascii=False)
    console.print(f"[green]💾 Enhanced Facial IP saved: {ip_path.name}[/green]")
    
    geometry_text = json.dumps(facial_ip, indent=2)
    
    results = []
    start = time.time()
    
    for i, char in enumerate(CHARACTERS, 1):
        console.print("\n" + "═" * 70)
        console.print(f"[bold magenta]🎭 [{i}/{len(CHARACTERS)}] {char['name'].replace('_', ' ')} ({char['show']})[/bold magenta]")
        console.print("═" * 70)
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with Progress(
            SpinnerColumn("dots12"),
            TextColumn("[cyan]{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            console=console
        ) as prog:
            task = prog.add_task("⚡ Generating with ENHANCED Face Math...", total=100)
            prog.update(task, advance=10)
            
            try:
                prompt = build_prompt(char, geometry_text)
                path = output_dir / f"ENHANCED_{char['name']}_{ts}.png"
                success = await generate_image(client, prompt, best_photo, path)
                
                prog.update(task, advance=90, description="✅ Complete!")
                if success:
                    size_kb = path.stat().st_size / 1024
                    console.print(f"   [green]✅ {path.name} ({size_kb:.0f} KB)[/green]")
                    results.append((char['name'], path, size_kb))
                else:
                    console.print("   [yellow]⚠️ No image returned[/yellow]")
            except Exception as e:
                console.print(f"   [red]❌ {str(e)[:80]}...[/red]")
        
        if i < len(CHARACTERS):
            if i % MEGA_BUFFER_EVERY == 0:
                console.print(f"\n[bold yellow]🔥 MEGA-BUFFER: {MEGA_BUFFER_SECONDS}s (4 min) after batch of 4[/bold yellow]")
                await animated_countdown(MEGA_BUFFER_SECONDS, f"MEGA-BUFFER ({i}/{len(CHARACTERS)} done)", mega=True)
            else:
                await animated_countdown(BUFFER_SECONDS, "Cooling down...")
    
    elapsed = time.time() - start
    console.print("\n" + "═" * 70)
    
    summary = Table(title="❄️ SNOW TEST 2 ENHANCED RESULTS", box=box.DOUBLE_EDGE)
    summary.add_column("#", style="dim")
    summary.add_column("Character", style="magenta")
    summary.add_column("File", style="white")
    summary.add_column("Size", style="green")
    
    for idx, (char, path, size) in enumerate(results, 1):
        summary.add_row(str(idx), char, path.name[:35], f"{size:.0f} KB")
    
    console.print(summary)
    console.print(f"\n[cyan]⏱️ Total: {elapsed/60:.1f} min | Generated: {len(results)}/{len(CHARACTERS)}[/cyan]")
    console.print(f"[green]📂 Output: {output_dir}[/green]")
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    console.print("\n[bold green]✨ ENHANCED TEST COMPLETE! ✨[/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
