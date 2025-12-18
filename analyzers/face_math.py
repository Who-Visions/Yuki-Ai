import os
import json
import math
from google import genai
from google.genai import types
from PIL import Image

# Configuration
PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global" # Gemini 3 models often require global or specific regions

class FaceMathArchitect:
    """
    Extracts mathematical facial schemas from images to preserve identity in cosplay generations.
    """
    
    def __init__(self):
        self.client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

    def extract_face_schema(self, image_path: str) -> dict:
        """
        Analyzes an image and returns a JSON schema of facial landmarks and geometry.
        Tries Gemini 3 Pro Preview first, falls back to Gemini 2.5 Flash Image.
        """
        print(f"Analyzing face geometry in: {image_path}")
        
        if not os.path.exists(image_path):
            return {"error": f"File not found: {image_path}"}

        image = Image.open(image_path)
        
        # Prompt for structured geometric analysis
        prompt = """
        Analyze the face(s) in this image and output a strict JSON schema describing the facial geometry and features.
        For each face detected, provide:
        1. "identity_vector": A dictionary of estimated geometric ratios (e.g., eye_spacing_ratio, face_width_height_ratio, jawline_angle).
        2. "feature_map": Detailed text descriptions of eyes, nose, lips, skin texture, and hair.
        3. "distinctive_marks": Scars, moles, freckles.
        4. "expression_weight": A numerical vector (0.0-1.0) for current expression (joy, anger, surprise, neutral).
        
        This JSON will be used to mathematically reconstruct this face in a 3D rendering engine. Precision is key.
        
        Output format:
        {
            "faces": [
                {
                    "id": "face_1",
                    "box_2d": [ymin, xmin, ymax, xmax],
                    "identity_vector": { ... },
                    "feature_map": { ... },
                    "distinctive_marks": [ ... ],
                    "expression_weight": { ... }
                }
            ]
        }
        """

        # Attempt 1: Gemini 3 Pro Preview (Global)
        try:
            print("  Attempting with Gemini 3 Pro Preview (Global)...")
            client_v3 = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
            response = client_v3.models.generate_content(
                model="gemini-3-pro-preview",
                contents=[prompt, image],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"  ⚠️ Gemini 3 failed: {e}")
            
            # Attempt 2: Gemini 2.5 Flash Image (US-Central1) - Fallback
            try:
                print("  ⚠️ Falling back to Gemini 2.5 Flash Image (US-Central1)...")
                client_v25 = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
                response = client_v25.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=[prompt, image],
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                return json.loads(response.text)
            except Exception as e2:
                return {"error": f"All models failed. Gemini 3: {e}, Gemini 2.5: {e2}"}

    def calculate_blended_schema(self, face_schemas: list, weights: list = None) -> dict:
        """
        Mathematically blends multiple face schemas (e.g., for a 'child of' or 'fusion' cosplay).
        """
        if not face_schemas:
            return {}
            
        if weights is None:
            weights = [1.0 / len(face_schemas)] * len(face_schemas)
            
        blended_vector = {}
        for i, schema in enumerate(face_schemas):
            vector = schema.get("identity_vector", {})
            weight = weights[i]
            for key, value in vector.items():
                if isinstance(value, (int, float)):
                    blended_vector[key] = blended_vector.get(key, 0) + (value * weight)
                    
        return {
            "type": "blended_identity",
            "source_count": len(face_schemas),
            "blended_identity_vector": blended_vector
        }

def test_face_math():
    architect = FaceMathArchitect()
    
    # Test with a sample image
    test_dir = r"C:\Yuki_Local\dave test images"
    if os.path.exists(test_dir):
        files = [f for f in os.listdir(test_dir) if f.endswith('.png')]
        if files:
            test_image = os.path.join(test_dir, files[0])
            print(f"Processing: {test_image}")
            
            # 1. Extract Schema
            schema = architect.extract_face_schema(test_image)
            print("Schema extracted.")
            
            # Save schema
            with open("face_schema_output.json", "w") as f:
                json.dump(schema, f, indent=2)
            
            if "error" in schema:
                print(f"Error extracting schema: {schema['error']}")
                return

            # 2. Generate Cosplay using the Schema
            from tools import generate_cosplay_image
            
            # Construct a prompt that uses the math
            # Handle potential list or dict structure depending on model output consistency
            faces = schema.get("faces", [])
            if not faces:
                 print("No faces found in schema.")
                 return

            identity_vector = faces[0].get("identity_vector", {})
            features = faces[0].get("feature_map", "Standard features")
            
            prompt = (
                f"Generate a hyper-realistic cosplay of Dante from Devil May Cry 5. "
                f"CRITICAL: You must construct the face using this exact geometric schema to preserve identity:\n"
                f"{json.dumps(identity_vector)}\n"
                f"Feature Map: {features}\n"
                f"The subject should look exactly like the person described by these metrics, wearing Dante's red coat. "
                f"Cinematic lighting, 8k resolution."
            )
            
            print("\nGenerating Image with Gemini 3 Pro...")
            result = generate_cosplay_image(
                prompt=prompt,
                model="gemini-3-pro-image-preview", # Primary
                reference_image_paths=[test_image]
            )
            
            if "Error" in result or "Failed" in result:
                print("\n⚠️ Gemini 3 Generation failed. Falling back to Gemini 2.5 Flash Image...")
                result = generate_cosplay_image(
                    prompt=prompt,
                    model="gemini-2.5-flash-image", # Fallback
                    reference_image_paths=[test_image]
                )
                
            print(result)

if __name__ == "__main__":
    test_face_math()
