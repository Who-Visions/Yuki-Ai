#!/usr/bin/env python3
"""
Cloud Vision Face Identity Extractor

Extracts face data from all photos in a subject folder using Cloud Vision API.
Caches results to face_identity.json for use in generation prompts.

Usage:
    python extract_face_identity.py "C:/Yuki_Local/Cosplay_Lab/Subjects/Maurice"
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from google.cloud import vision
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def extract_face_identity(subject_dir: Path) -> dict:
    """
    Extract face identity data from all photos in subject directory.
    Uses Cloud Vision API for accurate face detection and landmarks.
    """
    
    # Find all photos
    photo_extensions = ["*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG"]
    photos = []
    for ext in photo_extensions:
        photos.extend(subject_dir.glob(ext))
    
    if not photos:
        console.print(f"[red]No photos found in {subject_dir}[/red]")
        return None
    
    console.print(f"[cyan]Found {len(photos)} photos to analyze[/cyan]")
    
    # Initialize Cloud Vision client
    client = vision.ImageAnnotatorClient()
    
    results = {
        "subject_name": subject_dir.name,
        "extracted_at": datetime.now().isoformat(),
        "best_photo": None,
        "best_score": 0,
        "photos": []
    }
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Analyzing faces...", total=len(photos))
        
        for photo_path in photos:
            progress.update(task, description=f"Analyzing {photo_path.name}...")
            
            try:
                # Read image
                with open(photo_path, "rb") as f:
                    content = f.read()
                
                image = vision.Image(content=content)
                
                # Detect faces
                response = client.face_detection(image=image)
                
                if response.error.message:
                    console.print(f"[yellow]Error on {photo_path.name}: {response.error.message}[/yellow]")
                    continue
                
                faces = response.face_annotations
                
                if not faces:
                    console.print(f"   {photo_path.name}: [dim]No face detected[/dim]")
                    continue
                
                # Take the first (usually largest/most prominent) face
                face = faces[0]
                
                # Calculate quality score based on detection confidence and attributes
                quality_score = int(face.detection_confidence * 40)  # Base: 0-40
                
                # Bonus points based on attributes
                likelihood_scores = {
                    "UNKNOWN": 0, "VERY_UNLIKELY": 1, "UNLIKELY": 2,
                    "POSSIBLE": 3, "LIKELY": 4, "VERY_LIKELY": 5
                }
                
                # Prefer neutral expressions (not extreme joy/sorrow/anger)
                joy_val = likelihood_scores.get(vision.Likelihood(face.joy_likelihood).name, 0)
                sorrow_val = likelihood_scores.get(vision.Likelihood(face.sorrow_likelihood).name, 0)
                anger_val = likelihood_scores.get(vision.Likelihood(face.anger_likelihood).name, 0)
                
                # Moderate expression is good (not too extreme)
                if joy_val <= 3 and sorrow_val <= 2 and anger_val <= 2:
                    quality_score += 5
                
                # Penalize blurry or underexposed
                if likelihood_scores.get(vision.Likelihood(face.blurred_likelihood).name, 0) >= 3:
                    quality_score -= 10
                if likelihood_scores.get(vision.Likelihood(face.under_exposed_likelihood).name, 0) >= 3:
                    quality_score -= 5
                
                # Cap at 50
                quality_score = min(50, max(0, quality_score))
                
                # Extract bounding box
                vertices = face.bounding_poly.vertices
                if vertices:
                    # Get image dimensions (approximate from bounding box)
                    bbox = {
                        "vertices": [{"x": v.x, "y": v.y} for v in vertices]
                    }
                else:
                    bbox = None
                
                # Extract landmarks
                landmarks = {}
                landmark_mapping = {
                    vision.FaceAnnotation.Landmark.Type.LEFT_EYE: "left_eye",
                    vision.FaceAnnotation.Landmark.Type.RIGHT_EYE: "right_eye",
                    vision.FaceAnnotation.Landmark.Type.NOSE_TIP: "nose_tip",
                    vision.FaceAnnotation.Landmark.Type.MOUTH_CENTER: "mouth_center",
                    vision.FaceAnnotation.Landmark.Type.LEFT_EAR_TRAGION: "left_ear",
                    vision.FaceAnnotation.Landmark.Type.RIGHT_EAR_TRAGION: "right_ear",
                    vision.FaceAnnotation.Landmark.Type.FOREHEAD_GLABELLA: "forehead",
                    vision.FaceAnnotation.Landmark.Type.CHIN_GNATHION: "chin",
                }
                
                for landmark in face.landmarks:
                    if landmark.type_ in landmark_mapping:
                        landmarks[landmark_mapping[landmark.type_]] = {
                            "x": round(landmark.position.x, 2),
                            "y": round(landmark.position.y, 2),
                            "z": round(landmark.position.z, 2) if landmark.position.z else 0
                        }
                
                # Extract attributes
                attributes = {
                    "joy": vision.Likelihood(face.joy_likelihood).name,
                    "sorrow": vision.Likelihood(face.sorrow_likelihood).name,
                    "anger": vision.Likelihood(face.anger_likelihood).name,
                    "surprise": vision.Likelihood(face.surprise_likelihood).name,
                    "headwear": vision.Likelihood(face.headwear_likelihood).name,
                    "blurred": vision.Likelihood(face.blurred_likelihood).name,
                    "under_exposed": vision.Likelihood(face.under_exposed_likelihood).name,
                }
                
                # Pose angles
                pose = {
                    "roll": round(face.roll_angle, 2),
                    "pan": round(face.pan_angle, 2),
                    "tilt": round(face.tilt_angle, 2)
                }
                
                photo_data = {
                    "filename": photo_path.name,
                    "quality_score": quality_score,
                    "detection_confidence": round(face.detection_confidence, 3),
                    "bounding_box": bbox,
                    "landmarks": landmarks,
                    "attributes": attributes,
                    "pose": pose
                }
                
                results["photos"].append(photo_data)
                
                console.print(f"   {photo_path.name}: [green]{quality_score}/50[/green] (conf: {face.detection_confidence:.2f})")
                
                # Track best photo
                if quality_score > results["best_score"]:
                    results["best_score"] = quality_score
                    results["best_photo"] = photo_path.name
                
                # Rate limit - 1 request per second to avoid 429s
                time.sleep(1.0)
                
            except Exception as e:
                console.print(f"   {photo_path.name}: [red]Error: {str(e)[:50]}[/red]")
                continue
            
            progress.advance(task)
    
    # Sort photos by quality score
    results["photos"].sort(key=lambda x: x["quality_score"], reverse=True)
    
    # Generate face description from best photo
    if results["photos"]:
        best = results["photos"][0]
        desc_parts = []
        
        # Check for glasses/headwear from attributes
        if best["attributes"].get("headwear") in ["LIKELY", "VERY_LIKELY"]:
            desc_parts.append("wearing headwear")
        
        # Expression
        if best["attributes"].get("joy") in ["LIKELY", "VERY_LIKELY"]:
            desc_parts.append("smiling")
        elif best["attributes"].get("joy") in ["UNLIKELY", "VERY_UNLIKELY"]:
            desc_parts.append("neutral expression")
        
        results["face_description"] = ", ".join(desc_parts) if desc_parts else "neutral expression"
    
    return results


def main():
    if len(sys.argv) < 2:
        console.print("[red]Usage: python extract_face_identity.py <subject_directory>[/red]")
        console.print("Example: python extract_face_identity.py \"C:/Yuki_Local/Cosplay_Lab/Subjects/Maurice\"")
        sys.exit(1)
    
    subject_dir = Path(sys.argv[1])
    
    if not subject_dir.exists():
        console.print(f"[red]Directory not found: {subject_dir}[/red]")
        sys.exit(1)
    
    console.print(f"\n[bold cyan]Cloud Vision Face Identity Extractor[/bold cyan]")
    console.print(f"Subject: [yellow]{subject_dir.name}[/yellow]\n")
    
    # Extract face identity
    results = extract_face_identity(subject_dir)
    
    if not results or not results["photos"]:
        console.print("[red]No faces extracted![/red]")
        sys.exit(1)
    
    # Save to JSON
    output_path = subject_dir / "face_identity.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    console.print(f"\n[green]✓ Saved to {output_path}[/green]")
    console.print(f"[green]✓ Best photo: {results['best_photo']} ({results['best_score']}/50)[/green]")
    console.print(f"[green]✓ Total photos analyzed: {len(results['photos'])}[/green]")


if __name__ == "__main__":
    main()
