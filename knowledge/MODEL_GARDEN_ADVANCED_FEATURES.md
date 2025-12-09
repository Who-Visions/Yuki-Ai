# Vertex AI Model Garden - Advanced Features

**Overview**

Model optimization has emerged as a crucial step, allowing customers to balance cost-effectiveness, throughput and latency performance. We believe that there is no one-size-fits-all approach to deliver optimal performance for every customer. Even with the same model, the variation can occur as user traffic patterns and requirements may vary for different customers. For example, for chat applications, minimizing latency is key to offer an interactive experience, whereas other applications like recommendations may require maximizing throughput.

This guide offers a suite of advanced optimization techniques that would help users to customize and optimize AI model performance tailored to your unique use cases and workloads.

This tutorial will cover the following topics using Meta-Llama models as examples. You can replace them with any supported models available from Vertex Model Garden.

1.  **Prefix Caching**
2.  **Speculative Decoding**

## Prefix Caching

Prefix caching reuses computations from previously generated text, eliminating redundant processing. It’s a popular technique to reduce Time-To-First-Token for requests with common prompt prefixes. Typical use cases: Ask different questions with the same long documents as context; Multi-turn chat conversations.

### Supported models

Prefix caching supports the following models:

| Serving solution | Model |
| :--- | :--- |
| **vLLM** | Text-only LLMs with decoder-only architecture, e.g. Llama 3.1 (8b, 70b), Llama 3.3 (70b) etc. |
| **Hex-LLM** | Llama 2 (7b, 13b), Llama 3 (8b), Llama 3.1 (8b, 70b), Llama 3.2 (1b, 3b), Llama Guard (1b, 8b), CodeLlama (7b, 13b), Gemma (2b, 7b), CodeGemma (2b, 7b), Mistral-7B (v0.2, v0.3), Mixtral-8x7B (v0.1) |

## Speculative Decoding

Serving large LLM could be slow, and speculative decoding is a very effective optimization technique to reduce generation Time-Per-Output-Token latency. The standard LLM would generate tokens one-by-one sequentially with autoregressive decoding. In contrast, with speculative decoding, we use a fast drafter to efficiently guess multiple tokens and then utilize the larger LLM to verify them in parallel.

## Costs

This tutorial uses billable components of Google Cloud:
*   Vertex AI
*   Cloud Storage

## Before you begin

### Request for quota

You may require the following quotas to be able to try out the examples:

*   **Custom model serving TPU v5e cores per region**
*   **Custom model serving Nvidia A100 80GB GPUs per region**

By default, the quota for TPU deployment Custom model serving TPU v5e cores per region is 4, which is sufficient for serving the Llama 3.1 8B model. The Llama 3.1 70B model requires 16 TPU v5e cores. TPU quota is only available in `us-west1`.

The quota for A100_80GB deployment Custom model serving Nvidia A100 80GB GPUs per region is 0. You need to request at least 4 for 70B model and 1 for 8B model.

## Implementation Examples

### Setup

```python
# Install and import the necessary packages
! pip install -q openai google-auth requests

! git clone https://github.com/GoogleCloudPlatform/vertex-ai-samples.git

import datetime
import importlib
import os
import uuid
from typing import Tuple

from google.cloud import aiplatform

common_util = importlib.import_module(
    "vertex-ai-samples.community-content.vertex_model_garden.model_oss.notebook_util.common_util"
)

models, endpoints = {}, {}

# Get the default cloud project id.
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

# Get the default region for launching jobs.
REGION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

# Enable the Vertex AI API and Compute Engine API
! gcloud services enable aiplatform.googleapis.com compute.googleapis.com

# Initialize Vertex AI API.
aiplatform.init(project=PROJECT_ID, location=REGION)
```

### Prefix Caching with Hex-LLM

Hex-LLM is a High-Efficiency Large Language Model (LLM) TPU serving solution built with XLA.

```python
# Deploy the model with enable_prefix_cache_hbm=True

MODEL_ID = "Meta-Llama-3.1-8B-Instruct"
TPU_DEPLOYMENT_REGION = "us-west1"
model_id = os.path.join(VERTEX_AI_MODEL_GARDEN_LLAMA_3_1, MODEL_ID)

# The pre-built serving docker images.
HEXLLM_DOCKER_URI = "us-docker.pkg.dev/vertex-ai-restricted/vertex-vision-model-garden-dockers/hex-llm-serve:20241210_2323_RC00"

machine_type = "ct5lp-hightpu-4t"
tpu_count = 4
tpu_topo = "1x4"

# Server parameters.
tensor_parallel_size = tpu_count
hbm_utilization_factor = 0.8
max_running_seqs = 256
max_model_len = 4096
enable_prefix_cache_hbm = True

# Deploy function (simplified)
# ... (See full code in original notebook for deploy_model_hexllm function)

models["hexllm_tpu"], endpoints["hexllm_tpu"] = deploy_model_hexllm(
    model_name=common_util.get_job_name_with_datetime(prefix=MODEL_ID),
    model_id=model_id,
    service_account=SERVICE_ACCOUNT,
    # ... other args
    enable_prefix_cache_hbm=enable_prefix_cache_hbm,
)
```

### Prefix Caching with vLLM

Caching in GPU Memory and VM Host Memory.

```python
# Deploy the model to vLLM with GPU memory cache and host memory cache enabled

base_model_name = "Meta-Llama-3.1-8B-Instruct"
VLLM_DOCKER_URI = "us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20250116_0916_RC00"

enable_prefix_cache = True
host_prefix_kv_cache_utilization_target = 0.75
host_prefix_kv_cache_min_len = 1024

# Deploy function (simplified)
# ... (See full code in original notebook for deploy_model_vllm function)

models["vllm_gpu"], endpoints["vllm_gpu"] = deploy_model_vllm(
    model_name=common_util.get_job_name_with_datetime(prefix="llama3_1-serve"),
    # ... other args
    enable_prefix_cache=enable_prefix_cache,
    host_prefix_kv_cache_utilization_target=host_prefix_kv_cache_utilization_target,
    host_prefix_kv_cache_min_len=host_prefix_kv_cache_min_len,
)
```

### Speculative Decoding with vLLM

Speculative decoding reduces Time-per-Output-Token (TPOT) by using a drafter model.

```python
# Deploy the model to vLLM with Speculative Decoding

target_model_name = "Meta-Llama-3.1-8B-Instruct"
draft_model_name = "Llama-3.2-1B-Instruct"
speculative_token_count = 3
spec_method = "draft_model"

# Deploy function (simplified)
# ... (See full code in original notebook for deploy_model_vllm_speculative_decoding function)

(
    models["vllm_gpu_target"],
    draft_model,
    endpoints["vllm_gpu_spec"],
) = deploy_model_vllm_speculative_decoding(
    model_name=common_util.get_job_name_with_datetime(prefix="llama-spec-decoding-target"),
    # ... other args
    enable_speculative_decoding=True,
    speculation_method=spec_method,
    speculative_token_count=speculative_token_count,
    draft_model_id=draft_model_id,
    draft_model_name=common_util.get_job_name_with_datetime(prefix="llama-spec-decoding-draft"),
)
```

## Best practices

*   **Prefix Caching:**
    *   Put static contents at the beginning of the prompts and dynamic contents at the end.
    *   Try to warm up cache first before running batch queries in order to leverage caching.
    *   Monitor metrics (e.g. cache hit rates, latency, and the percentage of tokens cached).
*   **Speculative Decoding:**
    *   For 70B models, we recommend having at least 4 accelerators.
    *   The draft model will consume some of the HBM.
    *   TTFT will increase slightly due to the extra prefill for the draft model.
