# Gemini 2.5 Pro

Gemini 2.5 Pro is our most advanced reasoning Gemini model, capable of solving complex problems. Gemini 2.5 Pro can comprehend vast datasets and challenging problems from different information sources, including text, audio, images, video, and even entire code repositories.

For even more detailed technical information on Gemini 2.5 Pro (such as performance benchmarks, information on our training datasets, efforts on sustainability, intended usage and limitations, and our approach to ethics and safety), see our technical report on our Gemini 2.5 models.

## Model Details

| Property | Value |
| :--- | :--- |
| **Model ID** | `gemini-2.5-pro` |
| **Supported inputs** | Text, Code, Images, Audio, Video |
| **Supported outputs** | Text |
| **Maximum input tokens** | 1,048,576 |
| **Maximum output tokens** | 65,535 (default) |
| **Knowledge cutoff date** | January 2025 |
| **Launch stage** | GA |
| **Release date** | June 17, 2025 |
| **Discontinuation date** | June 17, 2026 |
| **Input size limit** | 500 MB |

## Capabilities

### Supported
*   Grounding with Google Search
*   Code execution
*   Tuning
*   System instructions
*   Structured output
*   Function calling
*   Count Tokens
*   Thinking
*   Implicit context caching
*   Explicit context caching
*   Vertex AI RAG Engine
*   Chat completions

### Not supported
*   Live API

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
*   **Supported MIME types:** `image/png`, `image/jpeg`, `image/webp`, `image/heic`, `image/heif`

### Documents
*   **Maximum number of files per prompt:** 3,000
*   **Maximum number of pages per file:** 1,000
*   **Maximum file size per file for the API or Cloud Storage imports:** 50 MB
*   **Maximum file size per file for direct uploads through the console:** 7 MB
*   **Supported MIME types:** `application/pdf`, `text/plain`

### Video
*   **Maximum video length (with audio):** Approximately 45 minutes
*   **Maximum video length (without audio):** Approximately 1 hour
*   **Maximum number of videos per prompt:** 10
*   **Supported MIME types:** `video/x-flv`, `video/quicktime`, `video/mpeg`, `video/mpegs`, `video/mpg`, `video/mp4`, `video/webm`, `video/wmv`, `video/3gpp`

### Audio
*   **Maximum audio length per prompt:** Appropximately 8.4 hours, or up to 1 million tokens
*   **Maximum number of audio files per prompt:** 1
*   **Speech understanding for:** Audio summarization, transcription, and translation
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
*   **Asia Pacific**: asia-northeast1

See Data residency for more information.
