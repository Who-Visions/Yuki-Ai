"""
Organize Test Results
Moves all generated images and logs into a unified folder structure.
"""

import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Organizer")

def organize_results():
    ROOT = Path("C:/Yuki_Local")
    UNIFIED = ROOT / "unified_test_results"
    UNIFIED.mkdir(exist_ok=True)
    
    # Define Categories
    categories = {
        "01_Single_Test_4K": ["test_sung_jinwoo_4k.png", "test_luffy.png"],
        "02_Top15_Batch": ["real_gen_results_top15"],
        "03_Crossplay_Safety_Test": ["real_gen_results_crossplay", "real_gen_results_safety_test"],
        "logs": ["*.log"]
    }
    
    logger.info("=== 📂 ORGANIZING RESULTS ===")
    
    for category, sources in categories.items():
        dest_dir = UNIFIED / category
        dest_dir.mkdir(exist_ok=True)
        
        for source in sources:
            # Handle glob patterns
            if "*" in source:
                for file in ROOT.glob(source):
                    try:
                        shutil.copy2(file, dest_dir / file.name)
                        logger.info(f"   ✅ Copied {file.name} -> {category}/")
                    except Exception as e:
                        logger.warning(f"   ⚠️ Failed to copy {file.name}: {e}")
            
            # Handle directories
            elif (ROOT / source).is_dir():
                src_dir = ROOT / source
                for file in src_dir.glob("*"):
                    try:
                        shutil.copy2(file, dest_dir / file.name)
                        logger.info(f"   ✅ Copied {file.name} -> {category}/")
                    except Exception as e:
                        logger.warning(f"   ⚠️ Failed to copy {file.name}: {e}")
            
            # Handle single files
            elif (ROOT / source).exists():
                src_file = ROOT / source
                try:
                    shutil.copy2(src_file, dest_dir / src_file.name)
                    logger.info(f"   ✅ Copied {src_file.name} -> {category}/")
                except Exception as e:
                    logger.warning(f"   ⚠️ Failed to copy {src_file.name}: {e}")
            
            # Handle files in test_results_test
            elif (ROOT / "real_gen_results_test" / source).exists():
                src_file = ROOT / "real_gen_results_test" / source
                try:
                    shutil.copy2(src_file, dest_dir / src_file.name)
                    logger.info(f"   ✅ Copied {src_file.name} -> {category}/")
                except Exception as e:
                    logger.warning(f"   ⚠️ Failed to copy {src_file.name}: {e}")

    logger.info(f"\n🎉 Organization Complete! Results in: {UNIFIED}")

if __name__ == "__main__":
    organize_results()
