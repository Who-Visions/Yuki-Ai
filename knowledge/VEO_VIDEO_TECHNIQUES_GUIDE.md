# Veo 3.1 & Nano Banana Pro: Advanced Video Techniques

*Based on "Nano Banana Pro + VEO 3.1 = GOD MODE!"*

## Core Concept: First & Last Frame Animation
The most powerful technique is generating a **First Frame** and a **Last Frame** in Nano Banana Pro (Imagen 4), then using Veo 3.1 to animate between them.

## Techniques

### 1. Cinematic Time-Lapses
*   **Seasons:**
    *   *Frame 1:* Summer tree (green leaves).
    *   *Frame 2:* Winter tree (snow, bare branches).
    *   *Prompt:* "Time lapse of an oak tree shifting through seasons... green summer leaves turning orange... falling... becoming bare and covered in snow."
*   **Blooming:**
    *   *Frame 1:* Tightly closed rose bud.
    *   *Frame 2:* Rose in full bloom.
    *   *Prompt:* "Time lapse of a rose blooming."
*   **Aging:**
    *   *Frame 1:* Young person.
    *   *Frame 2:* Elderly version of same person.
*   **Construction:** Empty site -> Skyscraper.

### 2. Aerial Zooms (The "God Mode" Zoom)
*   **Concept:** Zoom from a huge wide shot to an extreme close-up.
*   *Frame 1:* Aerial view of a cowboy on a horse (100m away).
*   *Frame 2:* Close-up of the cowboy's face.
*   *Prompt:* "Cinematic aerial zoom shot descending from the sky to a close-up."

### 3. Focal Point Shift (Rack Focus)
*   **Concept:** Change what is in focus to direct attention.
*   *Frame 1:* Macro shot of a watch (in focus) with blurred background.
*   *Frame 2:* Watch blurred, nature background in focus.
*   *Prompt:* "Dramatic focus change from the watch to the background."

### 4. Relighting
*   **Concept:** Change the time of day or lighting mood.
*   *Frame 1:* Dark, moody lighting.
*   *Frame 2:* Bright focal light.
*   *Prompt:* "Lighting shift from dark and moody to bright and hopeful."

### 5. Dynamic Dolly Zoom
*   **Concept:** Combine a physical camera move (dolly) with a time-lapse.
*   *Technique:* Change the zoom level slightly between Frame 1 and Frame 2 while also changing the subject state (e.g., mushroom growing).

## Workflow
1.  **Generate Frame 1:** Use `generate_cosplay_image` (Imagen 4/Gemini 3 Image).
2.  **Generate Frame 2:** Edit Frame 1 or generate a new matching image (e.g., "same scene but winter").
3.  **Animate:** Use Veo 3.1 with `image_to_video` (if supported) or `frames_to_video` (conceptual) using the two images and a text prompt.

## Prompts for Video
*   "Cinematic aerial zoom shot"
*   "Time lapse of [subject] changing from [state A] to [state B]"
*   "Dramatic focus change"
*   "Camera orbit around [character]"
