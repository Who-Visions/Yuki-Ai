# Gemini 2.5 Flash Image

Gemini 2.5 Flash Image is optimized for image understanding and generation and offers a balance of price and performance. Gemini 2.5 Flash Image uses the speed and cost-effectiveness of Gemini 2.5 Flash to provide fast and efficient image generation and editing capabilities.

## Model Details

| Property | Value |
| :--- | :--- |
| **Model ID** | `gemini-2.5-flash-image` |
| **Supported inputs** | Text, Images |
| **Supported outputs** | Text and image |
| **Maximum input tokens** | 32,768 |
| **Maximum output tokens** | 32,768 |
| **Knowledge cutoff date** | June 2025 |
| **Launch stage** | GA |
| **Release date** | October 2, 2025 |
| **Input size limit** | 500 MB |

## Capabilities

### Supported
*   System instructions
*   Count Tokens

### Not supported
*   Grounding with Google Search
*   Code execution
*   Tuning
*   Function calling
*   Live API
*   Thinking
*   Implicit context caching
*   Explicit context caching
*   Vertex AI RAG Engine
*   Chat completions

## Usage types

### Supported
*   Provisioned Throughput
*   Dynamic shared quota
*   Batch prediction

### Not supported
*   Fixed quota

## Technical specifications

### Images
*   **Maximum images per prompt:** 3
*   **Maximum image size:** 7 MB
*   **Maximum number of output images per prompt:** 10
*   **Supported aspect ratios:** 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, and 21:9
*   **Supported MIME types:** `image/png`, `image/jpeg`, `image/webp`, `image/heic`, `image/heif`

### Documents
*   **Maximum number of files per prompt:** 3
*   **Maximum number of pages per file:** 3
*   **Maximum file size per file:** 50 MB (API and Cloud Storage imports) or 7 MB (direct upload through Google Cloud console)
*   **Supported MIME types:** `application/pdf`, `text/plain`

## Parameter defaults
*   **Temperature:** 0.0-2.0 (default 1.0)
*   **topP:** 0.0-1.0 (default 0.95)
*   **topK:** 64 (fixed)
*   **candidateCount:** 1

## Supported regions

### Model availability
(Includes dynamic shared quota & Provisioned Throughput)

*   **Global**: global
*   **United States**: us-central1, us-east1, us-east4, us-east5, us-south1, us-west1, us-west4
*   **Europe**: europe-central2, europe-north1, europe-southwest1, europe-west1, europe-west4, europe-west8
*   **ML processing**:
    *   **United States**: Multi-region
    *   **Europe**: Multi-region

See Data residency for more information.
