# Quickstart: Generate and verify an image's watermark using Imagen text-to-image (Console)

> **API reference overview**: To view an overview of the API options for image generation and editing, see the imagegeneration model API reference.

Learn how to use Imagen on Vertex AI's text-to-image generation feature and verify a digital watermark (SynthID) on a generated image. This quickstart shows you how to use Imagen image generation in the Google Cloud console.

Imagen on Vertex AI pricing is based on the feature you use. For more information, see Pricing.

## Before you begin
1.  In the Google Cloud console, on the project selector page, select or create a Google Cloud project.
    *   **Note:** If you don't plan to keep the resources that you create in this procedure, create a project instead of selecting an existing project. After you finish these steps, you can delete the project, removing all resources associated with the project.
2.  Verify that billing is enabled for your Google Cloud project.
3.  Enable the Vertex AI API.
4.  Make sure that you have the following role or roles on the project: **Vertex AI User**

## Generate images and save a local copy
Send the text-to-image generation request using the Google Cloud console.

1.  In the Google Cloud console, go to the **Vertex AI > Media Studio** page.
2.  In the **Prompt** (Write your prompt here) field, enter the following prompt:
    `portrait of a french bulldog at the beach, 85mm f/2.8`
3.  If not selected, in the **Model options** box in the **Parameters** panel, select **Imagen 3**.
4.  If not selected, in the **Aspect ratio** section in the **Parameters** panel, select **1:1**.
5.  In the **Number of results** section, change the **Number of results** to **2**.
6.  Click **Generate**.
7.  To save a local copy of an image, click one of the images.
8.  In the **Image details** window that opens, click **Export**.
9.  In the **Export image** dialog box, click **Export**.

## Verify an image's digital watermark
After you generate watermarked images, you can verify the digital watermark of the novel images.

1.  Create generated images and save a local copy as you did in the previous step.
2.  In the **Image detail** window, click **Export**.
3.  In the lower panel, click **Verify**.
4.  Click **Upload image**.
5.  Select a locally-saved generated image.

Congratulations! You've just used the Imagen text-to-image generation feature to create novel images and verify the digital watermark of one of the images.

## Clean up
To avoid incurring charges to your Google Cloud account for the resources used on this page, follow these steps.

1.  Delete the project

## What's next
*   Learn about all image generative AI features in the Imagen on Vertex AI overview.
*   Read usage guidelines for Imagen on Vertex AI.
*   Explore more pretrained models in Model Garden.
*   Learn about responsible AI best practices and Vertex AI's safety filters.
