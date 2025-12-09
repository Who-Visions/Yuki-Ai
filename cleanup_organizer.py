"""
🧹 YUKI WORKSPACE CLEANUP 🧹
Moves files into organized 'Cosplay_Lab' structure.
"""
import shutil
import os
from pathlib import Path

ROOT = Path("c:/Yuki_Local")
LAB = ROOT / "Cosplay_Lab"

STRUCTURE = {
    "Subjects": [
        "jordan test", "snow test", "snow test 2", "Dav3 test", 
        "friends test", "jesse 1 pic test", "dave test images",
        "group test", "model test", "storm_input.png"
    ],
    "Renders": [
        "jordan_test_results", "jordan_dc_results", "jordan_dc_movies_results",
        "jordan_v6_random8_results", "jordan_v6_round2_results",
        "snow_test_results", "snow_test_opt3_results", "snow_test2_opt3_results",
        "snow_test2_enhanced_results", "snow_v3_test_results", "snow_v4_advanced_results",
        "snow_v5_photorealism_results", "snow_v5lite_results",
        "real_gen_results", "real_gen_results_fast", "real_gen_results_hybrid",
        "real_gen_results_crossplay", "real_gen_results_bypass", "real_gen_results_safety_test",
        "storm_results", "storm_results_v2",
        "yuki_v7_yolo_results", "generated_images", "stress_test_results",
        "unified_test_results", "dav3_anime_synergy_results", "dav3_comparison_results",
        "nadley_db_results", "nadley_2012_results", "nadley_retry_test", "nadley_6anime_test",
        "dave_test_results", "jesse_test_results", "live_sim_results"
    ],
    "Brain": [
        "yuki_brain_v7.py", "yuki_knowledge_service.py", "facial_ip_extractor_v7.py",
        "enrich_yuki_brain.py", "migrate_knowledge.py", "init_yuki_brain.py",
        "dc_character_bank.py", "anime_character_bank.py", "movie_characters_bank.py",
        "movie_stars_bank.py", "male_character_bank.py", "male_character_bank_1k.py",
        "yuki_memory.db", "jordan_v7_ip.json", "snow_v7_ip.json", "nadly_v7_ip.json", "jesse_v7_ip.json", "dav3_v7_ip.json"
    ],
    "Tests": [
        "jordan_v6_enhanced_test.py", "jordan_v6_random8_test.py", "jordan_fix_furiosa.py",
        "storm_gen_4versions.py", "storm_retry_mohawk.py", "storm_retry_90s.py", "storm_gen_v2_enhanced.py",
        "snow_test_generator.py", "snow_test_v2.py", "snow_test_comparison.py", "snow_test_opt3.py",
        "snow_test2_opt3.py", "snow_test2_enhanced.py", "snow_v3_test.py", "snow_v4_advanced_test.py",
        "snow_v5_photorealism_test.py", "snow_v5lite_test.py",
        "yuki_crossplay_test.py", "dav3_5char_comparison.py", "dav3_anime_synergy.py",
        "dav3_anime_classics_opt3.py", "jesse_classic_test.py", "jesse_corrected_test.py",
        "nadley_2012_test.py", "nadley_6anime_test.py", "nadley_retry_test.py",
        "jordan_dc_test.py", "jordan_dc_movies_test.py", "jordan_primary_subject_test.py",
        "facial_ip_extractor_v3.py", "facial_ip_extractor_v4_vfx.py", "facial_ip_extractor_v5.py", "facial_ip_extractor_v6.py"
    ],
    "Logs": [
        "real_gen.log", "real_gen_fast.log", "stress_test.log", "safety_stress_test.log",
        "jesse_test.log", "dave_test.log", "gender_bent_test.log", "live_sim.log", "top15_batch.log",
        "nadley_test.log", "nadley_6anime_test.log", "video_generation.log", "crossplay_test.log"
    ]
}

def main():
    print("🧹 Cleaning Workspace...")
    
    LAB.mkdir(exist_ok=True)
    for folder in STRUCTURE:
        (LAB / folder).mkdir(exist_ok=True)

    for category, items in STRUCTURE.items():
        dest_dir = LAB / category
        for item in items:
            src = ROOT / item
            if src.exists():
                try:
                    shutil.move(str(src), str(dest_dir / item))
                    print(f"Moved: {item} -> {category}/")
                except Exception as e:
                    print(f"FAILED {item}: {e}")
            else:
                # Wildcard check for missed files
                 pass

    print("✨ Cleanup Complete.")

if __name__ == "__main__":
    main()
