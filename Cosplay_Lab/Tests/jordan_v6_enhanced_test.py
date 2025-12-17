"""
⚡ JORDAN V6 ENHANCED - ROUND 2 ⚡
Implementing "Furiosa Protocol" + FACE MAPPING MATH
"""
import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
import subprocess, json

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
MODEL = "gemini-3-pro-image-preview"

# ROUND 2 - HIGH DIFFICULTY MIX
ROUND_2_CHARS = [
    {
        "name": "Gamora", "source": "Guardians of the Galaxy",
        "desc": "Green body paint cosplay, long two-tone magenta/black hair, black leather tactical armor, silver eye markings. REALISTIC COSPLAY.",
        "anti": "Do not generate Zoe Saldana. Do not change facial bone structure to look alien. Use SUBJECT'S face with Green Paint."
    },
    {
        "name": "Barbie_Movie", "source": "Barbie (2023)",
        "desc": "Pink gingham dress, blonde wig styled perfectly, pink accessories, plastic-perfect aesthetic but REAL human.",
        "anti": "Do not generate Margot Robbie. Do not lighten skin to white. Maintain Subject's skin tone (or natural makeup)."
    },
    {
        "name": "Katniss_Everdeen", "source": "Hunger Games",
        "desc": "Black tactical arena bodysuit, side braid, bow and arrows, quiver, forest dirt/grime.",
        "anti": "Do not generate Jennifer Lawrence. Subject's face must be preserved."
    },
    {
        "name": "Princess_Jasmine", "source": "Aladdin (Live Action)",
        "desc": "Turquoise silk two-piece outfit with gold trim, gold statement peacock jewelry, long dark hair blocked with ribbons.",
        "anti": "Do not generate Naomi Scott. Do not generate cartoon style."
    },
    {
        "name": "Raven", "source": "Teen Titans",
        "desc": "Grey/pale body paint (optional, or natural skin), classic blue cloak with hood casting shadow, black leotard, red chakra gem on forehead.",
        "anti": "Do not generate cartoon. Do not obscure face completely with shadow."
    },
    {
        "name": "Mikasa_Ackerman", "source": "Attack on Titan",
        "desc": "Scout Regiment uniform, brown jacket, white pants, red scarf, vertical maneuvering gear blades.",
        "anti": "Do not generate anime style. Do not generate 2D. Real photography only."
    },
    {
        "name": "Hela", "source": "Thor: Ragnarok",
        "desc": "Black and green bodysuit with antlers/spiked headdress, dark smoky eye makeup, villainous look.",
        "anti": "Do not generate Cate Blanchett. Face must be the Subject."
    },
    {
        "name": "Ahsoka_Tano", "source": "Star Wars (Live Action)",
        "desc": "Orange tone body paint, white facial markings, blue and white montrals/headtails, dual white lightsabers.",
        "anti": "Do not generate Rosario Dawson. Do not generate alien nose. Subject's nose/lips preserved."
    }
]

async def main():
    console.print("[bold cyan]🚀 JORDAN V6 ENHANCED - ROUND 2 TEST[/bold cyan]")
    console.print("[cyan]   Using 'Furiosa Protocol' + Face Mapping Math[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    
    # Load V6 Jordan map
    with open("c:/Yuki_Local/jordan_test_results/jordan_v6_full_zones.json") as f:
        full_map = json.load(f)
    
    # ENHANCEMENT 1: Extract Core Identity Markers
    skin_tone = full_map.get("zone_16_skin_surface", {}).get("tone_description", "deep warm brown")
    face_shape = full_map.get("face_calibration", {}).get("overall_shape", "heart")
    identifiers = full_map.get("critical_identity_lock", {}).get("top_7_unique_identifiers", [])
    
    # ENHANCEMENT 2: Extract Face Mapping Math (Geometry)
    # This guides the model to preserve exact ratios even if style changes
    math_map_str = json.dumps({
        "face_calibration": full_map.get("face_calibration", {}),
        "zone_9_ear_nose_ratio": full_map.get("zone_9_ear_nose_ratio", {}),
        "zone_12_inter_feature_distances": full_map.get("zone_12_inter_feature_distances", {}),
        "zone_13_face_angles": full_map.get("zone_13_face_angles", {}),
        "zone_4_nose": full_map.get("zone_4_nose", {}),
        "zone_10_lips": full_map.get("zone_10_lips", {}),
        "critical_identity_lock": full_map.get("critical_identity_lock", {})
    }, indent=2)

    # Load photo
    photos = sorted(Path("c:/Yuki_Local/jordan test").glob("*.jpg"))
    with open(photos[0], "rb") as f:
        photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    output = Path("c:/Yuki_Local/jordan_v6_round2_results")
    output.mkdir(exist_ok=True)
    
    for i, c in enumerate(ROUND_2_CHARS, 1):
        console.print(f"\n[magenta]🎲 [{i}/8] {c['name'].replace('_', ' ')}[/magenta]")
        
        # ENHANCEMENT 3: The "Furiosa Protocol" Prompt Structure with MATH
        prompt = f"""
📷 REAL PHOTOGRAPH - Canon EOS R6 Mark II, RF 85mm f/1.2L @ f/2.0
⚠️ CRITICAL: DNA-AUTHENTIC COSPLAY GENERATION

SUBJECT: The person in the reference photo (JORDAN).
CHARACTER: {c['name'].replace('_', ' ')} ({c['source']})

⛔ NEGATIVE CONSTRAINTS (STRICT):
- {c['anti']}
- DO NOT CHANGE SUBJECT'S BONE STRUCTURE.
- DO NOT CHANGE SUBJECT'S BASE APPEARANCE.
- DO NOT CHANGE FACE RATIOS (PRESERVE FACE MATH).

🔒 FACIAL IDENTITY LOCK (V6 GEOMETRY):
- Skin Tone: {skin_tone} (MANDATORY PRESERVATION)
- Face Shape: {face_shape}
- Unique Features: {identifiers}
- FACIAL GEOMETRY & MATH (PRESERVE EXACTLY):
{math_map_str}

COSTUME & STYLING:
{c['desc']}

SCENE:
Professional cosplay photoshoot setup, cinematic lighting.

GENERATE:
A photorealistic image of JORDAN cosplaying as {c['name']}.
Her face is the canvas. The character is the paint.
The GEOMETRY of the face must match the JSON data.
"""
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = output / f"V6_MATH_{c['name']}_{ts}.png"
        
        with console.status(f"[cyan]⚡ Generating {c['name']}...", spinner="dots12"):
            try:
                r = await client.aio.models.generate_content(model=MODEL, contents=[prompt, photo],
                    config=types.GenerateContentConfig(temperature=1.0, response_modalities=["IMAGE", "TEXT"],
                        safety_settings=[types.SafetySetting(category=cat, threshold="BLOCK_ONLY_HIGH") 
                            for cat in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", 
                                        "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]))
                for p in r.candidates[0].content.parts:
                    if hasattr(p, 'inline_data') and p.inline_data:
                        with open(path, "wb") as f: f.write(p.inline_data.data)
                        kb = path.stat().st_size / 1024
                        console.print(f"[green]✅ {path.name} ({kb:.0f} KB)[/green]")
                        break
            except Exception as e:
                console.print(f"[red]❌ {str(e)[:60]}[/red]")
        
        if i < len(ROUND_2_CHARS):
            if i % 4 == 0:
                console.print(f"[yellow]🔥 MEGA-BUFFER 240s[/yellow]")
                await asyncio.sleep(240)
            else:
                console.print(f"[cyan]⏳ 90s cooldown[/cyan]")
                await asyncio.sleep(90)
    
    subprocess.Popen(f'explorer "{output}"', shell=True)
    console.print("\n[bold green]✨ V6 ENHANCED WITH MATH TEST COMPLETE![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
