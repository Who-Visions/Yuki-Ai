"""
Facial Geometry Correction Module
Corrects perspective distortion and camera angle effects on facial proportions
"""

import asyncio
import logging
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GeometryCorrector")

class FacialGeometryCorrector:
    """
    Analyzes and corrects perspective distortion in facial photos
    """
    
    def __init__(self, project_id: str):
        self.client = genai.Client(vertexai=True, project=project_id, location="us-central1")
    
    async def analyze_perspective(self, image_path: Path) -> dict:
        """
        Analyze camera perspective and detect geometric distortions
        """
        img = Image.open(image_path)
        
        prompt = """Analyze this photo's CAMERA PERSPECTIVE and GEOMETRIC DISTORTIONS affecting facial features.

**CAMERA ANALYSIS:**
1. **Angle**: Is this frontal, 3/4 view, profile, low-angle (from below), high-angle (from above)?
2. **Distance**: Close-up (< 3 feet), medium (3-6 feet), or distant (> 6 feet)?
3. **Lens Type**: Wide-angle (distorts nose/forehead), normal (50mm equivalent), or telephoto (compresses)?

**DISTORTION DETECTION:**
1. **Nose Distortion**: Is the nose appearing LARGER than natural due to wide-angle/close perspective?
2. **Face Width**: Is the face appearing WIDER or NARROWER than natural?
3. **Forehead**: Is the forehead exaggerated or minimized?
4. **Jawline**: Is the jaw distorted by angle?

**CORRECTION NEEDED:**
Based on the detected distortions, what are the TRUE/CORRECTED proportions?
- If nose appears 20% larger due to close wide-angle shot, the TRUE nose is 20% smaller
- If face appears 15% wider, the TRUE face is 15% narrower

Respond in JSON format:
{
  "camera_angle": "description",
  "camera_distance": "close/medium/distant",
  "lens_type": "wide/normal/telephoto",
  "distortions": {
    "nose": "20% enlarged - CORRECT BY REDUCING",
    "face_width": "15% wider - CORRECT BY NARROWING",
    "forehead": "description",
    "jaw": "description"
  },
  "correction_instructions": "When generating, reduce nose size by 20%, narrow face by 15%..."
}"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[img, prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT"],
                    temperature=0.1
                )
            )
            
            # Parse response (simplified - in production use structured output)
            analysis_text = response.text
            logger.info(f"📐 Perspective Analysis Complete")
            
            return {
                "raw_analysis": analysis_text,
                "correction_prompt": self._build_correction_prompt(analysis_text)
            }
            
        except Exception as e:
            logger.error(f"Perspective analysis failed: {e}")
            return {
                "raw_analysis": "No distortion detected",
                "correction_prompt": "Use natural proportions as-is."
            }
    
    def _build_correction_prompt(self, analysis: str) -> str:
        """
        Build a correction prompt from the analysis
        """
        return f"""=== PERSPECTIVE CORRECTION REQUIRED ===

{analysis}

**CRITICAL GENERATION INSTRUCTIONS:**
- DO NOT replicate the distorted proportions from the input photo
- Apply the corrections above to restore TRUE facial geometry
- If the input shows enlarged nose due to camera angle, REDUCE nose size in output
- If the input shows widened face due to lens, NARROW face in output
- Generate based on CORRECTED proportions, not distorted input

**EXAMPLE:** If analysis says "nose 20% too large", make the nose 20% SMALLER than it appears in the photo."""
    
    async def get_corrected_analysis(self, image_path: Path) -> dict:
        """
        Get full corrected facial analysis with perspective compensation
        """
        # Get perspective correction
        perspective = await self.analyze_perspective(image_path)
        
        # Get standard facial analysis
        img = Image.open(image_path)
        prompt = f"""Analyze facial features with PERSPECTIVE CORRECTION applied.

{perspective['correction_prompt']}

Now provide the CORRECTED (not distorted) facial measurements:

**IDENTITY (MUST PRESERVE - NON-NEGOTIABLE):**
1. **RACE/ETHNICITY**: Exact racial and ethnic features (e.g., Black, Asian, Latino, etc.)
2. **SKIN TONE**: Exact skin color (dark brown, light brown, pale, etc.)
3. **GENDER**: Biological sex and gender presentation (male/female, masculine/feminine features)
4. **HAIR TYPE**: Natural hair texture (straight, wavy, curly, kinky, dreads, etc.)
5. **FACIAL STRUCTURE**: Ethnic-specific bone structure and features

**CORRECTED MEASUREMENTS (Geometric):**
1. True nose size/shape (after perspective correction)
2. True face width (after perspective correction)  
3. True facial proportions

**CRITICAL RULE:**
When transforming into an anime character:
- PRESERVE: Race, ethnicity, skin tone, gender, facial structure 100%
- TRANSFORM ONLY: Hair style/color, outfit, accessories to match character
- If the person is BLACK with DREADS, they STAY BLACK with features adapted
- If the person is MALE, they STAY MALE (no gender swap unless explicitly requested)

Provide these details for generation."""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[img, prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT"],
                    temperature=0.1
                )
            )
            
            return {
                "perspective_analysis": perspective['raw_analysis'],
                "corrected_features": response.text,
                "generation_prompt": f"""{perspective['correction_prompt']}

=== CORRECTED FACIAL FEATURES ===
{response.text}

USE THESE CORRECTED PROPORTIONS FOR GENERATION."""
            }
            
        except Exception as e:
            logger.error(f"Corrected analysis failed: {e}")
            return {"generation_prompt": "Use natural proportions."}


# Example usage
async def test_correction():
    corrector = FacialGeometryCorrector(project_id="gifted-cooler-479623-r7")
    
    test_img = Path("C:/Yuki_Local/jesse 1 pic test/20251202_181840.jpg")
    
    logger.info("\n=== Testing Perspective Correction ===")
    result = await corrector.get_corrected_analysis(test_img)
    
    logger.info(f"\nPerspective Analysis:\n{result['perspective_analysis']}")
    logger.info(f"\nCorrected Features:\n{result['corrected_features']}")
    logger.info(f"\nGeneration Prompt:\n{result['generation_prompt']}")

if __name__ == "__main__":
    asyncio.run(test_correction())
