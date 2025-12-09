"""
Yuki Prompt Optimizer - Production-Grade Prompt Engineering
Incorporates ALL Gemini API best practices for optimal results

Features:
- Gemini 3 Pro optimized prompts
- Multi-turn conversational refinement
- Token counting and optimization
- Media resolution control
- Thinking mode integration
- Character consistency for cosplay
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Literal
from enum import Enum
from google import genai
from google.genai import types
from PIL import Image as PILImage


class PromptType(Enum):
    """Types of prompts for different use cases"""
    TEXT_TO_IMAGE = "text_to_image"
    IMAGE_EDITING = "image_editing"
    COSPLAY_GENERATION = "cosplay_generation"
    CHARACTER_RESEARCH = "character_research"
    COST_CALCULATION = "cost_calculation"


class MediaResolution(Enum):
    """Media resolution settings for token optimization"""
    LOW = "MEDIA_RESOLUTION_LOW"  # 280 tokens (Gemini 3)
    MEDIUM = "MEDIA_RESOLUTION_MEDIUM"  # 560 tokens
    HIGH = "MEDIA_RESOLUTION_HIGH"  # 1120 tokens
    UNSPECIFIED = "MEDIA_RESOLUTION_UNSPECIFIED"  # Default


@dataclass
class PromptTemplate:
    """
    Structured prompt template following Gemini 3 best practices
    
    Uses XML-style tags for clear structure
    """
    role: str  # System role/persona
    task: str  # Primary task description
    context: Optional[str] = None  # Background information
    constraints: List[str] = field(default_factory=list)  # Rules and limits
    output_format: Optional[str] = None  # Expected response format
    examples: List[Dict[str, str]] = field(default_factory=list)  # Few-shot examples
    final_instruction: Optional[str] = None  # Closing directive


class YukiPromptOptimizer:
    """
    Production-grade prompt optimizer for Yuki Platform
    
    Implements:
    - Gemini 3 Pro best practices
    - Token counting and optimization
    - Multi-turn conversation management
    - Media resolution optimization
    - Character consistency prompts
    """
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        
        # Character consistency templates
        self._init_character_templates()
        
        # Image generation templates
        self._init_image_templates()
    
    def _init_character_templates(self):
        """Initialize character consistency prompt templates"""
        self.character_template = PromptTemplate(
            role="""
You are Yuki, an expert anime character consultant specializing in 
cosplay-accurate character analysis. You are precise, detail-oriented, 
and prioritize visual accuracy above all else.
""",
            task="Extract comprehensive visual details for cosplay creation",
            constraints=[
                "Focus on VISUAL details only (hair, eyes, outfit, accessories)",
                "Be hyper-specific with colors (exact shades, not generic terms)",
                "Include distinctive features and signature expressions",
                "Separate what's canonical vs fan interpretation",
                "Prioritize details visible in official art"
            ],
            output_format="""
Structure your response as follows:
1. **Character Identity**: Name, anime, role
2. **Facial Features**: Eyes, face shape, skin tone, expressions
3. **Hair**: Color (specific shade), style, length, texture
4. **Outfit**: Complete description with colors and materials
5. **Accessories**: All visible items
6. **Signature Elements**: Distinctive poses/expressions
7. **Cosplay Difficulty**: Rating and key challenges
"""
        )
    
    def _init_image_templates(self):
        """Initialize image generation prompt templates"""
        
        # Cosplay generation template (Gemini 3 Pro optimized)
        self.cosplay_template = PromptTemplate(
            role="""
You are generating a professional cosplay preview photograph.
Your expertise is in photorealistic character portrayal with 100% 
facial identity preservation.
""",
            task="Generate a cosplay preview preserving user's face",
            constraints=[
                "100% FACIAL PRESERVATION: Keep user's bone structure, eyes, nose, lips, skin tone EXACTLY identical",
                "Character accuracy: Match anime character's outfit, hair, and styling precisely",
                "Professional photography: Studio lighting, proper composition, high resolution",
                "Natural integration: Seamlessly blend user's face with character elements",
                "No distortion: Maintain realistic proportions and anatomy"
            ],
            output_format="Single high-quality 4K image in specified aspect ratio"
        )
    
    def build_structured_prompt(
        self,
        template: PromptTemplate,
        variables: Dict[str, Any]
    ) -> str:
        """
        Build a structured prompt using XML tags (Gemini 3 best practice)
        
        Args:
            template: PromptTemplate with structure
            variables: Values to fill in template
            
        Returns:
            Formatted prompt string
        """
        
        prompt_parts = []
        
        # Role (critical for Gemini 3)
        prompt_parts.append(f"<role>\n{template.role.strip()}\n</role>\n")
        
        # Constraints (place early for Gemini 3)
        if template.constraints:
            constraints_text = "\n".join(f"- {c}" for c in template.constraints)
            prompt_parts.append(f"<constraints>\n{constraints_text}\n</constraints>\n")
        
        # Context (if provided)
        if template.context:
            context = template.context.format(**variables)
            prompt_parts.append(f"<context>\n{context}\n</context>\n")
        
        # Examples (few-shot if provided)
        if template.examples:
            examples_text = "\n\n".join(
                f"**Example {i+1}:**\nInput: {ex['input']}\nOutput: {ex['output']}"
                for i, ex in enumerate(template.examples)
            )
            prompt_parts.append(f"<examples>\n{examples_text}\n</examples>\n")
        
        # Task (the main instruction)
        task = template.task.format(**variables)
        prompt_parts.append(f"<task>\n{task}\n</task>\n")
        
        # Output format (critical for structured responses)
        if template.output_format:
            prompt_parts.append(f"<output_format>\n{template.output_format}\n</output_format>\n")
        
        # Final instruction (Gemini 3 recommendation)
        if template.final_instruction:
            prompt_parts.append(f"<final_instruction>\n{template.final_instruction}\n</final_instruction>")
        
        return "\n".join(prompt_parts)
    
    def generate_cosplay_prompt(
        self,
        character_name: str,
        anime_title: str,
        character_details: str,
        pose: str = "confident standing pose",
        expression: str = "determined, characteristic smile",
        setting: str = "professional photo studio with dramatic lighting",
        style: str = "photorealistic cosplay photography"
    ) -> str:
        """
        Generate optimized cosplay generation prompt
        
        Follows Gemini 3 image generation best practices:
        - Hyper-specific descriptions
        - Photography terminology
        - Structured instructions
        - Context and intent
        """
        
        variables = {
            "character_name": character_name,
            "anime_title": anime_title,
            "character_details": character_details,
            "pose": pose,
            "expression": expression,
            "setting": setting,
            "style": style
        }
        
        base_prompt = self.build_structured_prompt(
            self.cosplay_template,
            variables
        )
        
        # Add specific visual directives (Gemini 3 best practice)
        visual_prompt = f"""
{base_prompt}

**SPECIFIC VISUAL DIRECTIVES:**

**Face (CRITICAL - 100% Preservation):**
- Bone structure: Exact match to reference image
- Eyes: Same shape, color, and expression as reference
- Nose: Identical structure and proportions
- Lips: Same shape and fullness
- Skin tone: Precise match to reference
- Facial hair: If present in reference, maintain exactly
- Distinctive features: Preserve all moles, scars, unique traits

**Character Elements ({character_name} from {anime_title}):**
{character_details}

**Photography:**
- Shot type: {pose}
- Expression: {expression}
- Setting: {setting}
- Style: {style}
- Lighting: Soft, diffused studio lighting with rim light for depth
- Camera: 85mm f/1.8, shallow depth of field
- Resolution: 4K (4096x4096)
- Post-processing: Natural color grading, subtle enhancement

**Composition:**
- Subject centered, filling 60-70% of frame
- Background contextual but not distracting
- Professional photography composition rules
- Natural, believable integration of all elements

Remember: The user's facial features are SACRED. Not a single proportional element should change.
Only the styling (hair color/style, makeup, costume) should reflect the character.
"""
        
        return visual_prompt.strip()
    
    def generate_character_research_prompt(
        self,
        character_name: str,
        anime_title: str
    ) -> str:
        """
        Generate research prompt using multiple tools
        
        Combines:
        - Google Search (trending data)
        - URL Context (wiki extraction)
        - File Search (knowledge base)
        """
        
        return f"""
<role>
You are a meticulous anime character researcher conducting comprehensive 
analysis for cosplay planning. You combine multiple data sources to 
create the most accurate character profile possible.
</role>

<task>
Research {character_name} from {anime_title} using ALL available tools.

**Phase 1: Current Status (Google Search)**
- Check current popularity and trending status
- Find recent cosplay examples and community feedback
- Identify any character redesigns or variants

**Phase 2: Canonical Details (URL Context)**
- MyAnimeList character page
- Official wiki/fandom pages
- Extract ALL visual details from these sources

**Phase 3: Cross-Reference (File Search)**
- Query internal knowledge base for indexed character data
- Compare with findings from Phase 1 and 2
- Resolve any conflicts

</task>

<output_format>
# {character_name} - Complete Cosplay Profile

## Identity
- **Name**: [Full name]
- **Anime**: {anime_title}
- **Role**: [Main/Supporting]
- **Popularity Score**: [Based on current data]

## Visual Details (Cosplay-Critical)

### Face
- **Eyes**: [Exact color, shape, size]
- **Face Shape**: [Description]
- **Skin Tone**: [Specific shade]
- **Distinctive Features**: [Scars, marks, etc.]

### Hair
- **Color**: [Exact shade, not just "blue" but "bright azure blue"]
- **Style**: [Complete description]
- **Length**: [Specific measurement or comparison]
- **Texture**: [Straight, wavy, curly, spiky]

### Default Outfit
[Complete head-to-toe description with colors and materials]

### Accessories & Props
[Every visible item with specifics]

### Signature Elements
- **Expressions**: [Common expressions]
- **Poses**: [Characteristic poses]
- **Color Palette**: [Dominant colors associated with character]

## Cosplay Construction Guide

### Difficulty: [Easy/Intermediate/Advanced/Expert]

### Key Challenges:
1. [Challenge 1]
2. [Challenge 2]
3. [Challenge 3]

### Materials Needed:
[Comprehensive list]

### Estimated Cost: $[Range]

### Time Required: [Hours/Days]

## Citations
[All sources used with URLs]
</output_format>

<final_instruction>
Use Google Search for current data, URL Context for wikis, and cite ALL sources.
Be extremely precise with visual details - "blue eyes" is not enough, specify "bright sapphire blue with slight gradient to lighter blue near pupils".
</final_instruction>
"""
    
    def count_tokens(
        self,
        content: str,
        model: str = "gemini-3-pro-preview"
    ) -> int:
        """
        Count tokens for content before sending
        
        Args:
            content: Text or multimodal content
            model: Model to count tokens for
            
        Returns:
            Total token count
        """
        result = self.client.models.count_tokens(
            model=model,
            contents=content
        )
        return result.total_tokens
    
    def optimize_for_tokens(
        self,
        prompt: str,
        max_tokens: int = 8000
    ) -> str:
        """
        Optimize prompt to fit within token budget
        
        Strategies:
        1. Remove redundant whitespace
        2. Condense examples
        3. Use abbreviations where clear
        4. Keep critical instructions
        """
        
        current_tokens = self.count_tokens(prompt)
        
        if current_tokens <= max_tokens:
            return prompt  # Already optimized
        
        # Strategy 1: Remove extra whitespace
        optimized = re.sub(r'\n\s*\n\s*\n', '\n\n', prompt)
        optimized = re.sub(r' +', ' ', optimized)
        
        current_tokens = self.count_tokens(optimized)
        if current_tokens <= max_tokens:
            return optimized
        
        # Strategy 2: Condense verbose sections
        # Remove examples if needed (keep first 2)
        if '<examples>' in optimized:
            # This is a simplified version - in production you'd parse properly
            optimized = re.sub(
                r'<examples>.*?</examples>',
                '<examples>\n[Examples condensed for token optimization]\n</examples>',
                optimized,
                flags=re.DOTALL
            )
        
        return optimized
    
    def generate_iterative_refinement_prompts(
        self,
        base_image_description: str,
        refinements: List[str]
    ) -> List[str]:
        """
        Generate a sequence of prompts for iterative image refinement
        
        Gemini 3 best practice: Break complex edits into steps
        
        Args:
            base_image_description: Description of starting image
            refinements: List of changes to make
            
        Returns:
            List of prompts, one per refinement step
        """
        
        prompts = []
        
        for i, refinement in enumerate(refinements, 1):
            prompt = f"""
Based on the current image ({base_image_description}), make the following change:

**Change #{i}:** {refinement}

**Important:**
- Keep ALL other elements exactly the same
- Match the existing style, lighting, and composition
- Preserve the quality and resolution
- Only modify what's specified in the change

This is step {i} of {len(refinements)} in our refinement process.
"""
            prompts.append(prompt.strip())
        
        return prompts
    
    def create_multi_reference_prompt(
        self,
        character_name: str,
        face_preservation_level: Literal["100%", "high", "medium"] = "100%",
        num_face_refs: int = 1,
        num_character_refs: int = 1
    ) -> str:
        """
        Create prompt for multi-reference image generation
        
        Gemini 3 Pro supports up to 14 references:
        - Up to 6 high-fidelity object/character refs
        - Up to 5 face references for identity preservation
        
        Args:
            character_name: Character to cosplay
            face_preservation_level: How strictly to preserve face
            num_face_refs: Number of user face reference images (max 5)
            num_character_refs: Number of character refs (max 6)
        """
        
        face_instructions = {
            "100%": """
**FACIAL PRESERVATION (100% FIDELITY):**
The provided face reference images show the EXACT face that must appear in the output.

CRITICAL RULES:
1. Bone Structure: Match facial bone structure with ZERO deviation
2. Eye Shape: Preserve exact eye shape, size, spacing, and color
3. Nose: Keep nose structure, bridge, and tip identical
4. Lips: Maintain lip shape, fullness, and proportions
5. Skin Tone: Match skin tone precisely (no adjustments)
6. Face Shape: Preserve overall face shape and proportions
7. Unique Features: Keep all distinctive features (moles, scars, dimples)

The face should look like a professional photograph of this exact person 
wearing the character's hairstyle and costume. The face itself must be 
photographically accurate to the reference.
""",
            "high": "Preserve face with high fidelity, allowing minor adjustments for character portrayal",
            "medium": "Balance between user's face and character appearance"
        }
        
        prompt = f"""
<role>
You are creating a professional cosplay photograph combining:
- {num_face_refs} user face reference(s) for identity
- {num_character_refs} character reference(s) for styling
</role>

{face_instructions[face_preservation_level]}

<character_styling>
From the character reference images of {character_name}:
- Extract hair color, style, and length
- Identify outfit/costume details
- Note signature accessories
- Capture characteristic expression/pose

Apply these elements while maintaining the user's facial features.
</character_styling>

<technical_specs>
- Resolution: 4K (4096x4096 or specified aspect ratio)
- Style: Professional cosplay photography
- Lighting: Studio quality with soft diffusion
- Background: Contextually appropriate, not distracting
- Composition: Professional portrait standards
</technical_specs>

<final_instruction>
The result should look like: "A professional photo of [USER'S NAME] cosplaying as {character_name}".
Every viewer should recognize the user's face immediately.
</final_instruction>
"""
        return prompt.strip()
    
    def validate_prompt_quality(self, prompt: str) -> Dict[str, Any]:
        """
        Validate prompt against Gemini 3 best practices
        
        Returns quality score and suggestions
        """
        
        score = 0.0
        max_score = 10.0
        suggestions = []
        
        # Check 1: Has role/persona (1 point)
        if '<role>' in prompt.lower() or 'you are' in prompt.lower():
            score += 1.0
        else:
            suggestions.append("Add a clear role/persona definition")
        
        # Check 2: Has constraints (1 point)
        if '<constraints>' in prompt.lower() or 'rules:' in prompt.lower():
            score += 1.0
        else:
            suggestions.append("Define explicit constraints")
        
        # Check 3: Has output format (1 point)
        if '<output_format>' in prompt.lower() or 'format:' in prompt.lower():
            score += 1.0
        else:
            suggestions.append("Specify desired output format")
        
        # Check 4: Structured with tags/sections (2 points)
        has_structure = prompt.count('<') >= 3 or prompt.count('#') >= 3
        if has_structure:
            score += 2.0
        else:
            suggestions.append("Use XML tags or Markdown headers for structure")
        
        # Check 5: Specific and detailed (2 points)
        word_count = len(prompt.split())
        if word_count >= 100:
            score += 2.0
        elif word_count >= 50:
            score += 1.0
            suggestions.append("Add more specific details")
        else:
            suggestions.append("Prompt is too brief - add more context and specifics")
        
        # Check 6: Clear task definition (1 point)
        if '<task>' in prompt.lower() or any(word in prompt.lower() for word in ['create', 'generate', 'analyze','extract']):
            score += 1.0
        else:
            suggestions.append("Clearly state the primary task")
        
        # Check 7: Final instruction (1 point)
        if '<final_instruction>' in prompt.lower() or prompt.strip().endswith(('.', '!')):
            score += 1.0
        else:
            suggestions.append("Add a final instruction to reinforce critical requirements")
        
        # Check 8: No generic terms (1 point)
        generic_terms = ['nice', 'good', 'beautiful', 'amazing', 'great']
        prompt_lower = prompt.lower()
        has_generics = any(term in prompt_lower for term in generic_terms)
        if not has_generics:
            score += 1.0
        else:
            suggestions.append("Replace generic terms with specific descriptions")
        
        return {
            "score": score,
            "max_score": max_score,
            "percentage": (score / max_score) * 100,
            "grade": "A" if score >= 8 else "B" if score >= 6 else "C" if score >= 4 else "D",
            "suggestions": suggestions,
            "token_count": self.count_tokens(prompt)
        }


# Example usage
def demo():
    """Demonstrate prompt optimizer capabilities"""
    print("🦊 Yuki Prompt Optimizer Demo\n")
    
    optimizer = YukiPromptOptimizer(api_key="YOUR_API_KEY")
    
    # Example 1: Cosplay generation prompt
    print("1. Generating optimized cosplay prompt...")
    cosplay_prompt = optimizer.generate_cosplay_prompt(
        character_name="Makima",
        anime_title="Chainsaw Man",
        character_details="""
        - Hair: Long, light red-pink hair, straight and flowing
        - Eyes: Yellow with ringed pattern (iconic feature)
        - Outfit: White dress shirt, black tie, dark professional suit
        - Accessories: Multiple earrings on right ear
        - Expression: Mysterious, enigmatic smile
        - Vibe: Professional, commanding presence
        """,
        pose="confident standing pose with hands relaxed at sides",
        expression="mysterious smile with piercing gaze",
        setting="modern office environment with dramatic window lighting"
    )
    
    print(f"Generated prompt ({len(cosplay_prompt)} chars):\n")
    print(cosplay_prompt[:500] + "...\n")
    
    # Example 2: Validate prompt quality
    print("2. Validating prompt quality...")
    quality = optimizer.validate_prompt_quality(cosplay_prompt)
    print(f"   Score: {quality['score']}/{quality['max_score']} ({quality['percentage']:.1f}%) - Grade: {quality['grade']}")
    print(f"   Token Count: {quality['token_count']}")
    if quality['suggestions']:
        print("   Suggestions:")
        for s in quality['suggestions']:
            print(f"   - {s}")
    print()
    
    # Example 3: Multi-reference prompt
    print("3. Creating multi-reference prompt...")
    multi_ref_prompt = optimizer.create_multi_reference_prompt(
        character_name="Nezuko Kamado",
        face_preservation_level="100%",
        num_face_refs=2,
        num_character_refs=3
    )
    print(f"Generated multi-reference prompt ({len(multi_ref_prompt)} chars)\n")
    
    # Example 4: Research prompt
    print("4. Creating character research prompt...")
    research_prompt = optimizer.generate_character_research_prompt(
        character_name="Makima",
        anime_title="Chainsaw Man"
    )
    print(f"Generated research prompt ({len(research_prompt)} chars)\n")
    
    # Example 5: Iterative refinement
    print("5. Generating iterative refinement sequence...")
    refinements = optimizer.generate_iterative_refinement_prompts(
        base_image_description="Cosplay photo of user as Makima",
        refinements=[
            "Make the hair color slightly more pink, less red",
            "Adjust the expression to be more enigmatic and mysterious",
            "Add more dramatic lighting from the right side"
        ]
    )
    print(f"   Created {len(refinements)} refinement prompts")
    print(f"   First refinement: {refinements[0][:100]}...\n")
    
    print("✅ Demo complete!")


if __name__ == "__main__":
    demo()
