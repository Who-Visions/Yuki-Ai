# Character Consistency Guide - Complete Knowledge Base

## 🎯 Core Principle: 100% Facial Preservation

**Critical Rule**: Keep the person exactly as shown in the reference image with 100% identical:
- Facial features
- Bone structure  
- Skin tone
- Facial expression
- Pose
- Appearance

**Technical Specs**: 1:1 aspect ratio, 4K detail

---

## 📚 Character Consistency Method - Industry Standard

### Three-Step Consistency Process (Adapted for Yuki Platform)

1. **Turn Reference into Assets (Gemini Video/Veo 2)**
2. **Build Composition from Assets**
3. **Edit and Refine Until Perfect**

---

## 🎨 Prompt #1: Dual Reference Generation

### Purpose
Create side-by-side references showing **closeup face + full body** for the same character.

### Template Structure
```
Side by side {MEDIUM_TAG} of a closeup face, and full body character design, of
{CHARACTER_DETAILS - multiple lines describing features}
{BACKGROUND_DESCRIPTION - simple plain background}
{STYLE_DESCRIPTION - consistent art style}
```

### Medium Tag Options
- `photo` - Photorealistic
- `painting` - Painted artwork
- `illustration` - Digital illustration
- `drawing` - Sketched/drawn
- `animated-render` - 3D animated
- `vector` - Vector graphics

### Left Side (Closeup Face)
**Must include**:
- Expression that shows personality
- All facial details visible
- Clear view of eyes, nose, mouth
- Hair details
- Skin tone and texture

### Right Side (Full Body)
**Must include**:
- Top of character (head/hair)
- Bottom of character (feet/shoes)
- Full anatomy visible
- Complete outfit details
- Consistent proportions

### Example Prompt
```
Side by side illustration of a closeup face, and full body character design, of 
Makima from Chainsaw Man. Left side: beautiful woman with yellow ringed eyes, 
pale skin, refined features, long light red-pink hair, mysterious calculating smile. 
Right side: tall elegant woman wearing white dress shirt with black tie, black suit 
pants, black dress shoes, multiple earrings on right ear, standing confidently, 
full body from head to toe visible. Soft gradient background. Realistic anime style, 
highly detailed, professional character design.
```

---

## 🎬 Prompt #2: Video Asset Generation

### Purpose
Convert a static reference into dynamic video footage with extractable frames for different poses using Gemini Video (Veo 2).

### Template Structure (12-15 lines for complexity)
```
Reference footage of {CHARACTER} striking several {POSES/EXPRESSIONS}.
The character starts by {STARTING_POSE}, then
moves into several {TARGET_ASSETS}, the footage freezes as if pausing at 
key moments where the {POSE} is most picturesque.

{DESCRIBE_PRIMARY_MOTION}
{DESCRIBE_SECONDARY_MOTION}
{DESCRIBE_TERTIARY_MOTIONS}
{DESCRIBE_STYLE_OF_MOTION}

FRAME EDGE CONTROL (critical for preventing cropping):
- Top: {what remains at top, e.g., "gray hat bounces slightly"}  
- Bottom: {what remains at bottom, e.g., "brown boots cast shadow"}
- Sides: {what remains on sides, e.g., "stubby fingers swing gently"}

Clean reference footage, with sharp and character-accurate motion perfect 
for pulling assets from.
```

### Motion Description Guidelines
1. **Primary Motion**: Biggest movement (arms, body rotation, etc.)
2. **Secondary Motion**: Supporting movement (shoulder lean, head tilt)
3. **Tertiary Motions**: Small details (hair sway, cloth movement)
4. **Style Description**: How motion looks (fluid, sharp, bounce, etc.)

### Frame Edge Control (CRITICAL)
Describe what stays visible at EVERY edge to prevent AI from:
- Zooming in
- Cropping parts
- Losing anatomical details

**Bad**: "Character remains visible"  
**Good**: "Character's pink hair bow bounces at top of frame as she turns"

### Example Video Prompts

**Expression Cycle:**
```
Reference footage of Nezuko striking several facial expressions. She starts by 
standing neutrally with bamboo muzzle, then moves into several emotions: 
determined gaze, soft smile, protective glare, gentle tilt. The footage freezes 
at peak expression moments. Her head rotates smoothly 15 degrees left and right. 
Her pink kimono collar shifts naturally with head movement. Her long black-to-orange 
hair sways gently in response to motion. The animation maintains perfect cel-shaded 
anime style with consistent line weight. Top frame shows her trademark pink ribbon 
staying centered. Bottom frame shows her kimono pattern remaining sharp. Left side 
shows her bamboo muzzle detail. Right side shows her hair gradient. Clean reference 
footage, with sharp and character-accurate motion perfect for pulling assets from.
```

**Action Poses:**
```
Reference footage of character executing combat stances. Starts in ready position, 
flows through attack pose, defensive crouch, victory stance, and rest position. 
Footage freezes at each peak pose. Primary motion: arms extend from guard to strike. 
Secondary motion: torso rotates to add power. Tertiary: hair whips with momentum, 
cloth ripples realistically. Motion style: sharp anime impact frames with motion blur 
trails. Top: spiky hair stays within frame boundary. Bottom: boots maintain ground 
contact with shadow. Sides: extended limbs remain fully visible. Clean reference 
footage, with sharp and character-accurate motion perfect for pulling assets from.
```

---

## ✂️ Prompt #3: Nano Banana Pro Editor Refinements

### Purpose
Make focused edits to specific parts of image while preserving the rest using Nano Banana Pro's inpainting capabilities.

### Template Structure
```
A(n) {MEDIUM_TAG} of {PRIMARY_EDIT_DESCRIPTION}.
With {DETAILED_EDIT_SPECS}.
{EDIT_IN_CONTEXT_OF_SURROUNDINGS}.
All while {SIMPLE_PASSIVE_DESCRIPTION_OF_FULL_IMAGE}.
```

### Key Principle
**The edit is the STAR** - spend most tokens describing the change, not the whole image.

### Example Edit Prompts

**Adding costume detail:**
```
An illustration of an ornate silver hair pin adorned with sakura blossoms. 
With delicate petals in pink gradient, silver chain dangles with small bells. 
The pin is secured in the character's updo hairstyle, casting subtle shadow 
on dark hair behind left ear. All while the character stands in traditional 
kimono in a cherry blossom garden.
```

**Changing background:**
```
A photo of a neon-lit cyberpunk city street at night. With holographic billboards, 
wet pavement reflecting pink and blue lights, volumetric fog. The street extends 
behind the character as distant cityscape. All while a cosplayer poses confidently 
in futuristic outfit.
```

---

## 🎞️ Prompt #4: Grid Editing for Consistency

### Purpose
Edit multiple variations simultaneously while maintaining consistency.

### General Refinement Template
```
A side-by-side {MEDIUM_TAG} collection of {SHARED_ELEMENTS}.
{DESCRIBE_ELEMENTS_IN_DETAIL - as if single image}.
Each {SUBJECT} is duplicated exactly with different {VARIATION_TYPE}.
```

### Edit Template
```
A side-by-side {MEDIUM_TAG} grid of {EDIT_DESCRIPTION}.
With {EDIT_DETAILS}.
{EDIT_IN_CONTEXT}.
All while {SIMPLE_IMAGE_DESCRIPTION}.
Each {EDIT} is duplicated exactly with different {VARIATION_TYPE}.
```

### Variation Types
- `lighting` - Different light angles/colors
- `angle` - Different camera angles
- `scale` - Different zoom levels  
- `expression` - Different facial expressions
- `pose` - Different body poses

### Example Grid Prompt
```
A side-by-side illustration collection of Luffy from One Piece in straw hat and 
red vest. Each shows determined expression with clenched fist. Background is 
simple blue gradient ocean. Character maintains exact proportions and features. 
Each Luffy is duplicated exactly with different lighting: golden hour, midday sun, 
moonlight, studio lighting.
```

---

## 🔧 Nano Banana Pro Best Practices

### Basic Components (6 Required)
1. **Subject**: Who/what (e.g., "bartender", "magical girl")
2. **Composition**: Camera angles (low angle, close-up, wide shot)
3. **Action**: What's happening (working out, casting spell, etc.)
4. **Setting/Location**: Where (roadside gym, fantasy castle)
5. **Style**: Art type (realistic, oil painting, anime, product shoot)
6. **Editing Instructions**: Direct commands (replace background, change decor)

### Advanced Components (Enhanced Quality)
7. **Aspect Ratio**: Canvas size (3:4 vertical, 1:1 square, 16:9 wide)
8. **Camera/Lighting**: Technical specs (f/1.8, long shadows, natural daylight)
9. **Text Rendering**: Actual text in quotes + placement + typography
10. **Factual Details**: Scientific/recipe/technical accuracy
11. **Reference Inputs**: Role of each input (character ref, style ref, background)

### Manga/Anime Specific
```
Create a manga of {CHARACTERS} and show {ACTION/SCENE}.
High-impact, comic-style {DESCRIPTION}.
Dynamic close-up portrait in graphic novel style.
Bold black ink lines, high contrast, gritty textured quality.
Stark color palette: black, white, {ACCENT_COLORS}.
```

### Product Photography (for Merchandise)
```
Show this {PRODUCT} {SETTING_DESCRIPTION}.
Add {BACKGROUND_STYLE} behind this {PRODUCT}.
Place this {PRODUCT} on {SURFACE} with {LIGHTING}.
Transform this {PRODUCT} into {AD_STYLE} with {EFFECTS}.
```

---

## 💯 100% Facial Preservation Techniques

### Critical Prompt Addition
```
Keep the person exactly as shown in the reference image with 100% identical 
facial features, bone structure, skin tone, facial expression, pose, and appearance.
```

### Reference Image Instructions
When using face reference:
```
Use reference image for:
- Exact facial geometry and proportions
- Precise skin tone and texture
- Bone structure (cheekbones, jaw, brow)
- Eye shape, color, and spacing
- Nose shape and size
- Mouth shape and lip thickness
- Facial expression maintained
- 1:1 aspect ratio, 4K detail
```

### Multi-Reference Strategy
```
Character reference: {character_image} for outfit and style
Face reference: {user_selfie} for 100% identical facial features
Style reference: {style_image} for art style and rendering
Maintain facial geometry exactly as face reference with zero deviation
```

---

## 🎭 Complete Cosplay Workflow

### Step 1: Generate Character References
**Tool**: Nano Banana Pro (Gemini Imagen 3)  
**Prompt**: Dual reference (face + body) using character consistency template  
**Output**: Side-by-side reference sheet

### Step 2: Create Asset Library
**Tool**: Gemini Video (Veo 2)  
**Prompts**: 
- Expression cycle video
- Action poses video  
- Camera turnaround video
**Output**: Extract key frames for asset library

### Step 3: User Face Integration
**Tool**: Nano Banana Pro with Multi-Reference  
**Inputs**:
- Character reference
- User selfie (face preservation)
- Style reference
**Prompt**:
```
Full body photo of person cosplaying as {CHARACTER} from {ANIME}, 
wearing {OUTFIT_DETAILS}, {SETTING}, professional cosplay photography, 
studio lighting, keep the person exactly as shown in the reference image 
with 100% identical facial features, bone structure, skin tone, 1:1 aspect 
ratio, 4K detail
```

### Step 4: Refine with Editor
**Tool**: Yuki Editor (Nano Banana Pro Inpainting)  
**Actions**:
- Adjust costume accuracy
- Perfect lighting/shadows
- Enhance background
- Fix any proportion issues

### Step 5: Final Polish
**Tool**: Adobe Remove Background (optional)  
**Use**: Extract character as asset for compositing

---

## 🛠️ Essential Tools (Yuki Platform Stack)

### 1. Nano Banana Pro - Google Gemini
**Purpose**: High-quality image generation with multi-reference support  
**Model**: Imagen 3.0 (via Google AI Studio)  
**Features**:
- Multi-reference inputs (character, face, style)
- Advanced prompt understanding
- 4K resolution output
- Inpainting capabilities
- 100% facial preservation support

### 2. Gemini Video (Veo 2)
**Purpose**: Video generation for asset extraction  
**Features**:
- Character-consistent video generation
- Frame-by-frame control
- Natural motion synthesis
- Asset-ready output

### 3. Yuki Prompt Engineering System
**Purpose**: Intelligent prompt optimization  
**Features**:
- Template library with 5+ professional prompts
- Quality scoring (0-1 scale)
- Automatic optimization
- Character consistency integration
- Export/import capabilities

### 4. Adobe Remove Background - FREE (Optional)
**Purpose**: Extract characters as clean assets  
**Link**: https://www.adobe.com/express/feature/image/remove-background  
**Use Cases**:
- Single image extraction
- Asset library preparation
- Background replacement

---

## 📊 Quality Scoring Checklist

### Prompt Quality Factors
- [ ] Subject clearly defined (20%)
- [ ] Setting/location specified (15%)  
- [ ] Art style described (15%)
- [ ] Composition details (15%)
- [ ] Lighting information (10%)
- [ ] Quality enhancers present (25%)

### Character Consistency Factors
- [ ] Dual reference generated
- [ ] Asset library created via video
- [ ] Face preservation instructions included
- [ ] Frame edge controls specified
- [ ] Style maintained across variations

### Technical Specs Checklist
- [ ] Aspect ratio specified
- [ ] Resolution target (4K)
- [ ] Medium tag appropriate
- [ ] Reference roles defined
- [ ] Motion described (if video)

---

## 🎯 Common Mistakes to Avoid

### ❌ Don't Do This
- Vague subject descriptions
- Missing frame edge controls in video
- Insufficient motion detail
- Generic "high quality" without specifics
- Forgetting facial preservation clause
- Cropped anatomy in references

### ✅ Do This Instead
- Precise subject with multiple descriptors
- Describe what's at ALL frame edges
- 12-15 lines of motion detail
- Specific quality terms (4K, ultra detailed, sharp focus)
- Always include 100% facial preservation
- Ensure full anatomy visible (head to toe)

---

## 🚀 Quick Reference Templates

### Cosplay Generation (User Face + Character)
```
Full body {medium} of person cosplaying as {character} from {anime}, 
{facial_details}, {outfit_top}, {outfit_bottom}, {footwear}, {accessories}, 
{pose}, {expression}, {setting}, {lighting}, {art_style}, 
keep the person exactly as shown in the reference image with 100% identical 
facial features, bone structure, skin tone, facial expression, pose, and appearance, 
use reference image for facial geometry and proportions, 1:1 aspect ratio, 4K detail, 
professional cosplay photography
```

### Character Reference Sheet
```
Side by side {medium} of a closeup face, and full body character design, of 
{character} from {anime}. Left: {face_description}, {expression_showing_personality}. 
Right: {body_type}, wearing {outfit_complete_description}, from head to toe fully 
visible, {footwear_visible}. {background}. {art_style}, highly detailed, 
professional character design
```

### Video Asset Extraction
```
Reference footage of {character} striking several {poses}. Starts by {initial_pose}, 
then moves into {target_poses}, footage freezes at peak moments. {primary_motion}. 
{secondary_motion}. {style_of_motion}. Top frame: {top_element}. Bottom frame: 
{bottom_element}. Left side: {left_element}. Right side: {right_element}. 
Clean reference footage, with sharp and character-accurate motion perfect for 
pulling assets from.
```

---

## 📖 Further Resources

- **Nano Banana Pro Guide**: 75 prompts + advanced use cases (Imagine.art)
- **Google AI Studio**: Gemini API documentation and examples
- **PromptBase**: 2,400+ free AI prompts for reference
- **Yuki Platform Docs**: Complete architecture and API reference
- **Gemini Multimodal Guide**: Advanced vision and video capabilities

---

**Last Updated**: 2025-12-02  
**Version**: 1.0 - Complete Integration  
**Status**: Production Ready 🦊
