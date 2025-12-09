import os
import json
from pathlib import Path
from typing import List, Dict
from anime_database import AnimeDatabase, CharacterFaceSchema, CosplayGeneration
from face_math import FaceMathArchitect
from tools import generate_cosplay_image
import datetime

class CharacterFaceMathProcessor:
    """
    Batch processor for extracting Face Math schemas and generating cosplays
    """
    
    def __init__(self, db: AnimeDatabase):
        self.db = db
        self.face_math = FaceMathArchitect()
        self.schemas_dir = Path("c:/Yuki_Local/face_schemas")
        self.schemas_dir.mkdir(exist_ok=True)
    
    def extract_face_schema_for_character(self, character_id: str) -> bool:
        """Extract face schema for a character using their reference images"""
        character = self.db.characters.get(character_id)
        if not character:
            print(f"⚠️ Character {character_id} not found")
            return False
        
        if not character.reference_images:
            print(f"⚠️ No reference images for {character.name_full}")
            return False
        
        print(f"\n[🧮 EXTRACTING FACE MATH] {character.name_full}")
        
        # Use the first reference image
        ref_image = character.reference_images[0]
        
        if not os.path.exists(ref_image):
            print(f"  ⚠️ Image not found: {ref_image}")
            return False
        
        # Extract schema
        schema_data = self.face_math.extract_face_schema(ref_image)
        
        if "error" in schema_data:
            print(f"  ❌ Failed: {schema_data['error']}")
            return False
        
        # Save schema to file
        schema_filename = f"{character_id}_schema.json"
        schema_path = self.schemas_dir / schema_filename
        
        with open(schema_path, 'w', encoding='utf-8') as f:
            json.dump(schema_data, f, indent=2)
        
        # Update character in database
        character.face_schema = CharacterFaceSchema(
            extracted=True,
            extraction_date=datetime.datetime.now().isoformat(),
            model_used="gemini-3-pro-preview",  # or the fallback model
            schema_data=schema_data,
            reference_image_hashes=[ref_image]
        )
        
        self.db.save()
        print(f"  ✅ Schema extracted and saved: {schema_path}")
        return True
    
    def batch_extract_schemas(self, limit: int = None):
        """Extract face schemas for all characters without schemas"""
        print(f"\n[🔄 BATCH FACE SCHEMA EXTRACTION]")
        
        characters_to_process = [
            c for c in self.db.characters.values() 
            if not c.face_schema.extracted and c.reference_images
        ]
        
        if limit:
            characters_to_process = characters_to_process[:limit]
        
        print(f"Processing {len(characters_to_process)} characters...")
        
        success_count = 0
        for i, character in enumerate(characters_to_process, 1):
            print(f"\n[{i}/{len(characters_to_process)}] {character.name_full}")
            if self.extract_face_schema_for_character(character.id):
                success_count += 1
        
        print(f"\n✅ Extracted {success_count}/{len(characters_to_process)} schemas")
        return success_count
    
    def generate_cosplay_for_character(
        self, 
        character_id: str, 
        target_character_name: str,
        source_image_path: str,
        num_variations: int = 1
    ) -> List[str]:
        """
        Generate a cosplay of target_character using source_image with face math constraints
        """
        character = self.db.characters.get(character_id)
        if not character:
            print(f"⚠️ Character {character_id} not found")
            return []
        
        if not character.face_schema.extracted:
            print(f"⚠️ No face schema for {character.name_full}. Extract first.")
            return []
        
        print(f"\n[🎨 GENERATING COSPLAY] {character.name_full} as {target_character_name}")
        
        # Get the face schema
        schema = character.face_schema.schema_data
        faces = schema.get("faces", [])
        
        if not faces:
            print(f"  ⚠️ No faces in schema")
            return []
        
        identity_vector = faces[0].get("identity_vector", {})
        features = faces[0].get("feature_map", {})
        
        # Construct prompt with Face Math constraints
        prompt = (
            f"Generate a hyper-realistic cosplay image of {target_character_name}. "
            f"CRITICAL IDENTITY CONSTRAINTS - The face must match this exact geometric schema:\n"
            f"{json.dumps(identity_vector, indent=2)}\n\n"
            f"FEATURE REQUIREMENTS:\n{json.dumps(features, indent=2)}\n\n"
            f"The character should be dressed as {target_character_name} in their iconic outfit, "
            f"but the face MUST preserve the identity defined by the geometric ratios above. "
            f"High quality, cinematic lighting, 8K resolution."
        )
        
        # Generate with fallback chain
        result = generate_cosplay_image(
            prompt=prompt,
            model="gemini-3-pro-image-preview",
            reference_image_paths=[source_image_path],
            number_of_images=num_variations
        )
        
        # Parse generated file paths
        generated_files = []
        if "Images generated successfully:" in result:
            files_str = result.split("Images generated successfully:")[1].strip()
            generated_files = [f.strip() for f in files_str.split(",")]
        
        # Record generation in database
        for i, filepath in enumerate(generated_files):
            generation = CosplayGeneration(
                generation_id=f"{character_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}",
                timestamp=datetime.datetime.now().isoformat(),
                model_used="gemini-3-pro-image-preview",
                prompt=prompt[:200] + "...",
                output_path=filepath,
                source_image_hash=source_image_path
            )
            character.cosplay_generations.append(generation)
        
        self.db.save()
        print(f"  ✅ Generated {len(generated_files)} variations")
        return generated_files
    
    def batch_generate_cosplays(
        self, 
        target_characters: List[str],
        source_image_path: str,
        limit: int = None
    ):
        """
        Batch generate cosplays for multiple characters
        """
        print(f"\n[🔄 BATCH COSPLAY GENERATION]")
        
        characters_with_schemas = [
            c for c in self.db.characters.values() 
            if c.face_schema.extracted
        ]
        
        if limit:
            characters_with_schemas = characters_with_schemas[:limit]
        
        print(f"Generating {len(target_characters)} cosplays for {len(characters_with_schemas)} characters...")
        
        total_generated = 0
        for character in characters_with_schemas:
            for target_char in target_characters:
                files = self.generate_cosplay_for_character(
                    character.id,
                    target_char,
                    source_image_path
                )
                total_generated += len(files)
        
        print(f"\n✅ Generated {total_generated} total cosplay images")
        return total_generated

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    db = AnimeDatabase()
    processor = CharacterFaceMathProcessor(db)
    
    # Example workflow:
    # 1. Extract face schemas for all characters
    # processor.batch_extract_schemas(limit=5)
    
    # 2. Generate cosplays
    # processor.batch_generate_cosplays(
    #     target_characters=["Dante (Devil May Cry)", "Cloud Strife (Final Fantasy VII)"],
    #     source_image_path="path/to/source/image.png",
    #     limit=3
    # )
    
    print("✅ Face Math Processor ready!")
