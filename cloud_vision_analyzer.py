"""
🦊 YUKI V9 - CLOUD VISION ANALYZER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cloud Vision API integration for V9 pipeline:
- Face Detection (emotions, landmarks, pose angles)
- Object Localization (Person detection)
- SafeSearch (content moderation)
- Result caching via Firestore (optional)

Pricing: First 1000 units/month FREE, then $1.50/1000
"""

from google.cloud import vision
from PIL import Image, ImageDraw
from pathlib import Path
from typing import Optional
import hashlib
import json


class CloudVisionAnalyzer:
    """Handles all Cloud Vision API interactions with optional caching."""
    
    LIKELIHOOD_NAMES = ["UNKNOWN", "VERY_UNLIKELY", "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"]
    
    def __init__(self, project_id: str = "yuki-app-prod", enable_cache: bool = False):
        """
        Initialize Cloud Vision client.
        
        Args:
            project_id: GCP project ID
            enable_cache: Enable local file caching (reduces API calls)
        """
        from google.api_core import client_options
        options = client_options.ClientOptions(quota_project_id=project_id)
        self.client = vision.ImageAnnotatorClient(client_options=options)
        self.project_id = project_id
        self.enable_cache = enable_cache
        self.cache_dir = Path(__file__).parent / "v9_results" / ".vision_cache"
        
        if enable_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            print(f"📦 Cloud Vision cache enabled: {self.cache_dir}")
    
    def _get_cache_key(self, image_bytes: bytes) -> str:
        """Generate cache key from image hash."""
        return hashlib.sha256(image_bytes).hexdigest()[:32]
    
    def _get_cached(self, cache_key: str) -> Optional[dict]:
        """Retrieve cached result from local file."""
        if not self.enable_cache:
            return None
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            if cache_file.exists():
                with open(cache_file, "r") as f:
                    return json.load(f)
        except:
            pass
        return None
    
    def _set_cached(self, cache_key: str, result: dict):
        """Store result in local file cache."""
        if not self.enable_cache:
            return
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, "w") as f:
                json.dump(result, f)
        except:
            pass
    
    def analyze_image(self, path: str, features: list[str] = None) -> dict:
        """
        Analyze image with Cloud Vision API.
        
        Args:
            path: Local file path to image
            features: List of features ["face", "object", "safe", "labels"]
                     Default: ["face"] for cost optimization
        
        Returns:
            dict with analysis results
        """
        features = features or ["face"]  # Default to face only (FREE tier friendly)
        
        # Load image
        with open(path, "rb") as f:
            content = f.read()
        
        # Check cache first
        if self.enable_cache:
            cache_key = self._get_cache_key(content)
            cached = self._get_cached(cache_key)
            if cached:
                return cached
        
        # Build feature request (single API call for all features)
        feature_types = []
        if "face" in features:
            feature_types.append({"type_": vision.Feature.Type.FACE_DETECTION, "max_results": 10})
        if "object" in features:
            feature_types.append({"type_": vision.Feature.Type.OBJECT_LOCALIZATION, "max_results": 20})
        if "safe" in features:
            feature_types.append({"type_": vision.Feature.Type.SAFE_SEARCH_DETECTION})
        if "labels" in features:
            feature_types.append({"type_": vision.Feature.Type.LABEL_DETECTION, "max_results": 10})
        
        # Make API request
        image = vision.Image(content=content)
        response = self.client.annotate_image({"image": image, "features": feature_types})
        
        # Parse response
        result = self._parse_response(response)
        
        # Cache result
        if self.enable_cache:
            self._set_cached(cache_key, result)
        
        return result
    
    def _parse_response(self, response) -> dict:
        """Parse Vision API response into clean dict."""
        result = {"success": True, "error": None}
        
        if response.error.message:
            result["success"] = False
            result["error"] = response.error.message
            return result
        
        # Face annotations
        if response.face_annotations:
            result["faces"] = []
            for face in response.face_annotations:
                result["faces"].append({
                    "confidence": face.detection_confidence,
                    "joy": self.LIKELIHOOD_NAMES[face.joy_likelihood],
                    "anger": self.LIKELIHOOD_NAMES[face.anger_likelihood],
                    "surprise": self.LIKELIHOOD_NAMES[face.surprise_likelihood],
                    "sorrow": self.LIKELIHOOD_NAMES[face.sorrow_likelihood],
                    "headwear": self.LIKELIHOOD_NAMES[face.headwear_likelihood],
                    "bounds": [(v.x, v.y) for v in face.bounding_poly.vertices],
                    "roll_angle": face.roll_angle,
                    "pan_angle": face.pan_angle,
                    "tilt_angle": face.tilt_angle,
                })
        
        # Object annotations
        if response.localized_object_annotations:
            result["objects"] = []
            for obj in response.localized_object_annotations:
                result["objects"].append({
                    "name": obj.name,
                    "score": obj.score,
                    "bounds": [(v.x, v.y) for v in obj.bounding_poly.normalized_vertices],
                })
        
        # SafeSearch
        if response.safe_search_annotation:
            ss = response.safe_search_annotation
            result["safe_search"] = {
                "adult": self.LIKELIHOOD_NAMES[ss.adult],
                "violence": self.LIKELIHOOD_NAMES[ss.violence],
                "racy": self.LIKELIHOOD_NAMES[ss.racy],
                "spoof": self.LIKELIHOOD_NAMES[ss.spoof],
                "medical": self.LIKELIHOOD_NAMES[ss.medical],
            }
        
        # Labels
        if response.label_annotations:
            result["labels"] = [
                {"description": label.description, "score": label.score}
                for label in response.label_annotations
            ]
        
        return result
    
    def validate_for_generation(self, analysis: dict) -> dict:
        """
        Check if image is suitable for cosplay generation.
        
        Returns:
            {
                "valid": bool,
                "quality_score": 0-100,
                "issues": ["list of problems"],
                "recommendations": ["list of tips"]
            }
        """
        issues = []
        recommendations = []
        quality_score = 100
        
        # Check face detection
        faces = analysis.get("faces", [])
        if not faces:
            issues.append("No face detected")
            quality_score -= 50
        elif len(faces) > 1:
            issues.append(f"Multiple faces detected ({len(faces)})")
            quality_score -= 20
        else:
            face = faces[0]
            
            # Check confidence
            if face["confidence"] < 0.8:
                issues.append(f"Low face confidence ({face['confidence']:.0%})")
                quality_score -= 15
            
            # Check pose (ideal: facing camera)
            if abs(face["pan_angle"]) > 30:
                issues.append("Face turned sideways")
                recommendations.append("Use front-facing photo")
                quality_score -= 10
            
            if abs(face["tilt_angle"]) > 25:
                issues.append("Face tilted")
                quality_score -= 10
            
            # Check headwear
            if face["headwear"] in ["LIKELY", "VERY_LIKELY"]:
                recommendations.append("Headwear may affect hairstyle")
        
        # Check SafeSearch (if available)
        safe = analysis.get("safe_search", {})
        if safe.get("adult") in ["LIKELY", "VERY_LIKELY"]:
            issues.append("Content flagged as inappropriate")
            quality_score = 0
        
        return {
            "valid": quality_score >= 50 and "inappropriate" not in str(issues),
            "quality_score": max(0, quality_score),
            "issues": issues,
            "recommendations": recommendations,
        }
    
    def draw_annotations(self, image_path: str, analysis: dict, output_path: str) -> str:
        """Draw face boxes on image for debugging."""
        im = Image.open(image_path)
        draw = ImageDraw.Draw(im)
        
        # Draw face boxes
        for face in analysis.get("faces", []):
            box = face["bounds"]
            if len(box) >= 4:
                draw.line(box + [box[0]], width=3, fill="#00FF00")
                label = f"{face['confidence']:.0%} | {face['joy']}"
                draw.text((box[0][0], box[0][1] - 20), label, fill="#00FF00")
        
        # Draw Person boxes
        for obj in analysis.get("objects", []):
            if obj["name"] == "Person":
                bounds = obj["bounds"]
                w, h = im.size
                box = [(int(x * w), int(y * h)) for x, y in bounds]
                if len(box) >= 4:
                    draw.line(box + [box[0]], width=2, fill="#0088FF")
        
        im.save(output_path)
        return output_path
    
    def extract_facial_ip(self, image_paths: list[str]) -> dict:
        """
        Extract facial IP from multiple photos for V9 generation.
        
        Args:
            image_paths: List of photo paths (up to 5)
        
        Returns:
            Aggregated facial analysis for identity lock
        """
        all_faces = []
        best_face = None
        best_confidence = 0
        
        for path in image_paths[:5]:
            analysis = self.analyze_image(path, features=["face"])
            faces = analysis.get("faces", [])
            
            if faces:
                face = faces[0]  # Primary face
                all_faces.append(face)
                
                # Track best quality face
                if face["confidence"] > best_confidence:
                    best_confidence = face["confidence"]
                    best_face = face
        
        if not all_faces:
            return {"error": "No faces detected in any photos"}
        
        # Aggregate emotions across photos
        emotion_counts = {"joy": 0, "neutral": 0, "serious": 0}
        for face in all_faces:
            if face["joy"] in ["LIKELY", "VERY_LIKELY"]:
                emotion_counts["joy"] += 1
            elif face["sorrow"] in ["LIKELY", "VERY_LIKELY"] or face["anger"] in ["LIKELY", "VERY_LIKELY"]:
                emotion_counts["serious"] += 1
            else:
                emotion_counts["neutral"] += 1
        
        return {
            "cloud_vision": {
                "face_count": len(all_faces),
                "best_confidence": best_confidence,
                "best_face": best_face,
                "average_roll": sum(f["roll_angle"] for f in all_faces) / len(all_faces),
                "average_pan": sum(f["pan_angle"] for f in all_faces) / len(all_faces),
                "emotion_diversity": emotion_counts,
            },
            "identity_anchors": best_face["bounds"] if best_face else None,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CLI TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    
    if len(sys.argv) < 2:
        console.print("[yellow]Usage: python cloud_vision_analyzer.py <image_path>[/yellow]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    console.print(f"\n[cyan]🔍 Analyzing: {image_path}[/cyan]\n")
    
    analyzer = CloudVisionAnalyzer()
    
    try:
        # Analyze with face detection only (FREE tier)
        result = analyzer.analyze_image(image_path, features=["face"])
        
        if not result["success"]:
            console.print(f"[red]Error: {result['error']}[/red]")
            sys.exit(1)
        
        # Display faces
        faces = result.get("faces", [])
        if faces:
            table = Table(title=f"✅ Detected {len(faces)} Face(s)")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="white")
            
            face = faces[0]
            table.add_row("Confidence", f"{face['confidence']:.1%}")
            table.add_row("Joy", face["joy"])
            table.add_row("Anger", face["anger"])
            table.add_row("Surprise", face["surprise"])
            table.add_row("Roll Angle", f"{face['roll_angle']:.1f}°")
            table.add_row("Pan Angle", f"{face['pan_angle']:.1f}°")
            table.add_row("Tilt Angle", f"{face['tilt_angle']:.1f}°")
            table.add_row("Headwear", face["headwear"])
            
            console.print(table)
        else:
            console.print("[yellow]No faces detected[/yellow]")
        
        # Validate
        validation = analyzer.validate_for_generation(result)
        console.print(f"\n[bold]Quality Score: {validation['quality_score']}/100[/bold]")
        console.print(f"Valid for generation: {'✅ Yes' if validation['valid'] else '❌ No'}")
        
        if validation["issues"]:
            console.print(f"[red]Issues: {', '.join(validation['issues'])}[/red]")
        if validation["recommendations"]:
            console.print(f"[yellow]Tips: {', '.join(validation['recommendations'])}[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Make sure Cloud Vision API is enabled: gcloud services enable vision.googleapis.com --project=yuki-app-prod[/yellow]")
