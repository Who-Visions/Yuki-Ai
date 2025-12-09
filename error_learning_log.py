"""
Yuki Self-Learning Error Log
Tracks mistakes, corrections, and prevents repeating errors
"""

ERROR_LOG = [
    {
        "error_id": "001",
        "timestamp": "2025-12-03T02:25:00",
        "error": "Identity Loss - Race Change",
        "description": "Shizuku Mizutani transformation: Black male with dreads → white female",
        "root_cause": [
            "No gender filtering in character DB queries",
            "Female character (Shizuku) selected for male user",
            "Perspective correction prompt didn't explicitly preserve race/ethnicity",
            "Model interpreted 'transform into character' as complete replacement"
        ],
        "fixes_applied": [
            "Added gender keyword filtering to get_characters_by_year()",
            "Added female_keywords list to filter out female characters",
            "Updated facial_geometry_corrector.py to explicitly preserve RACE/ETHNICITY",
            "Added 'PRESERVE: Race, ethnicity, skin tone, gender' to prompts",
            "Added verification: 'If person is BLACK with DREADS, they STAY BLACK'"
        ],
        "prevention": [
            "Always filter characters by gender before generation",
            "Explicitly state race/ethnicity preservation in all analysis prompts",
            "Add race detection to initial analysis phase",
            "Verify identity preservation in generated images"
        ],
        "status": "FIXED",
        "verification_test": "Nadley 2012 test with corrected system"
    },
    {
        "error_id": "002",
        "timestamp": "2025-12-02T22:10:00",
        "error": "Perspective Distortion - Nose Enlargement",
        "description": "Jesse's nose rendered larger than actual due to camera angle",
        "root_cause": [
            "Close-up wide-angle photo causes geometric distortion",
            "No perspective correction applied",
            "Model replicated distorted proportions from input photo"
        ],
        "fixes_applied": [
            "Created facial_geometry_corrector.py module",
            "Added camera angle detection (frontal, low-angle, etc.)",
            "Added lens distortion analysis (wide-angle, telephoto)",
            "Calculate corrected proportions (e.g., 'nose 20% smaller than appears')",
            "Instruct generation to use CORRECTED proportions, not input distortion"
        ],
        "prevention": [
            "Always run perspective correction before generation",
            "Detect close-up shots and adjust facial proportions",
            "Add 'USE CORRECTED PROPORTIONS' instruction to all prompts"
        ],
        "status": "FIXED",
        "verification_test": "Jesse corrected test vs original test comparison"
    },
    {
        "error_id": "003",
        "timestamp": "2025-12-03T01:20:00",
        "error": "Ghost API Calls - No Images Saved",
        "description": "API calls succeeding but files not written to disk",
        "root_cause": [
            "Image data extraction only checked part.image, not part.inline_data",
            "File write success not verified after save",
            "Silent failures - no exception raised when image missing"
        ],
        "fixes_applied": [
            "Updated _generate_single() to check BOTH part.image and part.inline_data",
            "Added explicit file existence verification after write",
            "Added file size logging to confirm save",
            "Raise exception if no image data found in response"
        ],
        "prevention": [
            "Always handle both image response formats",
            "Verify file.exists() after every write",
            "Log file size to confirm actual data written",
            "Never silently fail - always raise exceptions for debugging"
        ],
        "status": "FIXED",
        "verification_test": "Nadley DB test with verified file saves"
    },
    {
        "error_id": "004",
        "timestamp": "2025-12-03T00:14:00",
        "error": "API Quota Exhaustion",
        "description": "Batch generations failing due to rate limits",
        "root_cause": [
            "Too many requests in short time period",
            "No rate limiting or quota management",
            "Retry logic hitting same quota wall"
        ],
        "fixes_applied": [
            "Created local anime database to reduce API calls",
            "Character lookups now use local DB (0 API calls)",
            "Reduced batch size for testing (5 instead of 10)",
            "Added API call counting to track usage"
        ],
        "prevention": [
            "Always check local DB before API calls",
            "Implement exponential backoff for rate limit errors",
            "Start with small batch sizes to test quota",
            "Monitor API call count in real-time"
        ],
        "status": "MITIGATED",
        "notes": "Quota management improved but still subject to API limits"
    },
    {
        "error_id": "005",
        "timestamp": "2025-12-03T03:14:00",
        "error": "Aspect Ratio - Not Optimized for Mobile",
        "description": "Generated images not optimized for vertical mobile viewing",
        "root_cause": [
            "No aspect ratio specified in generation",
            "Defaults to square or landscape",
            "Not optimized for TikTok, Instagram Reels, YouTube Shorts",
            "Misses mobile-first content strategy"
        ],
        "fixes_applied": [
            "Added 9:16 aspect ratio specification to prompts",
            "Added 'Vertical portrait for mobile viewing' instruction",
            "Added 'Full body or 3/4 length shot optimized for phone screens'",
            "Updated all generation configs to prioritize portrait orientation"
        ],
        "prevention": [
            "Always specify 9:16 aspect ratio for mobile content",
            "Optimize composition for vertical viewing",
            "Test on actual phone screens",
            "Follow TikTok/IG Reels best practices"
        ],
        "status": "FIXED",
        "notes": "9:16 is the god ratio for modern social media (TikTok, IG Reels, YT Shorts)"
    },
    {
        "error_id": "006",
        "timestamp": "2025-12-03T08:54:00",
        "error": "Style Mismatch - Anime Art Instead of Photorealistic Cosplay",
        "description": "Model generated anime-style illustrations instead of photorealistic cosplay photos",
        "root_cause": [
            "Prompt said 'Transform into character' (implies becoming anime character)",
            "No explicit instruction for photorealistic style",
            "No instruction to keep person's real face",
            "Vague wording allowed model to interpret as anime art"
        ],
        "fixes_applied": [
            "Changed prompt to 'Create PHOTOREALISTIC COSPLAY photograph'",
            "Added 'Keep the person's REAL FACE (not anime-style)'",
            "Added 'This MUST be a PHOTOGRAPH, not illustration'",
            "Listed what to AVOID (anime art, drawings, cel-shading)",
            "Emphasized COSTUME change, not person transformation",
            "Added 'Think: cosplay convention photo, NOT: anime drawing'"
        ],
        "prevention": [
            "Always use 'PHOTOREALISTIC COSPLAY photograph' in prompt",
            "Explicitly state 'Keep person's REAL FACE'",
            "List forbidden styles (anime art, illustrations)",
            "Emphasize costume/clothing change only",
            "Use reference phrases like 'convention cosplay photo'"
        ],
        "status": "FIXED",
        "notes": "User wants to see THEMSELVES in the COSTUME, not turned into anime art"
    }
]

# Learning rules derived from errors
LEARNED_RULES = {
    "identity_preservation": {
        "rule": "ALWAYS explicitly preserve race, ethnicity, gender, and facial structure",
        "implementation": "Add to ALL analysis and generation prompts",
        "keywords": ["PRESERVE: Race", "PRESERVE: Ethnicity", "PRESERVE: Gender", "PRESERVE: Skin tone"]
    },
    "perspective_correction": {
        "rule": "ALWAYS run geometric correction before generation",
        "implementation": "Use facial_geometry_corrector.py on all input images",
        "keywords": ["CORRECTED proportions", "TRUE nose size", "Perspective compensation"]
    },
    "gender_filtering": {
        "rule": "ALWAYS filter characters by gender to match user",
        "implementation": "Use get_characters_by_year(gender='male'/'female')",
        "keywords": ["gender filter", "male characters only", "female characters only"]
    },
    "verification": {
        "rule": "ALWAYS verify files are actually written",
        "implementation": "Check file.exists() and log file size after save",
        "keywords": ["VERIFIED SAVED", "file size", "exists() check"]
    },
    "db_first": {
        "rule": "ALWAYS check local DB before making API calls",
        "implementation": "Query anime_characters_data.py for character lookups",
        "keywords": ["local DB", "0 API calls", "cached data"]
    },
    "aspect_ratio_mobile": {
        "rule": "ALWAYS use 9:16 aspect ratio for mobile-first content",
        "implementation": "Add 'FORMAT: Vertical portrait (9:16)' to all generation prompts",
        "keywords": ["9:16", "vertical portrait", "mobile viewing", "TikTok", "Instagram Reels"]
    }
}

def get_fixes_for_error_type(error_type: str):
    """Get all learned fixes for a specific error type"""
    return [e for e in ERROR_LOG if error_type.lower() in e['error'].lower()]

def get_prevention_checklist():
    """Get checklist of all preventions to apply"""
    checklist = []
    for error in ERROR_LOG:
        checklist.extend(error['prevention'])
    return list(set(checklist))  # Remove duplicates

# Prevention Checklist (to apply before EVERY generation)
PREVENTION_CHECKLIST = get_prevention_checklist()

if __name__ == "__main__":
    print("=== YUKI SELF-LEARNING ERROR LOG ===\n")
    print(f"Total Errors Logged: {len(ERROR_LOG)}")
    print(f"Fixed: {sum(1 for e in ERROR_LOG if e['status'] == 'FIXED')}")
    print(f"Learned Rules: {len(LEARNED_RULES)}\n")
    
    print("=== PREVENTION CHECKLIST ===")
    for i, item in enumerate(PREVENTION_CHECKLIST, 1):
        print(f"{i}. {item}")
