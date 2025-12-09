# Gemini 3 Pro Image

> **Caution**
>
> The `gemini-2.0-flash-preview-image-generation` and `gemini-2.5-flash-image-preview` models will be retired on October 31, 2025. Migrate any workflows to `gemini-2.5-flash-image` before that date to avoid service disruption.

> **Preview**
>
> This feature is a Generative AI Preview offering, subject to the "Pre-GA Offerings Terms" of the Google Cloud Service Specific Terms, as well as the Additional Terms for Generative AI Preview Products. For this Generative AI Preview offering, Customers may elect to use it for production or commercial purposes, disclose Generated Output to third-parties, and process personal data as outlined in the Cloud Data Processing Addendum, subject to the obligations and restrictions described in the agreement under which you access Google Cloud. Pre-GA products and features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

Gemini 3 Pro Image, or Gemini 3 Pro (with Nano Banana), is designed to tackle the most challenging image generation by incorporating state-of-the-art reasoning capabilities. It's the best model for complex and multi-turn image generation and editing, having improved accuracy and enhanced image quality.

For more information about image generation using Gemini 3 Pro Image, see Generate and edit images with Gemini.

## Model Details

| Property | Value |
| :--- | :--- |
| **Model ID** | `gemini-3-pro-image-preview` |
| **Supported inputs** | Text, Images |
| **Supported outputs** | Text and image |
| **Maximum input tokens** | 65,536 |
| **Maximum output tokens** | 32,768 |
| **Knowledge cutoff date** | January 2025 |
| **Launch stage** | Public preview |
| **Release date** | November 20, 2025 |
| **Input size limit** | 500 MB |

## Capabilities

### Supported
*   Grounding with Google Search
*   System instructions
*   Count Tokens
*   Thinking

### Not supported
*   Code execution
*   Tuning
*   Function calling
*   Live API preview
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
*   **Maximum images per prompt:** 14
*   **Maximum image size:** 7 MB
*   **Maximum number of output images per prompt:** Limited to 32,768 output tokens
*   **Supported aspect ratios:** 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, and 21:9
*   **Supported MIME types:** `image/png`, `image/jpeg`, `image/webp`, `image/heic`, `image/heif`

### Documents
*   **Maximum number of files per prompt:** As supported by the 65,536 token context window
*   **Maximum number of pages per file:** As supported by the 65,536 token context window
*   **Maximum file size per file:** 50 MB (API and Cloud Storage imports) or 7 MB (direct upload through Google Cloud console)
*   **Supported MIME types:** `application/pdf`, `text/plain`

## Parameter defaults
*   **Temperature:** 0.0-2.0
*   **topP:** 0.0-1.0 (default 0.95)
*   **topK:** 64 (fixed)
*   **candidateCount:** 1

## Supported regions
**Model availability** (Includes dynamic shared quota & Provisioned Throughput): **Global**

See Data residency for more information.
