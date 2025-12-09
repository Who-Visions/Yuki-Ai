# Use models in Model Garden

Discover, test, tune, and deploy models by using Model Garden in the Google Cloud console. You can also deploy Model Garden models by using the Google Cloud CLI.

## Send test prompts
1.  In the Google Cloud console, go to the **Model Garden** page.
2.  Find a supported model that you want to test and click **View details**.
3.  Click **Open prompt design**.
    *   You're taken to the **Prompt design** page.
4.  In **Prompt**, enter the prompt that you want to test.
5.  **Optional**: Configure the model parameters.
6.  Click **Submit**.

## Tune a model
1.  In the Google Cloud console, go to the **Model Garden** page.
2.  In **Search models**, enter `BERT` or `T5-FLAN`, then click the magnifying glass to search.
3.  Click **View details** on the T5-FLAN or the BERT model card.
4.  Click **Open fine-tuning pipeline**.
    *   You're taken to the **Vertex AI pipelines** page.
5.  To start tuning, click **Create run**.

## Tune in a notebook
The model cards for most open source foundation models and fine-tunable models support tuning in a notebook.

1.  In the Google Cloud console, go to the **Model Garden** page.
2.  Find a supported model that you want to tune and go to its model card.
3.  Click **Open notebook**.

## Deploy an open model
You can deploy a model by using its model card in the Google Cloud console or programmatically.

### Python Example

**List the models that you can deploy and record the model ID to deploy.**

```python
import vertexai
from vertexai import model_garden

# TODO(developer): Update and un-comment below lines
# PROJECT_ID = "your-project-id"
vertexai.init(project=PROJECT_ID, location="us-central1")

# List deployable models, optionally list Hugging Face models only or filter by model name.
deployable_models = model_garden.list_deployable_models(list_hf_models=False, model_filter="gemma")
print(deployable_models)
# Example response:
# ['google/gemma2@gemma-2-27b','google/gemma2@gemma-2-27b-it', ...]
```

**View the deployment specifications for a model by using the model ID from the previous step.**

```python
import vertexai
from vertexai import model_garden

# TODO(developer): Update and un-comment below lines
# PROJECT_ID = "your-project-id"
# model = "google/gemma3@gemma-3-1b-it"
vertexai.init(project=PROJECT_ID, location="us-central1")

# For Hugging Face modelsm the format is the Hugging Face model name, as in
# "meta-llama/Llama-3.3-70B-Instruct".
# Go to https://console.cloud.google.com/vertex-ai/model-garden to find all deployable
# model names.

model = model_garden.OpenModel(model)
deploy_options = model.list_deploy_options()
print(deploy_options)
# Example response:
# [
#   dedicated_resources {
#     machine_spec {
#       machine_type: "g2-standard-12"
#       accelerator_type: NVIDIA_L4
#       accelerator_count: 1
#     }
#   }
#   container_spec {
#     ...
#   }
#   ...
# ]
```

**Deploy a model to an endpoint.**

```python
import vertexai
from vertexai import model_garden

# TODO(developer): Update and un-comment below lines
# PROJECT_ID = "your-project-id"
vertexai.init(project=PROJECT_ID, location="us-central1")

open_model = model_garden.OpenModel("google/gemma3@gemma-3-12b-it")
endpoint = open_model.deploy(
    machine_type="g2-standard-48",
    accelerator_type="NVIDIA_L4",
    accelerator_count=4,
    accept_eula=True,
)

# Optional. Run predictions on the deployed endoint.
# endpoint.predict(instances=[{"prompt": "What is Generative AI?"}])
```

## Deploy a partner model and make prediction requests
In the Google Cloud console, go to the Model Garden page and use the **Model collections** filter to view the **Self-deploy partner models**. Choose from the list of self-deploy partner models, and purchase the model by clicking **Enable**.

You must deploy on the partner's required machine types, as described in the "Recommended hardware configuration" section on their Model Garden model card. When deployed, the model serving resources are located in a secure Google-managed project.

### 1-click model deployment

**View the deployment specifications for a model.**

```python
import vertexai
from vertexai import model_garden

vertexai.init(project=PROJECT_ID, location="us-central1")

model = model_garden.PartnerModel(model)
deploy_options = model.list_deploy_options()
print(deploy_options)
```

**Deploy a model with 1-click deployment.**

```python
from vertexai import model_garden

# Deploy model
model = model_garden.PartnerModel(f"{PUBLISHER}/{MODEL}@{VERSION}")

endpoint = model.deploy(
    machine_type=MACHINE_TYPE,
    accelerator_type=ACCELERATOR_TYPE,
    accelerator_count=ACCELERATOR_COUNT,
    min_replica_count=1,
    max_replica_count=1,
)
```

### Multi-step deployment
You can also upload a partner model, create an endpoint, and manually deploy the model.

```python
from google.cloud import aiplatform

aiplatform.init(project=PROJECT_ID, location=LOCATION)

# Upload a model
model = aiplatform.Model.upload(
    display_name="DISPLAY_NAME_MODEL",
    model_garden_source_model_name = f"publishers/PUBLISHER_NAME/models/PUBLISHER_MODEL_NAME",
)

# Create endpoint
my_endpoint = aiplatform.Endpoint.create(display_name="DISPLAY_NAME_ENDPOINT")

# Deploy model
MACHINE_TYPE = "MACHINE_TYPE"  # @param {type: "string"}
ACCELERATOR_TYPE = "ACCELERATOR_TYPE" # @param {type: "string"}
ACCELERATOR_COUNT = ACCELERATOR_COUNT # @param {type: "number"}

model.deploy(
    endpoint=my_endpoint,
    deployed_model_display_name="DISPLAY_NAME_DEPLOYED_MODEL",
    traffic_split={"0": 100},
    machine_type=MACHINE_TYPE,
    accelerator_type=ACCELERATOR_TYPE,
    accelerator_count=ACCELERATOR_COUNT,
    min_replica_count=1,
    max_replica_count=1,
)

# Unary call for predictions
PAYLOAD = {
    REQUEST_PAYLOAD
}

request = json.dumps(PAYLOAD)

response = my_endpoint.raw_predict(
    body = request,
    headers = {'Content-Type':'application/json'}
)

print(response)

# Streaming call for predictions
PAYLOAD = {
    REQUEST_PAYLOAD
}

request = json.dumps(PAYLOAD)

for stream_response in my_endpoint.stream_raw_predict(
    body = request,
    headers = {'Content-Type':'application/json'}
):
    print(stream_response)
```

## Deploy a model to a private endpoint
You can deploy models from Model Garden to a Private Service Connect (PSC) endpoint to create a secure and private connection to your model.

1.  In the Google Cloud console, go to the **Model Garden** page.
2.  Find a model to deploy and click its model card.
3.  Click **Deploy model**.
4.  Select **edit** setting that enables further deployment options including private access.
5.  Configure your deployment settings (location, machine type, reservation, availability policies).
6.  Configure endpoint Access for private networking.
    *   Select **Private (Private Service Connect)**
    *   Select **Project IDs**.
7.  Click **Deploy**.

**Obtain the Endpoint ID and Private Service Attachment URI:**

```bash
gcloud ai endpoints describe ENDPOINT_ID --region=REGION  | grep -i serviceAttachment:
```

## View or manage an endpoint
To view and manage your endpoint, go to the **Vertex AI Online prediction** page.

## Undeploy models and delete resources

### Undeploy models

```python
from google.cloud import aiplatform

aiplatform.init(project=PROJECT_ID, location=LOCATION)

# To find out which endpoints are available, un-comment the line below:
# endpoints = aiplatform.Endpoint.list()

endpoint = aiplatform.Endpoint(ENDPOINT_ID)
endpoint.undeploy_all()
```

### Delete endpoints

```python
from google.cloud import aiplatform

aiplatform.init(project=PROJECT_ID, location=LOCATION)

# To find out which endpoints are available, un-comment the line below:
# endpoints = aiplatform.Endpoint.list()

endpoint = aiplatform.Endpoint(ENDPOINT_ID)
endpoint.delete()
```

### Delete models

```python
from google.cloud import aiplatform

aiplatform.init(project=PROJECT_ID, location=LOCATION)

# To find out which models are available in Model Registry, un-comment the line below:
# models = aiplatform.Model.list()

model = aiplatform.Model(MODEL_ID)
model.delete()
```

## View code samples
Most of the model cards for task-specific solutions models contain code samples that you can copy and test.

1.  In the Google Cloud console, go to the **Model Garden** page.
2.  Find a supported model that you want to view code samples for and click the **Documentation** tab.

## Create a vision app
The model cards for applicable computer vision models support creating a vision application.

1.  In the Google Cloud console, go to the **Model Garden** page.
2.  Find a vision model in the **Task specific solutions** section that you want to use to create a vision application and click **View details**.
3.  Click **Build app**.
    *   You're taken to **Vertex AI Vision**.
4.  In **Application name**, enter a name for your application and click **Continue**.
5.  Select a billing plan and click **Create**.
