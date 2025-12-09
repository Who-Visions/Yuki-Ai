# Test model capabilities in Model Garden

Model Garden provides several options for you to quickly view and test model capabilities. For supported models, you can try demo playgrounds or launch demo applications called Model Garden Spaces that you can share with others to showcase a model's capabilities.

*   **Playgrounds** are powered by predeployed Vertex AI online prediction endpoints and don't incur charges. When you open the model card for a supported model, you can use the **Try out** panel to quickly test the model's capabilities by sending a text prompt. You can also set some of the most common parameters such as temperature and number of output tokens. The playground is limited to text input and output only.
*   When you launch **Spaces**, you have a working web application that's ready to use with far less manual effort than deploying a model and building an app to use the model's endpoint. Model Garden deploys your selected model in Vertex AI and deploys the sample app on a Cloud Run instance that uses the deployed model's endpoint. The application can also use existing endpoints, or a MaaS endpoint.

To launch a model, open the model card for the supported model, and in the **Try out Spaces** panel, click a Space to launch one. You are charged for the machines that are used for the deployment and for the Cloud Run instance that's hosting the app.

## Before you begin
1.  In the Google Cloud console, on the project selector page, select or create a Google Cloud project.
    *   **Note:** If you don't plan to keep the resources that you create in this procedure, create a project instead of selecting an existing project. After you finish these steps, you can delete the project, removing all resources associated with the project.
2.  Verify that billing is enabled for your Google Cloud project.
3.  Enable the Vertex AI API.

## Try a Playground
1.  In the Google Cloud console, go to a supported model's model card, such as the Gemma 2 model card.
2.  In the **Try out** panel:
    *   For **Region**, accept the default or choose your region.
    *   For **Endpoint**, select **Demo playground**.
    *   In the **Prompt** box, enter `Why is the sky blue?`.
    *   Expand the **Advanced options** section and view the default parameters.
3.  Click **Submit**. The output appears below the Submit button.

## Try Spaces
You can launch Spaces with models such as Gemini, Gemma, Llama, and Stable Diffusion. The following list is an example of what's supported:
*   BLIP image captioning
*   BLIP VQA
*   BLIP2
*   Flux
*   Gemma 2
*   Gemma 3
*   Gemini 2.5 Flash
*   Gemini 2.5 Pro
*   Instant ID
*   Llama 3.2
*   Llama 3.3
*   Llama 4
*   Llama 3.2 90B
*   Llama 4 Maverick 17B-128E
*   LLaVA 1.5 & LLaVA-NeXT
*   Mistral Self-host (7B & Nemo)
*   PaliGemma 1 & 2
*   Phi-3
*   Phi-4
*   Qwen2
*   Stable Diffusion Inpainting
*   Stable Diffusion v2.1
*   Stable Diffusion XL LCM
*   Stable Diffusion XL Lightning
*   Stable Diffusion XL
*   DeepSeek R1 (0528)

### IAM permissions
In addition to the existing permissions to use Vertex AI, you must have the following permissions to launch Spaces:

| Action | Required permissions | Purpose |
| :--- | :--- | :--- |
| **Enable additional APIs** | `serviceusage.services.enable` | Enable the following APIs:<br>• Cloud Run Admin API (`run.googleapis.com`)<br>• Artifact Registry API (`artifactregistry.googleapis.com`)<br>• Cloud Build API (`cloudbuild.googleapis.com`)<br>• Cloud Logging API (`logging.googleapis.com`) |
| **Grant permissions to service accounts** | `resourcemanager.projects.setIamPolicy` | Grant the Compute Engine default service account the following roles:<br>• Vertex AI Service Agent (`roles/aiplatform.serviceAgent`)<br>• Cloud Build Service Account (`roles/cloudbuild.builds.builder`) |
| **Deploy specific permissions** | `storage.buckets.create`<br>`run.services.create`<br>`artifactregistry.repositories.create`<br>`run.services.setIamPolicy` | During deployment, a set of source codes will be uploaded to Cloud Storage and then be deployed to Cloud Run with a new service created. The `artifactregistry.repositories.create` is required to create a repository for the container image. The `run.services.setIamPolicy` is required to make the service publicly accessible. |

If you are the owner of your project, you don't need to take additional actions but follow the guides in the Vertex AI Studio. If you are not the owner of your project, ask your project administrator to perform the first two actions, and then grant you the **Editor** (`roles/editor`) and the **Cloud Run Admin** (`roles/run.admin`) roles.

### Launch Spaces
Launch Spaces to test and experiment with a model from a sample Gradio application.

1.  In the Google Cloud console, go to **Model Garden** to view a model's model card.
2.  Select the model to use. Supported models have a **Try out Spaces** panel, such as the Gemma 3 model card.
3.  Click **Run** to launch a Space.
    *   You can choose to **Require authentication** (via Identity Aware Proxy) or **Allow public access**.
    *   **Important:** When using the app, don't include sensitive or personally identifiable information in your prompts.
4.  Click **Create new service** to start the deployment. You can monitor the deployment status from the model card.
5.  After the Spaces status changes to **Ready**, click it to view details about the deployment.
    *   For basic protection, the web application requires a secret key that must be appended to the URL when submitting prompts. This secret key is provided in the **Secret key** field.
6.  Click **Open** to start using the app. You can send prompts to the model and view its responses from within the app.
    *   You can share the URL so that others can try the app too.
7.  To close access to the app, click **Edit** in the **Access control** field.
8.  In the **Security** tab for your Cloud Run application, select **Require authentication** and then click **Save**. The application is no longer available through the URL. Visits to the URL result in a 403 error (forbidden).

## Clean up
To avoid incurring charges to your Google Cloud account for the resources used on this page, follow these steps.

### Delete Spaces
To clean up Spaces, you must delete both the model's resources and the sample application's resources on Cloud Run.

#### Delete model resources
From within the Gradio app, you can delete model endpoints to clean up Vertex AI resources. Then, you need to delete the Cloud Run service to stop and delete the Gradio app.

To manually delete Vertex AI resources, see Undeploy models and delete resources.

#### Delete Cloud Run service
Delete resources related to a service, including all revision of the service. Deleting a service doesn't include items like container images from Artifact Registry.

1.  In the Google Cloud console, view the list of Cloud Run services.
2.  Locate the service to delete, and then select it.
3.  Click **Delete**. This deletes all revisions of the service.

### Delete the project
The easiest way to eliminate billing is to delete the project that you created for the tutorial.

1.  In the Google Cloud console, go to the **Manage resources** page.
2.  In the project list, select the project that you want to delete, and then click **Delete**.
3.  In the dialog, type the project ID, and then click **Shut down** to delete the project.

## What's next
*   See an overview of Model Garden.
