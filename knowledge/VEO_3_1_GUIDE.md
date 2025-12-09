# Veo 3.1

Veo 3.1 is our latest line of video generation models. This page documents the capabilities and features of Veo 3.1.

## Model Details

| Property | Value |
| :--- | :--- |
| **Model ID** | `veo-3.1-generate-001` |
| **Versions** | 3.1 Generate, 3.1 Fast Generate |

## Capabilities

### Supported
*   Text to video
*   Image to video
*   Prompt rewriting
*   Generate videos from the first and last frames

### Not supported
*   Reference image to video
*   Extend a Veo video

## Usage types

### Supported
*   Provisioned Throughput
*   Fixed quota

### Not supported
*   Dynamic shared quota

## Technical specifications

### Video aspect ratios
*   16:9
*   9:16 (except for reference image to video)

### Supported resolutions
*   720
*   1080 (except for video extension)

### Supported framerates
*   24 FPS

### Prompt languages
*   English

## Limits
*   **Maximum API requests per minute per project:** 50
*   **Maximum videos returned per request:** 4
*   **Video length:** 4, 6, or 8 seconds; reference image to video only supports 8 seconds.

For Veo pricing information, see the Veo section of the Cost of building and deploying AI models in Vertex AI page.
