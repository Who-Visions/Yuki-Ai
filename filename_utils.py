"""
Filename Utility Module
Provides standardized, clean filename generation for Yuki Platform outputs.
"""

import re
import datetime
import uuid
from typing import Optional

def clean_string(text: str) -> str:
    """
    Sanitizes a string to be safe for filenames.
    - Replaces spaces with underscores
    - Removes non-alphanumeric characters (except underscores and hyphens)
    - Converts to lowercase
    """
    if not text:
        return "unknown"
    
    # Replace spaces with underscores
    text = text.replace(" ", "_")
    
    # Remove invalid characters (keep alphanumeric, _, -)
    text = re.sub(r'[^\w\-]', '', text)
    
    # Collapse multiple underscores
    text = re.sub(r'_+', '_', text)
    
    return text.lower().strip("_")

def generate_filename(
    base_name: str,
    category: str = "output",
    extension: str = "png",
    model_name: Optional[str] = None,
    include_timestamp: bool = True,
    include_uuid: bool = False
) -> str:
    """
    Generates a standardized filename.
    
    Format: {category}_{base_name}_{model}_{timestamp}_{short_uuid}.{extension}
    Example: cosplay_frieren_gemini3_20231027_103045_a1b2.png
    
    Args:
        base_name: Main identifier (e.g., character name, "frieren")
        category: Type of file (e.g., "cosplay", "ref", "video")
        extension: File extension (without dot)
        model_name: Name of the model used (e.g., "gemini-3-pro")
        include_timestamp: Whether to add YYYYMMDD_HHMMSS
        include_uuid: Whether to add a short random hash for uniqueness
    """
    parts = []
    
    # 1. Category
    if category:
        parts.append(clean_string(category))
        
    # 2. Base Name
    parts.append(clean_string(base_name))

    # 3. Model Name (New)
    if model_name:
        # Shorten common model names for cleaner files
        short_model = model_name
        if "gemini" in model_name: short_model = "gemini"
        if "imagen" in model_name: short_model = "imagen"
        if "veo" in model_name: short_model = "veo"
        parts.append(clean_string(short_model))
    
    # 4. Timestamp
    if include_timestamp:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        parts.append(ts)
        
    # 5. UUID (Short)
    if include_uuid:
        short_id = str(uuid.uuid4())[:4]
        parts.append(short_id)
        
    # Join parts
    filename = "_".join(parts)
    
    # Add extension
    return f"{filename}.{extension.lstrip('.')}"

# Example Usage
if __name__ == "__main__":
    print(generate_filename("Frieren: Beyond Journey's End", category="cosplay"))
    print(generate_filename("Makima", category="ref_sheet", include_uuid=True))
    print(generate_filename("Test Video", category="video", extension="mp4"))
