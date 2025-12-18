"""
Yuki Gemini Image Client (Nano Banana Pro Edition)
Powered by Gemini 3 Pro Image (gemini-3-pro-image-preview)

Features:
- "Thinking" process for complex prompt reasoning
- Google Search Grounding for real-time accuracy
- 4K Resolution support
- Multi-reference mixing (up to 14 images)
- Multilingual text generation
"""

import os
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from PIL import Image
import io

from google import genai
from google.genai import types

@dataclass
class GeneratedImage:
    image_data: Any  # PIL Image
    path: Optional[str] = None
    prompt: str = ""
    thoughts: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class YukiGeminiImageClient:
    """
    Client for Nano Banana Pro (Gemini 3 Pro Image)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-3-pro-image-preview"
        self.flash_model_id = "gemini-3-flash-preview" # Fallback/Fast model
        
    def generate_image(
        self,
        prompt: str,
        reference_images: List[Union[str, Image.Image]] = None,
        negative_prompt: Optional[str] = None,
        aspect_ratio: str = "16:9",
        resolution: str = "2K", # 1K, 2K, 4K
        person_generation: str = "allow_adult",
        use_search_grounding: bool = False,
        enable_thinking: bool = True,
        number_of_images: int = 1,
        save_path: Optional[str] = None
    ) -> GeneratedImage:
        """
        Generate image using Nano Banana Pro
        """
        
        print(f"🎨 Generating with {self.model_id}...")
        print(f"   Resolution: {resolution}, Aspect: {aspect_ratio}")
        if enable_thinking:
            print("   🧠 Thinking enabled")
        if use_search_grounding:
            print("   🌍 Search grounding enabled")

        # Prepare configuration
        config_args = {
            "response_modalities": ["IMAGE", "TEXT"] if enable_thinking else ["IMAGE"],
            "image_config": types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution,
            ),
            "number_of_images": number_of_images,
            "person_generation": person_generation
        }

        # Add tools
        tools = []
        if use_search_grounding:
            tools.append({"google_search": {}})
        
        if tools:
            config_args["tools"] = tools

        # Add thinking config
        if enable_thinking:
            config_args["thinking_config"] = types.ThinkingConfig(thinking_level="high")

        config = types.GenerateContentConfig(**config_args)

        # Prepare contents
        contents = [prompt]
        
        # Handle reference images (up to 14 for Pro)
        if reference_images:
            print(f"   📎 Mixing {len(reference_images)} reference images")
            for ref in reference_images:
                if isinstance(ref, str):
                    # Load from path
                    try:
                        img = Image.open(ref)
                        contents.append(img)
                    except Exception as e:
                        print(f"   ⚠️ Could not load reference {ref}: {e}")
                elif isinstance(ref, Image.Image):
                    contents.append(ref)

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=contents,
                config=config
            )

            generated_img = None
            thoughts = ""

            for part in response.parts:
                if part.thought:
                    thoughts += part.text + "\n"
                    print(f"   💭 Thought: {part.text[:100]}...")
                elif part.image:
                    generated_img = part.image
            
            if not generated_img:
                # Fallback check for candidates if parts parsing failed differently
                if response.candidates and response.candidates[0].content.parts:
                     for part in response.candidates[0].content.parts:
                        if part.image:
                            generated_img = part.image
                            break

            if generated_img:
                # Convert to PIL if it isn't already (SDK usually returns a wrapper)
                # The SDK `part.image` might be bytes or a specific object. 
                # Assuming standard SDK behavior:
                try:
                    # If it's the SDK object, it might have a .show() or .save()
                    # We want a PIL object for consistency
                    if hasattr(generated_img, 'image_bytes'):
                        pil_img = Image.open(io.BytesIO(generated_img.image_bytes))
                    else:
                        # It might already be PIL or compatible
                        pil_img = generated_img 
                except:
                     # Fallback if it's raw bytes
                     pil_img = Image.open(io.BytesIO(generated_img))

                if save_path:
                    pil_img.save(save_path)
                    print(f"   ✅ Saved to {save_path}")

                return GeneratedImage(
                    image_data=pil_img,
                    path=save_path,
                    prompt=prompt,
                    thoughts=thoughts,
                    metadata={"model": self.model_id, "resolution": resolution}
                )
            else:
                raise ValueError("No image generated in response")

        except Exception as e:
            print(f"   ❌ Generation failed: {e}")
            raise

# Example usage
if __name__ == "__main__":
    client = YukiGeminiImageClient()
    # Test run would go here
