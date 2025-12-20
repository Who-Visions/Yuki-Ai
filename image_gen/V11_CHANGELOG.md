# V11 Pipeline Changelog

## 2025-12-18 05:59 - Initial V11 Development

### Features Added

- **Cloud Vision Caching** - Failsafe cache-first system for Cloud Vision API
  - Cache stored in `c:/Yuki_Local/cache/cloud_vision/`
  - Uses MD5 file hash as cache key
  - Always checks cache before API call
  - Saves ~$0.0015 per cached hit

- **Subject Prep Utility** (`image_gen/subject_prep.py`)
  - HEIC → JPG conversion with EXIF preservation
  - Full EXIF metadata extraction (camera, time, GPS, settings)
  - Subject manifest generation with summary

- **68-Point + Neck/Jawline Expansion**
  - Expands Cloud Vision 34 landmarks to 68-point schema
  - Adds 5 neck nodes (points 68-72)
  - Includes detailed jawline/face geometry analysis

### Models Used

| Stage | Model | Purpose |
|---|---|---|
| 1 | Cloud Vision API | 34 facial landmarks |
| 2 | gemini-3-flash-preview | 68-point expansion |
| 3 | gemini-3-pro-preview | Deep analysis |
| 4 | gemini-3-pro-image-preview | Image generation |

### Subjects Processed

- **Keyosha Pullman** (2025-12-18)
  - 10 HEIC converted to JPG
  - 4 photos analyzed with Cloud Vision
  - 68-point + neck expansion complete
  - Camera: iPhone 17
  - Locations: Virginia, Pennsylvania

### Files Created

- `image_gen/v11_pipeline.py` - Main V11 pipeline
- `image_gen/subject_prep.py` - Subject preparation utility
- `run_cv_keyosha.py` - Cloud Vision runner
- `run_expand_keyosha.py` - 68-point expansion runner

### Security

- ⚠️ API keys scrubbed from all v10 files
- All scripts now use `os.environ.get("GEMINI_API_KEY")`

---

## 2025-12-18 06:14 - Stage 4 Batch Generation

### Keyosha Pullman - 12 Cosplay Renders

- **Model:** gemini-3-pro-image-preview
- **Method:** Vertex AI Project Quota (NO API KEYS)
- **Rate Limit:** 2.5 min between renders (12 in 30 min)
- **Output:** `C:/Yuki_Local/Cosplay_Lab/Subjects/Keyosha Pullman/Renders/`

**Characters (10 with 2 variants each = 20, running 12):**

1. Storm - Classic Black Suit ✅
2. Storm - Mohawk Punk Era
3. Michonne - Survivor Default
4. Michonne - Alexandria Constable
5. Shuri - Lab Tech Princess
6. Shuri - Black Panther Suit
7. Niobe - Matrix Operator
8. Niobe - Zion Casual
9. Rue - Arena Tribute
10. Rue - Reaping Day
11. Yoruichi - Stealth Force Commander
12. Yoruichi - Shunko Form

### Files Created

- `run_stage4_keyosha.py` - Main generation script
- `run_keyosha_batch.bat` - Failsafe runner with venv, dependency checks
- `face_swap_keyosha.py` - InsightFace post-processor for identity preservation
- `run_face_swap.bat` - Runner for face swap

### Identity Preservation Issue

Gemini 3 Pro Image cannot preserve exact facial identity from text prompts alone.
**Solution:** Use InsightFace face swap as post-processing:

1. Generate cosplay images (wrong face, right costume)
2. Run face_swap_keyosha.py to swap Keyosha's actual face onto images
3. Result: Keyosha's face + character costume

**Requires:** `pip install insightface onnxruntime-gpu opencv-python`
**Model:** Download `inswapper_128.onnx` from HuggingFace

---

## 2025-12-18 20:30 - Cloud Vision Face Identity Caching

### The Problem Solved

- Per-run photo analysis hitting **429 RESOURCE_EXHAUSTED** errors
- Multi-image prompts causing **face drift** (model blending/hallucinating faces)
- Deleting test outputs to re-run (losing comparison data)

### Solution: One-Time Extraction + Cache

**Architecture:**

```
[Subject Photos] → Cloud Vision API (once) → face_identity.json
                                                    ↓
                              [Generation] ← Uses cached data + single best photo
```

### New Scripts

| Script | Purpose |
|--------|---------|
| `extract_face_identity.py` | One-time Cloud Vision face extraction with 1s rate limiting |
| `run_stage4_v2.py` | Generation using cached identity + random character selection |

### Key Features

- **Cloud Vision API** extracts face landmarks, bounding boxes, attributes
- **1-second rate limiting** prevents 429 errors during extraction
- **face_identity.json** caches results in subject folder
- **Quality scoring** (0-50) based on detection confidence + attributes
- **Random character selection** ensures no overlap between test runs
- **Single best photo** at 1536px (not multiple low-res)
- **Face landmarks in prompt** for better identity preservation

### Test Results: Maurice

**Extraction:**

- 28 photos analyzed
- Best: `004E9A40-ADBA-4BD7-BAFD-F6962CBF6900.JPG` (44/50, 99% confidence)
- Zero 429 errors

**Generation (10 random characters):**

- Killer Bee, Lucio, Afro Samurai, Venom, Batwing, Miles Morales, Falcon, Green Lantern, Black Manta, Mace Windu
- All previous test renders preserved (16 total in folder)

### Dependencies

```bash
pip install google-cloud-vision
```

### Usage

```bash
# Step 1: Extract face identity (one-time per subject)
python extract_face_identity.py "C:/Yuki_Local/Cosplay_Lab/Subjects/maurice"

# Step 2: Generate (uses cached identity, random characters)
python run_stage4_v2.py
```
