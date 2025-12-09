import os
import random
import time
from yuki_local import YukiLocal, Colors

# Setup
IMAGE_DIR = r"C:\Yuki_Local\dave test images"
CHARACTERS = [
    "Dante (Devil May Cry 5)",
    "2B (Nier: Automata)",
    "Gojo Satoru (Jujutsu Kaisen)",
    "Lucy (Cyberpunk Edgerunners)",
    "Cloud Strife (Final Fantasy VII Remake)",
    "Makima (Chainsaw Man)",
    "Alucard (Hellsing Ultimate)",
    "Motoko Kusanagi (Ghost in the Shell)",
    "Spike Spiegel (Cowboy Bebop)",
    "Sephiroth (Final Fantasy VII)"
]
FORMATS = [
    "Cinematic Poster",
    "Cosplay Business Card",
    "Comic Book Cover",
    "Viral Social Media Selfie",
    "Action Shot",
    "Magazine Cover",
    "Character Sheet",
    "Cyberpunk Neon Ad",
    "Vintage Anime Style",
    "Hyper-Realistic 8K Render"
]

def run_batch():
    print(f"{Colors.FOX_FIRE}Initializing Batch Simulation Protocol...{Colors.RESET}")
    
    # Get images
    try:
        images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        images.sort() # Ensure consistent order
    except Exception as e:
        print(f"Error accessing image directory: {e}")
        return

    if not images:
        print("No images found!")
        return

    # Initialize Yuki
    yuki = YukiLocal()
    
    # Run simulations
    for i in range(10):
        if i >= len(images):
            break
            
        image_name = images[i]
        image_path = os.path.join(IMAGE_DIR, image_name)
        character = CHARACTERS[i % len(CHARACTERS)]
        fmt = FORMATS[i % len(FORMATS)]
        
        # Randomly choose number of variations (1, 2, or 4)
        num_variations = random.choice([1, 2, 4])
        
        print(f"\n{Colors.ICE_BLUE}═══════════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}SIMULATION {i+1}/10{Colors.RESET}")
        print(f"Image: {image_name}")
        print(f"Character: {character}")
        print(f"Format: {fmt}")
        print(f"Variations: {num_variations}")
        print(f"{Colors.ICE_BLUE}═══════════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        
        prompt = (
            f"I want to generate {num_variations} cosplay image variations. "
            f"Use this reference image: {image_path} "
            f"Transform the subject into {character}. "
            f"Render style: {fmt}. "
            f"Use Nano Banana Pro quality. "
            f"Ensure you use the file path provided."
        )
        
        # Execute Generation
        try:
            result = yuki.query(prompt)
            print(f"\n{Colors.SUCCESS_GREEN}>> Result for Simulation {i+1}:{Colors.RESET}")
            output_text = result.get("output", "No output")
            print(output_text)
            
            # Extract image path from output or logs (simple heuristic)
            # We look for the standard output format from our tool
            import re
            match = re.search(r"generated_images/yuki_\d+\.png", output_text)
            if not match:
                # Try to find it in the tool output logs if we could, but here we just scan the dir for the newest file
                # or just rely on the fact that we know where it saves.
                # Let's find the newest file in generated_images
                gen_dir = "generated_images"
                if os.path.exists(gen_dir):
                    files = [os.path.join(gen_dir, f) for f in os.listdir(gen_dir) if f.startswith("yuki_") and f.endswith(".png")]
                    if files:
                        generated_file = max(files, key=os.path.getctime)
                    else:
                        generated_file = None
                else:
                    generated_file = None
            else:
                generated_file = match.group(0)
            
            if generated_file and os.path.exists(generated_file):
                print(f"\n{Colors.FOX_FIRE}[☁️ CLOUD VERIFICATION] Testing Cloud Sync for {generated_file}...{Colors.RESET}")
                
                # 1. Upload to Cloud
                from tools import upload_file_to_gcs, download_from_gcs
                
                cloud_path = f"simulations/batch_1/{os.path.basename(generated_file)}"
                
                upload_result = upload_file_to_gcs(generated_file, cloud_path)
                print(f"    Upload: {upload_result}")
                
                if "Successfully uploaded" in upload_result:
                    # 2. Delete Local File (Simulate loss)
                    print(f"    🗑️ Deleting local file to test restore...")
                    os.remove(generated_file)
                    
                    if not os.path.exists(generated_file):
                        print(f"    ✓ Local file deleted.")
                    
                    # 3. Download from Cloud
                    restore_path = generated_file.replace("generated_images", "restored_images")
                    download_result = download_from_gcs(cloud_path, restore_path)
                    print(f"    Download: {download_result}")
                    
                    if os.path.exists(restore_path):
                        print(f"    {Colors.SUCCESS_GREEN}✓ VERIFICATION PASSED: Image restored from cloud!{Colors.RESET}")
                    else:
                        print(f"    {Colors.ERROR_RED}❌ VERIFICATION FAILED: Image not found after download.{Colors.RESET}")
                else:
                    print(f"    {Colors.ERROR_RED}❌ VERIFICATION FAILED: Upload failed.{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.ERROR_RED}Simulation failed: {e}{Colors.RESET}")
        
        # Small pause to be nice to the API
        time.sleep(2)

if __name__ == "__main__":
    run_batch()
