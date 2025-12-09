"""
Yuki Spatial Analyzer - 2D Spatial Understanding for Cosplay
Production-ready object detection and segmentation for costume analysis

Use Cases:
- Costume component detection (outfit breakdown)
- Accessory identification (props, jewelry, weapons)
- Color palette extraction from reference images
- Fabric/material identification
- Segmentation for virtual try-on
- Character reference analysis
- Cosplay accuracy checking

Features:
- Bounding box detection (Gemini 2.0+)
- Segmentation masks (Gemini 2.5+)
- Multilingual labeling
- Custom prompts for specific items
- JSON output parsing
"""

import json
import re
import base64
import io
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Literal, Tuple
from pathlib import Path
from enum import Enum

from google import genai
from google.genai import types
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageColor
import numpy as np


@dataclass
class BoundingBox:
    """2D bounding box with label"""
    label: str
    y1: int  # Top
    x1: int  # Left
    y2: int  # Bottom
    x2: int  # Right
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def normalized(self) -> List[int]:
        """Return normalized coordinates [y1, x1, y2, x2] in 0-1000 range"""
        return [self.y1, self.x1, self.y2, self.x2]


@dataclass
class SegmentationMask:
    """Segmentation mask with bounding box"""
    label: str
    y0: int  # Top (pixel coordinates)
    x0: int  # Left
    y1: int  # Bottom
    x1: int  # Right
    mask: np.ndarray  # [img_height, img_width] with values 0..255
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CostumeAnalysis:
    """Complete costume breakdown"""
    components: List[BoundingBox]
    accessories: List[BoundingBox]
    colors: List[str] = field(default_factory=list)
    materials: List[str] = field(default_factory=list)
    full_text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class AnalysisMode(str, Enum):
    """Analysis modes for different use cases"""
    COSTUME_BREAKDOWN = "costume_breakdown"
    ACCESSORY_DETECTION = "accessory_detection"
    COLOR_ANALYSIS = "color_analysis"
    MATERIAL_IDENTIFICATION = "material_identification"
    REFERENCE_COMPARISON = "reference_comparison"
    ACCURACY_CHECK = "accuracy_check"


class YukiSpatialAnalyzer:
    """
    Spatial understanding for cosplay costume analysis
    
    Powered by Gemini 2.0+ for object detection
    Gemini 2.5+ required for segmentation masks
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: str = "gemini-2.5-flash"
    ):
        """Initialize spatial analyzer"""
        self.client = genai.Client(api_key=api_key)
        self.default_model = default_model
        
        # System instructions for consistent JSON output
        self.bbox_system_instructions = """
Return bounding boxes as a JSON array with labels. Never return masks or code fencing. Limit to 25 objects.
If an object is present multiple times, name them according to their unique characteristic (colors, size, position, unique characteristics, etc.).
"""
    
    def _parse_json(self, json_output: str) -> str:
        """Remove markdown fencing from JSON output"""
        lines = json_output.splitlines()
        for i, line in enumerate(lines):
            if line.strip() in ["```json", "```"]:
                json_output = "\n".join(lines[i+1:])
                json_output = json_output.split("```")[0]
                break
        return json_output.strip()
    
    def _parse_bounding_boxes(
        self,
        json_str: str,
        img_width: int,
        img_height: int
    ) -> List[BoundingBox]:
        """Parse JSON bounding boxes to BoundingBox objects"""
        json_str = self._parse_json(json_str)
        
        boxes = []
        try:
            items = json.loads(json_str)
            for item in items:
                # Normalized coordinates [y1, x1, y2, x2] in 0-1000 range
                norm_coords = item.get("box_2d", [])
                if len(norm_coords) != 4:
                    continue
                
                # Convert to absolute pixel coordinates
                abs_y1 = int(norm_coords[0] / 1000 * img_height)
                abs_x1 = int(norm_coords[1] / 1000 * img_width)
                abs_y2 = int(norm_coords[2] / 1000 * img_height)
                abs_x2 = int(norm_coords[3] / 1000 * img_width)
                
                # Ensure x1 < x2 and y1 < y2
                if abs_x1 > abs_x2:
                    abs_x1, abs_x2 = abs_x2, abs_x1
                if abs_y1 > abs_y2:
                    abs_y1, abs_y2 = abs_y2, abs_y1
                
                boxes.append(BoundingBox(
                    label=item.get("label", "Unknown"),
                    y1=abs_y1,
                    x1=abs_x1,
                    y2=abs_y2,
                    x2=abs_x2,
                    metadata=item
                ))
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing error: {e}")
        
        return boxes
    
    async def analyze_costume_components(
        self,
        image_path: str,
        character_name: Optional[str] = None,
        outfit_focus: Literal["top", "bottom", "full", "accessories"] = "full"
    ) -> CostumeAnalysis:
        """
        Break down costume into components with bounding boxes
        
        Args:
            image_path: Path to cosplay or character reference image
            character_name: Optional character name for context
            outfit_focus: What to focus on
            
        Returns:
            CostumeAnalysis with detected components
        """
        
        prompts = {
            "top": "Detect all upper body costume components (shirt, jacket, vest, tie, collar, sleeves, buttons, etc.)",
            "bottom": "Detect all lower body costume components (pants, skirt, shorts, belt, pockets, etc.)",
            "full": "Detect all visible costume components from head to toe (clothing, accessories, props). Label each piece clearly.",
            "accessories": "Detect only accessories and props (jewelry, belts, bags, weapons, hats, glasses, etc.)"
        }
        
        prompt = prompts[outfit_focus]
        if character_name:
            prompt = f"Analyzing {character_name}'s costume. {prompt}"
        
        # Load and process image
        img = PILImage.open(image_path)
        img.thumbnail([1024, 1024], PILImage.Resampling.LANCZOS)
        width, height = img.size
        
        print(f"🔍 Analyzing costume components ({outfit_focus})...")
        
        response = self.client.models.generate_content(
            model=self.default_model,
            contents=[prompt, img],
            config=types.GenerateContentConfig(
                system_instruction=self.bbox_system_instructions,
                temperature=0.5,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        
        # Parse results
        components = self._parse_bounding_boxes(response.text, width, height)
        
        # Separate into components and accessories
        accessory_keywords = ["jewelry", "belt", "bag", "weapon", "hat", "glasses", "watch", "necklace", "ring"]
        accessories = [
            c for c in components 
            if any(kw in c.label.lower() for kw in accessory_keywords)
        ]
        main_components = [c for c in components if c not in accessories]
        
        return CostumeAnalysis(
            components=main_components,
            accessories=accessories,
            full_text=response.text,
            metadata={
                "character": character_name,
                "focus": outfit_focus,
                "total_items": len(components)
            }
        )
    
    async def extract_color_palette(
        self,
        image_path: str,
        character_name: Optional[str] = None
    ) -> CostumeAnalysis:
        """
        Extract color palette from costume with component mapping
        
        Args:
            image_path: Path to image
            character_name: Optional character name
            
        Returns:
            CostumeAnalysis with color-coded components
        """
        
        prompt = f"""
Detect all costume pieces and label each with its EXACT color shade.

For each item, include in the label:
- Item name
- Specific color (not "blue" but "sapphire blue", "navy blue", etc.)
- Material hint if visible (leather, cotton, silk, metal, etc.)

Example labels:
- "Blazer - Charcoal gray wool"
- "Shirt - Crisp white cotton"
- "Tie - Burgundy silk"
"""
        if character_name:
            prompt = f"Analyzing {character_name}'s costume colors.\n{prompt}"
        
        img = PILImage.open(image_path)
        img.thumbnail([1024, 1024], PILImage.Resampling.LANCZOS)
        width, height = img.size
        
        print(f"🎨 Extracting color palette...")
        
        response = self.client.models.generate_content(
            model=self.default_model,
            contents=[prompt, img],
            config=types.GenerateContentConfig(
                system_instruction=self.bbox_system_instructions,
                temperature=0.5,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        
        components = self._parse_bounding_boxes(response.text, width, height)
        
        # Extract unique colors
        colors = set()
        materials = set()
        for comp in components:
            # Simple extraction - could be enhanced
            label_lower = comp.label.lower()
            if " - " in comp.label:
                desc = comp.label.split(" - ")[1]
                colors.add(desc.split()[0] + " " + desc.split()[1] if len(desc.split()) > 1 else desc.split()[0])
                for mat in ["leather", "cotton", "silk", "metal", "wool", "denim"]:
                    if mat in label_lower:
                        materials.add(mat)
        
        return CostumeAnalysis(
            components=components,
            accessories=[],
            colors=list(colors),
            materials=list(materials),
            full_text=response.text,
            metadata={"character": character_name}
        )
    
    async def compare_cosplay_accuracy(
        self,
        reference_image: str,
        cosplay_image: str,
        character_name: str
    ) -> Dict[str, Any]:
        """
        Compare cosplay photo against character reference
        
        Args:
            reference_image: Official character artwork/screenshot
            cosplay_image: Cosplayer's photo
            character_name: Character name
            
        Returns:
            Comparison analysis with accuracy notes
        """
        
        prompt = f"""
Compare these two images of {character_name}:
1. Reference (official character design)
2. Cosplay recreation

For each major costume component visible in BOTH images, create a bounding box and label it:
- If accurate: "[Component] ✓ (matches reference)"
- If needs improvement: "[Component] ⚠ (difference: [specific detail])"
- If missing: "[Component] ✗ (missing from cosplay)"

Focus on: outfit pieces, colors, accessories, props.
"""
        
        ref_img = PILImage.open(reference_image)
        cos_img = PILImage.open(cosplay_image)
        
        ref_img.thumbnail([512, 512], PILImage.Resampling.LANCZOS)
        cos_img.thumbnail([512, 512], PILImage.Resampling.LANCZOS)
        
        print(f"⚖️ Comparing cosplay accuracy for {character_name}...")
        
        response = self.client.models.generate_content(
            model=self.default_model,
            contents=[prompt, ref_img, cos_img],
            config=types.GenerateContentConfig(
                system_instruction="Return bounding boxes for the COSPLAY image (second image).",
                temperature=0.5,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        
        width, height = cos_img.size
        components = self._parse_bounding_boxes(response.text, width, height)
        
        # Calculate accuracy score
        accurate = len([c for c in components if "✓" in c.label])
        needs_work = len([c for c in components if "⚠" in c.label])
        missing = len([c for c in components if "✗" in c.label])
        total = len(components)
        
        accuracy_score = (accurate / total * 100) if total > 0 else 0
        
        return {
            "accuracy_score": accuracy_score,
            "accurate_components": accurate,
            "needs_improvement": needs_work,
            "missing_components": missing,
            "total_checked": total,
            "components": components,
            "full_analysis": response.text
        }
    
    async def segment_costume_pieces(
        self,
        image_path: str,
        piece_types: List[str] = None
    ) -> List[SegmentationMask]:
        """
        Get segmentation masks for costume pieces (Gemini 2.5+ only)
        
        Args:
            image_path: Path to image
            piece_types: Optional list of specific pieces to segment
            
        Returns:
            List of SegmentationMask objects
        """
        
        if piece_types:
            prompt = f"Give segmentation masks for: {', '.join(piece_types)}. Use descriptive labels."
        else:
            prompt = "Give segmentation masks for all visible costume pieces and accessories. Use descriptive labels."
        
        prompt += ' Output a JSON list where each entry contains the 2D bounding box in "box_2d", the segmentation mask in "mask", and the text label in "label".'
        
        img = PILImage.open(image_path)
        img.thumbnail([1024, 1024], PILImage.Resampling.LANCZOS)
        width, height = img.size
        
        print(f"✂️ Generating segmentation masks...")
        
        response = self.client.models.generate_content(
            model=self.default_model,
            contents=[prompt, img],
            config=types.GenerateContentConfig(
                temperature=0.5,
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        
        # Parse segmentation masks
        masks = self._parse_segmentation_masks(response.text, height, width)
        
        return masks
    
    def _parse_segmentation_masks(
        self,
        json_str: str,
        img_height: int,
        img_width: int
    ) -> List[SegmentationMask]:
        """Parse segmentation masks from JSON response"""
        json_str = self._parse_json(json_str)
        
        masks = []
        try:
            items = json.loads(json_str)
            for item in items:
                # Get bounding box
                raw_box = item.get("box_2d", [])
                if len(raw_box) != 4:
                    continue
                
                abs_y0 = int(raw_box[0] / 1000 * img_height)
                abs_x0 = int(raw_box[1] / 1000 * img_width)
                abs_y1 = int(raw_box[2] / 1000 * img_height)
                abs_x1 = int(raw_box[3] / 1000 * img_width)
                
                if abs_y0 >= abs_y1 or abs_x0 >= abs_x1:
                    continue
                
                # Get mask PNG
                png_str = item.get("mask", "")
                if not png_str.startswith("data:image/png;base64,"):
                    continue
                
                png_str = png_str.removeprefix("data:image/png;base64,")
                png_bytes = base64.b64decode(png_str)
                mask_img = PILImage.open(io.BytesIO(png_bytes))
                
                # Resize mask to match bounding box
                bbox_height = abs_y1 - abs_y0
                bbox_width = abs_x1 - abs_x0
                
                if bbox_height < 1 or bbox_width < 1:
                    continue
                
                mask_img = mask_img.resize((bbox_width, bbox_height), resample=PILImage.Resampling.BILINEAR)
                
                # Create full-size mask array
                np_mask = np.zeros((img_height, img_width), dtype=np.uint8)
                np_mask[abs_y0:abs_y1, abs_x0:abs_x1] = np.array(mask_img)
                
                masks.append(SegmentationMask(
                    label=item.get("label", "Unknown"),
                    y0=abs_y0,
                    x0=abs_x0,
                    y1=abs_y1,
                    x1=abs_x1,
                    mask=np_mask,
                    metadata=item
                ))
        
        except Exception as e:
            print(f"⚠️ Mask parsing error: {e}")
        
        return masks
    
    def visualize_bounding_boxes(
        self,
        image_path: str,
        boxes: List[BoundingBox],
        output_path: Optional[str] = None
    ) -> PILImage.Image:
        """
        Draw bounding boxes on image
        
        Args:
            image_path: Original image path
            boxes: List of BoundingBox objects
            output_path: Optional save path
            
        Returns:
            PIL Image with boxes drawn
        """
        
        img = PILImage.open(image_path)
        img.thumbnail([1024, 1024], PILImage.Resampling.LANCZOS)
        draw = ImageDraw.Draw(img)
        
        colors = ["red", "green", "blue", "yellow", "orange", "pink", "purple", 
                  "cyan", "magenta", "lime", "navy", "teal", "coral", "gold"]
        
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        for i, box in enumerate(boxes):
            color = colors[i % len(colors)]
            
            # Draw rectangle
            draw.rectangle(
                [(box.x1, box.y1), (box.x2, box.y2)],
                outline=color,
                width=3
            )
            
            # Draw label
            draw.text(
                (box.x1 + 8, box.y1 + 6),
                box.label,
                fill=color,
                font=font
            )
        
        if output_path:
            img.save(output_path)
        
        return img


# Example usage
async def demo():
    """Demonstrate spatial analysis capabilities"""
    print("🦊 Yuki Spatial Analyzer Demo\n")
    
    analyzer = YukiSpatialAnalyzer(api_key="YOUR_API_KEY")
    
    # Example 1: Costume breakdown
    print("=" * 50)
    print("1. COSTUME COMPONENT DETECTION")
    print("=" * 50)
    
    analysis = await analyzer.analyze_costume_components(
        image_path="makima_cosplay.jpg",
        character_name="Makima",
        outfit_focus="full"
    )
    
    print(f"\n   Components found: {len(analysis.components)}")
    print(f"   Accessories found: {len(analysis.accessories)}")
    for comp in analysis.components[:5]:
        print(f"   - {comp.label}")
    
    # Example 2: Color palette extraction
    print("\n" + "=" * 50)
    print("2. COLOR PALETTE EXTRACTION")
    print("=" * 50)
    
    colors = await analyzer.extract_color_palette(
        image_path="character_ref.jpg",
        character_name="Makima"
    )
    
    print(f"\n   Colors: {', '.join(colors.colors)}")
    print(f"   Materials: {', '.join(colors.materials)}")
    
    # Example 3: Cosplay accuracy check
    print("\n" + "=" * 50)
    print("3. COSPLAY ACCURACY COMPARISON")
    print("=" * 50)
    
    comparison = await analyzer.compare_cosplay_accuracy(
        reference_image="official_art.jpg",
        cosplay_image="my_cosplay.jpg",
        character_name="Makima"
    )
    
    print(f"\n   Accuracy Score: {comparison['accuracy_score']:.1f}%")
    print(f"   ✓ Accurate: {comparison['accurate_components']}")
    print(f"   ⚠ Needs work: {comparison['needs_improvement']}")
    print(f"   ✗ Missing: {comparison['missing_components']}")
    
    # Example 4: Segmentation (Gemini 2.5+)
    print("\n" + "=" * 50)
    print("4. SEGMENTATION MASKS")
    print("=" * 50)
    
    masks = await analyzer.segment_costume_pieces(
        image_path="cosplay_photo.jpg",
        piece_types=["jacket", "tie", "shirt"]
    )
    
    print(f"\n   Generated {len(masks)} segmentation masks")
    
    print("\n✅ Demo complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo())
