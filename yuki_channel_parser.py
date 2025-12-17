import re
import json
from pathlib import Path

def parse_channels(input_file: Path, output_file: Path):
    """
    Parses a raw text dump of YouTube channels into structured JSON.
    Expected format:
    Name
    NameYoutube Channel URL
    Maybe Description
    """
    if not input_file.exists():
        print(f"Error: Input file {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    channels = []
    current_channel = {}
    
    # Simple state machine parser
    # We look for lines containing "Youtube Channel https" as the anchor
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # Check for URL line
        if "Youtube Channel http" in line:
            # Format usually: "NameYoutube Channel https://..."
            # Split by "Youtube Channel"
            parts = line.split("Youtube Channel")
            name_part = parts[0].strip()
            url_part = parts[1].strip()
            
            # Clean up URL (sometimes has trailing dots from scraping)
            url_part = url_part.rstrip(".")
            
            channels.append({
                "name": name_part,
                "url": url_part,
                "status": "pending"
            })

    output_data = {"channels": channels}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4)
        
    print(f"Successfully parsed {len(channels)} channels to {output_file}")

if __name__ == "__main__":
    input_path = Path(r"C:\Yuki_Local\data\raw_channels.txt")
    output_path = Path(r"C:\Yuki_Local\data\cosplay_channels.json")
    parse_channels(input_path, output_path)
