"""
Yuki Age Estimator
Uses Gemini 3 Pro Preview to analyze user photos and estimate age.
Ensures age-appropriate character transformations.
"""

import logging
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

logger = logging.getLogger("YukiAgeEstimator")

class YukiAgeEstimator:
    """Estimates age from user photos to ensure appropriate character matching"""
    
    def __init__(self, project_id: str = "gifted-cooler-479623-r7"):
        self.project_id = project_id
        self.model_id = "gemini-3-pro-preview"  # Non-image variant for analysis
        
        # Initialize Gemini client (global routing for Gemini 3)
        try:
            self.client = genai.Client(
                vertexai=True,
                project=project_id,
                location="global"
            )
            logger.info("   🧠 [Age Estimator] Gemini 3 Pro Online")
        except Exception as e:
            logger.error(f"   ❌ [Age Estimator] Failed to initialize: {e}")
            self.client = None
    
    async def estimate_age(self, image_path: Path) -> dict:
        """
        Analyze image and estimate age range
        
        Returns:
            dict with keys:
                - estimated_age: int (midpoint of range)
                - age_range: str (e.g., "18-25", "30-40")
                - confidence: str ("high", "medium", "low")
                - category: str ("child", "teen", "young_adult", "adult", "senior")
        """
        if not self.client:
            logger.warning("   ⚠️ Age estimator offline, using default age 25")
            return {
                "estimated_age": 25,
                "age_range": "20-30",
                "confidence": "low",
                "category": "young_adult"
            }
        
        try:
            # Load image
            img = Image.open(image_path)
            
            # Analyze age with Gemini
            prompt = """Analyze this person's age and provide the following information:
1. Estimated age range (e.g., "18-25", "30-40")
2. Confidence level (high/medium/low)
3. Age category (child/teen/young_adult/adult/senior)

Respond ONLY in this exact JSON format:
{
    "age_range": "XX-XX",
    "confidence": "high/medium/low",
    "category": "child/teen/young_adult/adult/senior"
}"""
            
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[img, prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT"]
                )
            )
            
            # Parse response
            import json
            response_text = response.text.strip()
            
            # Extract JSON from response (handle code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            
            # Calculate midpoint age
            age_range = result.get("age_range", "20-30")
            min_age, max_age = map(int, age_range.split("-"))
            estimated_age = (min_age + max_age) // 2
            
            result["estimated_age"] = estimated_age
            result["age_range"] = age_range
            
            logger.info(f"      🎂 Estimated Age: {estimated_age} ({age_range}) - {result['category']}")
            
            return result
            
        except Exception as e:
            logger.error(f"      ❌ Age estimation failed: {e}")
            # Fallback to default
            return {
                "estimated_age": 25,
                "age_range": "20-30",
                "confidence": "low",
                "category": "young_adult"
            }
    
    def get_age_appropriate_instruction(self, age_info: dict, character: str) -> str:
        """
        Generate age-appropriate transformation instruction
        
        Args:
            age_info: dict from estimate_age()
            character: target character name
            
        Returns:
            str: Age-appropriate instruction to append to prompt
        """
        category = age_info["category"]
        estimated_age = age_info["estimated_age"]
        
        if category == "child":
            return f"Depict as a child version (age {estimated_age}) of {character}. Maintain child-like facial features and proportions."
        elif category == "teen":
            return f"Depict as a teenage version (age {estimated_age}) of {character}. Maintain youthful teenage features."
        elif category == "young_adult":
            return f"Depict as a young adult version (age {estimated_age}) of {character}. Maintain young adult features and energy."
        elif category == "adult":
            return f"Depict as an adult version (age {estimated_age}) of {character}. Maintain mature adult features."
        elif category == "senior":
            return f"Depict as a mature version (age {estimated_age}) of {character}. Maintain dignified mature features."
        else:
            return f"Maintain the apparent age of approximately {estimated_age} years old."
