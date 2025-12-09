# V5-Lite Cosplay Generation Workflow

> **The Prime Method for DNA-Authentic Cosplay Generation**  
> Established: December 8, 2025

---

## Overview

V5-Lite is the optimized facial preservation + cosplay generation pipeline that produces **real photography quality** results with **fast generation times** (~20-40 seconds per image).

### Key Principles

1. **Face = Locked Identity** - The reference person must be INSTANTLY recognizable
2. **Costume = Character Styling** - Only apply costume, hair color, and scene changes
3. **Photography = Real** - Output must look like actual Canon R6 Mark II photos, NOT anime/illustration

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  1. FACIAL IP EXTRACTION (One-time per subject)                 │
│     - Model: gemini-3-pro-preview                               │
│     - Input: 10-14 reference photos from multiple angles        │
│     - Output: V5 Deep Node JSON (~7-8k chars full)              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. V5-LITE CONDENSATION                                        │
│     - Extract ESSENTIAL nodes only (~1.5-2k chars)              │
│     - Key fields: face_calibration, eye_nodes, nose_nodes,      │
│       lip_nodes, jaw_chin, skin, critical_identity_lock         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. IMAGE GENERATION                                            │
│     - Model: gemini-3-pro-image-preview                         │
│     - Endpoint: global                                          │
│     - Include: V5-Lite map + character desc + ANTI-ANIME rules  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Prompt Template

```
📷 REAL PHOTOGRAPH - Canon EOS R6 Mark II, RF 85mm f/1.2L @ f/2.0, 4K 9:16

⚠️ OUTPUT: REAL COSPLAY PHOTO with natural skin texture, real fabric, real hair
⚠️ NOT: anime, illustration, CGI, cartoon, digital art, cell shading

🔒 FACIAL IDENTITY (V5-LITE):
{v5_lite_json}

PRESERVE: Face shape, nose, eyes, lips, skin tone EXACTLY. 
This person must be INSTANTLY recognizable.

📷 COSPLAY: {character_name} from {show}
{character_description}
SCENE: {scene_description}

Generate ONE REAL cosplay photograph. NOT anime. Real person in costume.
```

---

## Rate Limiting Strategy

| Setting | Value |
|---------|-------|
| **Batch Size** | 4 generations max |
| **Buffer Between Gens** | 90 seconds |
| **Mega-Buffer After 4** | 240 seconds (4 min) |
| **Total for 12 chars** | ~30 minutes |

---

## V5-Lite JSON Structure

```python
def get_lite_map(full_map: dict) -> str:
    lite = {
        "face_calibration": full_map.get("face_calibration", {}),
        "eye_nodes": {
            "shape": full_map.get("eye_nodes", {}).get("eye_shape", ""),
            "size": full_map.get("eye_nodes", {}).get("eye_size", ""),
            "color": full_map.get("eye_nodes", {}).get("eye_color", ""),
            "spacing": full_map.get("eye_nodes", {}).get("eye_spacing", ""),
        },
        "nose_nodes": {
            "bridge": full_map.get("nose_nodes", {}).get("bridge_shape", ""),
            "tip": full_map.get("nose_nodes", {}).get("tip_shape", ""),
            "width": full_map.get("nose_nodes", {}).get("nose_width_ratio", ""),
            "piercings": full_map.get("nose_nodes", {}).get("piercings", "")
        },
        "lip_nodes": {
            "fullness": full_map.get("lip_nodes", {}).get("upper_lip_fullness", "") + 
                        "/" + full_map.get("lip_nodes", {}).get("lower_lip_fullness", ""),
            "cupids_bow": full_map.get("lip_nodes", {}).get("cupids_bow_definition", ""),
            "width": full_map.get("lip_nodes", {}).get("lip_width", "")
        },
        "jaw_chin": {
            "jaw_shape": full_map.get("jaw_chin_nodes", {}).get("jaw_shape", ""),
            "chin_shape": full_map.get("jaw_chin_nodes", {}).get("chin_shape", "")
        },
        "skin": {
            "fitzpatrick": full_map.get("skin_surface", {}).get("fitzpatrick", ""),
            "tone": full_map.get("skin_surface", {}).get("tone_description", ""),
            "undertone": full_map.get("skin_surface", {}).get("undertone", "")
        },
        "critical_identity_lock": full_map.get("critical_identity_lock", {})
    }
    return json.dumps(lite, indent=2)
```

---

## Extraction Models

| Purpose | Model | Notes |
|---------|-------|-------|
| **Facial Analysis** | `gemini-3-pro-preview` | Better vision accuracy, no hallucinations |
| **Image Generation** | `gemini-3-pro-image-preview` | Best quality, use `global` endpoint |
| **DO NOT USE** | `gemini-2.5-flash` for extraction | Hallucination risk (e.g., adding braces) |

---

## Character Description Best Practices

1. **Be Specific About Colors**
   - ✅ "Long ORANGE hair" 
   - ❌ "Colorful hair"

2. **Include Signature Features**
   - ✅ "DIAMOND MARK on forehead" (Tsunade)
   - ✅ "Pinwheel tattoo on left shoulder" (Nami)

3. **Specify Skin Tone When Character Has It**
   - ✅ "BROWN SKIN" (Mirko, Yoruichi)
   - This helps avoid whitewashing

4. **Describe Costume Concisely**
   - Keep to 2-3 lines max
   - Focus on iconic elements

---

## Files Created Per Subject

| File | Purpose |
|------|---------|
| `{name}_v5_deep_nodes.json` | Full facial topology (backup) |
| Generated images | `V5L_{character}_{timestamp}.png` |

---

## Quality Checklist

Before delivery, verify:

- [ ] Face is INSTANTLY recognizable as reference person
- [ ] Image is photorealistic (not anime/cartoon)
- [ ] Skin tone preserved accurately
- [ ] Character costume is correct
- [ ] No hallucinated features (braces, tattoos, etc.)

---

## Evolution History

| Version | Changes |
|---------|---------|
| V1-V3 | Basic facial IP extraction |
| V4 | VFX-inspired deep topology mapping |
| **V5** | 100+ anchor points, deep nodes |
| **V5-Lite** | Condensed essential nodes (1.5-2k chars), faster generation |

---

## Sample Test Results (December 8, 2025)

### Snow Test - 12 Characters
- **Success Rate:** 11/12 (92%)
- **Average Gen Time:** ~25 seconds per image
- **Total Runtime:** 30 minutes
- **Output Quality:** HIGH (real photography, not anime)

### Best Performers:
- Uraraka Ochaco
- Nana Shimura
- Yoruichi (various versions)
- OC Black Sorceress

---

## Usage

```bash
# 1. Extract V5 facial map (one-time)
python facial_ip_extractor_v5.py

# 2. Run V5-Lite generation
python snow_v5lite_test.py
```

---

*This workflow is maintained as the primary cosplay generation method for the Yuki platform.*
