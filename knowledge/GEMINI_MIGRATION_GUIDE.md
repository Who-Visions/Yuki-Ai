# Migrate to the latest Gemini models

This guide explains how to update your application to the latest Gemini version. This guide assumes your application already uses an older Gemini version. To learn how to start using Gemini in Vertex AI, see the Gemini API in Vertex AI quickstart.

This guide doesn't cover how to switch your application from the Vertex AI SDK to the current Google Gen AI SDK. For that information, see our Vertex AI SDK migration guide.

## What changes should I expect?
Updating most generative AI applications to the latest Gemini version requires few code or prompt changes. However, some applications may require prompt adjustments. It's hard to predict these changes without first testing your prompts with the new version. Thorough testing is recommended before fully migrating. For tips on creating effective prompts, see our prompt strategy guidance. Use our prompt health checklist to help find and fix prompt issues.

You only need to make major code changes for certain breaking changes or to use new Gemini capabilities.

## Which Gemini model should I migrate to?
The Gemini model you use depends on your application's needs. The following table compares the older Gemini 1.5 models with the latest Gemini models:

| Feature | 1.5 Pro | 1.5 Flash | 2.0 Flash | 2.0 Flash-Lite | 2.5 Pro | 2.5 Flash | 2.5 Flash-Lite | 3 Pro |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Launch stage** | Retired | Retired | Generally available | Generally available | Generally available | Generally available | Generally available | Preview |
| **Input modalities** | Text, Code, Images, Audio, Video | Text, Code, Images, Audio, Video | Text, Code, Images, Audio, Video | Text, Code, Images, Audio, Video | Text, Code, Images, Audio, Video | Text, Code, Images, Audio, Video | Text, Code, Images, Audio, Video | Text, Code, Images, Audio, Video, PDF |
| **Output modalities** | Text | Text | Text | Text | Text | Text | Text | Text |
| **Context window** | 2,097,152 | 1,048,576 | 1,048,576 | 1,048,576 | 1,048,576 | 1,048,576 | 1,048,576 | 1,048,576 |
| **Output context length** | 8,192 (default) | 8,192 (default) | 8,192 (default) | 8,192 (default) | 65,535 (default) | 65,535 (default) | 65,536 (default) | 65,536 |
| **Recommended SDK** | Vertex AI SDK | Vertex AI SDK | Gen AI SDK | Gen AI SDK | Gen AI SDK | Gen AI SDK | Gen AI SDK | Gen AI SDK |
| **Pricing units** | Character | Character | Token | Token | Token | Token | Token | Token |
| **Retirement date** | Sep 24, 2025 | Sep 24, 2025 | Feb 5, 2026 | Feb 25, 2026 | Jun 17, 2026 | Jun 17, 2026 | Jul 22, 2026 | |

*\* The Live API is available as a preview offering as part of gemini-live-2.5-flash and gemini-live-2.5-flash-preview-native-audio.*

## Before you begin migrating
Before you start the migration process, you should consider the following:
*   Information security (InfoSec), governance, and regulatory approvals
*   Location availability
*   Modality and tokenization-based pricing differences
*   Purchase or change Provisioned Throughput orders
*   Supervised fine-tuning
*   Regression testing

## How to migrate to the latest version
The following sections outline the steps to migrate to the latest Gemini version. For optimal results, complete these steps in order.

### 1. Document model evaluation and testing requirements
*   Prepare to repeat any relevant evaluations you performed when you first built your application, plus any evaluations performed since then.
*   If your current evaluations don't fully cover or measure all tasks your application performs, design and prepare more evaluations.
*   If your application involves RAG, tool use, complex agentic workflows, or prompt chains, make sure that your existing evaluation data allows for assessing each component independently.
*   If your application is critical or part of a larger user-facing real-time system, include online evaluation.

### 2. Make code upgrades and run tests
Upgrading your code requires three main changes:

1.  **Upgrade to the Google Gen AI SDK**: If your Gemini 1.x application uses the Vertex AI SDK, switch to the Gen AI SDK. Vertex AI SDK releases after June 2026 won't support Gemini.
2.  **Change your Gemini calls**: Update your prediction code to use one of the latest Gemini models. At a minimum, this means changing the model endpoint name.
3.  **Fix breaking code changes**:
    *   **Dynamic retrieval**: Switch to using Grounding with Google Search.
    *   **Content filters**: Note the default content filter settings.
    *   **Top-K token sampling parameter**: Models after `gemini-1.0-pro-vision` don't support changing the Top-K parameter.
    *   **Thinking**: Gemini 3 Pro and later models use the `thinking_level` parameter instead of `thinking_budget`.
    *   **Thought signatures**: For Gemini 3 Pro and later models, if a thought signature is expected in a turn but not provided, the model returns an error instead of a warning.
    *   **Media resolution and tokenization**: Gemini 3 Pro and later models use a variable sequence length for media tokenization instead of Pan and Scan, and have new default resolutions and token costs for images, PDFs, and video.
    *   **Usage metadata**: For Gemini 3 Pro and later models, PDF token counts in `usage_metadata` are reported under the IMAGE modality instead of DOCUMENT.
    *   **Image segmentation**: Image segmentation is not supported by Gemini 3 Pro and later models.
    *   **Multimodal function responses**: For Gemini 3 Pro and later models, you can include image and PDF data in function responses.
    *   **PDF processing**: For Gemini 3 Pro and later models, OCR is not used by default when processing scanned PDFs.

### 3. Run offline evaluations
Repeat the evaluations you performed when you first developed and launched your application. If your application uses fine-tuning, perform offline evaluation before re-tuning your model with the latest version of Gemini.

### 4. Assess evaluation results and tune your prompts and hyperparameters
If your offline evaluation shows your application performing less effectively, improve your application until its performance matches the older model. Do this by:
*   Iteratively refining your prompts to boost performance ("Hill Climbing").
*   If your application is affected by Dynamic Retrieval and Top-K breaking changes, experiment with adjusting your prompt and token sampling parameters.

### 5. Run load tests
If your application needs a certain minimum throughput, perform load testing to ensure the latest version of your application meets your throughput requirements.

### 6. (Optional) Run online evaluations
Move to online evaluation only if your offline evaluation shows high Gemini output quality and your application requires online evaluation.

### 7. Deploy to production
Once your evaluation shows that the latest Gemini model performs as well as or better than an older model, replace the existing application version with the new version.

## Improving model performance
As you migrate, apply these tips to achieve optimal performance from your chosen Gemini model:
*   **Temperature**: For Gemini 3 Pro and later models, Google strongly recommends keeping the temperature parameter at its default value of 1.0.
*   **Prompt Review**: Check your system instructions, prompts, and few-shot learning examples for any inconsistencies, contradictions, or irrelevant instructions and examples.
*   **Test a more powerful model**: For example, if you evaluated Gemini 2.0 Flash-Lite, try Gemini 2.0 Flash.
*   **Review automated evaluation results**: Ensure they match human judgment, especially results using a judge model.
*   **Fine-tune the model**.
*   **Examine evaluation outputs**: Look for patterns that show specific types of failures.
*   **Independent Evaluation**: Ensure you are evaluating different generative AI components independently.
*   **Token Sampling**: Experiment with adjusting token sampling parameters.

## Getting help
If you require assistance, Google Cloud offers support packages to meet your needs.

## What's next
*   See the list of frequently asked questions.
*   Migrate from the PaLM API to the Gemini API in Vertex AI.
