# Imagen 3

Imagen 3 is our current line of image generation models. This page documents the capabilities and features of the Imagen 3 models.

## Model Details

| Property | Value |
| :--- | :--- |
| **Model ID** | `imagen-3.0-generate-002` |
| **Versions** | 3.0 Generate 002, 3.0 Generate 001, 3.0 Fast Generate 001, 3.0 Capability 001 |

## Capabilities

### Supported
*   Image generation
*   Digital watermarking and verification
*   User-configurable safety settings
*   Prompt enhancement using prompt rewriter
*   Person generation checklist_rtl

### Not supported
*   Image customization using few-shot learning
*   Subject customization for product, person, and animal companion
*   Style customization
*   Controlled customization
*   Instruct customization or style transfer
*   Mask-based image editing
*   Insert objects in images
*   Remove objects from images
*   Outpainting
*   Product image editing
*   Upscale images
*   Negative prompting

## Usage types

### Supported
*   Provisioned Throughput

### Not supported
*   (None listed explicitly as not supported in the provided text, but implied by omission of others)

## Technical specifications

### Image ratios and resolutions
*   **1:1**: 1024x1024
*   **3:4**: 896x1280
*   **4:3**: 1280x896
*   **9:16**: 768x1408
*   **16:9**: 1408x768

### Prompt languages
*   English
*   Chinese (simplified) preview
*   Chinese (traditional) preview
*   Hindi preview
*   Japanese preview
*   Korean preview
*   Portuguese preview
*   Spanish preview

## Limits
*   **Maximum API requests per minute per project:** 20
*   **Maximum images returned per request (text-to-image generation):** 4
*   **Maximum image size uploaded or sent in a request (MB):** 10 MB
*   **Maximum input tokens (text-to-image generation prompt text):** 480 tokens

For Imagen pricing information, see the Imagen section of the Cost of building and deploying AI models in Vertex AI page.
