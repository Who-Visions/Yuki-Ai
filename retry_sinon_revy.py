"""
⚡ QUICK RETRY: Sinon & Revy Only ⚡
"""
import asyncio
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
import subprocess, time, json

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"
MODEL = "gemini-3-pro-image-preview"

CHARACTERS = [
    {
        "name": "Sinon",
        "show": "Sword Art Online",
        "description": "Sinon - Short AQUA/light blue hair (bob cut), teal eyes, GGO sniper outfit, futuristic combat gear",
        "scene": "Futuristic battlefield, blue/teal sci-fi lighting"
    },
    {
        "name": "Revy",
        "show": "Black Lagoon",
        "description": "Revy - TAN/brown skin, long dark purple hair in ponytail, black crop top, shorts, twin Beretta pistols, tribal tattoo on arm, wild expression",
        "scene": "Roanapur docks at night, neon signs"
    }
]

async def main():
    console.print("[bold cyan]⚡ QUICK RETRY: Sinon & Revy[/bold cyan]")
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    # Load existing facial IP
    ip_path = Path("c:/Yuki_Local/snow_test2_enhanced_results/snow2_enhanced_facial_ip.json")
    with open(ip_path) as f:
        facial_ip = json.load(f)
    geometry_text = json.dumps(facial_ip, indent=2)
    
    # Load best photo
    input_dir = Path("c:/Yuki_Local/snow test 2")
    input_images = sorted(input_dir.glob("*.jpg"))[:1]
    with open(input_images[0], "rb") as f:
        best_photo = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
    
    output_dir = Path("c:/Yuki_Local/snow_test2_enhanced_results")
    
    for i, char in enumerate(CHARACTERS, 1):
        console.print(f"\n[bold magenta]🎭 [{i}/2] {char['name']} ({char['show']})[/bold magenta]")
        
        prompt = f"""
PROFESSIONAL COSPLAY - {char['name']} from {char['show']}

🔒 FACIAL IDENTITY LOCK:
{geometry_text}

Use MUST_PRESERVE_EXACTLY fields. Face must be INSTANTLY recognizable.

CHARACTER: {char['description']}

CAMERA: Canon R6 Mark II, RF 85mm @ f/2.0, 4K, 9:16 vertical
SCENE: {char['scene']}

Generate photo where person is recognizable but in character costume.
"""
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = output_dir / f"ENHANCED_{char['name']}_{ts}.png"
        
        with console.status(f"[cyan]⚡ Generating {char['name']}...", spinner="dots12"):
            try:
                response = await client.aio.models.generate_content(
                    model=MODEL,
                    contents=[prompt, best_photo],
                    config=types.GenerateContentConfig(
                        temperature=1.0, response_modalities=["IMAGE", "TEXT"],
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
                        console.print(f"[green]✅ {path.name} ({path.stat().st_size/1024:.0f} KB)[/green]")
                        break
            except Exception as e:
                console.print(f"[red]❌ {str(e)[:80]}[/red]")
        
        if i < len(CHARACTERS):
            console.print("[yellow]⏳ 90s cooldown...[/yellow]")
            await asyncio.sleep(90)
    
    subprocess.Popen(f'explorer "{output_dir}"', shell=True)
    console.print("\n[bold green]✨ DONE![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
