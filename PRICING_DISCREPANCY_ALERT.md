# ⚠️ CRITICAL: Pricing Discrepancy Alert

## Yuki vs Unk Models Spec - Contract Pricing Comparison

**Date**: December 3, 2025  
**Source**: Who Visions LLC GCP Contract CSV

---

## 🚨 Key Finding

**Unk's `models_spec.py` has OUTDATED PRICING** that doesn't match the actual contract!

---

## 📊 Pricing Comparison

### Gemini 2.5 Flash

| Metric | Unk's Spec | Contract CSV | Difference |
|--------|------------|--------------|------------|
| **Input** | $0.10/1M | **$0.30/1M** | **+200%** ⬆️ |
| **Output** | $0.40/1M | **$2.50/1M** | **+525%** ⬆️ |
| **SKU** | - | FDAB-647C-5A22 | - |

**Impact**: Unk's cost estimates are **3-6x TOO LOW!**

### Gemini 2.5 Pro

| Metric | Unk's Spec | Contract CSV | Difference |
|--------|------------|--------------|------------|
| **Input** | **$2.50/1M** | $1.25/1M | **-50%** ⬇️ |
| **Output** | $10.00/1M | $10.00/1M | ✅ MATCH |
| **SKU** | - | A121-E2B5-1418 | - |

**Impact**: Unk's input pricing is **2x TOO HIGH**, but output matches.

### Gemini 3 Pro Image

| Metric | Unk's Spec | Contract CSV | Difference |
|--------|------------|--------------|------------|
| **Image Gen** | $0.13/image (est.) | **$0.12/image** | Close enough |
| **SKU** | - | 47A8-A5A1-B26C | - |

**Impact**: Unk's estimate is close.

---

## 💰 Real-World Impact on Yuki

### Today's Session Costs (18 images)

#### Using Unk's Pricing (WRONG)
- Analysis: $0.0005 (5K tokens @ $0.10/1M)
- Generation: $2.34 (18 images @ $0.13)
- **Total**: **$2.34**

#### Using Contract Pricing (CORRECT)
- Analysis: $0.0015 (5K tokens @ $0.30/1M)
- Generation: $2.16 (18 images @ $0.12)
- **Total**: **$2.16**

**Actual difference**: -$0.18 (Yuki costs LESS than Unk estimated!)

---

## ✅ Yuki's Solution

Created `yuki_models_spec.py` with **CORRECTED contract pricing**:

```python
from yuki_models_spec import calculate_session_cost

# Calculate costs using actual contract pricing
session = calculate_session_cost(
    analysis_tokens=5000,
    num_images=18
)

# Results:
# Analysis: $0.0015
# Generation: $2.16
# Total: $2.16
# Per Image: $0.12
#
# Imagen Alternative: $0.72 (67% savings!)
```

---

## 🎯 Recommendations

### For Yuki
1. ✅ Use `yuki_models_spec.py` for all cost calculations
2. ✅ Contract pricing is now accurate
3. ✅ Consider Imagen 3/4 for 67% cost savings

### For Unk
1. ⚠️ Update `models_spec.py` with contract CSV pricing
2. ⚠️ Flash input: $0.10 → $0.30
3. ⚠️ Flash output (thinking): $0.40 → $2.50
4. ⚠️ Pro input: $2.50 → $1.25

---

## 📁 Files Created

- ✅ `yuki_models_spec.py` - Corrected contract pricing
- ✅ `price_tracker.py` - Shared Unk/Yuki price tracking
- ✅ `yuki_cost_tracker.py` - Yuki-specific cost logging
- ✅ `PRICE_TRACKING_INTEGRATION.md` - Documentation

---

## 🔗 Source Files

- **Contract CSV**: `c:\Users\super\Downloads\Pricing for Who Visions LLC.csv`
- **Unk's Spec**: (in Unk repo) `gemini_agent/models_spec.py`
- **Yuki's Spec**: `c:\Yuki_Local\yuki_models_spec.py`

---

**Conclusion**: Yuki now has accurate pricing. Unk needs to update `models_spec.py` to match contract!

*Who Visions LLC - Billing Account Shared by Unk & Yuki*
