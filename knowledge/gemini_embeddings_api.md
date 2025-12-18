# Gemini Embeddings API Reference
>
> Last Updated: December 2025

## Model Info

| Property | Value |
|----------|-------|
| **Model ID** | `gemini-embedding-001` |
| **Input Limit** | 2,048 tokens |
| **Output Dimensions** | 128 - 3072 (recommended: 768, 1536, 3072) |
| **Batch Pricing** | 50% of interactive pricing |

---

## Quick Start (Python)

```python
from google import genai

client = genai.Client()

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What is the meaning of life?"
)

print(result.embeddings)
```

## Batch Embeddings

```python
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[
        "What is the meaning of life?",
        "What is the purpose of existence?",
        "How do I bake a cake?"
    ]
)
```

---

## Task Types

| Task Type | Use Case |
|-----------|----------|
| `SEMANTIC_SIMILARITY` | Recommendation systems, duplicate detection |
| `CLASSIFICATION` | Sentiment analysis, spam detection |
| `CLUSTERING` | Document organization, anomaly detection |
| `RETRIEVAL_DOCUMENT` | Indexing documents for search |
| `RETRIEVAL_QUERY` | Search queries |
| `CODE_RETRIEVAL_QUERY` | Code search from natural language |
| `QUESTION_ANSWERING` | Chatbots, Q&A systems |
| `FACT_VERIFICATION` | Fact-checking systems |

---

## Controlling Dimension Size

```python
from google.genai import types

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What is the meaning of life?",
    config=types.EmbedContentConfig(output_dimensionality=768)
)
```

### MTEB Scores by Dimension

| Dimension | Score |
|-----------|-------|
| 3072 | - |
| 2048 | 68.16 |
| 1536 | 68.17 |
| 768 | 67.99 |
| 512 | 67.55 |
| 256 | 66.19 |

---

## Semantic Similarity Example

```python
from google import genai
from google.genai import types
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

client = genai.Client()

texts = [
    "What is the meaning of life?",
    "What is the purpose of existence?",
    "How do I bake a cake?"
]

result = [
    np.array(e.values) for e in client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
    ).embeddings
]

embeddings_matrix = np.array(result)
similarity_matrix = cosine_similarity(embeddings_matrix)

for i, text1 in enumerate(texts):
    for j in range(i + 1, len(texts)):
        similarity = similarity_matrix[i, j]
        print(f"'{text1}' vs '{texts[j]}': {similarity:.4f}")
```

**Output:**

```
'meaning of life' vs 'purpose of existence': 0.9481
'meaning of life' vs 'bake a cake': 0.7471
```

---

## Vector Databases

- **Google Cloud:** BigQuery, AlloyDB, Cloud SQL
- **Third-party:** ChromaDB, Pinecone, Weaviate, Qdrant

---

## REST API

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "content": {"parts":[{"text": "What is the meaning of life?"}]},
    "output_dimensionality": 768
  }'
```

---

## Deprecation Notice

**Deprecating Oct 2025:**

- `embedding-001`
- `embedding-gecko-001`
- `gemini-embedding-exp-03-07`

**Use:** `gemini-embedding-001` (stable)
