"""
⚡ JORDAN V5 - DC MOVIE FRANCHISE TEST ⚡
Using V5 Deep Nodes with accurate movie costumes
"""
import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
import subprocess, time, json

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
MODEL = "gemini-3-pro-image-preview"
BUFFER = 90
MEGA_BUFFER = 240

# DC MOVIE FRANCHISE characters with accurate movie costumes
DC_MOVIE_CHARS = [
    {
        "name": "Harley_Quinn_Suicide_Squad",
        "movie": "Suicide Squad (2016)",
        "costume": "Daddy's Lil Monster white cropped t-shirt, red and blue satin jacket with gold lettering, tiny denim shorts with ripped edges, fishnet stockings, high heel boots, studded belt, Good Night baseball bat, Puddin choker necklace",
        "hair": "Blonde pigtails with dip-dyed tips - one side pink, one side blue, messy and playful",
        "makeup": "Pale foundation, heavy black eye makeup smudged, red lips, blue and red eyeshadow on opposite eyes, heart drawn on cheek",
        "scene": "Grimy Gotham alley, neon signs, rain-slicked streets"
    },
    {
        "name": "Harley_Quinn_Birds_of_Prey",
        "movie": "Birds of Prey (2020)",
        "costume": "Colorful caution tape crop top, bright pink sports bra visible, high-waisted clear suspenders over sheer top, confetti-colored shorts, mismatched sneakers, roller skating aesthetic",
        "hair": "Blonde with full rainbow/multi-color dyed sections - pink, blue, yellow, orange throughout, loose and messy, some in twisted buns",
        "makeup": "Glittery, colorful, heart-shaped face gems, smeared red and pink lips, playful chaos",
        "scene": "Abandoned amusement park, colorful graffiti, confetti chaos"
    },
    {
        "name": "Catwoman_Dark_Knight_Rises",
        "movie": "The Dark Knight Rises (2012) - Anne Hathaway",
        "costume": "Sleek black leather catsuit, high-tech night vision goggles that flip up to look like cat ears, no actual cat ears, utility belt, stiletto heeled boots, practical tactical look",
        "hair": "Brown hair, slicked back or in a low ponytail, clean and practical",
        "makeup": "Minimal makeup, red lips, dramatic but realistic look, small black mask over eyes",
        "scene": "Gotham rooftop at night, city skyline, moonlight"
    },
    {
        "name": "Catwoman_The_Batman",
        "movie": "The Batman (2022) - Zoe Kravitz",
        "costume": "Homemade tactical catsuit - black leather biker jacket, leather pants, makeshift balaclava/ski mask with cut-out eyes, no cat ears, utilitarian motorcycle thief aesthetic, combat boots",
        "hair": "Short dark curly hair, visible when mask is pulled back",
        "makeup": "Minimal, dark eyeliner, natural look, small cuts/bruises from fighting",
        "scene": "Rainy Gotham night, crime scene, dark noir atmosphere"
    },
    {
        "name": "Poison_Ivy_Batman_Robin",
        "movie": "Batman & Robin (1997) - Uma Thurman",
        "costume": "Red glittery corset bodysuit covered in leaves, leafy green opera gloves, vine accessories wrapped around arms, dramatic theatrical look, seductive villain aesthetic",
        "hair": "Vibrant flame-red long curly hair, wild and dramatic, some leaves woven in",
        "makeup": "Heavy green eyeshadow, exaggerated red lips, theatrical dramatic makeup, glitter",
        "scene": "Greenhouse lair, exotic plants, green lighting, dramatic fog"
    },
    {
        "name": "Wonder_Woman_DCEU",
        "movie": "Wonder Woman (2017) - Gal Gadot",
        "costume": "Dark red leather corset armor with gold eagle emblem, dark blue leather skirt with gold star accents, brown leather battle skirt underneath, gold tiara with red star, silver bracers, lasso of truth at hip, brown leather battle boots",
        "hair": "Long dark brown wavy hair, flowing freely, battle-ready",
        "makeup": "Natural, minimal, bronze glow, strong warrior look",
        "scene": "No Man's Land WWI battlefield, dramatic fog and debris"
    },
    {
        "name": "Mera_Aquaman",
        "movie": "Aquaman (2018) - Amber Heard",
        "costume": "Emerald green scaled bodysuit like armor, iridescent green material, gold accents at shoulders and belt, Atlantean royal aesthetic, sleeveless with high collar",
        "hair": "Extremely long bright red wavy hair, flowing as if underwater, vibrant",
        "makeup": "Flawless dewy skin, coral lips, minimal eye makeup, aquatic glow",
        "scene": "Atlantis throne room, underwater blue lighting, bioluminescent elements"
    },
    {
        "name": "Black_Canary_Birds_Prey",
        "movie": "Birds of Prey (2020) - Jurnee Smollett",
        "costume": "Black leather cropped jacket, black crop top or bustier, high-waisted black pants or leather shorts, gold hoop earrings, singer/fighter aesthetic, practical combat wear",
        "hair": "Black natural curly hair, sometimes in half-up style or loose",
        "makeup": "Bronze glow, natural lips, subtle but glam, gold eyeshadow accents",
        "scene": "Underground fight club, concert stage lighting, urban Gotham"
    }
]

def get_lite_map(full_map: dict) -> str:
    return json.dumps({
        "face_calibration": full_map.get("face_calibration", {}),
        "eye_nodes": full_map.get("eye_nodes", {}),
        "nose_nodes": full_map.get("nose_nodes", {}),
        "lip_nodes": full_map.get("lip_nodes", {}),
        "cheek_nodes": full_map.get("cheek_nodes", {}),
        "jaw_chin_nodes": full_map.get("jaw_chin_nodes", {}),
        "skin_surface": full_map.get("skin_surface", {}),
        "critical_identity_lock": full_map.get("critical_identity_lock", {})
    }, indent=2)

async def main():
    console.print("[bold cyan]🎬 JORDAN V5 - DC MOVIE FRANCHISE TEST[/bold cyan]")
    console.print("[cyan]   Using accurate movie costumes[/cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    
    # Load V5 Jordan IP
    with open("c:/Yuki_Local/jordan_test_results/jordan_v5_deep_nodes.json") as f:
        full_map = json.load(f)
    lite_map = get_lite_map(full_map)
    console.print(f"[green]✅ Jordan V5 IP loaded ({len(lite_map)} chars)[/green]")
    
    # Load photo
    photos = sorted(Path("c:/Yuki_Local/jordan test").glob("*.jpg"))
    with open(photos[0], "rb") as f:
        photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    output = Path("c:/Yuki_Local/jordan_dc_movies_results")
    output.mkdir(exist_ok=True)
    
    results = []
    for i, c in enumerate(DC_MOVIE_CHARS, 1):
        console.print(f"\n[magenta]🎬 [{i}/{len(DC_MOVIE_CHARS)}] {c['name'].replace('_', ' ')}[/magenta]")
        console.print(f"[dim]   {c['movie']}[/dim]")
        
        prompt = f"""
📷 REAL PHOTOGRAPH - Canon EOS R6 Mark II, RF 85mm f/1.2L @ f/2.0, 4K 9:16 vertical portrait
⚠️ REAL COSPLAY PHOTOSHOOT (not anime, not illustration, not CGI, not cartoon)

🔒 FACIAL IDENTITY (V5 DEEP NODES - PRIMARY SUBJECT):
{lite_map}

CRITICAL: Preserve this EXACT face. Must be INSTANTLY recognizable as the reference person.
Apply costume and styling, but face structure, skin tone, features = LOCKED.

🎬 DC MOVIE COSPLAY: {c['name'].replace('_', ' ')}
FROM: {c['movie']}

COSTUME (MOVIE ACCURATE):
{c['costume']}

HAIR:
{c['hair']}

MAKEUP:
{c['makeup']}

SCENE: {c['scene']}

Generate ONE REAL cosplay photograph that looks like it was shot TODAY on set of the movie.
The person's face is the reference. The costume is from the film.
"""
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = output / f"JORDAN_MOVIE_{c['name']}_{ts}.png"
        
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
                        results.append((c['name'], kb))
                        break
            except Exception as e:
                console.print(f"[red]❌ {str(e)[:60]}[/red]")
        
        if i < len(DC_MOVIE_CHARS):
            if i % 4 == 0:
                console.print(f"[yellow]🔥 MEGA-BUFFER {MEGA_BUFFER}s[/yellow]")
                await asyncio.sleep(MEGA_BUFFER)
            else:
                console.print(f"[cyan]⏳ {BUFFER}s cooldown[/cyan]")
                await asyncio.sleep(BUFFER)
    
    console.print(f"\n[cyan]⏱️ Generated: {len(results)}/{len(DC_MOVIE_CHARS)}[/cyan]")
    subprocess.Popen(f'explorer "{output}"', shell=True)
    console.print("\n[bold green]✨ DC MOVIE FRANCHISE TEST COMPLETE![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
