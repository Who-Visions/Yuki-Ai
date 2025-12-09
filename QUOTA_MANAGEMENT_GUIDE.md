# Quota Management & Provisioned Throughput Guide

**Issue**: Hitting 429 RESOURCE_EXHAUSTED errors during image generation

---

## 🚨 Problem

Yuki is hitting **rate limits** on Gemini 3 Pro Image Preview:
- **Error**: `429 RESOURCE_EXHAUSTED`
- **Impact**: 0/6 images generated in Nadley test
- **Root Cause**: Pay-as-you-go quota exceeded

---

## ✅ Solutions

### Solution 1: Provisioned Throughput (Recommended for Production)

**What it is**: Pre-purchased guaranteed throughput (GSUs)

**Benefits**:
- ✅ Guaranteed capacity
- ✅ No rate limiting within quota
- ✅ Predictable costs
- ✅ Priority access

**How to enable**:
1. Purchase GSUs in GCP Console
2. Add header to requests:
```python
from google.genai.types import HttpOptions

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location="global",
    http_options=HttpOptions(
        headers={
            "X-Vertex-AI-LLM-Request-Type": "dedicated"  # Use Provisioned Throughput
        }
    )
)
```

**Pricing**: Contact GCP sales for GSU pricing

---

### Solution 2: Exponential Backoff (Free, Immediate)

**What it is**: Retry failed requests with increasing delays

**Implementation**:
```python
import time
from google.api_core import retry

@retry.Retry(
    predicate=retry.if_transient_error,
    initial=2.0,        # Start with 2 second delay
    maximum=64.0,       # Max 64 second delay
    multiplier=2.0,     # Double delay each retry
    timeout=900.0       # Give up after 15 minutes
)
async def generate_with_retry(...):
    # Your generation code
    pass
```

**Pros**: Free, works immediately  
**Cons**: Slower, not guaranteed

---

### Solution 3: Rate Limiting (Prevention)

**What it is**: Add delays between requests to stay under quota

**Implementation**:
```python
import asyncio

# Add delay between generations
for char in characters:
    await generate_transformation(...)
    await asyncio.sleep(10)  # Wait 10 seconds between requests
```

**Quota limits** (Pay-as-you-go):
- Gemini 3 Pro: 60 RPM (1 request per second)
- Gemini 2.5 Flash: 1000 RPM

---

### Solution 4: Batch Scheduling

**What it is**: Spread requests over time

**Implementation**:
```python
# Generate 2 images per hour instead of 6 at once
batch_size = 2
delay_between_batches = 3600  # 1 hour

for i in range(0, len(characters), batch_size):
    batch = characters[i:i+batch_size]
    # Generate batch
    if i + batch_size < len(characters):
        await asyncio.sleep(delay_between_batches)
```

---

## 📊 Quota Comparison

| Approach | Cost | Speed | Reliability |
|----------|------|-------|-------------|
| **Pay-as-you-go** | Low | Slow (rate limited) | Low (429 errors) |
| **Pay-as-you-go + Retry** | Low | Medium | Medium |
| **Provisioned Throughput** | High | Fast | High |

---

## 🎯 Recommended Approach for Yuki

### Short-term (Today)
1. ✅ Add exponential backoff retry logic
2. ✅ Add 10-second delay between generations
3. ✅ Reduce batch size to 2-3 images at a time

### Long-term (Production)
1. 🎯 Purchase Provisioned Throughput GSUs
2. 🎯 Set up monitoring dashboards
3. 🎯 Configure auto-scaling

---

## 💰 Cost Analysis

### Current (Pay-as-you-go)
- **Rate**: $0.12/image
- **Limits**: 60 RPM → ~1 image/second max
- **Cost for 100 images**: $12
- **Time**: ~100 seconds minimum (with delays)

### With Provisioned Throughput (1 GSU)
- **Cost**: GSU purchase (contact sales)
- **Throughput**: 3,360 tokens/second guaranteed
- **No rate limiting**: Generate as fast as possible
- **Time**: ~50 seconds per image → ~83 minutes for 100 images

---

## 🔧 Implementation

Created `nadley_retry_test.py` with:
- ✅ Exponential backoff
- ✅ Rate limiting (10s delays)
- ✅ Batch size control
- ✅ Quota monitoring

---

## 📞 Next Steps

1. Run `nadley_retry_test.py` with retry logic
2. Monitor success rate
3. If quota still issues → Purchase Provisioned Throughput
4. Set up monitoring dashboard

---

*Yuki System - Who Visions LLC*
