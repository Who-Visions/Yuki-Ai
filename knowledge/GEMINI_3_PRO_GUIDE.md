# Gemini 3 Pro

> **Preview**
>
> This product or feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms, and the Additional Terms for Generative AI Preview Products. You can process personal data for this product or feature as outlined in the Cloud Data Processing Addendum, subject to the obligations and restrictions described in the agreement under which you access Google Cloud. Pre-GA products and features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

Gemini 3 Pro is our most advanced reasoning Gemini model, capable of solving complex problems. Gemini 3 Pro can comprehend vast datasets and challenging problems from different information sources, including text, audio, images, video, PDFs, and even entire code repositories with its 1M token context window.

**Note:** PDF token counts will be listed under the `IMAGE` modality instead of the `DOCUMENT` modality in `usage_metadata`.

Gemini 3 Pro introduces several new features to improve performance, control, and multimodal fidelity:

*   **Thinking level:** Use the `thinking_level` parameter to control the amount of internal reasoning the model performs (low or high) to balance response quality, reasoning complexity, latency, and cost. The `thinking_level` parameter replaces `thinking_budget` for Gemini 3 models.
*   **Media resolution:** Use the `media_resolution` parameter (low, medium, or high) to control vision processing for multimodal inputs, impacting token usage and latency. See Get started with Gemini 3 for default resolution settings.
*   **Thought signatures:** Stricter validation of thought signatures improves reliability in multi-turn function calling.
*   **Multimodal function responses:** Function responses can now include multimodal objects like images and PDFs in addition to text.
*   **Streaming Function calling:** Stream partial function call arguments to improve user experience during tool use.

For more information on using these features, see Get started with Gemini 3 Pro.

## Model Details

| Property | Value |
| :--- | :--- |
| **Model ID** | `gemini-3-pro-preview` |
| **Supported inputs** | Text, Code, Images, Audio, Video, PDF |
| **Supported outputs** | Text |
| **Maximum input tokens** | 1,048,576 |
| **Maximum output tokens** | 65,536 |
| **Knowledge cutoff date** | January 2025 |
| **Launch stage** | Public preview |
| **Release date** | November 18, 2025 |

## Capabilities

### Supported
*   Grounding with Google Search
*   Code execution
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
*   Tuning
*   Live API preview

## Usage types

### Supported
*   Provisioned Throughput
*   Dynamic shared quota
*   Batch prediction

### Not supported
*   Fixed quota

## Technical specifications

### Images
*   **Maximum images per prompt:** 900
*   **Maximum image size:** 7 MB
*   **Default resolution tokens:** 1120
*   **Supported MIME types:** `image/png`, `image/jpeg`, `image/webp`, `image/heic`, `image/heif`

### Documents
*   **Maximum number of files per prompt:** 900
*   **Maximum number of pages per file:** 900
*   **Maximum file size per file for the API or Cloud Storage imports:** 50 MB
*   **Maximum file size per file for direct uploads through the console:** 7 MB
*   **Default resolution tokens:** 560
*   **OCR for scanned PDFs:** Not used by default
*   **Supported MIME types:** `application/pdf`, `text/plain`

### Video
*   **Maximum video length (with audio):** Approximately 45 minutes
*   **Maximum video length (without audio):** Approximately 1 hour
*   **Maximum number of videos per prompt:** 10
*   **Default resolution tokens per frame:** 70
*   **Supported MIME types:** `video/x-flv`, `video/quicktime`, `video/mpeg`, `video/mpegs`, `video/mpg`, `video/mp4`, `video/webm`, `video/wmv`, `video/3gpp`

### Audio
*   **Maximum audio length per prompt:** Approximately 8.4 hours, or up to 1 million tokens
*   **Maximum number of audio files per prompt:** 1
*   **Speech understanding for:** Audio summarization, transcription, and translation
*   **Supported MIME types:** `audio/x-aac`, `audio/flac`, `audio/mp3`, `audio/m4a`, `audio/mpeg`, `audio/mpga`, `audio/mp4`, `audio/ogg`, `audio/pcm`, `audio/wav`, `audio/webm`

## Parameter defaults
*   **Temperature:** 0.0-2.0 (default 1.0)
*   **topP:** 0.0-1.0 (default 0.95)
*   **topK:** 64 (fixed)
*   **candidateCount:** 1–8 (default 1)

## Supported regions
**Model availability** (Includes dynamic shared quota & Provisioned Throughput): **Global**

See Data residency for more information.
