# Gemini API Rate Limits Reference
>
> Last Updated: December 2025

## Rate Limit Dimensions

- **RPM**: Requests per minute
- **TPM**: Tokens per minute (input)
- **RPD**: Requests per day (resets at midnight Pacific)
- **IPM**: Images per minute (Imagen models only)

Rate limits are per **project**, not per API key.

---

## Usage Tiers

| Tier | Qualification |
|------|--------------|
| Free | Users in eligible countries |
| Tier 1 | Full paid Billing account linked |
| Tier 2 | Total spend > $250 + 30 days since payment |
| Tier 3 | Total spend > $1,000 + 30 days since payment |

---

## Batch API Rate Limits

- **Concurrent batch requests**: 100
- **Input file size limit**: 2GB
- **File storage limit**: 20GB

### Batch Enqueued Token Limits

| Model | Tier 1 | Tier 2 | Tier 3 |
|-------|--------|--------|--------|
| Gemini 3 Pro | 50M | 500M | 1B |
| Gemini 3 Flash | 3M | 400M | 500M |
| Gemini 3 Pro Image 🍌 | 2M | 270M | 1B |
| Gemini 2.5 Pro | 5M | 500M | 1B |
| Gemini 2.5 Flash | 3M | 400M | 1B |
| Gemini 2.0 Flash | 10M | 1B | 5B |

---

## Upgrading Tiers

1. Navigate to [API keys page](https://aistudio.google.com/app/apikey)
2. Locate eligible project and click "Upgrade"
3. Approval is automatic after validation

---

## Request Rate Limit Increase

[Submit request form](https://forms.gle/ETzX94k8jf7iSotH9)

No guarantees, but requests are reviewed.
