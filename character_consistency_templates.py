"""
Character Consistency System - Glibatree Integration
Advanced character reference generation and consistency management

Based on Glibatree's proven method:
1. Generate dual references (closeup face + full body)
2. Use video model to create asset-ready poses
3. Extract frames for consistent character library
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class MediumTag(Enum):
    """Medium tags for Midjourney prompts"""
    PHOTO = "photo"
    PAINTING = "painting"
    ILLUSTRATION = "illustration"
    DRAWING = "drawing"
    ANIMATED_RENDER = "animated-render"
    VECTOR = "vector"


@dataclass
class CharacterReferenceSpec:
    """Character reference specifications for consistent generation"""
    character_name: str
    anime_title: str
    
    # Physical features
    face_description: str
    hair_description: str
    eye_description: str
    body_type: str
    
    # Outfit details
    outfit_top: str
    outfit_bottom: str
    footwear: str
    accessories: List[str] = field(default_factory=list)
    
    # Personality/Expression
    personality_traits: List[str] = field(default_factory=list)
    signature_expression: str = "confident determined look"
    
    # Style preferences
    art_style: str = "anime style, highly detailed"
    medium: MediumTag = MediumTag.ILLUSTRATION
    background_color: str = "soft gradient background"


class GlibatreePromptGenerator:
    """
    Generate Midjourney prompts using Glibatree's proven methods
    for character consistency
    """
    
    @staticmethod
    def generate_dual_reference_prompt(
        spec: CharacterReferenceSpec
    ) -> str:
        """
        Generate side-by-side reference (closeup + full body)
        
        Template from Glibatree:
        "Side by side {medium} of a closeup face, and full body character design, of
        {character details}
        {background}
        {style}"
        """
        # Left side: closeup face with expression showing all facial details
        closeup_desc = f"{spec.face_description}, {spec.hair_description}, {spec.eye_description}, {spec.signature_expression}"
        
        # Right side: full body ensuring entire anatomy visible
        fullbody_desc = f"full body character design showing {spec.body_type}, wearing {spec.outfit_top}, {spec.outfit_bottom}, {spec.footwear}"
        
        # Add accessories
        if spec.accessories:
            fullbody_desc += f", with {', '.join(spec.accessories)}"
        
        # Construct prompt
        prompt = f"Side by side {spec.medium.value} of a closeup face, and full body character design, of {spec.character_name} from {spec.anime_title}. "
        prompt += f"Left side: {closeup_desc}. "
        prompt += f"Right side: {fullbody_desc}, "
        prompt += f"from head to toe fully visible. "
        prompt += f"{spec.background_color}. "
        prompt += f"{spec.art_style}"
        
        return prompt
    
    @staticmethod
    def generate_video_asset_prompt(
        character_name: str,
        starting_pose: str,
        target_assets: List[str],
        frame_details: Dict[str, str],
        medium: MediumTag = MediumTag.ANIMATED_RENDER
    ) -> str:
        """
        Generate video prompt for extracting character assets
        
        Args:
            character_name: Character identifier
            starting_pose: Initial pose/expression from reference
            target_assets: List of poses/expressions needed
            frame_details: Details about frame edges (top, bottom, sides)
        
        Based on Glibatree template for reference footage generation
        """
        assets_desc = ", ".join(target_assets)
        
        prompt = f"Reference footage of {character_name} striking several {assets_desc}. "
        prompt += f"The character starts by {starting_pose}, "
        prompt += f"then moves into several {assets_desc}, "
        prompt += "the footage freezes as if pausing at key moments where the pose is most picturesque. "
        
        # Add motion descriptions
        prompt += "The character's movements are smooth and natural, "
        prompt += "with fluid transitions between poses. "
        
        # Frame edge descriptions to prevent cropping
        if "top" in frame_details:
            prompt += f"{frame_details['top']}. "
        if "bottom" in frame_details:
            prompt += f"{frame_details['bottom']}. "
        if "left" in frame_details:
            prompt += f"{frame_details['left']}. "
        if "right" in frame_details:
            prompt += f"{frame_details['right']}. "
        
        # Ensure consistent style throughout motion
        prompt += "The animation maintains perfect character consistency, "
        prompt += "with accurate proportions and details throughout. "
        prompt += "Clean reference footage, with sharp and character-accurate motion perfect for pulling assets from."
        
        return prompt
    
    @staticmethod
    def generate_edit_prompt(
        medium: MediumTag,
        edit_description: str,
        edit_details: str,
        surrounding_context: str,
        image_context: str
    ) -> str:
        """
        Generate focused edit prompt for Midjourney Editor
        
        Template:
        "A(n) {medium} of {edit}, with {details}, {context}, while {scene}"
        """
        prompt = f"A {medium.value} of {edit_description}. "
        prompt += f"With {edit_details}. "
        prompt += f"{surrounding_context}. "
        prompt += f"All while {image_context}."
        
        return prompt
    
    @staticmethod
    def generate_grid_refinement_prompt(
        medium: MediumTag,
        shared_elements: str,
        variation_type: str
    ) -> str:
        """
        Generate prompt for refining multiple variations at once
        
        For side-by-side grids with subtle differences
        """
        prompt = f"A side-by-side {medium.value} collection of {shared_elements}. "
        prompt += "Each image shows the same subject with consistent style, "
        prompt += f"duplicated exactly with different {variation_type}."
        
        return prompt


class CosplayReferenceGenerator:
    """
    Complete character reference generation system
    Combines anime character data with Glibatree methods
    """
    
    def __init__(self):
        self.glibatree = GlibatreePromptGenerator()
    
    def create_character_spec_from_anime(
        self,
        character_data: Dict[str, Any],
        anime_data: Dict[str, Any]
    ) -> CharacterReferenceSpec:
        """
        Create character spec from anime database data
        
        Args:
            character_data: Character info from Jikan API
            anime_data: Anime info from Jikan API
        """
        # Extract or infer character details
        # In production, this would use ML/CV to extract visual features
        
        spec = CharacterReferenceSpec(
            character_name=character_data.get("name", ""),
            anime_title=anime_data.get("title", ""),
            face_description="detailed anime face with expressive features",
            hair_description=self._infer_hair_from_text(character_data.get("about", "")),
            eye_description="large expressive anime eyes",
            body_type="anime character proportions",
            outfit_top="signature character outfit top",
            outfit_bottom="signature character outfit bottom",
            footwear="character shoes/boots",
            accessories=[],
            personality_traits=self._extract_personality(character_data.get("about", "")),
            art_style="anime style, cel shaded, highly detailed"
        )
        
        return spec
    
    def _infer_hair_from_text(self, text: str) -> str:
        """Extract hair description from character bio"""
        # Simple keyword matching - would use NER in production
        colors = ["pink", "blue", "blonde", "black", "red", "white", "purple", "green"]
        styles = ["long", "short", "spiky", "wavy", "straight", "curly"]
        
        text_lower = text.lower()
        found_color = next((c for c in colors if c in text_lower), "dark")
        found_style = next((s for s in styles if s in text_lower), "styled")
        
        return f"{found_style} {found_color} hair"
    
    def _extract_personality(self, text: str) -> List[str]:
        """Extract personality traits from bio"""
        traits = []
        keywords = {
            "brave": ["brave", "courageous", "fearless"],
            "kind": ["kind", "gentle", "caring"],
            "determined": ["determined", "resolute", "strong-willed"],
            "cheerful": ["cheerful", "happy", "optimistic"]
        }
        
        text_lower = text.lower()
        for trait, words in keywords.items():
            if any(w in text_lower for w in words):
                traits.append(trait)
        
        return traits or ["confident"]
    
    def generate_reference_set(
        self,
        spec: CharacterReferenceSpec
    ) -> Dict[str, str]:
        """
        Generate complete reference set for character
        
        Returns:
            Dictionary with prompt types and prompts
        """
        prompts = {}
        
        # 1. Dual reference (face + body)
        prompts["dual_reference"] = self.glibatree.generate_dual_reference_prompt(spec)
        
        # 2. Video assets for different expressions
        prompts["expression_cycle"] = self.glibatree.generate_video_asset_prompt(
            character_name=spec.character_name,
            starting_pose="neutral standing pose",
            target_assets=["happy smile", "serious look", "surprised expression", "determined gaze"],
            frame_details={
                "top": f"{spec.hair_description} stays fully visible at top of frame",
                "bottom": f"{spec.footwear} remain visible at bottom with cast shadows",
                "left": "left arm and hand details stay in frame",
                "right": "right arm and hand details stay in frame"
            }
        )
        
        # 3. Action poses video
        prompts["action_poses"] = self.glibatree.generate_video_asset_prompt(
            character_name=spec.character_name,
            starting_pose="standing ready pose",
            target_assets=["running pose", "jumping pose", "fighting stance", "victory pose"],
            frame_details={
                "top": "full head and hair visible",
                "bottom": "feet and ground contact visible",
                "left": "left side of body in frame",
                "right": "right side of body in frame"
            }
        )
        
        # 4. Camera orbit video
        prompts["turnaround"] = self.glibatree.generate_video_asset_prompt(
            character_name=spec.character_name,
            starting_pose="standing in neutral pose",
            target_assets=["front view", "side view", "back view", "three-quarter view"],
            frame_details={
                "top": "top of head remains visible",
                "bottom": "feet remain grounded and visible",
                "left": "character stays centered as camera orbits",
                "right": "character stays centered as camera orbits"
            },
            medium=spec.medium
        )
        
        return prompts
    
    def generate_cosplay_workflow(
        self,
        spec: CharacterReferenceSpec,
        user_face_reference: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate complete cosplay generation workflow
        
        Returns workflow with steps and prompts
        """
        workflow = {
            "character": spec.character_name,
            "anime": spec.anime_title,
            "steps": []
        }
        
        # Step 1: Generate character references
        workflow["steps"].append({
            "step": 1,
            "name": "Generate Character References",
            "prompt": self.glibatree.generate_dual_reference_prompt(spec),
            "action": "Generate in Midjourney and save reference image"
        })
        
        # Step 2: Create asset library via video
        workflow["steps"].append({
            "step": 2,
            "name": "Generate Asset Videos",
            "prompts": self.generate_reference_set(spec),
            "action": "Generate videos and extract key frames for asset library"
        })
        
        # Step 3: Combine user face with character
        if user_face_reference:
            workflow["steps"].append({
                "step": 3,
                "name": "Blend User Face with Character",
                "prompt": f"Full body photo of person cosplaying as {spec.character_name} from {spec.anime_title}, "
                         f"wearing {spec.outfit_top}, {spec.outfit_bottom}, {spec.footwear}, "
                         f"{spec.art_style}, use reference image for facial features and skin tone, "
                         "professional cosplay photography, studio lighting",
                "action": "Use user photo + character reference in Midjourney blend"
            })
        
        # Step 4: Refine and finalize
        workflow["steps"].append({
            "step": 4,
            "name": "Refine Final Cosplay",
            "action": "Use Midjourney Editor to adjust details, enhance costume accuracy, perfect lighting"
        })
        
        return workflow


# Example usage
if __name__ == "__main__":
    # Create spec for popular character
    spec = CharacterReferenceSpec(
        character_name="Makima",
        anime_title="Chainsaw Man",
        face_description="beautiful woman with yellow ringed eyes, pale skin, refined features",
        hair_description="long light red-pink hair worn loose",
        eye_description="distinctive yellow ringed eyes with red-orange irises",
        body_type="tall elegant woman",
        outfit_top="white dress shirt with black tie",
        outfit_bottom="black suit pants",
        footwear="black dress shoes",
        accessories=["multiple earrings on right ear"],
        personality_traits=["mysterious", "commanding", "composed"],
        signature_expression="mysterious smile with calculating gaze",
        art_style="realistic anime style, highly detailed, professional character design",
        medium=MediumTag.ILLUSTRATION
    )
    
    # Generate reference set
    generator = CosplayReferenceGenerator()
    reference_prompts = generator.generate_reference_set(spec)
    
    print("=== Makima Reference Generation Prompts ===\n")
    for prompt_type, prompt in reference_prompts.items():
        print(f"{prompt_type.upper()}:")
        print(f"{prompt}\n")
    
    # Generate complete workflow
    workflow = generator.generate_cosplay_workflow(
        spec,
        user_face_reference="user_selfie.jpg"
    )
    
    print("\n=== Complete Cosplay Workflow ===")
    for step in workflow["steps"]:
        print(f"\nStep {step['step']}: {step['name']}")
        print(f"Action: {step['action']}")
        if "prompt" in step:
            print(f"Prompt: {step['prompt']}")
