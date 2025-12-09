# Gemini API Best Practices for Yuki Platform
> Complete integration guide incorporating all Gemini capabilities

## Table of Contents
1. [Media Resolution Optimization](#media-resolution-optimization)
2. [Token Management](#token-management)
3. [Prompt Engineering](#prompt-engineering)
4. [Image Generation (Nano Banana)](#image-generation)
5. [Video Generation (Veo 3.1)](#video-generation)
6. [Cost Optimization](#cost-optimization)

---

## Media Resolution Optimization

### Token Counts by Model

#### Gemini 3 Models
| MediaResolution | Image | Video (per frame) | PDF |
|----------------|-------|-------------------|-----|
| UNSPECIFIED (Default) | 1120 | 70 | 560 |
| LOW | 280 | 70 | 280 + Native Text |
| MEDIUM | 560 | 70 | 560 + Native Text |
| HIGH | 1120 | 280 | 1120 + Native Text |

#### Gemini 2.5 Models
| MediaResolution | Image | Video | PDF (Scanned) | PDF (Native) |
|----------------|-------|-------|---------------|--------------|
| UNSPECIFIED (Default) | 256 + Pan & Scan (~2048) | 256 | 256 + OCR | 256 + Native Text |
| LOW | 64 | 64 | 64 + OCR | 64 + Native Text |
| MEDIUM | 256 | 256 | 256 + OCR | 256 + Native Text |
| HIGH | 256 + Pan & Scan | 256 | 256 + OCR | 256 + Native Text |

### Recommended Settings for Yuki Platform

```python
# Cosplay reference images (character details are critical)
media_resolution = "MEDIA_RESOLUTION_HIGH"  # 1120 tokens
# Ensures maximum quality for facial feature extraction

# PDF costume guides
media_resolution = "MEDIA_RESOLUTION_MEDIUM"  # 560 tokens
# Optimal for document understanding

# Video tutorials (general)
media_resolution = "MEDIA_RESOLUTION_LOW"  # 70 tokens/frame
# Sufficient for action recognition

# Video with text (sewing patterns)
media_resolution = "MEDIA_RESOLUTION_HIGH"  # 280 tokens/frame
# Required for reading text details
```

### Per-Part Resolution (Gemini 3 Only)

Mix resolution levels in a single request:

```python
from google import genai
from google.genai import types

client = genai.Client(http_options={'api_version': 'v1alpha'})

# High res for character face, low res for background reference
image_part_face = types.Part.from_bytes(
    data=face_bytes,
    mime_type='image/jpeg',
    media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH  # 1120 tokens
)

image_part_bg = types.Part.from_bytes(
    data=bg_bytes,
    mime_type='image/jpeg',
    media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW  # 280 tokens
)

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=["Extract facial features from main image, use bg for context:", 
              image_part_face, image_part_bg]
)
```

---

## Token Management

### Counting Tokens

**Always count tokens before expensive operations:**

```python
# Text tokens
total_tokens = client.models.count_tokens(
    model="gemini-3-pro-preview",
    contents=prompt
)
print(f"Prompt will use {total_tokens} tokens")

# Multimodal tokens (image + text)
total_tokens = client.models.count_tokens(
    model="gemini-3-pro-preview",
    contents=[prompt, user_image, character_image]
)
# With MEDIA_RESOLUTION_HIGH: ~10 (text) + 1120 (img1) + 1120 (img2) = 2250 tokens

# Get usage from response
response = client.models.generate_content(...)
print(response.usage_metadata)
# { prompt_token_count: 2250, candidates_token_count: 150, total_token_count: 2400 }
```

### Token Budgeting for Yuki

| Operation | Token Budget | Notes |
|-----------|--------------|-------|
| Character Analysis | ~1,500 | 1 character image (HIGH) + text |
| Cosplay Preview | ~3,000 | 2 images (user + char) + prompt |
| Multi-reference Gen | ~8,000 | Up to 5 images + detailed prompt |
| Knowledge Search | ~500 | File Search queries are FREE |
| Video Analysis (10s) | ~1,800 | 70 tokens/frame × 24fps × 10s / sampling |

---

## Prompt Engineering

### Gemini 3 Pro Specific Best Practices

#### 1. Use XML Structure (Critical for Gemini 3)

```python
prompt = """
<role>
You are Yuki, an anime cosplay consultant specializing in character accuracy.
</role>

<constraints>
- Focus ONLY on visual details (hair, eyes, outfit, accessories)
- Use specific color shades (not "blue" but "sapphire blue")
- Separate canonical details from fan interpretations
</constraints>

<context>
Character: {character_name} from {anime_title}
Reference images provided: {num_images}
</context>

<task>
Extract all visual features needed for accurate cosplay recreation.
Include hair color (exact shade), eye characteristics, outfit components, 
and any signature accessories or expressions.
</task>

<output_format>
## Facial Features
- Eyes: [exact color, shape, size]
- Face: [shape, skin tone]
- Distinctive marks: [scars, beauty marks, etc.]

## Hair
- Color: [exact shade, not generic]
- Style: [complete description]
- Length: [specific]

## Default Outfit
[Head-to-toe description with materials and colors]

## Signature Elements
[Expressions, poses, color palette]
</output_format>

<final_instruction>
Be hyper-specific with colors. "Blue eyes" is not enough - specify "bright sapphire 
blue with slight gradient to lighter blue near pupils".
</final_instruction>
"""
```

#### 2. Temperature Settings

**CRITICAL FOR GEMINI 3:**
- **Default 1.0**: ALWAYS use for Gemini 3
- **Below 1.0**: Can cause looping or degraded performance
- **Never change** unless absolutely necessary

```python
# ✅ CORRECT for Gemini 3
config = types.GenerateContentConfig(
    temperature=1.0  # Default - leave as is
)

# ❌ WRONG for Gemini 3
config = types.GenerateContentConfig(
    temperature=0.7  # Can cause issues!
)
```

#### 3. Few-Shot Examples

**Always include 2-3 examples:**

```python
prompt = """
<examples>
**Example 1:**
Input: Describe the outfit of Makima from Chainsaw Man
Output:
- Top: White dress shirt, professional fit
- Tie: Black necktie, standard width
- Jacket: Dark suit jacket, tailored

**Example 2:**
Input: Describe the outfit of Nezuko from Demon Slayer
Output:
- Kimono: Pink with geometric hemp pattern
- Obi: Red-orange, traditional wrap
- Haori: None (wears bamboo muzzle instead)
</examples>

<task>
Now describe the outfit of {character_name} from {anime_title}
</task>
"""
```

#### 4. Step-by-Step for Complex Tasks

```python
prompt = """
Extract cosplay details step-by-step:

1. First, identify the character's most distinctive visual feature
2. Then, list all facial characteristics (eyes, face shape, skin)
3. Next, describe hair (color with exact shade, style, length)
4. After that, detail the default outfit from head to toe
5. Finally, note any signature accessories or props

Think through each step before providing your final answer.
"""
```

---

## Image Generation

### Nano Banana (gemini-2.5-flash-image)
**Use for**: Fast, cost-effective generation

```python
# Basic generation
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["Create a photorealistic anime cosplay photo"],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],  # Image only, no text
        image_config=types.ImageConfig(
            aspect_ratio="16:9"
        )
    )
)
```

### Nano Banana Pro (gemini-3-pro-image-preview)
**Use for**: Professional assets, 4K, Google Search grounding

```python
# 4K generation with search grounding
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Generate a cosplay preview of Makima with accurate 2023 character design",
        user_selfie
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="4K"  # 1K, 2K, or 4K
        ),
        tools=[{"google_search": {}}],  # Enable grounding
        thinking_config=types.ThinkingConfig(
            include_thoughts=True  # See reasoning process
        )
    )
)

# Check thoughts
for part in response.parts:
    if part.thought and part.text:
        print(f"Model thinking: {part.text}")
```

### Multi-Reference (Up to 14 Images with Pro)

```python
# Character consistency with multiple references
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Office group photo of these people, making funny faces",
        user_face_1,
        user_face_2,
        character_ref,
        outfit_ref,
        prop_ref
    ],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="5:4",
            image_size="2K"
        )
    )
)
```

### Chat Mode for Iterative Refinement

```python
chat = client.chats.create(model="gemini-3-pro-image-preview")

# First generation
response = chat.send_message("Create a cosplay preview")

# Iterative edits
response = chat.send_message("Make the hair color more pink")
response = chat.send_message("Add the signature red ribbon")
response = chat.send_message(
    "Change aspect ratio to 16:9",
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(aspect_ratio="16:9")
    )
)
```

---

## Video Generation

### Veo 3.1 Capabilities

```python
# Text-to-video
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="Tutorial: How to style a wig for Makima cosplay",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        resolution="1080p",  # 720p or 1080p (8s only)
        duration_seconds="8",
        person_generation="allow_all"
    )
)

# Poll for completion
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

# Download
video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("tutorial.mp4")
```

### Image-to-Video

```python
# Generate image first
image_response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="Cosplay wig on mannequin head, pink and red styling",
    config={"response_modalities": ['IMAGE']}
)

# Animate it
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="Slowly rotate the mannequin to show all angles of the wig",
    image=image_response.parts[0].as_image()
)
```

### Reference Images (Up to 3)

```python
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="Woman walks confidently in flamingo dress with heart sunglasses",
    config=types.GenerateVideosConfig(
        reference_images=[
            types.VideoGenerationReferenceImage(image=dress_img, reference_type="asset"),
            types.VideoGenerationReferenceImage(image=glasses_img, reference_type="asset"),
            types.VideoGenerationReferenceImage(image=woman_img, reference_type="asset")
        ],
        duration_seconds="8",
        resolution="720p"
    )
)
```

---

## Cost Optimization

### Priority 1: Use File Search (FREE)
```python
# File Search queries are FREE - use liberally
knowledge = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What cosplay materials work best for armor?",
    config=types.GenerateContentConfig(
        tools=[{
            "file_search": {
                "stores": [cosplay_guides_store_id]
            }
        }]
    )
)
```

### Priority 2: Batch API (50% Cheaper)
```python
# Queue bulk operations
batch_job = client.batches.create(
    model="gemini-2.5-flash",
    requests=[
        {"contents": f"Analyze character {char}"} 
        for char in character_list
    ]
)
# Process within 24 hours at 50% cost
```

### Priority 3: Model Selection
| Task | Model | Cost (per 1M tokens) |
|------|-------|---------------------|
| Character Research | gemini-2.5-flash | Input: $0.075, Output: $0.30 |
| Image Generation | gemini-2.5-flash-image | 1290 tokens/image (~$0.04/image) |
| Pro Generation (4K) | gemini-3-pro-image-preview | Higher, use strategically |
| Video Generation | veo-3.1 | Pay-as-you-go, cache frames |

### Priority 4: Media Resolution
```python
# Use per-part resolution to optimize
contents = [
    prompt,
    high_res_character_face,  # 1120 tokens - critical detail
    low_res_background,       # 280 tokens - context only
    medium_res_outfit,        # 560 tokens - moderate detail
]
# Total: ~1960 tokens vs 3360 if all HIGH
```

### Cost Calculation Example

**Scenario**: Generate cosplay preview for 100 characters

| Approach | Cost |
|----------|------|
| ❌ Bad: Pro model, HIGH res, sync | ~$150 |
| ✅ Good: Flash model, MEDIUM res, batch | ~$15 |
| 🏆 Best: Flash + File Search + caching | ~$5 |

---

## Production Checklist

### Before Launch
- [ ] Implement token counting for all operations
- [ ] Set up media resolution per use case
- [ ] Use Batch API for bulk operations
- [ ] Enable File Search for knowledge base
- [ ] Configure Google Search grounding for trending data
- [ ] Set up error handling for video generation (2-day retention)
- [ ] Implement thought signature handling for chat sessions
- [ ] Add SynthID watermark verification
- [ ] Configure rate limiting and quotas
- [ ] Set temperature=1.0 for Gemini 3 models

### Monitoring
- Track token usage per user
- Monitor media resolution effectiveness
- Measure batch completion rates
- Alert on failed video generations
- Log thought processes for debugging

---

## Quick Reference

### Model Aliases
- **Nano Banana** = `gemini-2.5-flash-image` (fast, cheap)
- **Nano Banana Pro** = `gemini-3-pro-image-preview` (advanced, 4K, thinking)
- **Veo** = `veo-3.1-generate-preview` (video generation)

### Key Limits
- **Image refs**: 3 (Flash), 14 (Pro, 6 high-fidelity)
- **Video refs**: 3 images
- **Video length**: 4s, 6s, 8s
- **Video resolution**: 720p (always), 1080p (8s only)
- **Context window**: 1M tokens (Gemini 2.5 Flash)
- **Output limit**: 8K tokens (typical)

### Cost Savers
1. **File Search** - Free queries
2. **Batch API** - 50% discount
3. **Flash model** - 15x cheaper than Pro
4. **LOW resolution** - 4x fewer tokens
5. **Caching** - Reuse expensive prompts

---

**Next Steps**: Implement these patterns in production code →
