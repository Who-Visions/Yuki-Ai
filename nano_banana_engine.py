"""
Yuki Nano Banana Engine
Leverages Gemini 3 Pro Image Preview's hidden reasoning layer
"The better the automation, the better the creation"
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from google import genai
from google.genai import types
import datetime

PROJECT_ID = "gifted-cooler-479623-r7"
LOCATION = "global"

class NanoBananaEngine:
    """
    Advanced image generation using Gemini 3 Pro Image Preview
    Implements best practices from the Nano Banana Pro masterclass
    """
    
    def __init__(self):
        self.client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
        self.outputs_dir = Path("c:/Yuki_Local/nano_banana_outputs")
        self.outputs_dir.mkdir(exist_ok=True)
    
    def generate_with_reasoning(
        self,
        prompt: str,
        context_research: Optional[str] = None,
        reference_images: List[str] = None,
        aspect_ratio: str = "3:4",
        resolution: str = "2K",
        use_search: bool = True,
        character_consistency: bool = False
    ) -> Dict:
        """
        Generate image using Nano Banana Pro's hidden reasoning layer
        
        Key insight: Provide context research to reduce search overhead
        and let the model focus on image generation
        """
        print(f"\n[🧠 NANO BANANA] Generating with reasoning layer...")
        
        # Build contents array
        contents = []
        
        # Add context research (best practice from video)
        if context_research:
            contents.append(f"<context>\n{context_research}\n</context>\n\n")
        
        # Add the main prompt
        contents.append(prompt)
        
        # Add reference images for style/character consistency
        if reference_images:
            for img_path in reference_images:
                if os.path.exists(img_path):
                    with open(img_path, "rb") as f:
                        img_bytes = f.read()
                    mime_type = "image/png" if img_path.endswith(".png") else "image/jpeg"
                    contents.append(types.Part.from_bytes(data=img_bytes, mime_type=mime_type))
        
        # Map resolution
        size_map = {"1K": "1K", "2K": "2K", "4K": "4K"}
        image_size = size_map.get(resolution, "2K")
        
        # Build tools (Google Search grounding)
        tools = [types.Tool(google_search=types.GoogleSearch())] if use_search else None
        
        print(f"  Resolution: {image_size} | Aspect: {aspect_ratio} | Search: {use_search}")
        print(f"  Reference Images: {len(reference_images) if reference_images else 0}")
        
        # Generate with hidden reasoning
        response = self.client.models.generate_content(
            model="gemini-3-pro-image-preview",  # Official API name for "Nano Banana Pro"
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size=image_size
                ),
                tools=tools,
                temperature=1.0  # Default recommended temp
            )
        )
        
        # Extract images (handle response format)
        saved_files = []
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if response.candidates:
            for i, candidate in enumerate(response.candidates):
                for part in candidate.content.parts:
                    if part.text:
                        print(f"  [Reasoning]: {part.text[:100]}...")
                    if part.inline_data:
                        filename = self.outputs_dir / f"nano_banana_{timestamp}_{i+1}.png"
                        with open(filename, "wb") as f:
                            f.write(part.inline_data.data)
                        saved_files.append(str(filename))
                        print(f"  ✓ Saved: {filename.name}")
        
        return {
            "files": saved_files,
            "reasoning_used": True,
            "search_grounding": use_search,
            "timestamp": timestamp
        }
    
    def character_consistency_generation(
        self,
        base_character_image: str,
        target_scenarios: List[str],
        character_name: str = "Character"
    ) -> List[Dict]:
        """
        Generate multiple variations with character consistency
        Key insight: No need for LoRAs! Just use reference images
        """
        print(f"\n[🎭 CHARACTER CONSISTENCY] {character_name}")
        
        results = []
        for scenario in target_scenarios:
            prompt = f"""
            Create an image of {character_name} in this scenario: {scenario}
            
            CRITICAL: Maintain exact facial features, proportions, and identity from the reference image.
            The character should be instantly recognizable as the same person.
            Only change: clothing, environment, pose, lighting to match the scenario.
            
            High quality, cinematic, 8K details.
            """
            
            result = self.generate_with_reasoning(
                prompt=prompt,
                reference_images=[base_character_image],
                aspect_ratio="3:4",
                resolution="2K",
                use_search=False,  # Don't need search for character consistency
                character_consistency=True
            )
            
            results.append({
                "scenario": scenario,
                "files": result["files"]
            })
        
        print(f"\n✅ Generated {len(results)} character variations")
        return results
    
    def infographic_generator(
        self,
        topic: str,
        research_data: str,
        style: str = "professional",
        annotations: bool = True
    ) -> Dict:
        """
        Generate educational infographics (400% learning boost!)
        Key insight: Visual learning is 60,000x faster than text
        """
        print(f"\n[📊 INFOGRAPHIC] {topic}")
        
        prompt = f"""
        Create a high-quality infographic explaining: {topic}
        
        Style: {style}
        Include annotations: {'Yes - add clear labels and explanations' if annotations else 'No'}
        
        Requirements:
        1. Visual hierarchy - most important info stands out
        2. Clean typography - readable from a distance
        3. Color coding - use colors to group related concepts
        4. Icons and symbols - make it scannable
        5. Data visualization - charts/graphs where applicable
        
        The goal is to maximize learning efficiency (visual learning = 400% boost).
        Make complex concepts simple and memorable.
        """
        
        return self.generate_with_reasoning(
            prompt=prompt,
            context_research=f"<research_data>\n{research_data}\n</research_data>",
            aspect_ratio="16:9",  # Good for presentations
            resolution="4K",  # High detail for text clarity
            use_search=False  # We provided research
        )
    
    def social_media_campaign(
        self,
        product_name: str,
        product_description: str,
        target_audience: str,
        num_variations: int = 4
    ) -> List[Dict]:
        """
        Generate social media creatives for campaigns
        Key insight: Perfect text + high realism = game changer for marketing
        """
        print(f"\n[📱 SOCIAL MEDIA] {product_name} Campaign")
        
        formats = [
            {"name": "Instagram Story", "aspect": "9:16", "cta": "Swipe Up"},
            {"name": "Instagram Post", "aspect": "1:1", "cta": "Learn More"},
            {"name": "YouTube Thumbnail", "aspect": "16:9", "cta": "Watch Now"},
            {"name": "Twitter/X Post", "aspect": "16:9", "cta": "Click Here"}
        ]
        
        results = []
        for format_spec in formats[:num_variations]:
            prompt = f"""
            Create a professional {format_spec['name']} promoting {product_name}.
            
            Product Details:
            {product_description}
            
            Target Audience: {target_audience}
            
            Requirements:
            1. Eye-catching, attention-grabbing design
            2. Clear, perfect text with product name
            3. Strong call-to-action: "{format_spec['cta']}"
            4. Brand-appropriate colors and style
            5. High contrast for mobile viewing
            
            Make it stand out in a crowded feed.
            """
            
            result = self.generate_with_reasoning(
                prompt=prompt,
                aspect_ratio=format_spec['aspect'],
                resolution="2K",
                use_search=False
            )
            
            results.append({
                "format": format_spec['name'],
                "files": result["files"]
            })
        
        print(f"\n✅ Generated {len(results)} social media creatives")
        return results

# =============================================================================
# AUTOMATION WORKFLOWS
# =============================================================================

class NanoBananaAutomation:
    """
    Automated workflows using Nano Banana Pro
    "Build the system that builds the system"
    """
    
    def __init__(self):
        self.engine = NanoBananaEngine()
        self.db_path = Path("c:/Yuki_Local/anime_database.json")
    
    def auto_generate_character_variations(self, character_id: str) -> Dict:
        """
        Automatically generate character in multiple scenarios/styles
        No LoRA training needed!
        """
        # Load character from database
        with open(self.db_path) as f:
            db = json.load(f)
        
        character = db["characters"].get(character_id)
        if not character or not character.get("reference_images"):
            return {"error": "Character not found or no reference images"}
        
        # Define scenario variations
        scenarios = [
            "1920s Great Gatsby party with period-accurate clothing",
            "Cyberpunk 2077 style futuristic city with neon lights",
            "Medieval knight in full armor at castle",
            "Modern business professional in office",
            "Astronaut in space with Earth in background",
            "Victorian era aristocrat in formal dress",
            "Samurai in feudal Japan with cherry blossoms",
            "Modern streetwear in urban environment"
        ]
        
        base_image = character["reference_images"][0]
        
        return self.engine.character_consistency_generation(
            base_character_image=base_image,
            target_scenarios=scenarios,
            character_name=character["name_full"]
        )
    
    def auto_create_learning_materials(self, topic: str) -> Dict:
        """
        Automatically research topic and create visual learning materials
        """
        print(f"\n[🎓 AUTO LEARNING] {topic}")
        
        # Step 1: Deep research (would use Perplexity or Gemini)
        research_prompt = f"Explain {topic} in detail with key concepts, examples, and important facts."
        
        # Use Gemini 3 for research
        research_client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
        research_response = research_client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=research_prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        research_data = research_response.text
        
        # Step 2: Generate infographic
        return self.engine.infographic_generator(
            topic=topic,
            research_data=research_data,
            style="educational professional",
            annotations=True
        )

# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    engine = NanoBananaEngine()
    
    # Example: Character consistency
    result = engine.character_consistency_generation(
        base_character_image="c:/Yuki_Local/dave test images/0Y9A3958.png",
        target_scenarios=[
            "Dante from Devil May Cry with red coat",
            "Cloud Strife from Final Fantasy VII",
            "Kirito from Sword Art Online"
        ],
        character_name="Dave"
    )
    
    print(f"\n✅ Generation complete!")
    print(json.dumps(result, indent=2))
