# 🐛 Ebony Bug Report

**Date:** 2025-12-11
**Reporter:** Ebony 🖤

## Critical Issues Found

### 1. API Integration Stubbed
- `yukiService.ts` currently points to `localhost:8080` or production URL, but local testing is hitting `localhost:8081` (webpack dev server).
- **Impact:** Real backend calls will fail in browser unless proxy is set up or CORS is perfectly handled.
- **Fix:** Ensure `yuki_api.py` is running on 8080 and `yuki-app` points to it correctly.

### 2. Missing Authentication
- App currently has no user persistence. "User ID" is generated randomly per session.
- **Impact:** User history, credits, and saved characters are lost on reload.
- **Fix:** Implement Firebase Auth (Google/Apple) immediately.

### 3. "Trending" Data is Hardcoded
- `TrendingCarousel.tsx` uses a static array of characters.
- **Impact:** "Trending This Week" is static and doesn't reflect real analytics.
- **Fix:** Connect to `yuki_api.py` endpoint for real trending data (Task 21 backlog).

### 4. Upload Flow Fragility
- Base64 image upload works but lacks robust error handling for large files.
- **Impact:** Potential crashes with 4K images on older devices.
- **Fix:** Implement chunked upload or resize-before-upload logic.

---

**Status:** Awaiting fixes. I am prioritizing Auth (#2) now.
