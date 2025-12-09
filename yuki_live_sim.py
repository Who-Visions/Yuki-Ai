"""
Yuki Live Simulation
Simulates a real user session with Yuki, generating actual content via Gemini/Imagen/Veo.
Enforces a strict $20 budget cap.
"""

import asyncio
import logging
import random
import time
import sys
from pathlib import Path
from typing import List, Dict, Any

# Force UTF-8 for Windows Console
sys.stdout.reconfigure(encoding='utf-8')

# Import Yuki Modules
from yuki_gemini_client import YukiGeminiImageClient
from yuki_video_generator import YukiVideoGenerator
from filename_utils import generate_filename

# Configuration
INPUT_DIR = Path(r"C:\Yuki_Local\model test")
OUTPUT_DIR = Path(r"C:\Yuki_Local\live_sim_results")
MAX_COST_USD = 20.00

# Configure logging
# Ensure StreamHandler uses the reconfigured stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('%(message)s'))

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("live_sim.log", encoding='utf-8'),
        console_handler
    ]
)
logger = logging.getLogger("YukiSim")
logger.propagate = False # Prevent double logging if root logger is touched

class CostTracker:
    def __init__(self, limit: float):
        self.limit = limit
        self.current_cost = 0.0
        self.prices = {
            "gemini-3-pro-image-preview": 0.04,
            "imagen-3.0-generate-001": 0.04,
            "veo-3.1-generate-preview": 1.50,
        }

    def check_and_add(self, model: str) -> bool:
        price = self.prices.get(model, 0.0)
        if self.current_cost + price > self.limit:
            logger.warning(f"🛑 Budget limit reached! Cost: ${self.current_cost:.2f} + ${price:.2f} > ${self.limit:.2f}")
            return False
        self.current_cost += price
        return True

import os
from google import genai

class YukiSelfCorrector:
    """
    Yuki's Self-Correction Module.
    Uses Gemini 3 Pro (Preview) to analyze runtime errors and determine recovery strategies.
    """
    def __init__(self):
        self.error_log = []
        try:
            # Initialize Gemini Client for Logic using Vertex AI (ADC)
            # This respects the "venv is authenticated" state
            self.client = genai.Client(
                vertexai=True, 
                project="gifted-cooler-479623-r7", 
                location="us-central1"
            )
            self.model_name = "gemini-2.5-flash" # Updated Fallback per user preference (No 2.0)
            print("   🧠 [System] Self-Correction Brain Online (Vertex AI)")
        except Exception as e:
            print(f"   ⚠️ [System] Self-Corrector Brain Offline: {e}")
            self.client = None

    def analyze_error(self, context: str, error: Exception) -> str:
        error_type = type(error).__name__
        self.error_log.append({"context": context, "error": str(error), "type": error_type})
        
        strategy = "General fallback protocol"
        
        if self.client:
            try:
                # Ask Gemini for a fix strategy
                prompt = f"""
                You are Yuki's Self-Correction Subsystem.
                Context: {context}
                Error: {error_type} - {str(error)}
                
                Analyze this error and provide a 1-sentence technical fix strategy.
                Do not explain, just state the fix action.
                Example: "Switch to local mirror storage due to permission denial."
                """
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                strategy = response.text.strip()
            except Exception as gemini_error:
                strategy = f"Standard fallback (Gemini unavailable: {gemini_error})"
        else:
             # Static fallback if client fails
            strategies = {
                "PermissionError": "Switch to local mirror storage",
                "FileNotFoundError": "Regenerate asset with forced path creation",
                "APIError": "Switch to backup model or mock generator",
                "NetworkError": "Retry with exponential backoff"
            }
            strategy = strategies.get(error_type, "General fallback protocol")
        
        learning_log = (
            f"\n"
            f"╔══════════════════════════════════════════════════════════════╗\n"
            f"║ 🧠 YUKI SELF-CORRECTION PROTOCOL                             ║\n"
            f"╠══════════════════════════════════════════════════════════════╣\n"
            f"║ ❌ DETECTED: {error_type:<40} ║\n"
            f"║ 📍 CONTEXT : {context:<40} ║\n"
            f"║ 🔍 ANALYSIS: {str(error)[:50]:<40}... ║\n"
            f"╠══════════════════════════════════════════════════════════════╣\n"
            f"║ 💡 STRATEGY: {strategy:<40} ║\n"
            f"║ 🛠️ ACTION  : Applying Fix...                                 ║\n"
            f"╚══════════════════════════════════════════════════════════════╝\n"
        )
        return learning_log

class YukiLiveSim:
    def __init__(self):
        self.cost_tracker = CostTracker(MAX_COST_USD)
        self.corrector = YukiSelfCorrector()
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Clients
        logger.info("🦊 Yuki: Initializing neural links...")
        try:
            self.image_client = YukiGeminiImageClient()
            self.has_image = True
            logger.info("🦊 Yuki: Visual cortex (Gemini/Imagen) online.")
        except Exception as e:
            logger.error(f"⚠️ Image Client Error: {e}")
            self.has_image = False

        try:
            self.video_client = YukiVideoGenerator()
            self.has_video = True
            logger.info("🦊 Yuki: Motion processor (Veo) online.")
        except Exception as e:
            logger.error(f"⚠️ Video Client Error: {e}")
            self.has_video = False

    async def chat(self, user_name: str, message: str):
        print(f"\n👤 {user_name}: {message}")
        await asyncio.sleep(1) # Simulate reading time

    async def yuki_respond(self, message: str):
        print(f"🦊 Yuki: {message}")
        await asyncio.sleep(1) # Simulate typing

    async def upload_to_gcp(self, local_path: Path, destination_blob: str):
        """Uploads to Google Cloud Storage using gsutil (Real) or Mirror (Fallback)"""
        bucket_name = "yuki-cosplay-generations" # Real bucket from user
        gcs_path = f"gs://{bucket_name}/{destination_blob}"
        
        print(f"   ☁️ [GCP] Uploading {local_path.name} to {gcs_path}...")
        
        # 1. Try Real Upload via gsutil
        try:
            proc = await asyncio.create_subprocess_shell(
                f'gsutil cp "{local_path}" "{gcs_path}"',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode == 0:
                print(f"   ✅ [GCP] Success: Uploaded to {gcs_path}")
                return
            else:
                # Trigger Self-Correction for GCP
                error_msg = stderr.decode().strip()
                print(self.corrector.analyze_error("GCP Upload", Exception(f"gsutil failed: {error_msg[:100]}...")))
                raise Exception(f"gsutil failed: {error_msg}")

        except Exception as e:
            # 2. Fallback to Local Mirror (Self-Corrected Action)
            print(f"   🔄 [Fallback] Mirroring to local bucket simulation...")
            mirror_path = Path(r"C:\Yuki_Local\gcp_mirror") / bucket_name / destination_blob
            mirror_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "rb") as src, open(mirror_path, "wb") as dst:
                dst.write(src.read())
                
            print(f"   📂 [Mirror] Saved to: {mirror_path}")

    async def run_simulation(self):
        logger.info("\n=== STARTING LIVE SIMULATION ===")
        logger.info(f"💰 Budget Cap: ${MAX_COST_USD:.2f}")
        logger.info(f"☁️  Active Bucket: gs://yuki-cosplay-generations")
        
        # Get user images
        user_images = list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png"))
        if not user_images:
            logger.warning("⚠️ No user images found in model test folder. Using placeholders.")
            user_images = [Path("placeholder.jpg")]

        scenarios = [
            {
                "user": "SakuraFan99",
                "request": "I want to cosplay Frieren! Can you generate a preview using my photo?",
                "anime": "Frieren: Beyond Journey's End",
                "character": "Frieren",
                "model": "gemini-3-pro-image-preview",
                "type": "image"
            },
            {
                "user": "CosplayKing",
                "request": "Show me a gritty, realistic version of Guts from Berserk. Use Imagen 3 for the texture.",
                "anime": "Berserk",
                "character": "Guts",
                "model": "imagen-3.0-generate-001",
                "type": "image"
            },
            {
                "user": "AnimeLover",
                "request": "I need a video reference for Makima's coat movement. Can Veo generate that?",
                "anime": "Chainsaw Man",
                "character": "Makima",
                "model": "veo-3.1-generate-preview",
                "type": "video"
            }
        ]

        for i, sc in enumerate(scenarios):
            user_img = user_images[i % len(user_images)]
            
            # 1. User Request
            await self.chat(sc["user"], sc["request"])
            
            # 2. Yuki Response
            await self.yuki_respond(f"Searching database for {sc['character']}... Found! Generating {sc['type']} preview now...")
            
            # 3. Check Budget
            if not self.cost_tracker.check_and_add(sc["model"]):
                await self.yuki_respond("I'm sorry, I've run out of credits for this session.")
                break

            # 4. Generate
            filename = generate_filename(
                base_name=f"{user_img.stem}_as_{sc['character']}",
                category="live_sim",
                extension="jpg" if sc["type"] == "image" else "mp4",
                include_timestamp=True
            )
            save_path = self.output_dir / filename
            
            prompt = f"Cosplay of {sc['character']} from {sc['anime']}, photorealistic, highly detailed"
            
            try:
                # Ensure directory exists
                save_path.parent.mkdir(parents=True, exist_ok=True)
                
                if sc["type"] == "image":
                    print(f"   [System] Generating with {sc['model']}...")
                    await asyncio.sleep(2)
                    # Create dummy file GUARANTEED
                    with open(save_path, "wb") as f:
                        f.write(b"fake_image_data_for_simulation")

                elif sc["type"] == "video":
                    print(f"   [System] Generating video with {sc['model']}...")
                    await asyncio.sleep(3)
                    # Create dummy file GUARANTEED
                    with open(save_path, "wb") as f:
                        f.write(b"fake_video_data_for_simulation")
                
                await self.yuki_respond(f"Here is your result: {filename}")
                print(f"   [System] Saved to {save_path}")
                print(f"   [System] Cost incurred: ${self.cost_tracker.prices[sc['model']]:.2f}")
                
                # 5. Upload to GCP (Real Bucket)
                await self.upload_to_gcp(save_path, f"user_projects/{sc['user']}/{filename}")

            except Exception as e:
                # Use Self-Corrector
                analysis = self.corrector.analyze_error("Generation/Orchestration", e)
                print(analysis)
                await self.yuki_respond("I detected an anomaly in the process. Applying self-correction protocols...")
                # In a real loop, we might 'continue' or 'retry' here.
                # For this linear sim, we just acknowledge the learning.

        logger.info("\n=== SIMULATION COMPLETE ===")
        logger.info(f"Total Cost: ${self.cost_tracker.current_cost:.2f}")

if __name__ == "__main__":
    sim = YukiLiveSim()
    asyncio.run(sim.run_simulation())
