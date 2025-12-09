# Local Hyperrealistic Consistent Character Guide (ComfyUI + Wan 2.1)

*Based on "Create HYPERREALISTIC Consistent AI Characters - FREE & LOCAL! [Full ComfyUI Masterclass 2025]"*

## Overview
This workflow provides a **free, local, and uncensored** alternative to commercial tools like Nano Banana Pro (Imagen 4). It focuses on creating a perfect dataset from a single input image, training a custom LoRA, and generating hyperrealistic images and 4K videos using the **Wan 2.1** model.

## Core Technology Stack
*   **ComfyUI**: The node-based interface for orchestration.
*   **Gwen Image Edit (Alibaba)**: Open-source model for character merging, pose extraction, and virtual try-on.
*   **Flux + Yuzo**: Used for high-fidelity upscaling and consistency preservation during dataset creation.
*   **AI Toolkit**: For training LoRAs (Local or Cloud/RunPod).
*   **Wan 2.1**: A powerful video generation model that also excels at hyperrealistic image generation.

## Workflow Stages

### Phase 1: Character Expansion (Gwen Image Edit)
**Goal:** Turn a single input image into a diverse set of reference images.
1.  **Input:** Drag and drop a single reference image (any style).
2.  **Prompting:**
    *   Set a **Trigger Word** (e.g., character name). This is crucial for LoRA training later.
    *   Add clothing details to the prompt (e.g., "wearing chunky sneakers") to fill in missing information from a portrait crop.
3.  **Generation Modules:**
    *   **Turnaround Sheet:** Generates front, side, and back views.
    *   **Emotions:** Generates variations like "Ah" (mouth open), angry, happy.
    *   **Poses:** T-pose, laying down, walking in nature.
    *   **Virtual Try-On:** Drag and drop a clothing item image to dress the character.
    *   **Pose Transfer:** Upload a reference pose image to apply it to the character.
4.  **Output:** A folder of raw character images in various situations.

### Phase 2: Dataset Creation (Automated)
**Goal:** Clean, caption, and upscale the raw images for training.
1.  **Selection:** Choose the best images from Phase 1 (or use all).
2.  **Process:**
    *   **Auto-Captioning:** Generates detailed text descriptions including the trigger word.
    *   **Upscaling (Flux + Yuzo):** Upscales images to **2K resolution**.
    *   **Consistency Check:** Yuzo ensures the character's identity remains stable during upscaling.
    *   *Tip:* Adjust "Start Step" (e.g., 12-18 out of 20) to control how much detail is added vs. original identity preserved.
3.  **Result:** A `dataset` folder containing high-res images and matching `.txt` caption files.

### Phase 3: LoRA Training (Wan 2.1)
**Goal:** Train a model that "knows" your character perfectly.
*   **Tool:** AI Toolkit (via Pinocchio locally or RunPod for speed).
*   **Model Selection:** Train on **Wan 2.1** (or 2.0 compatible). Wan 2.1 is a video model but creates SOTA realistic images.
*   **Configuration:**
    *   **Steps:** Save checkpoints every 500 steps.
    *   **Resolution:** 512x512 or higher (depending on VRAM).
    *   **Samples:** Generate sample images during training to monitor progress.
*   **Cost/Time:** ~1.5 hours on a cloud GPU (~$4) or longer locally.

### Phase 4: Inference (Image & Video)
**Goal:** Generate final assets.
*   **Setup:** ComfyUI with Wan 2.1 model + Your Trained LoRA.
*   **Realism Stack:**
    *   **LoRAs:** Use `Lenovo Ultra Real` and `Insta Real 2.2` alongside your character LoRA.
    *   **Post-Processing:** Add Chromatic Aberration, Artificial Sharpening, Bloom, and Film Grain for a cinematic look.
*   **Speed Hack (LightX):** Use "LightX" LoRAs to reduce generation steps from ~30 to **4-8 steps** (50s vs 160s).
*   **Video Generation:**
    *   Switch workflow to video mode (e.g., 41 frames).
    *   Use LLMs (Claude/Gemini) to rewrite image prompts into dynamic video prompts (describing camera movement).
    *   **4K Upscaling:** Use a tiled upscaling workflow to reach 4K resolution without exploding VRAM.

## Key Advantages vs. Nano Banana
*   **Uncensored:** No safety filters blocking creative outputs.
*   **Consistency:** LoRA training provides superior identity retention compared to zero-shot prompting.
*   **Video Native:** Wan 2.1 is built for video, allowing seamless transition from still images to 4K motion.
*   **Free/Cheap:** Runs locally (free) or cheaply on cloud GPUs, avoiding subscription costs.
