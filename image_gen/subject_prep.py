"""
⚡ SUBJECT PREPARATION UTILITY ⚡

Prepares subject photos for V11 pipeline:
1. Convert HEIC/HEIF to JPG
2. Extract EXIF metadata (camera, time, GPS, etc.)
3. Generate subject manifest with all metadata
4. Validate photos for face detection readiness
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Try to import HEIC support
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    HEIC_SUPPORTED = False
    print("⚠️ pillow-heif not installed. Run: pip install pillow-heif")

# =============================================================================
# EXIF EXTRACTION
# =============================================================================

def extract_exif(image_path: Path) -> Dict[str, Any]:
    """
    Extract comprehensive EXIF metadata from image
    
    Returns:
        dict with camera info, datetime, GPS, etc.
    """
    metadata = {
        "source_file": str(image_path),
        "filename": image_path.name,
        "extracted_at": datetime.now().isoformat()
    }
    
    try:
        with Image.open(image_path) as img:
            # Basic image info
            metadata["image_info"] = {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode
            }
            
            # Get EXIF data
            exif_data = img._getexif()
            if not exif_data:
                metadata["exif_available"] = False
                return metadata
            
            metadata["exif_available"] = True
            
            # Parse EXIF tags
            exif_parsed = {}
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                
                # Handle bytes
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', errors='ignore')
                    except:
                        value = str(value)
                
                exif_parsed[tag_name] = value
            
            # Camera info
            metadata["camera"] = {
                "make": exif_parsed.get("Make", "Unknown"),
                "model": exif_parsed.get("Model", "Unknown"),
                "software": exif_parsed.get("Software", "Unknown"),
                "lens_make": exif_parsed.get("LensMake", "Unknown"),
                "lens_model": exif_parsed.get("LensModel", "Unknown")
            }
            
            # Datetime info
            datetime_original = exif_parsed.get("DateTimeOriginal")
            datetime_digitized = exif_parsed.get("DateTimeDigitized")
            metadata["datetime"] = {
                "original": datetime_original,
                "digitized": datetime_digitized,
                "modified": exif_parsed.get("DateTime")
            }
            
            # Camera settings
            metadata["settings"] = {
                "exposure_time": str(exif_parsed.get("ExposureTime", "Unknown")),
                "f_number": str(exif_parsed.get("FNumber", "Unknown")),
                "iso": exif_parsed.get("ISOSpeedRatings", "Unknown"),
                "focal_length": str(exif_parsed.get("FocalLength", "Unknown")),
                "focal_length_35mm": exif_parsed.get("FocalLengthIn35mmFilm", "Unknown"),
                "flash": exif_parsed.get("Flash", "Unknown"),
                "white_balance": exif_parsed.get("WhiteBalance", "Unknown"),
                "exposure_mode": exif_parsed.get("ExposureMode", "Unknown")
            }
            
            # GPS info
            gps_info = exif_parsed.get("GPSInfo")
            if gps_info:
                metadata["gps"] = _parse_gps(gps_info)
            else:
                metadata["gps"] = None
            
            # Orientation
            metadata["orientation"] = exif_parsed.get("Orientation", 1)
            
    except Exception as e:
        metadata["error"] = str(e)
    
    return metadata


def _parse_gps(gps_info: Dict) -> Optional[Dict[str, Any]]:
    """Parse GPS EXIF data into readable coordinates"""
    try:
        gps_data = {}
        for key, val in gps_info.items():
            tag_name = GPSTAGS.get(key, key)
            gps_data[tag_name] = val
        
        # Calculate decimal coordinates
        lat = gps_data.get("GPSLatitude")
        lat_ref = gps_data.get("GPSLatitudeRef", "N")
        lon = gps_data.get("GPSLongitude")
        lon_ref = gps_data.get("GPSLongitudeRef", "E")
        
        if lat and lon:
            lat_decimal = _dms_to_decimal(lat, lat_ref)
            lon_decimal = _dms_to_decimal(lon, lon_ref)
            
            return {
                "latitude": lat_decimal,
                "longitude": lon_decimal,
                "altitude": gps_data.get("GPSAltitude"),
                "timestamp": gps_data.get("GPSTimeStamp"),
                "google_maps_url": f"https://maps.google.com/?q={lat_decimal},{lon_decimal}"
            }
    except Exception as e:
        return {"error": str(e)}
    
    return None


def _dms_to_decimal(dms, ref: str) -> float:
    """Convert degrees, minutes, seconds to decimal degrees"""
    try:
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if ref in ['S', 'W']:
            decimal = -decimal
        return round(decimal, 6)
    except:
        return 0.0


# =============================================================================
# HEIC CONVERSION
# =============================================================================

def convert_heic_to_jpg(heic_path: Path, output_dir: Optional[Path] = None, quality: int = 95) -> Optional[Path]:
    """
    Convert HEIC/HEIF to JPG while preserving EXIF
    
    Args:
        heic_path: Path to HEIC file
        output_dir: Where to save JPG (default: same directory)
        quality: JPG quality 1-100
        
    Returns:
        Path to converted JPG or None if failed
    """
    if not HEIC_SUPPORTED:
        print(f"   ❌ Cannot convert {heic_path.name} - pillow-heif not installed")
        return None
    
    output_dir = output_dir or heic_path.parent
    output_path = output_dir / f"{heic_path.stem}.jpg"
    
    try:
        with Image.open(heic_path) as img:
            # Preserve EXIF if available
            exif = img.info.get('exif')
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save as JPG
            if exif:
                img.save(output_path, 'JPEG', quality=quality, exif=exif)
            else:
                img.save(output_path, 'JPEG', quality=quality)
        
        print(f"   ✅ Converted: {heic_path.name} → {output_path.name}")
        return output_path
        
    except Exception as e:
        print(f"   ❌ Failed to convert {heic_path.name}: {e}")
        return None


# =============================================================================
# SUBJECT PREPARATION
# =============================================================================

class SubjectPrep:
    """Prepare subject photos for V11 pipeline"""
    
    def __init__(self, subject_dir: Path):
        self.subject_dir = Path(subject_dir)
        self.subject_name = self.subject_dir.name
        self.manifest_path = self.subject_dir / "subject_manifest.json"
        
    def prepare(self, convert_heic: bool = True, extract_metadata: bool = True) -> Dict[str, Any]:
        """
        Full subject preparation pipeline
        
        1. Find all image files
        2. Convert HEIC to JPG if needed
        3. Extract EXIF metadata
        4. Generate subject manifest
        
        Returns:
            Subject manifest with all metadata
        """
        print(f"\n{'='*60}")
        print(f"⚡ PREPARING SUBJECT: {self.subject_name}")
        print(f"{'='*60}")
        print(f"   Directory: {self.subject_dir}")
        
        manifest = {
            "subject_name": self.subject_name,
            "directory": str(self.subject_dir),
            "prepared_at": datetime.now().isoformat(),
            "photos": [],
            "summary": {}
        }
        
        # Find all images
        heic_files = list(self.subject_dir.glob("*.HEIC")) + list(self.subject_dir.glob("*.heic"))
        jpg_files = list(self.subject_dir.glob("*.jpg")) + list(self.subject_dir.glob("*.JPG")) + list(self.subject_dir.glob("*.jpeg"))
        png_files = list(self.subject_dir.glob("*.png")) + list(self.subject_dir.glob("*.PNG"))
        
        print(f"\n📸 Found images:")
        print(f"   HEIC: {len(heic_files)}")
        print(f"   JPG:  {len(jpg_files)}")
        print(f"   PNG:  {len(png_files)}")
        
        # Convert HEIC files
        if convert_heic and heic_files:
            print(f"\n🔄 Converting HEIC to JPG...")
            for heic in heic_files:
                converted = convert_heic_to_jpg(heic)
                if converted:
                    jpg_files.append(converted)
        
        # Process all usable images
        all_images = jpg_files + png_files
        print(f"\n🔍 Processing {len(all_images)} images...")
        
        for img_path in all_images:
            photo_data = {
                "filename": img_path.name,
                "path": str(img_path),
                "size_bytes": img_path.stat().st_size
            }
            
            if extract_metadata:
                photo_data["exif"] = extract_exif(img_path)
            
            manifest["photos"].append(photo_data)
            print(f"   ✓ {img_path.name}")
        
        # Generate summary
        manifest["summary"] = {
            "total_photos": len(manifest["photos"]),
            "heic_converted": len(heic_files) if convert_heic else 0,
            "cameras_used": list(set(
                p.get("exif", {}).get("camera", {}).get("model", "Unknown")
                for p in manifest["photos"]
            )),
            "date_range": self._get_date_range(manifest["photos"]),
            "has_gps": any(
                p.get("exif", {}).get("gps") is not None 
                for p in manifest["photos"]
            )
        }
        
        # Save manifest
        self._save_manifest(manifest)
        
        print(f"\n{'='*60}")
        print(f"✅ SUBJECT PREPARED: {self.subject_name}")
        print(f"   Total photos: {manifest['summary']['total_photos']}")
        print(f"   Cameras: {', '.join(manifest['summary']['cameras_used'])}")
        print(f"   Manifest: {self.manifest_path}")
        print(f"{'='*60}")
        
        return manifest
    
    def _get_date_range(self, photos: List[Dict]) -> Dict[str, str]:
        """Get earliest and latest photo dates"""
        dates = []
        for p in photos:
            dt = p.get("exif", {}).get("datetime", {}).get("original")
            if dt:
                dates.append(dt)
        
        if dates:
            dates.sort()
            return {"earliest": dates[0], "latest": dates[-1]}
        return {"earliest": None, "latest": None}
    
    def _save_manifest(self, manifest: Dict) -> None:
        """Save manifest with robust error handling"""
        try:
            # Create backup if exists
            if self.manifest_path.exists():
                backup_path = self.subject_dir / f"subject_manifest_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                self.manifest_path.rename(backup_path)
                print(f"   📦 Backed up old manifest: {backup_path.name}")
            
            # Write new manifest
            with open(self.manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, default=str)
            
            print(f"   💾 Saved manifest: {self.manifest_path.name}")
            
        except Exception as e:
            print(f"   ❌ Failed to save manifest: {e}")
            # Try alternate location
            alt_path = self.subject_dir / f"manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(alt_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, default=str)
            print(f"   💾 Saved to alternate: {alt_path.name}")
    
    def get_best_photos(self, count: int = 4) -> List[Path]:
        """Get best photos for pipeline (prioritize JPG, largest files)"""
        photos = []
        
        # Prefer JPG
        for ext in ["*.jpg", "*.JPG", "*.jpeg", "*.png", "*.PNG"]:
            photos.extend(self.subject_dir.glob(ext))
        
        # Sort by size (larger = higher quality typically)
        photos.sort(key=lambda p: p.stat().st_size, reverse=True)
        
        return photos[:count]


# =============================================================================
# CLI
# =============================================================================

def prepare_subject(subject_path: str) -> Dict:
    """Prepare a subject for the pipeline"""
    prep = SubjectPrep(Path(subject_path))
    return prep.prepare()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        subject_path = sys.argv[1]
    else:
        # Default to Keyosha Pullman
        subject_path = "C:/Yuki_Local/Cosplay_Lab/Subjects/Keyosha Pullman"
    
    manifest = prepare_subject(subject_path)
    print(f"\n📋 Summary: {json.dumps(manifest['summary'], indent=2)}")
