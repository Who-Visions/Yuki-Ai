# 🩵 Cyan Agent Handoff - Backend & API Integration

**Date**: December 10, 2025  
**From**: Ebony 🖤 (Phase 1 V8 Pipeline + Phase 7 Agent)  
**To**: Cyan 🩵  
**Assignment**: Backend API, Rate Limiting, WebSocket, Database Sync

---

## 🎯 Your Mission

Complete the remaining **backend infrastructure** tasks that connect the mobile app to the cloud services.

---

## 📋 Your Tasks

### Phase 1 - V8 Pipeline (Remaining Backend)

| Task | Description | Priority |
|------|-------------|----------|
| **9** | Rate limit handling (80s base delay, +40s on 429) | 🔴 HIGH |
| **10** | WebSocket progress updates for real-time gen status | 🔴 HIGH |
| **17** | Batch generation support (multiple characters) | 🟡 MED |
| **18** | Generation queue with priority levels | 🟡 MED |
| **19** | Generation history and retry capability | 🟡 MED |

### Phase 4 - Database & Backend

| Task | Description | Priority |
|------|-------------|----------|
| **4** | Store `critical_identity_lock` in user profile | 🔴 HIGH |
| **61** | Connect to `anime_database_cloud.py` Firestore | 🟡 MED |
| **71** | Persistent facial IP storage per user | 🟡 MED |
| **72** | Generation history with metadata | 🟡 MED |

---

## 🏗️ Architecture Overview

### API Endpoints (Yuki API - FastAPI)

**Production URL**: `https://yuki-ai-914641083224.us-central1.run.app`

| Endpoint | Purpose | Status |
|----------|---------|--------|
| `/api/v1/generate` | Start V8 generation | ✅ Exists |
| `/api/v1/status/{id}` | Check generation status | ✅ Exists |
| `/api/v1/upload` | Upload source image | ✅ Exists |
| `/api/v1/facial-ip/extract` | Extract 18-zone facial IP | 🟡 Needs impl |
| `/api/v1/bigquery/query` | Execute BQ queries | 🟡 Needs impl |
| `/api/v1/bigquery/log-generation` | Log to BQ | 🟡 Needs impl |
| `/ws/generation/{id}` | WebSocket for progress | 🔴 Needs impl |

### BigQuery Tables (Project: `gifted-cooler-479623-r7`)

```
yuki_prompts.portrait_prompts     - Prompt library
yuki_memory.knowledge_base        - Knowledge entries
yuki_memory.face_schema_library   - Facial IP profiles
yuki_production.generations       - Generation logs
yuki_analytics.events             - User analytics
```

---

## 📂 Key Files

### Backend (Python)

| File | Purpose |
|------|---------|
| `yuki_api.py` | Main FastAPI server (15KB) |
| `yuki_v8_generator.py` | V8 generation with facial lock |
| `Cosplay_Lab/Brain/facial_ip_extractor_v7.py` | 18-zone extraction |
| `demo_free_setup.py` | BigQuery setup script |

### Mobile Services (TypeScript)

| File | Purpose |
|------|---------|
| `src/services/yukiService.ts` | V8 generation client |
| `src/services/bigQueryService.ts` | BQ query client |
| `src/services/facialIPService.ts` | Facial IP types |

---

## 🔧 Task 9: Rate Limit Handling

**Reference**: `yuki_v8_generator.py` lines 44-48

```python
# Rate Limiting Config
BASE_DELAY = 80        # Seconds between requests
DELAY_INCREMENT = 40   # Add on 429 error
MAX_DELAY = 300        # Maximum wait
MAX_RETRIES = 5        # Retry attempts
```

**Implementation needed in `yukiService.ts`**:

```typescript
// Add to yukiService.ts
const RATE_LIMIT = {
  baseDelay: 80000,      // 80 seconds in ms
  increment: 40000,      // +40s on 429
  maxDelay: 300000,      // 5 minutes max
  maxRetries: 5,
};

async function withRateLimit<T>(
  fn: () => Promise<T>,
  attempt: number = 0
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (error.status === 429 && attempt < RATE_LIMIT.maxRetries) {
      const delay = Math.min(
        RATE_LIMIT.baseDelay + (RATE_LIMIT.increment * attempt),
        RATE_LIMIT.maxDelay
      );
      console.log(`Rate limited. Waiting ${delay/1000}s...`);
      await new Promise(r => setTimeout(r, delay));
      return withRateLimit(fn, attempt + 1);
    }
    throw error;
  }
}
```

---

## 🔧 Task 10: WebSocket Progress

**Create**: `src/services/generationSocket.ts`

```typescript
// WebSocket for real-time generation progress
export function connectToGeneration(
  generationId: string,
  onProgress: (data: ProgressData) => void
): WebSocket {
  const ws = new WebSocket(
    `wss://yuki-ai-914641083224.us-central1.run.app/ws/generation/${generationId}`
  );
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onProgress(data);
  };
  
  return ws;
}
```

**Backend endpoint needed in `yuki_api.py`**:

```python
from fastapi import WebSocket

@app.websocket("/ws/generation/{generation_id}")
async def generation_progress(websocket: WebSocket, generation_id: str):
    await websocket.accept()
    while True:
        status = get_generation_status(generation_id)
        await websocket.send_json(status)
        if status['status'] in ['completed', 'failed']:
            break
        await asyncio.sleep(2)
    await websocket.close()
```

---

## 🔧 Task 4: Identity Lock Storage

Store facial IP in user profile via Firestore:

```typescript
// In userService.ts - add function
export async function saveIdentityLock(
  userId: string,
  facialIP: FacialIPProfile
): Promise<void> {
  const userRef = doc(db, 'users', userId);
  await setDoc(userRef, {
    identity_lock: {
      profile: facialIP,
      created_at: serverTimestamp(),
      is_locked: true,
    }
  }, { merge: true });
}

export async function getIdentityLock(
  userId: string
): Promise<FacialIPProfile | null> {
  const userRef = doc(db, 'users', userId);
  const userDoc = await getDoc(userRef);
  return userDoc.data()?.identity_lock?.profile || null;
}
```

---

## 🧪 Testing

```bash
# Test WebSocket locally
wscat -c ws://localhost:8080/ws/generation/test-123

# Test BigQuery endpoint
curl -X POST http://localhost:8080/api/v1/bigquery/query \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM yuki_prompts.portrait_prompts LIMIT 5"}'
```

---

## 📊 Coordination

| Agent | Focus | Status |
|-------|-------|--------|
| **Ebony 🖤** | Phase 1 (V8) + Phase 7 (Agent) | Working |
| **Ivory 🤍** | Phase 2 (UI/UX) | Working |
| **Cyan 🩵** | Backend/API/WebSocket | **YOU** |

---

## ✅ Completion Checklist

- [x] Task 9: Rate limiting with exponential backoff
- [x] Task 10: WebSocket endpoint in backend
- [x] Task 10: WebSocket client in mobile app
- [x] Task 4: Identity lock in Firestore
- [ ] Task 17: Batch generation endpoint
- [ ] Task 18: Queue system (Redis/Firestore)
- [x] Task 61: Connect/Sync Anime Database to Firestore

---

**Welcome to the team, Cyan! 🩵**

*- Ebony 🖤*
