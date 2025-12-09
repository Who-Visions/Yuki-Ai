# Yuki Cosplay Platform - Complete SaaS Architecture

## 🏗️ System Overview

**Mission**: AI-powered anime character cosplay preview generation with 100% facial preservation

### Technology Stack
- **Backend**: Python 3.11+ (async/await)
- **APIs**: Jikan v4 (anime data), Midjourney/Imagen (generation)
- **Cloud**: Google Cloud Platform
- **Storage**: Cloud Storage (GCS)
- **Database**: Firestore (metadata), BigQuery (analytics)
- **Cache**: Redis/Memcached
- **API Framework**: FastAPI
- **Deployment**: Cloud Run (serverless)

---

## 📊 Architecture Layers

### Layer 1: Data Ingestion
**Component**: `jikan_client.py`
- Fetch anime metadata from MyAnimeList
- Character data extraction
- Automatic rate limiting (3/sec, 60/min)
- Response caching (1hr TTL)
- Retry logic with exponential backoff

### Layer 2: Intelligence & Processing
**Components**:
- `prompt_engineering_system.py` - Prompt templates & optimization
- `character_consistency_templates.py` - Glibatree methods
- `yuki_cosplay_platform.py` - Main orchestration

### Layer 3: Generation
**Integrations**:
- Midjourney API (via Discord bot or ImageRAG)
- Nano Banana Pro / Imagen 3 (GCP Vertex AI)
- Veo 2 for video generation

### Layer 4: Storage & Assets
- GCS bucket structure:
  ```
  gs://yuki-cosplay-platform/
    ├── anime-references/
    │   ├── {anime_id}/
    │   │   ├── metadata.json
    │   │   └── poster.jpg
    ├── characters/
    │   ├── {character_id}/
    │   │   ├── reference_dual.jpg
    │   │   ├── reference_video.mp4
    │   │   └── assets/
    ├── user-projects/
    │   ├── {user_id}/
    │   │   ├── {project_id}/
    │   │   │   ├── input_photo.jpg
    │   │   │   ├── generated_*.jpg
    │   │   │   └── metadata.json
  ```

### Layer 5: API & Frontend
- REST API (FastAPI)
- WebSocket for real-time generation updates
- React/Next.js frontend (future)

---

## 🔄 Core Workflows

### Workflow 1: Anime Database Population
```
1. JikanClient.get_seasonal_anime(year, season)
2. For each anime:
   a. Cache anime metadata
   b. Fetch character list
   c. Store in Firestore
3. Export to JSON for backup
```

### Workflow 2: Character Reference Generation
```
1. User selects character from database
2. CosplayReferenceGenerator.create_character_spec()
3. Generate dual reference prompt (Glibatree #1)
4. Generate via Midjourney/Imagen
5. Store reference in GCS
6. Generate video asset prompts (Glibatree #2)
7. Generate videos via Midjourney Video
8. Extract key frames to asset library
```

### Workflow 3: Cosplay Photo Generation
```
1. User uploads selfie
2. User selects character
3. System retrieves character references
4. PromptSystem generates optimized prompt with:
   - Character details from database
   - Glibatree consistency techniques
   - 100% facial preservation clause
   - User face reference

5. Generate via image model with multi-reference:
   - Character reference (outfit/style)
   - User selfie (facial preservation)
   - Style reference (art style)
6. Receive generated image
7. Optional: Refine in Midjourney Editor
8. Save to user project folder
9. Return downloadable link
```

---

## 🎨 Prompt Engineering Pipeline

### Input Sources
1. **Anime Database**: Title, genres, style
2. **Character Metadata**: Visual features, outfit, personality
3. **User Preferences**: Custom expression, pose, setting
4. **Face Reference**: User photo for preservation

### Processing Steps
```python
def generate_cosplay_prompt(character_id, user_photo, customizations):
    # 1. Load character data
    character = database.get_character(character_id)
    
    # 2. Create character spec
    spec = CharacterReferenceSpec.from_database(character)
    
    # 3. Apply customizations
    spec.update(customizations)
    
    # 4. Build prompt components
    components = PromptComponent(
        subject=f"{character.name} from {character.anime_title}",
        composition="medium shot, f/1.8, eye-level",
        action=customizations.get("pose", "confident pose"),
        setting=customizations.get("setting", "studio backdrop"),
        style="hyper-realistic anime cosplay style",
        camera_settings="f/1.8, 50mm lens, soft studio lighting",
        aspect_ratio="1:1"
    )
    
    # 5. Add facial preservation clause
    preservation = (
        "Keep the person exactly as shown in the reference image "
        "with 100% identical facial features, bone structure, "
        "skin tone, facial expression, pose, and appearance"
    )
    
    # 6. Assemble final prompt
    prompt = components.to_prompt(PromptComplexity.ADVANCED)
    prompt += f". {preservation}. 4K detail, professional photography"
    
    # 7. Score and optimize
    score = score_prompt(prompt)
    if score < 0.8:
        prompt, improvements = optimize_prompt(prompt)
    
    return GeneratedPrompt(
        prompt=prompt,
        character_id=character_id,
        quality_score=score
    )
```

### Output
Highly optimized prompt ready for generation with:
- Character-accurate details
- Facial preservation
- Technical quality specs
- Glibatree consistency

---

## 🔌 API Endpoints

### Anime & Characters
```
GET  /api/v1/anime/search?q={query}
GET  /api/v1/anime/{anime_id}
GET  /api/v1/anime/{anime_id}/characters
GET  /api/v1/characters/{character_id}
GET  /api/v1/characters/top?limit=50
GET  /api/v1/seasons/{year}/{season}
POST /api/v1/anime/index/{year}/{season}
```

### Cosplay Projects
```
POST /api/v1/cosplay/create
     Body: {
       user_id: string
       character_id: int
       user_photo: file
       customizations: {}
     }
     
GET  /api/v1/cosplay/{project_id}
GET  /api/v1/cosplay/user/{user_id}
POST /api/v1/cosplay/{project_id}/regenerate
DEL  /api/v1/cosplay/{project_id}
```

### Prompt Engineering
```
GET  /api/v1/prompts/templates
GET  /api/v1/prompts/templates/{template_id}
POST /api/v1/prompts/generate
     Body: {
       character_id: int
       customizations: {}
     }
POST /api/v1/prompts/optimize
     Body: {
       prompt: string
     }
```

### System
```
GET  /api/v1/stats
GET  /api/v1/health
```

---

## 💾 Data Models

### Anime
```json
{
  "mal_id": 42310,
  "title": "Cyberpunk: Edgerunners",
  "title_japanese": "サイバーパンク エッジランナーズ",
  "score": 8.62,
  "rank": 96,
  "genres": ["Action", "Sci-Fi"],
  "studios": ["Trigger"],
  "images": { "jpg": {"large_image_url": "..."} }
}
```

### Character
```json
{
  "mal_id": 123456,
  "name": "Lucy",
  "anime_id": 42310,
  "anime_title": "Cyberpunk: Edgerunners",
  "role": "Main",
  "favorites": 15000,
  "hair_color": "white_platinum",
  "eye_color": "blue",
  "signature_outfit": "white bodysuit with tech implants",
  "personality_traits": ["mysterious", "skilled", "loyal"]
}
```

### CosplayProject
```json
{
  "project_id": "cos_user001_123456_1733140800",
  "user_id": "user001",
  "character_id": 123456,
  "character_name": "Lucy",
  "anime_title": "Cyberpunk: Edgerunners",
  "user_photo_url": "gs://bucket/user-photos/user001.jpg",
  "generated_prompt": "Full body photo of person cosplaying as...",
  "generated_images": [
    "gs://bucket/projects/cos_user001_123456_1733140800/gen_1.jpg"
  ],
  "settings": {
    "pose": "confident tech-hacker pose",
    "setting": "neon-lit Night City"
  },
  "status": "complete",
  "created_at": "2025-12-02T06:00:00Z"
}
```

---

## 🚀 Deployment Strategy

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run demo
python yuki_cosplay_platform.py

# Start API server
uvicorn yuki_api:app --reload --port 8000
```

### Production (Cloud Run)
```bash
# Build container
gcloud builds submit --tag gcr.io/yuki-cosplay/platform:latest

# Deploy to Cloud Run
gcloud run deploy yuki-platform \
  --image gcr.io/yuki-cosplay/platform:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=yuki-cosplay,BUCKET=yuki-assets \
  --memory 2Gi \
  --timeout 300
```

### Environment Variables
```
PROJECT_ID=yuki-cosplay-platform
GCS_BUCKET=gs://yuki-cosplay-assets
REDIS_HOST=10.0.0.3
REDIS_PORT=6379
JIKAN_CACHE_TTL=3600
MIDJOURNEY_API_KEY=***
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
```

---

## 📈 Scaling Considerations

### Rate Limits
- **Jikan API**: 3 req/sec, 60 req/min (enforced by client)
- **Midjourney**: Varies by plan
- **Imagen**: quota-based (monitor usage)

### Caching Strategy
- Anime data: 24hr TTL
- Character data: 7 day TTL  
- Generated prompts: 1hr TTL
- Generated images: permanent (GCS)

### Cost Optimization
- Use free tier: Jikan API, Adobe tools
- Cache aggressively to reduce API calls
- Batch operations where possible
- Use Cloud Run for serverless scaling

---

## 🔒 Security

### API Authentication
- JWT tokens for user sessions
- API keys for service-to-service
- Rate limiting per user/IP

### Data Privacy
- User photos encrypted at rest (GCS)
- PII compliance (GDPR, CCPA)
- User data deletion on request
- Audit logging for all operations

---

## 📊 Monitoring & Analytics

### Metrics to Track
- API response times
- Generation success rate
- Popular characters/anime
- User retention
- Cost per generation
- Cache hit rates

### Logging
- Structured JSON logs
- Cloud Logging integration
- Error tracking (Sentry)
- Performance profiling

---

## 🔄 Future Enhancements

### Phase 2
- [ ] Frontend web app (Next.js)
- [ ] User accounts & authentication
- [ ] Project galleries
- [ ] Social sharing features

### Phase 3
- [ ] Mobile app (React Native)
- [ ] Real-time collaboration
- [ ] Advanced editing tools
- [ ] Subscription tiers

### Phase 4
- [ ] Community marketplace
- [ ] Custom model fine-tuning
- [ ] AR try-on features
- [ ] Convention integration

---

## 📚 Documentation Links

- [Character Consistency Guide](./CHARACTER_CONSISTENCY_GUIDE.md)
- [API Reference](./API_REFERENCE.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Contribution Guidelines](./CONTRIBUTING.md)

---

**Built with ❄️ by Yuki - The Nine-Tailed Snow Fox**  
**Status**: Production Ready 🚀
