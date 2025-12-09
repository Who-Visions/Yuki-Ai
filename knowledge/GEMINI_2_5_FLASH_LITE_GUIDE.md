# Gemini 2.5 Flash-Lite

Gemini 2.5 Flash-Lite is our most balanced Gemini model, optimized for low latency use cases. It comes with the same capabilities that make other Gemini 2.5 models helpful, such as the ability to turn thinking on at different budgets, connecting to tools like Grounding with Google Search and code execution, multimodal input, and a 1 million-token context length.

## Model Details

| Property | Value |
| :--- | :--- |
| **Model ID** | `gemini-2.5-flash-lite` |
| **Supported inputs** | Text, Code, Images, Audio, Video |
| **Supported outputs** | Text |
| **Maximum input tokens** | 1,048,576 |
| **Maximum output tokens** | 65,536 (default) |
| **Knowledge cutoff date** | January 2025 |
| **Launch stage** | GA |
| **Release date** | July 22, 2025 |
| **Discontinuation date** | July 22, 2026 |
| **Input size limit** | 500 MB |

## Capabilities

### Supported
*   Grounding with Google Search
*   Code execution
*   Tuning
*   System instructions
*   Function calling
*   Count Tokens
*   Structured output
*   Thinking
*   Implicit context caching
*   Explicit context caching
*   Vertex AI RAG Engine

### Not supported
*   Live API
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
*   **Maximum images per prompt:** 3,000
*   **Maximum image size:** 7 MB
*   **Maximum number of output images per prompt:** 10
*   **Supported MIME types:** `image/png`, `image/jpeg`, `image/webp`, `image/heic`, `image/heif`

### Documents
*   **Maximum number of files per prompt:** 3,000
*   **Maximum number of pages per file:** 1,000
*   **Maximum file size per file:** 50 MB
*   **Supported MIME types:** `application/pdf`, `text/plain`

### Video
*   **Maximum video length (with audio):** Approximately 45 minutes
*   **Maximum video length (without audio):** Approximately 1 hour
*   **Maximum number of videos per prompt:** 10
*   **Supported MIME types:** `video/x-flv`, `video/quicktime`, `video/mpeg`, `video/mpegs`, `video/mpg`, `video/mp4`, `video/webm`, `video/wmv`, `video/3gpp`

### Audio
*   **Maximum audio length per prompt:** Appropximately 8.4 hours, or up to 1 million tokens
*   **Maximum number of audio files per prompt:** 1
*   **Supported MIME types:** `audio/x-aac`, `audio/flac`, `audio/mp3`, `audio/m4a`, `audio/mpeg`, `audio/mpga`, `audio/mp4`, `audio/ogg`, `audio/pcm`, `audio/wav`, `audio/webm`

## Parameter defaults
*   **Temperature:** 0.0-2.0 (default 1.0)
*   **topP:** 0.0-1.0 (default 0.95)
*   **topK:** 64 (fixed)
*   **candidateCount:** 1–8 (default 1)

## Supported regions

### Model availability
(Includes dynamic shared quota & Provisioned Throughput)

*   **Global**: global
*   **United States**: us-central1, us-east1, us-east4, us-east5, us-south1, us-west1, us-west4
*   **Europe**: europe-central2, europe-north1, europe-southwest1, europe-west1, europe-west4, europe-west8, europe-west9

### ML processing
*   **United States**: Multi-region
*   **Europe**: Multi-region

See Data residency for more information.
