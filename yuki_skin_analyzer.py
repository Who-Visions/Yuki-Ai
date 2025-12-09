"""
Yuki Skin Tone Analyzer (Sub-Agent)
Analyzes skin pigmentation to preserve ethnic authenticity in transformations.
Uses async processing to avoid blocking main Yuki workflow.
"""

import asyncio
import logging
import numpy as np
from pathlib import Path
from PIL import Image
from typing import Dict, Tuple
import colorsys

logger = logging.getLogger("YukiSkinAnalyzer")

class YukiSkinAnalyzer:
    """
    Async sub-agent for skin tone analysis
    Preserves ethnic and DNA authenticity in character transformations
    """
    
    def __init__(self):
        # Fitzpatrick Scale Reference (for categorization)
        self.fitzpatrick_ranges = {
            "I": {"name": "Very Fair", "rgb_range": (240, 255), "description": "Pale white, always burns"},
            "II": {"name": "Fair", "rgb_range": (210, 240), "description": "White, usually burns"},
            "III": {"name": "Medium", "rgb_range": (180, 210), "description": "Light brown, sometimes burns"},
            "IV": {"name": "Olive", "rgb_range": (140, 180), "description": "Moderate brown, rarely burns"},
            "V": {"name": "Brown", "rgb_range": (100, 140), "description": "Dark brown, very rarely burns"},
            "VI": {"name": "Deep Brown", "rgb_range": (50, 100), "description": "Deeply pigmented, never burns"}
        }
        logger.info("   🎨 [Skin Analyzer] Sub-Agent Online")
    
    async def analyze_skin_tone(self, image_path: Path) -> Dict:
        """
        Async analysis of skin tone from image
        
        Returns:
            dict with:
                - dominant_rgb: tuple (R, G, B)
                - dominant_hex: str (e.g., "#C8A882")
                - fitzpatrick_type: str (I-VI)
                - category: str (e.g., "Medium", "Brown")
                - undertone: str ("warm", "cool", "neutral")
                - preservation_prompt: str (guidance for transformation)
        """
        try:
            # Run CPU-intensive analysis in executor to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self._analyze_skin_sync, image_path)
            
            logger.info(f"      🎨 Skin: {result['category']} (Type {result['fitzpatrick_type']}) - {result['undertone']} undertone")
            return result
            
        except Exception as e:
            logger.error(f"      ❌ Skin analysis failed: {e}")
            # Fallback to neutral medium tone
            return self._get_fallback_result()
    
    def _analyze_skin_sync(self, image_path: Path) -> Dict:
        """Synchronous skin analysis (runs in executor)"""
        
        # Load image
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        
        # Extract skin tone (simplified approach - analyze center region assuming face)
        # In production, you'd use face detection (cv2/mediapipe) for accuracy
        height, width, _ = img_array.shape
        
        # Sample from center region (likely contains face)
        center_y_start = int(height * 0.25)
        center_y_end = int(height * 0.75)
        center_x_start = int(width * 0.25)
        center_x_end = int(width * 0.75)
        
        face_region = img_array[center_y_start:center_y_end, center_x_start:center_x_end]
        
        # Calculate dominant skin tone
        # Filter out extreme values (likely backgrounds/shadows)
        pixels = face_region.reshape(-1, 3)
        
        # Remove very dark (shadows) and very bright (highlights) pixels
        brightness = np.mean(pixels, axis=1)
        mask = (brightness > 50) & (brightness < 240)
        filtered_pixels = pixels[mask]
        
        if len(filtered_pixels) == 0:
            return self._get_fallback_result()
        
        # Calculate median RGB (more robust than mean)
        dominant_rgb = tuple(np.median(filtered_pixels, axis=0).astype(int))
        
        # Convert to hex
        dominant_hex = "#{:02x}{:02x}{:02x}".format(*dominant_rgb)
        
        # Determine Fitzpatrick type
        avg_brightness = np.mean(dominant_rgb)
        fitzpatrick_type = self._classify_fitzpatrick(avg_brightness)
        
        # Determine undertone
        undertone = self._determine_undertone(dominant_rgb)
        
        # Generate preservation prompt
        preservation_prompt = self._generate_preservation_prompt(
            dominant_rgb, fitzpatrick_type, undertone
        )
        
        return {
            "dominant_rgb": dominant_rgb,
            "dominant_hex": dominant_hex,
            "fitzpatrick_type": fitzpatrick_type,
            "category": self.fitzpatrick_ranges[fitzpatrick_type]["name"],
            "undertone": undertone,
            "preservation_prompt": preservation_prompt
        }
    
    def _classify_fitzpatrick(self, avg_brightness: float) -> str:
        """Classify skin into Fitzpatrick type based on brightness"""
        for fitz_type, info in self.fitzpatrick_ranges.items():
            min_val, max_val = info["rgb_range"]
            if min_val <= avg_brightness <= max_val:
                return fitz_type
        return "III"  # Default to medium
    
    def _determine_undertone(self, rgb: Tuple[int, int, int]) -> str:
        """
        Determine skin undertone (warm/cool/neutral)
        Based on RGB ratios
        """
        r, g, b = rgb
        
        # Convert to HSV for better undertone analysis
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # Warm undertones: higher red/yellow (hue ~0-60 degrees)
        # Cool undertones: higher blue/pink (hue ~180-300 degrees)
        # Neutral: balanced
        
        hue_degrees = h * 360
        
        if hue_degrees < 30 or hue_degrees > 330:
            return "warm"  # Red-orange range
        elif 30 <= hue_degrees < 60:
            return "warm"  # Yellow-orange range
        elif 180 <= hue_degrees < 300:
            return "cool"  # Blue-purple range
        else:
            return "neutral"
    
    def _generate_preservation_prompt(self, rgb: Tuple[int, int, int], 
                                     fitzpatrick: str, undertone: str) -> str:
        """Generate prompt guidance for preserving authentic skin tone"""
        
        category = self.fitzpatrick_ranges[fitzpatrick]["name"]
        r, g, b = rgb
        
        prompt = f"""CRITICAL: Preserve authentic skin tone - {category} complexion (Fitzpatrick Type {fitzpatrick}).
        
Exact skin color reference: RGB({r}, {g}, {b}) with {undertone} undertones.

DO NOT alter skin pigmentation, ethnic features, or melanin levels. The character transformation must maintain:
- Original skin tone and complexion
- Natural ethnic characteristics
- DNA-authentic pigmentation
- {undertone.capitalize()} undertone balance

Apply only the character's styling (hair, outfit, accessories) while keeping the person's authentic skin."""
        
        return prompt
    
    def _get_fallback_result(self) -> Dict:
        """Fallback result if analysis fails"""
        return {
            "dominant_rgb": (200, 168, 130),  # Neutral medium tone
            "dominant_hex": "#C8A882",
            "fitzpatrick_type": "III",
            "category": "Medium",
            "undertone": "neutral",
            "preservation_prompt": "Preserve the person's natural skin tone and ethnic characteristics."
        }
