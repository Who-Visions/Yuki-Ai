import cv2
import os
import json
import glob
from pathlib import Path

# Paths
ASSETS_DIR = r"c:\Yuki_Local\yuki-app\src\assets\renders"
OUTPUT_FILE = r"c:\Yuki_Local\yuki-app\src\config\focusMap.json"

# Load Haar Cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def analyze_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width, _ = img.shape
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    focus_y_percent = 25 # Default to 25% (upper quarter) if detection fails
    
    if len(faces) > 0:
        # Sort faces by area (largest is likely the subject)
        faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
        (x, y, w, h) = faces[0]
        
        # roi_gray = gray[y:y+h, x:x+w]
        
        # Calculate eye line (approx 1/3 down the face)
        eye_level_y = y + (h * 0.35)
        
        # Convert to percentage of total image height
        focus_y_percent = (eye_level_y / height) * 100
        
        # Clamp to reasonable bounds (0-100)
        focus_y_percent = max(0, min(100, focus_y_percent))
    
    return f"center {focus_y_percent:.1f}%"

def main():
    focus_map = {}
    
    # Recursive search for images
    image_files = glob.glob(os.path.join(ASSETS_DIR, "**", "*.png"), recursive=True)
    image_files += glob.glob(os.path.join(ASSETS_DIR, "**", "*.jpg"), recursive=True)
    
    print(f"Analyzing {len(image_files)} images for Smart Focus...")
    
    for img_path in image_files:
        # Get relative path key for JSON (consistent with require())
        # We'll use the filename as the key since requires are mapped that way often, 
        # or better: we map by "relative path key" used in the app? 
        # Actually simplest is just filename for now, or relative path from assets.
        
        relative_path = os.path.relpath(img_path, ASSETS_DIR).replace("\\", "/")
        print(f"Scanning: {relative_path}")
        
        alignment = analyze_image(img_path)
        if alignment:
            focus_map[relative_path] = alignment
            print(f"  -> Focus: {alignment}")
            
    # Write map
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(focus_map, f, indent=4)
        
    print(f"Smart Focus Map saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
