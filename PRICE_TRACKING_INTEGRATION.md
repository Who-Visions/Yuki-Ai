# Price Spike Tracking - Quick Setup Guide (Yuki Integration)

**Shared with Unk via Who Visions LLC Billing Account**

---

## ✅ Integration Notes

- **Yuki Project**: `gifted-cooler-479623-r7`
- **Unk Project**: Separate project ID
- **Billing**: Shared billing account (costs pool together)
- **Pricing**: Same Who Visions LLC contract pricing
- **Quotas**: Separate per project

---

## 🚀 Quick Start for Yuki

### Import Pricing Data

```bash
cd c:\Yuki_Local
python yuki_cost_tracker.py
```

This will:
- Use contract pricing from Who Visions LLC
- Track Yuki-specific image generation costs
- Log all costs to `data/yuki_costs.json`

---

## 💰 Corrected Yuki Pricing (from Contract CSV)

### Gemini 2.5 Flash (Analysis)
- **Input**: $0.30 per 1M tokens (was $0.10 - **3x correction**)
- **Output**: $2.50 per 1M tokens with thinking (was $0.40 - **6x correction**)
- **Caching**: $0.03 per 1M tokens (90% discount)

### Gemini 3.0 Pro Image Preview (Generation)
- **Image Output**: $0.12 per image ($120 per 1M images)
- **Text Input**: $2.00 per 1M tokens
- **Image Input**: $2.00 per 1M images

### Imagen 3 & 4 (Alternative)
- **Generation**: $0.04 per image (3x cheaper than Gemini 3 Pro)

---

## 📊 Today's Session Cost (CORRECTED)

### Tests Performed
1. **Jesse Test**: 10 character transformations
2. **Nadley Test**: 8 character transformations (5 with corrections)

### Cost Breakdown
- **Analysis** (Gemini 2.5 Flash): ~5,000 tokens @ $0.30/1M = $0.0015
- **Generation** (Gemini 3 Pro): 18 images @ $0.12/image = $2.16
- **TOTAL**: ~$2.16 (vs $1.30 estimated - 66% higher!)

---

## 🎯 Cost Optimization Strategies

1. **Use Imagen Instead of Gemini 3 Pro**
   - Imagen 3/4: $0.04/image
   - Gemini 3 Pro: $0.12/image
   - **Savings**: 67% ($0.08 per image)

2. **Enable Caching for Analysis**
   - Regular: $0.30/1M tokens
   - Cached: $0.03/1M tokens
   - **Savings**: 90%

3. **Batch Generations**
   - Single analysis for multiple generations
   - Amortize analysis cost across batch

---

## 📈 Monitoring Setup

Use Yuki's cost tracker to monitor spending:

```python
from yuki_cost_tracker import YukiCostTracker

tracker = YukiCostTracker(project_id="gifted-cooler-479623-r7")

# Get session costs
session = tracker.get_session_cost(hours=24)
print(f"Last 24h: ${session['total_cost']:.2f}")

# Check quota warning
status = tracker.check_quota_usage(warn_threshold=10.0)
print(status['message'])
```

---

## 🔗 Related Resources

- **Full Unk Price Tracking**: `docs/PRICE_TRACKING.md` (in Unk repo)
- **Pricing Breakdown**: `docs/PRICING_BREAKDOWN.md` (in Unk repo)
- **Yuki Cost Tracker**: `yuki_cost_tracker.py`
- **Contract CSV**: `c:\Users\super\Downloads\Pricing for Who Visions LLC.csv`

---

*Yuki System - Who Visions LLC Billing Integration*
