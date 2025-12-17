"""
Convert HEIC files to JPG for Cloud Vision compatibility.
"""

from pathlib import Path
from PIL import Image
import pillow_heif

# Register HEIC opener with Pillow
pillow_heif.register_heif_opener()

def convert_heic_folder(input_dir: Path, output_dir: Path = None):
    """Convert all HEIC files in folder to JPG."""
    output_dir = output_dir or input_dir
    output_dir.mkdir(exist_ok=True)
    
    heic_files = list(input_dir.glob("*.heic")) + list(input_dir.glob("*.HEIC"))
    
    print(f"Found {len(heic_files)} HEIC files")
    
    for heic_path in heic_files:
        jpg_path = output_dir / f"{heic_path.stem}.jpg"
        
        if jpg_path.exists():
            print(f"  Skip (exists): {jpg_path.name}")
            continue
        
        try:
            img = Image.open(heic_path)
            img = img.convert("RGB")
            img.save(jpg_path, "JPEG", quality=95)
            print(f"  ✅ Converted: {heic_path.name} → {jpg_path.name}")
        except Exception as e:
            print(f"  ❌ Failed: {heic_path.name} - {e}")
    
    print(f"\nDone! JPGs in: {output_dir}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python convert_heic.py <folder>")
        sys.exit(1)
    
    folder = Path(sys.argv[1])
    convert_heic_folder(folder)
