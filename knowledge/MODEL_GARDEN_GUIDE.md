# Overview of Model Garden

Model Garden is an AI/ML model library that helps you discover, test, customize, and deploy models and assets from Google and Google partners.

## Advantages of Model Garden
When you're working with AI models, Model Garden provides the following advantages:
*   Available models are all grouped in a single location
*   Model Garden provides a consistent deployment pattern for different types of models
*   Model Garden provides built-in integration with other parts of Vertex AI such as model tuning, evaluation, and serving
*   Serving generative AI models can be difficult—Vertex AI handles model deployment and serving for you

## Explore models
To view the list of available Vertex AI and open source foundation, tunable, and task-specific models, go to the Model Garden page in the Google Cloud console.

The model categories available in Model Garden are:

| Category | Description |
| :--- | :--- |
| **Foundation models** | Pretrained multitask large models that can be tuned or customized for specific tasks using Vertex AI Studio, Vertex AI API, and the Vertex AI SDK for Python. |
| **Fine-tunable models** | Models that you can fine-tune using a custom notebook or pipeline. |
| **Task-specific solutions** | Most of these prebuilt models are ready to use. Many can be customized using your own data. |

To filter models in the filter pane, specify the following:
*   **Tasks**: Click the task that you want the model to perform.
*   **Model collections**: Click to choose models that are managed by Google, partners, or you.
*   **Providers**: Click the provider of the model.
*   **Features**: Click the features that you want in the model.

To learn more about each model, click its model card.

For a list of models available in Model Garden, see Models available in Model Garden.

## Model security scanning
Google does thorough testing and benchmarking on the serving and tuning containers that we provide. Active vulnerability scanning is also applied to container artifacts.

Third-party models from featured partners undergo model checkpoint scans to ensure authenticity. Third-party models from HuggingFace Hub are scanned directly by HuggingFace and their third-party scanner for malware, pickle files, Keras Lambda layers, and secrets. Models deemed unsafe from these scans are flagged by HuggingFace and blocked from deployment in Model Garden. Models deemed suspicious or those that have the ability to potentially execute remote code are indicated in Model Garden but can still be deployed. We recommend you perform a thorough review of any suspicious model before deploying it within Model Garden.

## Pricing
For the open source models in Model Garden, you are charged for use of following on Vertex AI:
*   **Model tuning**: You are charged for the compute resources used at the same rate as custom training. See custom training pricing.
*   **Model deployment**: You are charged for the compute resources used to deploy the model to an endpoint. See predictions pricing.
*   **Colab Enterprise**: See Colab Enterprise pricing.

## Control access to specific models
You can set a Model Garden organization policy at the organization, folder, or project level to control access to specific models in Model Garden. For example, you can allow access to specific models that you've vetted and deny access to all others.

## Learn more about Model Garden
For more information about the deployment options and customizations that you can do with models in Model Garden, view the resources in the following sections, which include links to tutorials, references, notebooks, and YouTube videos.

### Deploy and serve
Learn more about customizing deployments and advance serving features.
*   Deploy and serve open source model using Python SDK, CLI, REST API, or console
*   Developer blog: Introducing the new Vertex AI Model Garden CLI and SDK
*   Deploy open models by using the SDK tutorial notebook
*   Get started with Vertex AI Model Garden SDK notebook
*   Deploying and fine-tuning Gemma 3 in Model Garden YouTube video
*   Deploying Gemma and making predictions
*   Serve open models with a Hex-LLM container on Cloud TPUs
*   Deploying Llama models by using Hex-LLM tutorial notebook
*   Use prefix caching and speculative decoding with Hex-LLM or vLLM tutorial notebook
*   Use vLLM to serve text-only and multimodel language models on Cloud GPUs
    *   Text-only models tutorial notebook
    *   Multimodal models tutorial notebook
*   Use xDiT GPU serving container for image and video generation
*   Serving Gemma 2 with multiple LoRA adapters with HuggingFace DLC for PyTorch inference tutorial on Medium
*   Use custom handles to serve PaliGemma for image captioning with HuggingFace DLC for PyTorch inference tutorial on LinkedIn
*   Deploy and serve a model that uses Spot VMs or a Compute Engine reservation tutorial notebook
*   Deploy and serve a HuggingFace model

### Container compliance
Model Garden offers the following FedRAMP high compliant containers for model serving.

| Container name | Supported tasks | Container image version | Notebook example |
| :--- | :--- | :--- | :--- |
| **HuggingFace Text Embeddings Inference (TEI)** | `text2embeddings` | `us-docker.pkg.dev/deeplearning-platform-release/vertex-model-garden/hf-tei.cu125.0-1.ubuntu2204.py310:model-garden.hf-tei-0-1-release_20251126.01_p0` | Hugging Face Text Embeddings Inference Deployment |

### Tuning
Learn more about tuning models to tailor responses for specific use cases.
*   Workbench fine-tuning tutorial notebook
*   Fine-tuning and evaluation tutorial notebook
*   Deploying and fine-tuning Gemma 3 in Model Garden YouTube video

### Evaluation
Learn more about assessing model responses with Vertex AI
*   Evaluate Gemma 2 with the generative AI evaluation service YouTube video

### Additional resources
*   Model and user journey-specific Model Garden notebooks
*   Vertex AI open model serving, fine-tuning and evaluation notebooks
