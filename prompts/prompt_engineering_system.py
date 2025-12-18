"""
Prompt Engineering System - SaaS Grade
Advanced prompt optimization and management system for Nano Banana Pro
Features:
- Prompt templates with variable interpolation
- Quality scoring and optimization
- A/B testing support
- Prompt versioning
- Category-based organization
- Cloud storage integration
"""

import hashlib
import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptCategory(Enum):
    """Prompt categories based on Nano Banana Pro guide"""
    PRODUCT_PHOTOGRAPHY = "product_photography"
    MANGA_ANIME = "manga_anime"
    PHOTO_EDITING = "photo_editing"
    CHARACTER_COSPLAY = "character_cosplay"
    PORTRAIT = "portrait"
    BRANDING = "branding"
    UI_UX = "ui_ux"
    INFOGRAPHICS = "infographics"
    GENERAL = "general"


class PromptComplexity(Enum):
    """Prompt complexity levels"""
    BASIC = "basic"
    DETAILED = "detailed"
    ADVANCED = "advanced"


@dataclass
class PromptComponent:
    """
    Individual prompt components based on Nano Banana Pro best practices
    """
    subject: Optional[str] = None  # Who/what in the image
    composition: Optional[str] = None  # Camera angles, framing
    action: Optional[str] = None  # What's happening
    setting: Optional[str] = None  # Location/environment
    style: Optional[str] = None  # Art style, look and feel
    editing_instructions: Optional[str] = None  # Specific edits
    aspect_ratio: Optional[str] = None  # Canvas size
    camera_settings: Optional[str] = None  # Lens, lighting
    text_rendering: Optional[str] = None  # Text in image
    reference_inputs: Optional[List[str]] = None  # Reference images
    
    def to_prompt(self, complexity: PromptComplexity = PromptComplexity.DETAILED) -> str:
        """Generate prompt string from components"""
        parts = []
        
        # Basic components (always included)
        if self.subject:
            parts.append(self.subject)
        if self.action:
            parts.append(self.action)
        if self.setting:
            parts.append(f"in {self.setting}")
        
        # Medium complexity additions
        if complexity != PromptComplexity.BASIC:
            if self.composition:
                parts.append(f"shot: {self.composition}")
            if self.style:
                parts.append(f"style: {self.style}")
        
        # Advanced complexity additions
        if complexity == PromptComplexity.ADVANCED:
            if self.camera_settings:
                parts.append(f"camera: {self.camera_settings}")
            if self.aspect_ratio:
                parts.append(f"aspect ratio: {self.aspect_ratio}")
            if self.text_rendering:
                parts.append(f"text: {self.text_rendering}")
        
        # Editing instructions (always at end if present)
        if self.editing_instructions:
            parts.append(f"| {self.editing_instructions}")
        
        return ", ".join(parts)


@dataclass
class PromptTemplate:
    """Reusable prompt template with variables"""
    id: str
    name: str
    category: PromptCategory
    template: str
    variables: List[str] = field(default_factory=list)
    description: str = ""
    examples: List[Dict[str, str]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    quality_score: float = 0.0
    usage_count: int = 0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def render(self, **kwargs) -> str:
        """Render template with provided variables"""
        prompt = self.template
        for var, value in kwargs.items():
            prompt = prompt.replace(f"{{{var}}}", str(value))
        
        # Check if all variables were replaced
        remaining = re.findall(r'\{([^}]+)\}', prompt)
        if remaining:
            logger.warning(f"Template has unfilled variables: {remaining}")
        
        return prompt
    
    def generate_id(self) -> str:
        """Generate unique ID for template"""
        content = f"{self.name}:{self.template}:{self.category.value}"
        return hashlib.md5(content.encode()).hexdigest()[:12]


@dataclass
class GeneratedPrompt:
    """A generated prompt with metadata"""
    prompt: str
    template_id: Optional[str] = None
    category: Optional[PromptCategory] = None
    variables: Dict[str, str] = field(default_factory=dict)
    quality_score: float = 0.0
    character_id: Optional[int] = None  # Link to anime character
    anime_id: Optional[int] = None  # Link to anime
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def cache_key(self) -> str:
        """Generate cache key"""
        return hashlib.md5(self.prompt.encode()).hexdigest()


class PromptEngineering:
    """
    Advanced prompt engineering and optimization system
    
    Features:
    - Template management
    - Variable interpolation
    - Quality scoring
    - Optimization suggestions
    - A/B testing support
    """
    
    def __init__(self, storage_backend: Optional[Any] = None):
        """
        Initialize prompt engineering system
        
        Args:
            storage_backend: Optional cloud storage (Firestore, etc.)
        """
        self.storage = storage_backend
        self.templates: Dict[str, PromptTemplate] = {}
        self.generated: Dict[str, GeneratedPrompt] = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default Nano Banana Pro templates"""
        
        # Character Cosplay Templates
        self.add_template(PromptTemplate(
            id="cosplay_anime_character",
            name="Anime Character Cosplay",
            category=PromptCategory.CHARACTER_COSPLAY,
            template="{character_name} from {anime_title}, {pose}, {facial_expression}, wearing {outfit_description}, {setting}, {lighting}, shot: {composition}, style: {art_style}, ultra detailed, 4K quality",
            variables=["character_name", "anime_title", "pose", "facial_expression", "outfit_description", "setting", "lighting", "composition", "art_style"],
            description="Generate cosplay photos matching anime character appearance",
            tags=["cosplay", "anime", "character", "portrait"],
            examples=[{
                "character_name": "Nezuko Kamado",
                "anime_title": "Demon Slayer",
                "pose": "confident stance",
                "facial_expression": "determined look",
                "outfit_description": "pink kimono with bamboo muzzle",
                "setting": "bamboo forest at dusk",
                "lighting": "soft golden hour light",
                "composition": "medium shot, f/2.8",
                "art_style": "realistic anime style"
            }]
        ))
        
        # Manga/Anime Style Templates
        self.add_template(PromptTemplate(
            id="manga_panel_generator",
            name="Manga Panel Generator",
            category=PromptCategory.MANGA_ANIME,
            template="manga panel showing {character_description}, {action}, {emotion}, intense {art_style} style, dynamic {composition}, high contrast black and white with {color_accents}",
            variables=["character_description", "action", "emotion", "art_style", "composition", "color_accents"],
            description="Create manga-style panels with dramatic composition",
            tags=["manga", "comic", "panel", "anime"],
            examples=[{
                "character_description": "spiky-haired protagonist",
                "action": "powering up energy attack",
                "emotion": "fierce determination",
                "art_style": "shonen manga",
                "composition": "low angle shot with speed lines",
                "color_accents": "glowing blue energy effects"
            }]
        ))
        
        # Product Photography for Character Merchandise
        self.add_template(PromptTemplate(
            id="anime_merchandise_photo",
            name="Anime Merchandise Photography",
            category=PromptCategory.PRODUCT_PHOTOGRAPHY,
            template="{product_type} featuring {character_name} from {anime_title}, placed {setting}, {lighting}, {background}, shot: {composition}, professional product photography",
            variables=["product_type", "character_name", "anime_title", "setting", "lighting", "background", "composition"],
            description="Professional product shots for anime merchandise",
            tags=["product", "merchandise", "anime", "photography"],
            examples=[{
                "product_type": "acrylic standee",
                "character_name": "Luffy",
                "anime_title": "One Piece",
                "setting": "on premium wooden display stand",
                "lighting": "soft studio light with rim lighting",
                "background": "clean white background with subtle shadow",
                "composition": "3/4 view, shallow depth of field"
            }]
        ))
        
        # Portrait Enhancement
        self.add_template(PromptTemplate(
            id="cosplay_portrait_enhancement",
            name="Cosplay Portrait Enhancement",
            category=PromptCategory.PHOTO_EDITING,
            template="Enhance this cosplay portrait: {enhancement_goals}, maintain {preserve_elements}, adjust {modification_elements}, add {artistic_effects}, final look: {target_style}",
            variables=["enhancement_goals", "preserve_elements", "modification_elements", "artistic_effects", "target_style"],
            description="AI-powered cosplay photo enhancement",
            tags=["portrait", "enhancement", "cosplay", "editing"]
        ))
        
        # Character Reference Sheet
        self.add_template(PromptTemplate(
            id="character_reference_sheet",
            name="Character Reference Sheet",
            category=PromptCategory.CHARACTER_COSPLAY,
            template="Character reference sheet for {character_name}, showing: front view, side view, back view, close-up face details, {costume_details}, {color_palette}, {distinguishing_features}, professional character design sheet, clean white background",
            variables=["character_name", "costume_details", "color_palette", "distinguishing_features"],
            description="Generate comprehensive character reference sheets",
            tags=["reference", "character", "design", "turnaround"]
        ))
    
    def add_template(self, template: PromptTemplate):
        """Add or update a template"""
        if not template.id:
            template.id = template.generate_id()
        
        template.updated_at = datetime.utcnow().isoformat()
        self.templates[template.id] = template
        
        logger.info(f"Added template: {template.name} ({template.id})")
    
    def get_template(self, template_id: str) -> Optional[PromptTemplate]:
        """Get template by ID"""
        return self.templates.get(template_id)
    
    def search_templates(
        self,
        category: Optional[PromptCategory] = None,
        tags: Optional[List[str]] = None,
        query: Optional[str] = None
    ) -> List[PromptTemplate]:
        """Search templates by category, tags, or query"""
        results = list(self.templates.values())
        
        if category:
            results = [t for t in results if t.category == category]
        
        if tags:
            results = [
                t for t in results
                if any(tag in t.tags for tag in tags)
            ]
        
        if query:
            query_lower = query.lower()
            results = [
                t for t in results
                if query_lower in t.name.lower()
                or query_lower in t.description.lower()
            ]
        
        return sorted(results, key=lambda t: t.quality_score, reverse=True)
    
    def generate_prompt(
        self,
        template_id: str,
        **variables
    ) -> GeneratedPrompt:
        """Generate a prompt from a template"""
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        # Render the prompt
        prompt_text = template.render(**variables)
        
        # Create generated prompt object
        generated = GeneratedPrompt(
            prompt=prompt_text,
            template_id=template_id,
            category=template.category,
            variables=variables
        )
        
        # Update template usage
        template.usage_count += 1
        
        # Store generated prompt
        self.generated[generated.cache_key()] = generated
        
        logger.info(f"Generated prompt from template {template.name}")
        return generated
    
    def generate_cosplay_prompt(
        self,
        character_name: str,
        anime_title: str,
        user_photo_path: Optional[str] = None,
        **kwargs
    ) -> GeneratedPrompt:
        """
        Generate optimized cosplay prompt for Nano Banana Pro
        
        Args:
            character_name: Anime character name
            anime_title: Source anime title
            user_photo_path: Optional user photo for face reference
            **kwargs: Additional customization parameters
        """
        # Set defaults
        defaults = {
            "pose": "confident heroic pose",
            "facial_expression": "determined smile",
            "outfit_description": "character signature outfit",
            "setting": "dramatic background matching character theme",
            "lighting": "cinematic studio lighting with rim light",
            "composition": "medium shot, f/1.8, eye-level angle",
            "art_style": "hyper-realistic anime style with soft skin tones"
        }
        
        # Merge with user overrides
        params = {**defaults, **kwargs}
        params["character_name"] = character_name
        params["anime_title"] = anime_title
        
        # Generate using template
        generated = self.generate_prompt("cosplay_anime_character", **params)
        
        # Add reference input if photo provided
        if user_photo_path:
            generated.prompt += " | Use reference image for facial features and skin tone"
        
        return generated
    
    def optimize_prompt(self, prompt: str) -> Tuple[str, List[str]]:
        """
        Optimize a prompt based on Nano Banana Pro best practices
        
        Returns:
            Optimized prompt and list of improvements made
        """
        improvements = []
        optimized = prompt
        
        # Check for required components
        components = {
            "subject": ["character", "person", "figure", "subject"],
            "setting": ["in ", "at ", "background", "environment"],
            "style": ["style", "art ", "aesthetic"],
            "composition": ["shot", "angle", "view", "framing"]
        }
        
        for component, keywords in components.items():
            if not any(kw in optimized.lower() for kw in keywords):
                improvements.append(f"Missing {component} specification")
        
        # Add quality boosters if not present
        quality_terms = ["detailed", "high quality", "professional", "4K", "ultra"]
        if not any(term in optimized.lower() for term in quality_terms):
            optimized += ", highly detailed, professional quality"
            improvements.append("Added quality enhancers")
        
        # Improve composition specificity
        if "shot" not in optimized.lower():
            optimized += ", medium shot composition"
            improvements.append("Added composition details")
        
        return optimized, improvements
    
    def score_prompt(self, prompt: str) -> float:
        """
        Score prompt quality (0-1) based on best practices
        """
        score = 0.0
        checks = 0
        
        # Component checks
        components = {
            "subject": 0.2,
            "setting": 0.15,
            "style": 0.15,
            "composition": 0.15,
            "lighting": 0.1,
            "quality": 0.25
        }
        
        prompt_lower = prompt.lower()
        
        # Subject
        checks += 1
        if any(w in prompt_lower for w in ["character", "person", "portrait", "figure"]):
            score += components["subject"]
        
        # Setting
        checks += 1
        if any(w in prompt_lower for w in ["in ", "at ", "setting", "environment", "background"]):
            score += components["setting"]
        
        # Style
        checks += 1
        if any(w in prompt_lower for w in ["style", "aesthetic", "art", "realistic", "anime"]):
            score += components["style"]
        
        # Composition
        checks += 1
        if any(w in prompt_lower for w in ["shot", "angle", "view", "composition", "framing"]):
            score += components["composition"]
        
        # Lighting
        checks += 1
        if any(w in prompt_lower for w in ["light", "lighting", "golden hour", "studio"]):
            score += components["lighting"]
        
        # Quality terms
        checks += 1
        quality_count = sum(1 for w in ["detailed", "professional", "4k", "ultra", "high quality"]
                          if w in prompt_lower)
        score += components["quality"] * min(quality_count / 2, 1.0)
        
        return round(score, 2)
    
    def export_templates(self, filepath: str):
        """Export all templates to JSON file"""
        data = {
            template_id: {
                **asdict(template),
                "category": template.category.value
            }
            for template_id, template in self.templates.items()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(data)} templates to {filepath}")
    
    def import_templates(self, filepath: str):
        """Import templates from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for template_data in data.values():
            # Convert category string back to enum
            template_data["category"] = PromptCategory(template_data["category"])
            template = PromptTemplate(**template_data)
            self.add_template(template)
        
        logger.info(f"Imported {len(data)} templates from {filepath}")


# Example usage
if __name__ == "__main__":
    # Initialize system
    prompt_system = PromptEngineering()
    
    # Generate a cosplay prompt
    generated = prompt_system.generate_cosplay_prompt(
        character_name="Makima",
        anime_title="Chainsaw Man",
        pose="sitting confidently in office chair",
        facial_expression="mysterious smile with yellow ringed eyes",
        outfit_description="white shirt with black tie and dark suit",
        setting="modern office with large windows"
    )
    
    print(f"Generated Prompt:\n{generated.prompt}\n")
    
    # Score the prompt
    score = prompt_system.score_prompt(generated.prompt)
    print(f"Quality Score: {score}/1.0\n")
    
    # Optimize a basic prompt
    basic = "anime girl with pink hair"
    optimized, improvements = prompt_system.optimize_prompt(basic)
    print(f"Original: {basic}")
    print(f"Optimized: {optimized}")
    print(f"Improvements: {', '.join(improvements)}")
