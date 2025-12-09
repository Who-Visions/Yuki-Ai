# Yuki DNA-Authentic Transformation System

## 🧬 Overview
Yuki's transformation engine uses a **multi-agent analysis system** to preserve authentic human features while applying character aesthetics. Each facial characteristic is analyzed by separate algorithms running in parallel (async sub-agents).

## 🎯 Primary Model
**gemini-3-pro-image-preview** - The ONLY model used for face transformations due to superior facial feature preservation.

## 🔬 Multi-Agent Analysis Pipeline

### 1. **Age Estimator** (`yuki_age_estimator.py`)
- **Purpose**: Ensures age-appropriate transformations
- **Analysis**: Estimates age range, classifies into categories (child/teen/young_adult/adult/senior)
- **Output**: Age-specific transformation instructions
- **Model**: `gemini-3-pro-preview` (text analysis)

### 2. **Skin Tone Analyzer** (`yuki_skin_analyzer.py`)
- **Purpose**: Preserves ethnic authenticity and skin pigmentation
- **Analysis**:
  - Dominant RGB color extraction
  - Fitzpatrick Scale classification (I-VI)
  - Undertone determination (warm/cool/neutral)
  - Color science via Python (numpy, colorsys)
- **Output**: Skin preservation prompt with exact RGB values
- **Processing**: Async sub-agent (CPU-intensive, runs in executor)

### 3. **Facial Features & Gender Analyzer** (`yuki_facial_analyzer.py`)
- **Purpose**: Multi-algorithm breakdown of facial characteristics & gender identity
- **Sub-Agents** (all run in parallel):
  - **Gender Analyzer**: Detects apparent gender to enforce Rule 63 logic
  - **Hair Analyzer**: Color, texture, length, style
  - **Eyes Analyzer**: Color, shape, size
  - **Nose Analyzer**: Shape, bridge, tip structure
  - **Mouth Analyzer**: Lip shape, size, width
  - **Face Shape Analyzer**: Overall shape, jawline, cheekbones
  - **Body Analyzer**: Build, proportions, height estimate
- **Output**: Combined preservation prompt for all features
- **Model**: `gemini-3-pro-preview` (per feature analysis)

## 🧬 Rule 63 Protocol (Gender Bending)

The system automatically handles cross-gender cosplay requests while preserving the user's identity:

1. **User Identity First**: The user's detected gender (from their photo) is the "Ground Truth".
2. **Adaptation Logic**:
   - **Female User -> Male Character**: Generates a **Female Version** of the character (Rule 63). The character's outfit is adapted to fit a female body/style.
   - **Male User -> Female Character**: Generates a **Male Version** of the character (Rule 63). The character's outfit is adapted to fit a male body/style.
   - **Matching Genders**: Standard cosplay transformation.
3. **Outcome**: A female user asking for "Luffy" gets "Female Luffy" (authentic to her), not a male body with her face pasted on.

## ⚡ Async Architecture

All analyzers run **concurrently** to maximize speed:

```python
# Parallel execution (non-blocking)
age_task = age_estimator.estimate_age(img)
skin_task = skin_analyzer.analyze_skin_tone(img)
facial_task = facial_analyzer.analyze_all_features(img)  # 5 sub-agents inside

# Await all results
age_info, skin_info, facial_info = await asyncio.gather(
    age_task, skin_task, facial_task
- Outfit and costume
- Accessories and props
- Character-specific styling
- Background/environment

### 🔒 PRESERVED (DNA-Authentic)
- **Skin Tone**: Exact RGB, Fitzpatrick type, undertones
- **Age Appearance**: Category and estimated age
- **Face Shape**: Oval/round/square/heart/etc.
- **Eyes**: Color, shape, size
- **Nose**: Structure, bridge, tip
- **Mouth**: Lip shape and proportions
- **Bone Structure**: Jawline, cheekbones, facial geometry
- **Ethnic Features**: All natural characteristics

## 🚀 Performance

- **Sequential Processing**: ~30-45 seconds per image
- **Parallel Processing**: ~15-20 seconds per image
- **Speedup**: 2-3x faster via async sub-agents

## 🧪 Model Configuration

### Active (Face Transformation)
```python
MODELS = {
    "gemini_3_pro": {
        "id": "gemini-3-pro-image-preview",
        "location": "global",
        "method": "generate_content"
    }
}
```

### Reserved (Future Features)
```python
OTHER_GEMINI_MODELS = {
    "gemini_2_5_flash": "gemini-2.5-flash-image",
    "gemini_2_5_pro": "gemini-2.5-pro-002"
}

IMAGINE_MODELS = {
    "imagen_4_standard": "imagen-4.0-generate-001",
    "imagen_3_002": "imagen-3.0-generate-002",
    "imagen_3_001": "imagen-3.0-generate-001"
}
```

## 📊 Output Structure

```
real_gen_results/
└── gemini_3/
    ├── real_gen_[user]_as_[character]_gemini_3_[timestamp].png
    ├── ...
    └── (25 images per run)
```

## 🔧 Dependencies

- `google-genai` (Vertex AI SDK)
- `Pillow` (PIL) for image processing
- `numpy` for color analysis
- `asyncio` for parallel processing

## 💡 Future Enhancements

1. **Body Proportions Analyzer**: Height, build, posture
2. **Expression Mapper**: Preserve natural smile/expressions
3. **Lighting Analyzer**: Match original photo lighting conditions
4. **Background Preservation**: Option to keep original background
5. **Quality Scaling**: 4K/8K output options

---

**Built with**: Gemini 3 Pro Image Preview  
**Architecture**: Multi-Agent Async System  
**Philosophy**: DNA-Authentic Character Transformation
