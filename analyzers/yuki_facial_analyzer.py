"""
Yuki Facial Features Analyzer (Multi-Agent System)
Modular analysis of facial features to preserve authentic characteristics.
Each feature analyzed by separate algorithm, combined for final output.
"""

import asyncio
import logging
import numpy as np
from pathlib import Path
from PIL import Image
from typing import Dict, List
from google import genai
from google.genai import types

logger = logging.getLogger("YukiFacialAnalyzer")

class YukiFacialAnalyzer:
    """
    Multi-agent system for comprehensive facial feature analysis
    Preserves: Hair, Eyes, Nose, Mouth, Face Shape
    """
    
    def __init__(self, project_id: str = "gifted-cooler-479623-r7"):
        self.project_id = project_id
        self.model_id = "gemini-3-pro-preview"  # Analysis model
        
        # Initialize Gemini client for feature analysis
        try:
            self.client = genai.Client(
                vertexai=True,
                project=project_id,
                location="global"
            )
            logger.info("   🔬 [Facial Analyzer] Multi-Agent System Online")
        except Exception as e:
            logger.error(f"   ❌ [Facial Analyzer] Failed to initialize: {e}")
            self.client = None
    
    async def analyze_all_features(self, image_path: Path) -> Dict:
        """
        Run all feature analyzers in parallel (async)
        
        Returns:
            dict with keys:
                - hair: dict (color, texture, length, style)
                - eyes: dict (color, shape, size)
                - nose: dict (shape, bridge, tip)
                - mouth: dict (lip_shape, size)
                - face_shape: dict (shape, jawline, cheekbones)
                - body: dict (build, height_estimate, proportions)
                - combined_prompt: str (unified preservation instructions)
        """
        if not self.client:
            return self._get_fallback_features()
        
        try:
            # Load image once
            img = Image.open(image_path)
            
            # Run all analyzers in parallel for speed
            hair_task = self._analyze_hair(img)
            eyes_task = self._analyze_eyes(img)
            nose_task = self._analyze_nose(img)
            mouth_task = self._analyze_mouth(img)
            face_task = self._analyze_face_shape(img)
            body_task = self._analyze_body_composition(img)
            gender_task = self._analyze_gender(img)
            
            # Await all tasks concurrently
            hair, eyes, nose, mouth, face_shape, body, gender = await asyncio.gather(
                hair_task, eyes_task, nose_task, mouth_task, face_task, body_task, gender_task,
                return_exceptions=True
            )
            
            # Handle any failures
            hair = hair if not isinstance(hair, Exception) else {"color": "natural", "texture": "standard"}
            eyes = eyes if not isinstance(eyes, Exception) else {"color": "natural", "shape": "standard"}
            nose = nose if not isinstance(nose, Exception) else {"shape": "standard"}
            mouth = mouth if not isinstance(mouth, Exception) else {"lip_shape": "standard"}
            face_shape = face_shape if not isinstance(face_shape, Exception) else {"shape": "oval"}
            body = body if not isinstance(body, Exception) else {"build": "average", "proportions": "balanced"}
            gender = gender if not isinstance(gender, Exception) else {"detected": "neutral", "confidence": "low"}
            
            # Build combined preservation prompt
            combined_prompt = self._build_combined_prompt(hair, eyes, nose, mouth, face_shape, body, gender)
            
            logger.info(f"      🔬 Features: Gender({gender.get('detected', 'N/A')}), Body({body.get('build', 'N/A')})")
            
            return {
                "hair": hair,
                "eyes": eyes,
                "nose": nose,
                "mouth": mouth,
                "face_shape": face_shape,
                "body": body,
                "gender": gender,
                "combined_prompt": combined_prompt
            }
            
        except Exception as e:
            logger.error(f"      ❌ Facial analysis failed: {e}")
            return self._get_fallback_features()
    
    async def _analyze_hair(self, img: Image.Image) -> Dict:
        """Analyze hair characteristics"""
        prompt = """Analyze ONLY the hair in this image. Provide:
1. Primary color (e.g., "black", "brown", "blonde", "red", "gray", specific shades)
2. Texture (e.g., "straight", "wavy", "curly", "coily")
3. Length (e.g., "short", "medium", "long")
4. Style notes (e.g., "natural", "styled", specific cut)

Respond in JSON:
{
    "color": "primary color",
    "texture": "texture type",
    "length": "length",
    "style": "style notes"
}"""
        
        result = await self._query_gemini(img, prompt)
        return result if result else {"color": "natural", "texture": "standard", "length": "medium", "style": "natural"}
    
    async def _analyze_eyes(self, img: Image.Image) -> Dict:
        """Analyze eye characteristics"""
        prompt = """Analyze ONLY the eyes in this image. Provide:
1. Eye color (e.g., "brown", "blue", "green", "hazel", specific shade)
2. Eye shape (e.g., "almond", "round", "hooded", "monolid")
3. Size relative to face (e.g., "small", "medium", "large")

Respond in JSON:
{
    "color": "eye color",
    "shape": "eye shape",
    "size": "relative size"
}"""
        
        result = await self._query_gemini(img, prompt)
        return result if result else {"color": "brown", "shape": "almond", "size": "medium"}
    
    async def _analyze_nose(self, img: Image.Image) -> Dict:
        """Analyze nose structure"""
        prompt = """Analyze ONLY the nose in this image. Provide:
1. Overall shape (e.g., "straight", "aquiline", "button", "wide", "narrow")
2. Bridge type (e.g., "high", "medium", "low", "flat")
3. Tip shape (e.g., "rounded", "pointed", "bulbous")

Respond in JSON:
{
    "shape": "overall shape",
    "bridge": "bridge type",
    "tip": "tip shape"
}"""
        
        result = await self._query_gemini(img, prompt)
        return result if result else {"shape": "standard", "bridge": "medium", "tip": "rounded"}
    
    async def _analyze_mouth(self, img: Image.Image) -> Dict:
        """Analyze mouth and lip characteristics"""
        prompt = """Analyze ONLY the mouth/lips in this image. Provide:
1. Lip shape (e.g., "full", "thin", "medium", "heart-shaped")
2. Lip size (e.g., "small", "medium", "large")
3. Mouth width (e.g., "narrow", "medium", "wide")

Respond in JSON:
{
    "lip_shape": "lip shape",
    "size": "lip size",
    "width": "mouth width"
}"""
        
        result = await self._query_gemini(img, prompt)
        return result if result else {"lip_shape": "medium", "size": "medium", "width": "medium"}
    
    async def _analyze_face_shape(self, img: Image.Image) -> Dict:
        """Analyze overall face structure"""
        prompt = """Analyze the overall face shape in this image. Provide:
1. Face shape (e.g., "oval", "round", "square", "heart", "diamond", "oblong")
2. Jawline (e.g., "defined", "soft", "angular", "rounded")
3. Cheekbone structure (e.g., "high", "medium", "low", "prominent")

Respond in JSON:
{
    "shape": "face shape",
    "jawline": "jawline type",
    "cheekbones": "cheekbone structure"
}"""
        
        result = await self._query_gemini(img, prompt)
        return result if result else {"shape": "oval", "jawline": "soft", "cheekbones": "medium"}
    
    async def _analyze_body_composition(self, img: Image.Image) -> Dict:
        """Analyze body type and proportions"""
        prompt = """Analyze the body composition visible in this image. Provide:
1. Build type (e.g., "slim/petite", "athletic", "average", "muscular", "curvy", "plus-size")
2. Visible proportions (e.g., "balanced", "top-heavy", "bottom-heavy", "hourglass", "rectangular")
3. Relative height (if full body visible: "short", "average", "tall"; if only upper body: "proportional")
4. Body confidence notes (e.g., "toned", "soft", "strong", "natural")

Respond in JSON:
{
    "build": "build type",
    "proportions": "proportion type",
    "height_estimate": "height category",
    "notes": "body confidence notes"
}"""
        
        result = await self._query_gemini(img, prompt)
        return result if result else {"build": "average", "proportions": "balanced", "height_estimate": "proportional", "notes": "natural"}
    
    async def _analyze_gender(self, img: Image.Image) -> Dict:
        """Analyze apparent gender presentation"""
        prompt = """Analyze the apparent gender presentation in this image. Provide:
1. Detected gender (e.g., "male", "female", "androgynous")
2. Key gender markers (e.g., "facial structure", "hair style", "clothing")
3. Confidence (high/medium/low)

Respond in JSON:
{
    "detected": "male/female/androgynous",
    "markers": "key markers",
    "confidence": "confidence level"
}"""
        
        result = await self._query_gemini(img, prompt)
        return result if result else {"detected": "neutral", "markers": "ambiguous", "confidence": "low"}

    async def _query_gemini(self, img: Image.Image, prompt: str) -> Dict:
        """Query Gemini for feature analysis"""
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[img, prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT"]
                )
            )
            
            # Parse JSON response
            import json
            response_text = response.text.strip()
            
            # Extract JSON from response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            return json.loads(response_text)
            
        except Exception as e:
            logger.warning(f"      ⚠️ Feature query failed: {e}")
            return None

    def _build_combined_prompt(self, hair: Dict, eyes: Dict, nose: Dict, 
                               mouth: Dict, face_shape: Dict, body: Dict, gender: Dict) -> str:
        """Build unified preservation prompt from all features"""
        
        prompt = f"""PRESERVE AUTHENTIC FACIAL & BODY FEATURES:

👤 Gender Presentation:
- Apparent Gender: {gender.get('detected', 'neutral')}
- Markers: {gender.get('markers', 'natural')}

🎭 Face Structure:
- Face shape: {face_shape.get('shape', 'natural')}
- Jawline: {face_shape.get('jawline', 'natural')}
- Cheekbones: {face_shape.get('cheekbones', 'natural')}

👁️ Eyes:
- Color: {eyes.get('color', 'natural')}
- Shape: {eyes.get('shape', 'natural')}
- Size: {eyes.get('size', 'natural')}

👃 Nose:
- Shape: {nose.get('shape', 'natural')}
- Bridge: {nose.get('bridge', 'natural')}
- Tip: {nose.get('tip', 'natural')}

👄 Mouth:
- Lip shape: {mouth.get('lip_shape', 'natural')}
- Lip size: {mouth.get('size', 'natural')}
- Width: {mouth.get('width', 'natural')}

💪 Body Composition:
- Build: {body.get('build', 'natural')}
- Proportions: {body.get('proportions', 'balanced')}
- Height: {body.get('height_estimate', 'natural')}
- Notes: {body.get('notes', 'natural')}

💇 Hair (can be transformed to character):
- Current: {hair.get('color', 'natural')} {hair.get('texture', 'natural')} hair, {hair.get('length', 'medium')} length
- Style as character requires, but maintain hair texture authenticity

CRITICAL PRESERVATION RULES:
1. Maintain ALL facial proportions and bone structure
2. PRESERVE body type - DO NOT make slim people curvy, DO NOT make plus-size people slim
3. PRESERVE height proportions - DO NOT alter apparent height/body length
4. PRESERVE build - DO NOT make skinny people muscular or vice versa
5. PRESERVE GENDER IDENTITY (Rule 63 Protocol):
   - Detected User Gender: {gender.get('detected', 'neutral')}
   - IF User is Female AND Character is Male -> GENERATE FEMALE VERSION of the character (Rule 63). Adapt the male character's outfit/style to fit a female body while keeping the user's female face/body.
   - IF User is Male AND Character is Female -> GENERATE MALE VERSION of the character (Rule 63). Adapt the female character's outfit/style to fit a male body while keeping the user's male face/body.
   - IF Genders match -> Proceed with standard cosplay transformation.
6. ONLY transform hair style/color, outfit, and accessories to match character
7. Character's outfit should FIT the person's actual body type, not change their body"""
        
        return prompt
    
    def _get_fallback_features(self) -> Dict:
        """Fallback if analysis fails"""
        return {
            "hair": {"color": "natural", "texture": "natural", "length": "medium", "style": "natural"},
            "eyes": {"color": "natural", "shape": "almond", "size": "medium"},
            "nose": {"shape": "natural", "bridge": "medium", "tip": "natural"},
            "mouth": {"lip_shape": "natural", "size": "medium", "width": "medium"},
            "face_shape": {"shape": "oval", "jawline": "natural", "cheekbones": "natural"},
            "body": {"build": "average", "proportions": "balanced", "height_estimate": "proportional", "notes": "natural"},
            "gender": {"detected": "neutral", "markers": "ambiguous", "confidence": "low"},
            "combined_prompt": "Preserve all natural facial features, body proportions, gender presentation, and physique."
        }
