"""
CRITICAL PROMPT FIX - Photorealistic Cosplay
=============================================
The model was creating ANIME ART when we need PHOTOREALISTIC COSPLAY.

KEY DIFFERENCE:
❌ WRONG: Anime-style drawing of the person
✅ RIGHT: Real photo of the person wearing the character's costume
"""

# WRONG PROMPT (creates anime art):
WRONG_PROMPT = """
Transform this person into {character} from {anime}.
CHARACTER: {character}
"""

# CORRECT PROMPT (photorealistic cosplay):
CORRECT_PROMPT = """
Create a PHOTOREALISTIC COSPLAY photograph of this person.

{identity_preservation_rules}

=== COSPLAY REQUIREMENTS ===
COSTUME: Dress the person in {character}'s outfit from {anime}
- Include character's distinctive clothing
- Include character's accessories  
- Include character's hair style/color (wig or styled hair)

STYLE: PHOTOREALISTIC PHOTOGRAPHY
- Keep the person's REAL FACE (not anime-style)
- Keep the person's REAL BODY TYPE
- Professional cosplay photography
- Convention or studio setting
- High-quality camera photo (NOT illustration, NOT anime art, NOT drawing)

COMPOSITION:
- Vertical portrait (9:16 aspect ratio)
- Full body or 3/4 length shot
- Optimized for mobile screens
- 4K resolution

LIGHTING:
- Professional photography lighting
- Studio quality or convention setting
- Sharp focus on face and costume details

=== CRITICAL RULES ===
1. This MUST be a PHOTOGRAPH, not an illustration
2. The person's FACE stays REALISTIC (their actual face)
3. ONLY the COSTUME changes to match the character
4. NO anime art style
5. NO cel-shading or cartoon effects
6. PHOTOREALISTIC like a real cosplay photo at a convention

Think: "Person wearing a high-quality cosplay costume in a professional photo"
NOT: "Anime-style drawing of the character"
"""

# Example of correct vs wrong:
EXAMPLES = {
    "wrong": "Anime-style illustration of Nadley as Naruto (cartoonized face)",
    "correct": "Real photograph of Nadley wearing Naruto's orange jumpsuit costume (his real face, professional cosplay photo)"
}

if __name__ == "__main__":
    print("=== PROMPT FIX GUIDE ===\n")
    print("❌ WRONG OUTPUT:")
    print("   - Anime-style drawing")
    print("   - Cartoonized face")
    print("   - Illustration/art style")
    print("")
    print("✅ CORRECT OUTPUT:")
    print("   - PHOTOREALISTIC photograph")
    print("   - Person's REAL FACE")
    print("   - Wearing character's COSTUME")
    print("   - Professional cosplay photography")
    print("")
    print("KEY PHRASE TO ADD:")
    print('   "Create a PHOTOREALISTIC COSPLAY photograph"')
    print('   "This MUST be a PHOTOGRAPH, not an illustration"')
    print('   "Keep the person\'s REAL FACE (not anime-style)"')
