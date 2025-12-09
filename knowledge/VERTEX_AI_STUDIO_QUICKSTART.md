# Quickstart: Send text prompts to Gemini using Vertex AI Studio

You can use Vertex AI Studio to design, test, and manage prompts for Google's Gemini large language models (LLMs) and third-party models. Vertex AI Studio supports certain third-party models that are offered on Vertex AI as models as a service (MaaS), such as Anthropic Claude models and Meta's Llama models.

> **Note:** On your initial use for third-party models, Vertex AI prompts you to accept the third-party's terms and conditions. You must do this once for each third-party provider to start using their models.

In this quickstart, you:
*   Send these prompts to the Gemini API using samples from the generative AI prompt gallery, including the following:
    *   A summarization text prompt
    *   A code generation prompt
*   View the code used to generate the responses

## Before you begin prompting in Vertex AI Studio
This quickstart requires you to complete the following steps to set up a Google Cloud project and enable the Vertex AI API.

To get the permissions that you need to complete the tasks in this quickstart, ask your administrator to grant you the following IAM roles on your project:
*   To enable the Vertex AI API if it isn't already enabled: `serviceusage.serviceUsageAdmin`
*   To run prompts in Vertex AI Studio: `Vertex AI User` (`roles/aiplatform.user`)

1.  In the Google Cloud console, on the project selector page, select or create a Google Cloud project.
2.  Verify that billing is enabled for your Google Cloud project.
3.  Enable the Vertex AI API.

## Sample prompts in Vertex AI Studio
A prompt is a natural language request submitted to a language model that generates a response. Prompts can contain questions, instructions, contextual information, few-shot examples, and partial input for the model to complete. After the model receives a prompt, depending on the type of model used, it can generate text, embeddings, code, images, videos, music, and more.

The sample prompts in Vertex AI Studio prompt gallery are predesigned to help demonstrate model capabilities. Each prompt is preconfigured with specified model and parameter values so you can open the sample prompt and click Submit to generate a response.

## Test the Gemini flash model using a summarization text prompt
Send a summarization text prompt to the Gemini API in Vertex AI. A summarization task extracts the most important information from text. You can provide information in the prompt to help the model create a summary, or ask the model to create a summary on its own.

1.  Go to the **Prompt gallery** page from the Vertex AI section in the Google Cloud console.
2.  In the **Tasks** drop-down menu, select **Summarize**.
3.  Open the **Audio summarization** card.
    *   This sample prompt includes an audio file and requests a summary of the file contents in a bulleted list.
4.  Notice that in the settings panel, the model's default value is set to `Gemini-2.0-flash-001`. You can choose a different Gemini model by clicking **Switch model**.
5.  Click **Submit** to generate the summary.
6.  The output is displayed in the response.
7.  To view the Vertex AI API code used to generate the transcript summary, click **Build with code > Get code**.
8.  In the **Get code** panel, you can choose your preferred language to get the sample code for the prompt, or you can open the Python code in a Colab Enterprise notebook.

## Test the Gemini flash model using a code generation prompt
Send a code generation prompt to the Gemini API in Vertex AI. A code generation task generates code using a natural language description.

1.  Go to the **Prompt gallery** page from the Vertex AI section in the Google Cloud console.
2.  In the **Tasks** drop-down menu, select **Code**.
3.  Open the **Generate code from comments** card.
    *   This sample prompt includes a system instruction that tells the model how to respond and some incomplete Java methods.
4.  Notice that in the settings panel, the model's default value is set to `Gemini-2.0-flash-001`. You can choose a different Gemini model by clicking **Switch model**.
5.  To complete each method by generating code in the areas marked `<WRITE CODE HERE>`, click **Submit**.
6.  The output is displayed in the response.
7.  To view the Vertex AI API code used to generate the transcript summary, click **Build with code > Get code**.
8.  In the **Get code** panel, you can choose your preferred language to get the sample code for the prompt, or you can open the Python code in a Colab Enterprise notebook.

## Discover what's next with prompts
*   To learn more about the capabilities in Vertex AI Studio, see Vertex AI Studio capabilities.
*   See an introduction to prompt design.
*   Learn about designing multimodal prompts and chat prompts.
