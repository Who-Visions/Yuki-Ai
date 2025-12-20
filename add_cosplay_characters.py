"""
Add 10 cosplay characters to Yuki Knowledge Database
With comprehensive costume descriptions and alt suits
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.schema import Base, Character, AppearanceVariant, Series, Genre, Tag, GenderEnum, RoleEnum

DB_PATH = "sqlite:///c:/Yuki_Local/database/yuki_knowledge.db"

# Character data with default + alt costumes
CHARACTERS = [
    {
        "name_romaji": "Storm (Ororo Munroe)",
        "name_native": "Storm",
        "alternative_names": ["Ororo", "Weather Witch", "Goddess"],
        "gender": GenderEnum.FEMALE,
        "age": "30s",
        "description": "Weather-controlling mutant and X-Men leader. African goddess aesthetic.",
        "base_prompt": "Storm from X-Men, dark skin, white hair, regal bearing, weather powers",
        "series_title": "X-Men",
        "variants": [
            {
                "name": "Classic Black Suit",
                "is_default": True,
                "hair_style": "Long flowing white hair",
                "hair_color": "#FFFFFF",
                "eye_color": "White (glowing) or Blue",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["gold tiara", "dramatic white mohawk optional"],
                    "upper": ["black leather bodysuit", "gold trim", "cape attached"],
                    "lower": ["black leather pants", "gold belt"],
                    "accessories": ["gold arm cuffs", "flowing black cape"]
                },
                "prompt_tags": "storm xmen, white hair, black bodysuit, gold accents, cape, dramatic sky background, lightning",
                "negative_prompt": "pale skin, short hair",
                "color_palette": {"primary": "#000000", "secondary": "#FFD700", "accent": "#FFFFFF"}
            },
            {
                "name": "Mohawk Punk Era",
                "is_default": False,
                "hair_style": "White mohawk, shaved sides",
                "hair_color": "#FFFFFF",
                "eye_color": "Blue",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["white mohawk"],
                    "upper": ["black leather jacket", "punk studs", "mesh top"],
                    "lower": ["black leather pants", "chains"],
                    "accessories": ["punk jewelry", "arm bands"]
                },
                "prompt_tags": "storm punk era, mohawk, black leather, punk aesthetic, 80s xmen",
                "negative_prompt": "long hair, cape",
                "color_palette": {"primary": "#000000", "secondary": "#C0C0C0", "accent": "#FFFFFF"}
            }
        ]
    },
    {
        "name_romaji": "Michonne",
        "name_native": "Michonne Hawthorne",
        "alternative_names": ["Michonne"],
        "gender": GenderEnum.FEMALE,
        "age": "30s-40s",
        "description": "Katana-wielding survivor from The Walking Dead. Fierce warrior.",
        "base_prompt": "Michonne from Walking Dead, dark skin, dreadlocks, katana, fierce expression",
        "series_title": "The Walking Dead",
        "variants": [
            {
                "name": "Survivor Default",
                "is_default": True,
                "hair_style": "Long dreadlocks",
                "hair_color": "#1A1A1A",
                "eye_color": "Dark brown",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["dreadlocks"],
                    "upper": ["distressed tank top", "leather vest", "arm wraps"],
                    "lower": ["cargo pants", "utility belt"],
                    "accessories": ["katana on back", "machete", "rope"]
                },
                "prompt_tags": "michonne walking dead, dreadlocks, katana, post apocalyptic, warrior, fierce",
                "negative_prompt": "clean clothes, bright colors, smiling",
                "color_palette": {"primary": "#3D2B1F", "secondary": "#1A1A1A", "accent": "#8B4513"}
            },
            {
                "name": "Alexandria Constable",
                "is_default": False,
                "hair_style": "Clean dreadlocks, pulled back",
                "hair_color": "#1A1A1A",
                "eye_color": "Dark brown",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["dreadlocks tied back"],
                    "upper": ["clean button shirt", "constable uniform"],
                    "lower": ["dark pants", "duty belt"],
                    "accessories": ["badge", "walkie talkie"]
                },
                "prompt_tags": "michonne constable uniform, clean appearance, leadership",
                "negative_prompt": "dirty, torn clothes",
                "color_palette": {"primary": "#2F4F4F", "secondary": "#C0C0C0", "accent": "#1A1A1A"}
            }
        ]
    },
    {
        "name_romaji": "Shuri",
        "name_native": "Shuri",
        "alternative_names": ["Princess Shuri", "Black Panther"],
        "gender": GenderEnum.FEMALE,
        "age": "16-22",
        "description": "Wakandan princess, tech genius, eventual Black Panther.",
        "base_prompt": "Shuri from Black Panther, dark skin, braided hair, Wakandan technology",
        "series_title": "Black Panther",
        "variants": [
            {
                "name": "Lab Tech Princess",
                "is_default": True,
                "hair_style": "Braided designs, bantu knots",
                "hair_color": "#1A1A1A",
                "eye_color": "Dark brown",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["intricate braided hairstyle"],
                    "upper": ["white lab suit", "purple accents", "vibranium tech"],
                    "lower": ["white tech pants"],
                    "accessories": ["kimoyo beads", "hologram projector", "vibranium gauntlets"]
                },
                "prompt_tags": "shuri black panther, wakandan tech, lab coat, purple holograms, genius inventor",
                "negative_prompt": "male, old",
                "color_palette": {"primary": "#FFFFFF", "secondary": "#9B30FF", "accent": "#C0C0C0"}
            },
            {
                "name": "Black Panther Suit",
                "is_default": False,
                "hair_style": "Natural under suit",
                "hair_color": "#1A1A1A",
                "eye_color": "Dark brown",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["Black Panther mask with gold accents"],
                    "upper": ["vibranium nanotech suit", "gold highlights"],
                    "lower": ["full bodysuit"],
                    "accessories": ["retractable claws", "necklace visible"]
                },
                "prompt_tags": "shuri black panther suit, gold accents, vibranium, hero pose",
                "negative_prompt": "tChalla, male",
                "color_palette": {"primary": "#1A1A1A", "secondary": "#FFD700", "accent": "#9B30FF"}
            }
        ]
    },
    {
        "name_romaji": "Niobe",
        "name_native": "Niobe",
        "alternative_names": ["Captain Niobe"],
        "gender": GenderEnum.FEMALE,
        "age": "30s",
        "description": "Ship captain in The Matrix, skilled pilot and fighter.",
        "base_prompt": "Niobe from Matrix, dark skin, short hair, black leather, sunglasses",
        "series_title": "The Matrix",
        "variants": [
            {
                "name": "Matrix Operator",
                "is_default": True,
                "hair_style": "Short cropped or slicked back",
                "hair_color": "#1A1A1A",
                "eye_color": "Brown (hidden by sunglasses)",
                "skin_tone": "Medium brown",
                "outfit_structure": {
                    "head": ["slicked back hair", "small sunglasses"],
                    "upper": ["long black leather coat", "form-fitting top"],
                    "lower": ["black leather pants", "boots"],
                    "accessories": ["dual pistols", "earpiece", "small sunglasses"]
                },
                "prompt_tags": "niobe matrix, black leather, sunglasses, cyberpunk, action pose",
                "negative_prompt": "colorful, casual wear",
                "color_palette": {"primary": "#0A0A0A", "secondary": "#006400", "accent": "#C0C0C0"}
            },
            {
                "name": "Zion Casual",
                "is_default": False,
                "hair_style": "Natural short",
                "hair_color": "#1A1A1A",
                "eye_color": "Brown",
                "skin_tone": "Medium brown",
                "outfit_structure": {
                    "head": ["natural hair"],
                    "upper": ["woven tunic", "earthy tones"],
                    "lower": ["loose pants", "sandals"],
                    "accessories": ["minimal jewelry"]
                },
                "prompt_tags": "niobe zion, casual wear, underground city, natural",
                "negative_prompt": "leather, sunglasses",
                "color_palette": {"primary": "#8B7355", "secondary": "#D2691E", "accent": "#1A1A1A"}
            }
        ]
    },
    {
        "name_romaji": "Rue",
        "name_native": "Rue",
        "alternative_names": ["District 11 Tribute"],
        "gender": GenderEnum.FEMALE,
        "age": "12",
        "description": "Young tribute from District 11, innocent and resourceful.",
        "base_prompt": "Rue from Hunger Games, young dark skin girl, natural hair, innocent expression",
        "series_title": "The Hunger Games",
        "variants": [
            {
                "name": "Arena Tribute",
                "is_default": True,
                "hair_style": "Natural curly puffs",
                "hair_color": "#1A1A1A",
                "eye_color": "Dark brown",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["natural curly hair"],
                    "upper": ["grey/green arena jacket", "tribute number"],
                    "lower": ["cargo pants", "boots"],
                    "accessories": ["slingshot", "hidden in trees"]
                },
                "prompt_tags": "rue hunger games, young girl, arena outfit, forest, innocent",
                "negative_prompt": "adult, weapon, violent",
                "color_palette": {"primary": "#556B2F", "secondary": "#2F4F4F", "accent": "#1A1A1A"}
            },
            {
                "name": "Reaping Day",
                "is_default": False,
                "hair_style": "Neat, braided",
                "hair_color": "#1A1A1A",
                "eye_color": "Dark brown",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["neat braids"],
                    "upper": ["simple white blouse"],
                    "lower": ["simple skirt", "clean shoes"],
                    "accessories": ["minimal"]
                },
                "prompt_tags": "rue reaping day, simple dress, nervous expression",
                "negative_prompt": "arena, dirty",
                "color_palette": {"primary": "#FFFFFF", "secondary": "#F5F5DC", "accent": "#1A1A1A"}
            }
        ]
    },
    {
        "name_romaji": "Yoruichi Shihouin",
        "name_native": "四楓院 夜一",
        "alternative_names": ["Flash Goddess", "Yoruichi"],
        "gender": GenderEnum.FEMALE,
        "age": "Unknown (appears 20s)",
        "description": "Former Soul Society captain, master of flash step, can transform into cat.",
        "base_prompt": "Yoruichi from Bleach, dark skin, purple hair, golden eyes, athletic",
        "series_title": "Bleach",
        "variants": [
            {
                "name": "Stealth Force Commander",
                "is_default": True,
                "hair_style": "Long purple ponytail",
                "hair_color": "#6A0DAD",
                "eye_color": "#FFD700",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["long purple hair in ponytail"],
                    "upper": ["orange sleeveless top", "no sleeves"],
                    "lower": ["black tights", "barefoot or sandals"],
                    "accessories": ["arm bandages", "athletic build"]
                },
                "prompt_tags": "yoruichi bleach, purple hair, golden eyes, orange top, athletic, flash step",
                "negative_prompt": "cat form, male, pale skin",
                "color_palette": {"primary": "#FF8C00", "secondary": "#6A0DAD", "accent": "#FFD700"}
            },
            {
                "name": "Shunko Form",
                "is_default": False,
                "hair_style": "Purple hair flowing with energy",
                "hair_color": "#6A0DAD",
                "eye_color": "#FFD700",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["wild purple hair", "energy aura"],
                    "upper": ["backless top", "energy wings", "minimal coverage"],
                    "lower": ["form-fitting pants", "energy flowing"],
                    "accessories": ["white energy aura", "lightning effects"]
                },
                "prompt_tags": "yoruichi shunko, energy aura, white lightning, powerful, combat",
                "negative_prompt": "casual, calm",
                "color_palette": {"primary": "#FFFFFF", "secondary": "#6A0DAD", "accent": "#00BFFF"}
            }
        ]
    },
    {
        "name_romaji": "Canary",
        "name_native": "カナリア",
        "alternative_names": ["Canary"],
        "gender": GenderEnum.FEMALE,
        "age": "Teen",
        "description": "Zoldyck family apprentice butler, skilled fighter.",
        "base_prompt": "Canary from Hunter x Hunter, dark skin, short black hair, butler uniform",
        "series_title": "Hunter x Hunter",
        "variants": [
            {
                "name": "Butler Uniform",
                "is_default": True,
                "hair_style": "Short black hair",
                "hair_color": "#1A1A1A",
                "eye_color": "Dark brown",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["short neat black hair"],
                    "upper": ["black butler vest", "white dress shirt", "black tie"],
                    "lower": ["black pants", "formal shoes"],
                    "accessories": ["white gloves", "staff weapon"]
                },
                "prompt_tags": "canary hunter x hunter, butler uniform, professional, loyal, strength",
                "negative_prompt": "casual clothes, smiling",
                "color_palette": {"primary": "#000000", "secondary": "#FFFFFF", "accent": "#1A1A1A"}
            },
            {
                "name": "Combat Ready",
                "is_default": False,
                "hair_style": "Short black hair",
                "hair_color": "#1A1A1A",
                "eye_color": "Dark brown",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["short hair, determined expression"],
                    "upper": ["modified butler uniform", "rolled sleeves"],
                    "lower": ["combat stance"],
                    "accessories": ["staff raised", "fighting pose"]
                },
                "prompt_tags": "canary fighting, staff combat, protective, determined",
                "negative_prompt": "formal, passive",
                "color_palette": {"primary": "#000000", "secondary": "#FFFFFF", "accent": "#8B4513"}
            }
        ]
    },
    {
        "name_romaji": "Nessa",
        "name_native": "ルリナ",
        "alternative_names": ["Rurina"],
        "gender": GenderEnum.FEMALE,
        "age": "20s",
        "description": "Water-type Gym Leader from Galar region, also a model.",
        "base_prompt": "Nessa from Pokemon Sword Shield, dark skin, blue black hair, water gym leader",
        "series_title": "Pokemon Sword/Shield",
        "variants": [
            {
                "name": "Gym Leader Uniform",
                "is_default": True,
                "hair_style": "Long black hair with blue highlights",
                "hair_color": "#000080",
                "eye_color": "Blue",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["long flowing hair", "blue streaks"],
                    "upper": ["blue and white athletic crop top", "sponsor logos"],
                    "lower": ["blue shorts", "athletic shoes"],
                    "accessories": ["pokeball", "water gym badge"]
                },
                "prompt_tags": "nessa pokemon, gym leader, water type, athletic, confident, blue aesthetic",
                "negative_prompt": "fire type, red colors",
                "color_palette": {"primary": "#1E90FF", "secondary": "#FFFFFF", "accent": "#000080"}
            },
            {
                "name": "Model Photoshoot",
                "is_default": False,
                "hair_style": "Styled long hair",
                "hair_color": "#000080",
                "eye_color": "Blue",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["styled glamorous hair"],
                    "upper": ["fashionable top", "designer outfit"],
                    "lower": ["high fashion bottoms", "heels"],
                    "accessories": ["jewelry", "modeling pose"]
                },
                "prompt_tags": "nessa model, fashion photoshoot, glamorous, magazine cover",
                "negative_prompt": "gym battle, sporty",
                "color_palette": {"primary": "#FFD700", "secondary": "#1E90FF", "accent": "#FFFFFF"}
            }
        ]
    },
    {
        "name_romaji": "Domino (Neena Thurman)",
        "name_native": "Domino",
        "alternative_names": ["Neena", "Lucky"],
        "gender": GenderEnum.FEMALE,
        "age": "30s",
        "description": "Mutant mercenary with probability manipulation powers. Lucky.",
        "base_prompt": "Domino from Deadpool 2, dark skin, big afro, white eye patch vitiligo",
        "series_title": "Deadpool 2",
        "variants": [
            {
                "name": "X-Force Tactical",
                "is_default": True,
                "hair_style": "Large natural afro",
                "hair_color": "#1A1A1A",
                "eye_color": "Brown",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["large afro", "white patch around left eye"],
                    "upper": ["black tactical suit", "armored vest"],
                    "lower": ["tactical pants", "combat boots"],
                    "accessories": ["dual pistols", "utility belt", "confident smirk"]
                },
                "prompt_tags": "domino xforce, afro, white eye patch, black tactical, lucky, action hero",
                "negative_prompt": "no eye patch, comic version pale skin",
                "color_palette": {"primary": "#000000", "secondary": "#FFFFFF", "accent": "#C0C0C0"}
            },
            {
                "name": "Casual Lucky",
                "is_default": False,
                "hair_style": "Afro, relaxed",
                "hair_color": "#1A1A1A",
                "eye_color": "Brown",
                "skin_tone": "Dark brown",
                "outfit_structure": {
                    "head": ["afro", "white eye patch still visible"],
                    "upper": ["casual jacket", "t-shirt"],
                    "lower": ["jeans"],
                    "accessories": ["lucky charm", "relaxed smirk"]
                },
                "prompt_tags": "domino casual, off duty, lucky vibes",
                "negative_prompt": "combat, serious",
                "color_palette": {"primary": "#2F4F4F", "secondary": "#FFFFFF", "accent": "#1A1A1A"}
            }
        ]
    },
    {
        "name_romaji": "Valkyrie (Brunnhilde)",
        "name_native": "Valkyrie",
        "alternative_names": ["Scrapper 142", "King of New Asgard"],
        "gender": GenderEnum.FEMALE,
        "age": "Ancient (appears 30s)",
        "description": "Asgardian warrior, former Valkyrie, King of New Asgard.",
        "base_prompt": "Valkyrie from Thor Ragnarok, dark skin, curly hair, Asgardian armor",
        "series_title": "Thor: Ragnarok",
        "variants": [
            {
                "name": "Valkyrie Armor",
                "is_default": True,
                "hair_style": "Natural curly or braided warrior style",
                "hair_color": "#1A1A1A",
                "eye_color": "Brown",
                "skin_tone": "Medium brown",
                "outfit_structure": {
                    "head": ["curly hair or warrior braids", "optional winged helmet"],
                    "upper": ["silver Asgardian armor", "cape", "blue accents"],
                    "lower": ["armored skirt/pants", "boots"],
                    "accessories": ["Dragonfang sword", "cape", "Asgardian symbols"]
                },
                "prompt_tags": "valkyrie thor, asgardian armor, warrior, dragonfang sword, heroic",
                "negative_prompt": "casual, scrapper outfit",
                "color_palette": {"primary": "#C0C0C0", "secondary": "#4169E1", "accent": "#1A1A1A"}
            },
            {
                "name": "Scrapper 142",
                "is_default": False,
                "hair_style": "Messy natural",
                "hair_color": "#1A1A1A",
                "eye_color": "Brown",
                "skin_tone": "Medium brown",
                "outfit_structure": {
                    "head": ["messy curly hair"],
                    "upper": ["leather jacket", "worn armor pieces", "blue cape"],
                    "lower": ["leather pants", "boots"],
                    "accessories": ["obedience disk controller", "bottle", "cynical expression"]
                },
                "prompt_tags": "valkyrie scrapper, sakaar, bounty hunter, worn leather",
                "negative_prompt": "clean armor, heroic",
                "color_palette": {"primary": "#8B4513", "secondary": "#4169E1", "accent": "#1A1A1A"}
            }
        ]
    }
]


def add_characters_to_db():
    """Add all 10 characters with their variants to the database"""
    engine = create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("=" * 60)
    print("📚 Adding 10 Cosplay Characters to Yuki Knowledge DB")
    print("=" * 60)
    
    added = 0
    for char_data in CHARACTERS:
        # Check if character already exists
        existing = session.query(Character).filter_by(name_romaji=char_data["name_romaji"]).first()
        if existing:
            print(f"   ⚠️ Already exists: {char_data['name_romaji']}")
            continue
        
        # Create character
        character = Character(
            name_romaji=char_data["name_romaji"],
            name_native=char_data["name_native"],
            alternative_names=char_data["alternative_names"],
            gender=char_data["gender"],
            age=char_data["age"],
            description=char_data["description"],
            base_prompt=char_data["base_prompt"],
            role=RoleEnum.MAIN
        )
        session.add(character)
        session.flush()  # Get ID
        
        # Add variants (costumes)
        for var in char_data["variants"]:
            variant = AppearanceVariant(
                character_id=character.id,
                name=var["name"],
                is_default=var["is_default"],
                hair_style=var["hair_style"],
                hair_color=var["hair_color"],
                eye_color=var["eye_color"],
                skin_tone=var["skin_tone"],
                outfit_structure=var["outfit_structure"],
                prompt_tags=var["prompt_tags"],
                negative_prompt=var["negative_prompt"],
                color_palette=var["color_palette"]
            )
            session.add(variant)
        
        print(f"   ✅ Added: {char_data['name_romaji']} ({len(char_data['variants'])} variants)")
        added += 1
    
    session.commit()
    session.close()
    
    print(f"\n{'='*60}")
    print(f"✅ Added {added} characters to database")
    print(f"💾 Database: {DB_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    add_characters_to_db()
