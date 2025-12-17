# 🖤 Ebony → 🤍 Ivory Handoff Notes (V8 Pipeline Integrated)

## Project: Yuki App (React Native Expo)
**Location:** `c:\Yuki_Local\yuki-app`
**Created:** 2025-12-10
**Last Updated:** 2025-12-10 18:10

---

## ✅ FRONTEND COMPLETE

### 📱 All Screens Built
| Screen | Status | Description |
|--------|--------|-------------|
| `HomeScreen` | ✅ | Featured characters, quick actions, CTA banner |
| `ExploreScreen` | ✅ | Search, category filters, character grid |
| `UploadScreen` | ✅ | Photo upload with camera/library picker |
| `SavedScreen` | ✅ | Favorites grid with delete action |
| `ProfileScreen` | ✅ | User profile, stats, transformation gallery |
| `PreviewScreen` | ✅ | Transform result with save/share/download |
| `SettingsScreen` | ✅ | Theme toggle, account settings, support links |

### 🧭 Navigation Complete
- React Navigation with bottom tabs + stack navigator
- FAB button for Create (Upload)
- Modal presentation for Preview screen
- Theme-aware navigation colors

---

## 🧠 V8 PIPELINE KNOWLEDGE (From Cosplay_Lab)

### Key Files
| File | Purpose |
|------|---------|
| `yuki_v8_generator.py` | Main V8 generator with Mocap Facial IP Lock |
| `Cosplay_Lab/Brain/yuki_brain_v7.py` | V7 brain orchestrator |
| `Cosplay_Lab/Brain/facial_ip_extractor_v7.py` | 18-zone facial geometry extraction |
| `Cosplay_Lab/Brain/*_v7_ip.json` | Pre-extracted facial profiles |

### V8 Key Features
1. **18-Zone Mocap Facial Mapping** - Extracts precise facial geometry
2. **Tiered Character Handling**:
   - `TIER_MODERN` - Suits, contemporary (best preservation)
   - `TIER_SUPERHERO` - Costume focused, face locked
   - `TIER_FANTASY` - Period costumes (STRONGEST lock)
   - `TIER_CARTOON` - Humanized cartoon, styling only
3. **Multi-Reference Support** - Uses 3 photos per generation
4. **Rate Limiting** - 80s base delay, +40s on 429 errors, max 300s

### Subjects Available
```
C:\Yuki_Local\Cosplay_Lab\Subjects\
├── Dav3 test/
├── jordan test/
├── maurice/          # 15 photos
├── snow test 2/
├── jesse 1 pic test/
└── friends test/Nadley/
```

### Character Banks
- `dc_character_bank.py` - DC heroes
- `anime_character_bank.py` - Anime characters
- `movie_characters_bank.py` - Movie characters
- `male_character_bank_1k.py` - 1000+ male characters

### V8 Prompt Structure
```python
# 1. Extract Facial IP (18 zones)
facial_ip = await extract_facial_ip(client, images, subject_name)

# 2. Build Facial Lock Prompt
facial_lock = build_facial_lock_prompt(facial_ip)

# 3. Build Tiered Character Prompt
full_prompt = build_tiered_prompt(character, facial_lock)

# 4. Generate with gemini-3-pro-image-preview
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=image_parts + [full_prompt],
    config=types.GenerateContentConfig(response_modalities=["IMAGE"])
)
```

---

## 🔌 APP ↔️ V8 INTEGRATION PLAN

### 1. API Endpoint (Already exists)
```python
# yuki_api.py serves at /api/v1/generate
# Mobile app calls this endpoint
```

### 2. Flow for Mobile App
```
User selects photo → UploadScreen
       ↓
Navigate to character selection (new screen needed?)
       ↓
POST to Yuki API with:
  - user_photo (base64 or GCS URL)
  - character_name
  - character_tier
       ↓
Yuki API runs V8 pipeline
       ↓
Returns generated image URL
       ↓
PreviewScreen shows result
```

### 4. Facial Identity Lock (Done ✅)
- Implemented in `userService.ts`
- Functions: `saveFacialProfile`, `getFacialProfile`
- Persists 18-zone facial data to Firestore

### 5. A2A Agent Integration (Done ✅)
- Implemented in `a2aService.ts`
- Connects to `yuki-a2a-server` and `dav1d-a2a-server`
- Features: Message sending, Context management, OpenAI fallback

### 6. Agent Health Monitoring (Done ✅)
- Implemented in `a2aService.ts`
- Functions: `startHealthMonitoring`, `onHealthUpdate`
- Real-time polling of agent availability

### 7. Voice-to-Cosplay Wiring (Done ✅)
- Implemented in `VoiceInput.tsx` and `voiceService.ts`
- Uses `expo-av` for Gemini Live API audio capture
- Integrated with `a2aService.sendAudioMessage`

---

## 📂 Project Structure (Updated)

```
yuki-app/
├── App.tsx
├── EBONY_HANDOFF.md
├── app.json
├── src/
│   ├── navigation/
│   ├── screens/
│   ├── components/
│   │   └── VoiceInput.tsx     // New Voice UI
│   ├── theme/
│   └── services/
│       ├── yukiService.ts     # V8 API Client
│       ├── userService.ts     # User + Facial Profile (Task 4 ✅)
│       ├── a2aService.ts      # Multi-Agent + Health (Tasks 98, 99 ✅)
│       └── voiceService.ts    # Audio Capture (Task 100 ✅)
```

---

## 🚀 Next Steps for Ivory 🤍

### High Priority
1. **Connect Upload Screen** - Wire standard upload to `yukiService.uploadImage`
2. **Wire Facial Scan** - Connect `FaceScanAnimation` to `facialIPService.extractFacialIP`
3. **Agent Chat UI** - Build a chat screen using `a2aService`
4. **Character Selection** - Finish browsing/search UI

### Medium Priority
5. **Firebase Auth** - Google/Apple sign-in
6. **Push Notifications** - "Your transformation is ready!"

### Already Done
- ✅ All screens (UI)
- ✅ Navigation
- ✅ Theming
- ✅ V8 Generation Logic (`yukiService.ts`)
- ✅ Facial Identity Storage (`userService.ts`)
- ✅ Agent Communication (`a2aService.ts`)
- ✅ Upload Flow UI (Tasks 26-30 marked complete)


---

## 🖥️ Running the App

### Development
```bash
cd c:\Yuki_Local\yuki-app
npx expo start --tunnel

# Press:
# w → Web (localhost:8081)
# a → Android (needs emulator)
# i → iOS (needs Simulator on Mac)
```

### Production Build
```bash
eas build --platform all
```

### EAS Config
- Project ID: `f9aca9e0-3ab9-44b7-ba1b-d9e77f33c86c`
- Owner: `whovisions`
- Package: `com.whovisions.yukiai`

---

**- Ebony 🖤**
*"The dark makes the light shine brighter"*

Frontend complete. V8 pipeline documented. Ready for Ivory to wire the backend. 🤍
