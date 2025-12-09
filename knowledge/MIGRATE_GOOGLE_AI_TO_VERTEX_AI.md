# Migrate from Google AI Studio to Vertex AI

As your Gemini API applications mature, you might find that you need a more expansive platform for building and deploying generative AI applications and solutions end-to-end. Vertex AI provides a comprehensive ecosystem of tools to enable developers to harness the power of generative AI, from the initial stages of app development to app deployment, app hosting, and managing complex data at scale.

With Vertex AI, you get access to a suite of Machine Learning Operations (MLOps) tools to streamline usage, deployment, and monitoring of AI models for efficiency and reliability. Additionally, integrations with databases, Development Operations (DevOps) tools, logging, monitoring, and IAM offer a comprehensive approach to managing the entire generative AI lifecycle.

## Differences between using the Gemini API on its own and Vertex AI

The following table summarizes the main differences between the Gemini API and Vertex AI to help you decide which option is right for your use case:

| Feature | Gemini API | Vertex AI |
| :--- | :--- | :--- |
| **Endpoint names** | `generativelanguage.googleapis.com` | `aiplatform.googleapis.com` |
| **Sign up** | Google Account | Google Cloud account (with terms agreement and billing) |
| **Authentication** | API key | Google Cloud service account |
| **User interface playground** | Google AI Studio | Vertex AI Studio |
| **API & SDK** | Server and mobile/web client SDKs<br>Server: Python, Node.js, Go, Dart, ABAP<br>Mobile/Web client (via Firebase AI Logic): Android (Kotlin/Java), Swift, Web, Flutter, and Unity | Server and mobile/web client SDKs<br>Server: Python, Node.js, Go, Java, ABAP<br>Mobile/Web client (via Firebase AI Logic): Android (Kotlin/Java), Swift, Web, Flutter, and Unity |
| **No-cost usage of API & SDK** | Yes, where applicable | $300 Google Cloud credit for new users |
| **Quota (requests per minute)** | Varies based on model and pricing plan (see detailed information) | Varies based on model and region (see detailed information) |
| **Enterprise support** | No | Yes |
| **Customer encryption key** | No | Yes |
| **Virtual private cloud** | No | Yes |
| **Data residency** | No | Yes |
| **Access transparency** | No | Yes |
| **Scalable infrastructure for application hosting** | No | Yes |
| **Databases and data storage** | No | Yes |
| **MLOps** | No | Full MLOps on Vertex AI (examples: model evaluation, Model Monitoring, Model Registry) |

## Migration steps

The following sections cover the steps required to migrate your Gemini API code to Vertex AI. These steps assume you have prompt data from Google AI Studio saved in Google Drive.

When migrating to Vertex AI:
*   You can use your existing Google Cloud project (the same one you used to generate your Gemini API key) or you can create a new Google Cloud project.
*   Supported regions might differ between the Gemini API and Vertex AI. See the list of supported regions for generative AI on Google Cloud.
*   Any models you created in Google AI Studio need to be retrained in Vertex AI.

### 1. Migrate your prompts to Vertex AI Studio
Your Google AI Studio prompt data is saved in a Google Drive folder. This section shows how to migrate your prompts to Vertex AI Studio.

1.  Open Google Drive.
2.  Navigate to the `AI_Studio` folder where the prompts are stored.
3.  Download your prompts from Google Drive to a local directory.
    *   **Note:** Prompts downloaded from Google Drive are in the text (`txt`) format. Before you upload them to Vertex AI Studio, change the file extensions from `.txt` to `.json` to convert them to JSON files.
4.  Open Vertex AI Studio in the Google Cloud console.
5.  In the Vertex AI menu, click **Recents > View all** to open the **Prompt management** menu.
6.  Click **Import prompt**.
7.  Next to the **Prompt file** field, click **Browse** and select a prompt from your local directory.
    *   To upload prompts in bulk, you must manually combine your prompts into a single JSON file.
8.  Click **Upload**.

### 2. Upload training data to Vertex AI Studio
To migrate your training data to Vertex AI, you need to upload your data to a Cloud Storage bucket. For more information, see Introduction to tuning.

### 3. Delete unused API Keys
If you no longer need to use your Gemini API key for the Gemini Developer API, then follow security best practices and delete it.

To delete an API key:
1.  Open the Google Cloud API Credentials page.
2.  Find the API key that you want to delete and click the **Actions** icon.
3.  Select **Delete API key**.
4.  In the Delete credential modal, select **Delete**.

Deleting an API key takes a few minutes to propagate. After propagation completes, any traffic using the deleted API key is rejected.

> **Important:** If you delete a key that's still used in production and need to recover it, see `gcloud beta services api-keys undelete`.

## What's next
Try a quickstart tutorial using Vertex AI Studio or the Vertex AI API.
