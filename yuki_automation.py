"""
Yuki Automation Engine
Complete end-to-end automation: Scrape → Extract → Generate → Test
"Build the system that builds the system" - Fully automated character processing
"""

import asyncio
import json
from pathlib import Path
from typing import List, Dict
from gemini_orchestrator import GeminiOrchestrator, SubAgentTask, OrchestratorSession
from anime_database import AnimeDatabase
from face_math import FaceMathArchitect
from tools import generate_cosplay_image
import datetime

class YukiAutomationEngine:
    """
    Complete automation engine for anime character processing
    Implements the "orchestration level" from the video
    """
    
    def __init__(self):
        self.orchestrator = GeminiOrchestrator()
        self.db = AnimeDatabase()
        self.face_math = FaceMathArchitect()
        self.automation_logs = Path("c:/Yuki_Local/automation_logs")
        self.automation_logs.mkdir(exist_ok=True)
    
    async def full_pipeline_automation(
        self,
        anime_titles: List[str],
        target_cosplay_characters: List[str],
        source_image_path: str
    ) -> Dict:
        """
        COMPLETE AUTOMATION PIPELINE
        
        Step 1: Scrape character data for anime titles
        Step 2: Organize training data
        Step 3: Extract face schemas (parallelized)
        Step 4: Generate cosplays (parallelized)
        Step 5: Test outputs
        
        Pattern: Plan → Build → Host → Test (from the video)
        """
        print(f"\n{'='*80}")
        print(f"🚀 YUKI AUTOMATION ENGINE - FULL PIPELINE")
        print(f"{'='*80}")
        
        pipeline_start = datetime.datetime.now()
        log = {
            "started_at": pipeline_start.isoformat(),
            "anime_titles": anime_titles,
            "target_characters": target_cosplay_characters,
            "stages": []
        }
        
        # ====================================================================
        # STAGE 1: AUTOMATED SCRAPING & DATA ORGANIZATION
        # ====================================================================
        print(f"\n[STAGE 1/5] 📥 Automated Character Scraping")
        stage1_start = datetime.datetime.now()
        
        scrape_session = self.orchestrator.create_orchestration_plan(
            objective=f"Scrape character data for {len(anime_titles)} anime series",
            context={
                "anime_titles": anime_titles,
                "operation": "scrape_characters",
                "data_sources": ["myanimelist", "anilist", "animenewsnetwork"]
            }
        )
        
        scrape_results = await self.orchestrator.execute_plan_parallel(scrape_session)
        
        log["stages"].append({
            "stage": 1,
            "name": "scraping",
            "duration_seconds": (datetime.datetime.now() - stage1_start).total_seconds(),
            "sub_agents_used": scrape_session.total_tasks,
            "completed": scrape_session.completed_tasks
        })
        
        # ====================================================================
        # STAGE 2: AUTOMATED TRAINING DATA ORGANIZATION
        # ====================================================================
        print(f"\n[STAGE 2/5] 📁 Automated Training Organization")
        stage2_start = datetime.datetime.now()
        
        org_session = self.orchestrator.create_orchestration_plan(
            objective="Organize character images into training structure",
            context={
                "database_path": "c:/Yuki_Local/anime_database.json",
                "operation": "organize_training",
                "create_manifest": True
            }
        )
        
        org_results = await self.orchestrator.execute_plan_parallel(org_session)
        
        log["stages"].append({
            "stage": 2,
            "name": "organization",
            "duration_seconds": (datetime.datetime.now() - stage2_start).total_seconds(),
            "sub_agents_used": org_session.total_tasks
        })
        
        # ====================================================================
        # STAGE 3: PARALLEL FACE SCHEMA EXTRACTION
        # ====================================================================
        print(f"\n[STAGE 3/5] 🧮 Parallel Face Math Extraction")
        stage3_start = datetime.datetime.now()
        
        # Get all characters from database
        characters_to_process = list(self.db.characters.values())[:10]  # Limit for demo
        
        extraction_session = self.orchestrator.create_orchestration_plan(
            objective=f"Extract face schemas for {len(characters_to_process)} characters in parallel",
            context={
                "character_ids": [c.id for c in characters_to_process],
                "operation": "extract_face_schemas",
                "use_gemini_3": True,
                "fallback_to_2_5": True
            }
        )
        
        extraction_results = await self.orchestrator.execute_plan_parallel(extraction_session)
        
        log["stages"].append({
            "stage": 3,
            "name": "face_extraction",
            "duration_seconds": (datetime.datetime.now() - stage3_start).total_seconds(),
            "sub_agents_used": extraction_session.total_tasks,
            "schemas_extracted": extraction_session.completed_tasks
        })
        
        # ====================================================================
        # STAGE 4: BATCH COSPLAY GENERATION (PARALLELIZED)
        # ====================================================================
        print(f"\n[STAGE 4/5] 🎨 Parallel Cosplay Generation")
        stage4_start = datetime.datetime.now()
        
        # Get characters with extracted schemas
        chars_with_schemas = [
            c for c in self.db.characters.values() 
            if c.face_schema.extracted
        ][:5]  # Limit for demo
        
        # Create all source x target combinations
        generation_tasks = []
        for char in chars_with_schemas:
            for target_char in target_cosplay_characters:
                generation_tasks.append({
                    "source_character": char.name_full,
                    "target_character": target_char,
                    "source_image": source_image_path
                })
        
        gen_session = self.orchestrator.create_orchestration_plan(
            objective=f"Generate {len(generation_tasks)} cosplay variations in parallel",
            context={
                "generation_tasks": generation_tasks,
                "operation": "batch_cosplay_generation",
                "use_gemini_3_image": True,
                "fallback_chain": ["gemini-2.5-flash-image", "imagen-4.0-ultra-generate-001"]
            }
        )
        
        gen_results = await self.orchestrator.execute_plan_parallel(gen_session)
        
        log["stages"].append({
            "stage": 4,
            "name": "cosplay_generation",
            "duration_seconds": (datetime.datetime.now() - stage4_start).total_seconds(),
            "sub_agents_used": gen_session.total_tasks,
            "images_generated": gen_session.completed_tasks
        })
        
        # ====================================================================
        # STAGE 5: AUTOMATED QUALITY TESTING
        # ====================================================================
        print(f"\n[STAGE 5/5] ✅ Automated Quality Testing")
        stage5_start = datetime.datetime.now()
        
        test_session = self.orchestrator.create_orchestration_plan(
            objective="Test generated cosplay outputs for quality and identity preservation",
            context={
                "operation": "quality_testing",
                "test_metrics": [
                    "identity_preservation",
                    "costume_accuracy",
                    "image_quality",
                    "face_schema_adherence"
                ]
            }
        )
        
        test_results = await self.orchestrator.execute_plan_parallel(test_session)
        
        log["stages"].append({
            "stage": 5,
            "name": "testing",
            "duration_seconds": (datetime.datetime.now() - stage5_start).total_seconds(),
            "sub_agents_used": test_session.total_tasks
        })
        
        # ====================================================================
        # FINAL SYNTHESIS
        # ====================================================================
        total_duration = (datetime.datetime.now() - pipeline_start).total_seconds()
        log["completed_at"] = datetime.datetime.now().isoformat()
        log["total_duration_seconds"] = total_duration
        log["total_sub_agents_spawned"] = sum(s["sub_agents_used"] for s in log["stages"])
        
        # Save automation log
        log_file = self.automation_logs / f"automation_{pipeline_start.strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=2)
        
        print(f"\n{'='*80}")
        print(f"✅ PIPELINE COMPLETE")
        print(f"{'='*80}")
        print(f"  Total Duration: {total_duration:.1f}s")
        print(f"  Sub-Agents Spawned: {log['total_sub_agents_spawned']}")
        print(f"  Log: {log_file}")
        print(f"{'='*80}\n")
        
        return log

    async def continuous_monitoring_automation(self, interval_seconds: int = 3600):
        """
        Continuous automation loop
        "Build the system that builds the system"
        
        Monitors database for:
        - New characters without face schemas → Auto-extract
        - Characters with schemas but no cosplays → Auto-generate
        - Failed extractions → Retry with different models
        """
        print(f"\n[♾️ CONTINUOUS AUTOMATION] Starting monitoring loop...")
        print(f"  Checking every {interval_seconds}s")
        
        while True:
            print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Scanning database...")
            
            # Check for characters needing schema extraction
            needs_extraction = [
                c for c in self.db.characters.values()
                if not c.face_schema.extracted and c.reference_images
            ]
            
            if needs_extraction:
                print(f"  Found {len(needs_extraction)} characters needing extraction")
                session = self.orchestrator.create_orchestration_plan(
                    objective=f"Auto-extract {len(needs_extraction)} missing schemas",
                    context={
                        "character_ids": [c.id for c in needs_extraction],
                        "operation": "auto_extract"
                    }
                )
                await self.orchestrator.execute_plan_parallel(session)
            
            # Check for characters with schemas but no generations
            needs_generation = [
                c for c in self.db.characters.values()
                if c.face_schema.extracted and len(c.cosplay_generations) == 0
            ]
            
            if needs_generation:
                print(f"  Found {len(needs_generation)} characters ready for generation")
                # Auto-generate with default target characters
                session = self.orchestrator.create_orchestration_plan(
                    objective=f"Auto-generate cosplays for {len(needs_generation)} characters",
                    context={
                        "character_ids": [c.id for c in needs_generation],
                        "default_targets": ["Dante", "Cloud Strife", "Kirito"],
                        "operation": "auto_generate"
                    }
                )
                await self.orchestrator.execute_plan_parallel(session)
            
            if not needs_extraction and not needs_generation:
                print(f"  ✓ Database is up-to-date")
            
            print(f"  Sleeping for {interval_seconds}s...")
            await asyncio.sleep(interval_seconds)

# =============================================================================
# CLI INTERFACE
# =============================================================================

async def main():
    import sys
    
    engine = YukiAutomationEngine()
    
    if len(sys.argv) < 2:
        print("""
        Yuki Automation Engine
        
        Commands:
            # Full pipeline automation
            python yuki_automation.py pipeline "FMA,Death Note" "Dante,Cloud" path.png
            
            # Continuous monitoring (runs forever)
            python yuki_automation.py monitor
            
            # Custom interval (in seconds)
            python yuki_automation.py monitor 1800
        """)
        return
    
    command = sys.argv[1]
    
    if command == "pipeline":
        anime_titles = sys.argv[2].split(",")
        targets = sys.argv[3].split(",")
        image = sys.argv[4]
        
        log = await engine.full_pipeline_automation(
            anime_titles=anime_titles,
            target_cosplay_characters=targets,
            source_image_path=image
        )
        
        print(f"\n📊 AUTOMATION SUMMARY")
        print(json.dumps(log, indent=2))
    
    elif command == "monitor":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
        await engine.continuous_monitoring_automation(interval_seconds=interval)

if __name__ == "__main__":
    asyncio.run(main())
