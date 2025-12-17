# 🤍 IVORY HANDOFF - Phase 2: UI/UX Enhancement

**From**: Ebony 🖤  
**To**: Ivory 🤍  
**Date**: December 10, 2025  
**Project**: Yuki Mobile App (`c:\Yuki_Local\yuki-app`)

---

## 📋 Your Assignment: Phase 2 (Tasks 21-40)

Ebony is handling **Phase 1** (V8 Pipeline) and **Phase 7** (Agent Integration).  
You own **Phase 2**: UI/UX Enhancement.

---

## 🎯 Your Tasks (20 Total)

### Home Screen Upgrades (21-25)
- [ ] **21.** Add trending characters carousel from `jikan_client.py` seasonal data
- [ ] **22.** Show "Your Transformations" section with generation history
- [ ] **23.** Display credits balance and usage meter
- [ ] **24.** Add seasonal/holiday character collection banners
- [ ] **25.** Implement pull-to-refresh for real-time character updates

### Upload Flow Enhancement (26-30)
- [ ] **26.** Add multi-photo selection for stronger facial lock (3 photos)
- [ ] **27.** Create face detection validation before upload
- [ ] **28.** Show facial quality score (lighting, clarity, angle)
- [ ] **29.** Add photo cropping with face-centered auto-crop
- [ ] **30.** Implement background removal option (Adobe API integration)

### Character Selection Improvements (31-35)
- [ ] **31.** Add character difficulty rating (tier badge) in cards
- [ ] **32.** Show "Popular This Week" section from analytics
- [ ] **33.** Add character franchise/universe filtering
- [ ] **34.** Implement recent characters history
- [ ] **35.** Create "Favorites" save functionality

### Generation Screen (36-40)
- [ ] **36.** Add real face scan animation with 18-zone visualization
- [ ] **37.** Show "DNA Lock" confirmation when facial IP extracted
- [ ] **38.** Display estimated generation time based on tier
- [ ] **39.** Add generation queue position indicator
- [ ] **40.** Implement generation cancellation with credit refund

---

## 📁 Key Files You'll Work With

### Screens to Modify
```
src/screens/HomeScreen.tsx       - Tasks 21-25
src/screens/UploadScreen.tsx     - Tasks 26-30
src/screens/CharacterSelectScreen.tsx - Tasks 31-35
src/screens/GenerateScreen.tsx   - Tasks 36-40
```

### Services to Use
```
src/services/yukiService.ts      - API calls
src/services/facialIPService.ts  - Facial zones (I created this)
src/services/userService.ts      - User data
```

### Theme System
```
src/theme/colors.ts     - Light/dark colors
src/theme/spacing.ts    - Spacing scale
src/theme/typography.ts - Font sizes
```

---

## 🎨 Design Reference

### Yuki Renders Available
All in `src/assets/renders/`:
- blade.png, morpheus.png, jules.png
- ghost_rider.png, jon_snow.png, nightwing.png
- luffy.png, mikasa.png, frieren.png
- kakashi.png, makima.png, nezuko.png

### Color Palette
- Primary: `#13b6ec` (Yuki cyan)
- Background Dark: `#0c1518`
- Surface: `#141d21`
- Accent: `#00d9ff`

### Tier Colors (for Task 31)
```typescript
MODERN: '#10b981'     // Green
SUPERHERO: '#6366f1'  // Indigo
FANTASY: '#f59e0b'    // Amber
CARTOON: '#ec4899'    // Pink
```

---

## 🔧 Running the App

```powershell
cd c:\Yuki_Local\yuki-app

# Web
npx expo start --web

# Mobile (tunnel for device testing)
npx expo start --tunnel
```

**Current Status**: App is running on port 8081 with tunnel active.

---

## 📐 18-Zone Face Mapping (for Task 36)

From `facialIPService.ts`:
```typescript
const FACIAL_ZONES = [
  { id: 1, name: 'Ears', icon: '👂' },
  { id: 2, name: 'Eyes', icon: '👁️' },
  { id: 3, name: 'Mouth', icon: '👄' },
  { id: 4, name: 'Nose', icon: '👃' },
  // ... zones 5-18
];
```

Use these for the face scan animation - show each zone lighting up as it's "scanned".

---

## 🚀 Priority Order

1. **Tasks 36-40** (Generation Screen) - Most visible, enhances core flow
2. **Tasks 21-25** (Home Screen) - First thing users see
3. **Tasks 31-35** (Character Selection) - Discovery experience
4. **Tasks 26-30** (Upload Flow) - Quality improvement

---

## 💬 Notes from Ebony

- I've already imported 12 real Yuki renders into `src/assets/renders/`
- The character system uses tiers: MODERN, SUPERHERO, FANTASY, CARTOON
- `facialIPService.ts` has the 18-zone structure ready for animations
- Navigation is set up with all screens registered in `AppNavigator.tsx`

**Questions?** Check `YUKI_APP_100_TASKS.md` for full context.

---

**Let's make this UI premium! 🦊✨**

*- Ebony 🖤*
