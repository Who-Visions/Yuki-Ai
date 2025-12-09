# Gemini 2.5 Flash Live API native audio

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

Gemini 2.5 Flash with Live API native audio features our cutting-edge native audio functionality for Live API. In addition to the standard Live API features, this preview model includes:

*   **Enhanced audio quality:** Experience dramatically improved audio quality that feels like speaking with a person.
*   **Enhanced voice quality and adaptability:** Live API native audio provides richer, more natural voice interactions with 30 HD voices in 24 languages.
*   **Introducing Proactive Audio:** When Proactive Audio is enabled, the model only responds when it's relevant. The model generates text transcripts and audio responses proactively only for queries directed to the device, and does not respond to non-device directed queries.
*   **Introducing Affective Dialog:** Models using Live API native audio can understand and respond appropriately to users' emotional expressions for more nuanced conversations.
*   **Improved barge-in:** Interrupt Gemini more naturally and reliably, even in loud and noisy environments.
*   **Robust function calling:** We've improved the triggering rate, allowing Gemini to successfully execute the functions you define to support your use cases.
*   **Accurate transcription:** The accuracy of audio-to-text transcription has been significantly enhanced.
*   **Seamless multilingual support:** Speak to Gemini in multiple languages, and it will effortlessly switch between them without any pre-configuration. Language is no longer a barrier.

For more information on Live API, see:
*   Our standalone Live API documentation.
*   Our Live API supported audio formats.
*   Our Live API concurrent session limits.

## Model Details

| Property | Value |
| :--- | :--- |
| **Model ID** | `gemini-live-2.5-flash-preview-native-audio-09-2025` |
| **Supported inputs** | Text, Images, Audio, Video |
| **Supported outputs** | Text, Audio |
| **Maximum input tokens** | 128K |
| **Maximum output tokens** | 64K |
| **Context window** | 32K (default), upgradable to 128K |
| **Knowledge cutoff date** | January 2025 |
| **Launch stage** | Public preview |
| **Release date** | September 18, 2025 |

## Capabilities

### Supported
*   Grounding with Google Search
*   System instructions
*   Function calling
*   Live API

### Not supported
*   Code execution
*   Tuning
*   Structured output
*   Thinking
*   Implicit context caching
*   Explicit context caching
*   Vertex AI RAG Engine
*   Chat completions

## Usage types

### Supported
*   Up to 1000 concurrent sessions
*   Provisioned Throughput

### Not supported
*   Dynamic shared quota
*   Batch prediction

## Technical specifications

### Images
*   **Maximum images per prompt:** 3,000
*   **Maximum image size:** 7 MB
*   **Supported MIME types:** `image/png`, `image/jpeg`, `image/webp`, `image/heic`, `image/heif`

### Video
*   **Standard resolution:** 768 x 768
*   **Supported MIME types:** `video/x-flv`, `video/quicktime`, `video/mpeg`, `video/mpegs`, `video/mpg`, `video/mp4`, `video/webm`, `video/wmv`, `video/3gpp`

### Audio
*   **Maximum conversation length:** Default 10 minutes that can be extended.
*   **Required audio input format:** Raw 16-bit PCM audio at 16kHz, little-endian
*   **Required audio output format:** Raw 16-bit PCM audio at 24kHz, little-endian
*   **Supported MIME types:** `audio/x-aac`, `audio/flac`, `audio/mp3`, `audio/m4a`, `audio/mpeg`, `audio/mpga`, `audio/mp4`, `audio/ogg`, `audio/pcm`, `audio/wav`, `audio/webm`

## Parameter defaults
*   **Start of speech sensitivity:** Low
*   **End of speech sensitivity:** High
*   **Prefix padding:** 0
*   **Max context size:** 128K

## Supported regions

### Model availability
*   **United States**: us-central1

See Data residency for more information.

## Versions
*   `gemini-live-2.5-flash-preview-native-audio-09-2025`
    *   Launch stage: Public preview
    *   Release date: September 18, 2025
*   `gemini-live-2.5-flash-preview-native-audio`
    *   Launch stage: Public preview
    *   Release date: June 17, 2025
    *   Discontinuation date: October 18, 2025
