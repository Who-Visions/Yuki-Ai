# OpenAI compatibility

Gemini models are accessible using the OpenAI libraries (Python and TypeScript / Javascript) along with the REST API. Only Google Cloud Auth is supported using the OpenAI library in Vertex AI. If you aren't already using the OpenAI libraries, we recommend that you call the Gemini API directly.

## Python

```python
import openai
from google.auth import default
import google.auth.transport.requests

# TODO(developer): Update and un-comment below lines
# project_id = "PROJECT_ID"
# location = "global"

# Programmatically get an access token
credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

# OpenAI Client
client = openai.OpenAI(
  base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
  api_key=credentials.token
)

response = client.chat.completions.create(
  model="google/gemini-2.0-flash-001",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain to me how AI works"}
  ]
)

print(response.choices[0].message)
```

### What changed?

*   `api_key=credentials.token`: To use Google Cloud authentication, get a Google Cloud auth token using the sample code.
*   `base_url`: This tells the OpenAI library to send requests to Google Cloud instead of the default URL.
*   `model="google/gemini-2.0-flash-001"`: Choose a compatible Gemini model out of the models that Vertex hosts.

## Thinking
Gemini 2.5 models are trained to think through complex problems, leading to significantly improved reasoning. The Gemini API comes with a "thinking budget" parameter which gives fine-grained control over how much the model will think.

Unlike the Gemini API, the OpenAI API offers three levels of thinking control: "low", "medium", and "high", which are mapped behind the scenes to 1K, 8K, and 24K thinking token budgets.

Not specifying a reasoning effort at all is equivalent to not specifying a thinking budget.

For more direct control of thinking budgets and other thinking-related configs from the OpenAI-compatible API, utilize `extra_body.google.thinking_config`.

### Python

```python
import openai
from google.auth import default
import google.auth.transport.requests

# TODO(developer): Update and un-comment below lines
# project_id = "PROJECT_ID"
# location = "global"

# # Programmatically get an access token
credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

# OpenAI Client
client = openai.OpenAI(
  base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
  api_key=credentials.token
)

response = client.chat.completions.create(
  model="google/gemini-2.5-flash",
  reasoning_effort="low",
  messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {
          "role": "user",
          "content": "Explain to me how AI works"
      }
  ]
)
print(response.choices[0].message)
```

## Streaming
The Gemini API supports streaming responses.

### Python

```python
import openai
from google.auth import default
import google.auth.transport.requests

# TODO(developer): Update and un-comment below lines
# project_id = "PROJECT_ID"
# location = "global"

credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

client = openai.OpenAI(
  base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
  api_key=credentials.token
)
response = client.chat.completions.create(
  model="google/gemini-2.0-flash",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  stream=True
)

for chunk in response:
  print(chunk.choices[0].delta)
```

## Function calling
Function calling makes it easier to get structured data outputs from generative models and is supported in the Gemini API.

### Python

```python
import openai
from google.auth import default
import google.auth.transport.requests

# TODO(developer): Update and un-comment below lines
# project_id = "PROJECT_ID"
# location = "global"

credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

client = openai.OpenAI(
  base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
  api_key=credentials.token
)

tools = [
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get the weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. Chicago, IL",
          },
          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
      },
    }
  }
]

messages = [{"role": "user", "content": "What's the weather like in Chicago today?"}]
response = client.chat.completions.create(
  model="google/gemini-2.0-flash",
  messages=messages,
  tools=tools,
  tool_choice="auto"
)

print(response)
```

## Image understanding
Gemini models are natively multimodal and provide best in class performance on many common vision tasks.

### Python

```python
from google.auth import default
import google.auth.transport.requests

import base64
from openai import OpenAI

# TODO(developer): Update and un-comment below lines
# project_id = "PROJECT_ID"
# location = "global"

# Programmatically get an access token
credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

# OpenAI Client
client = openai.OpenAI(
  base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
  api_key=credentials.token,
)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
# base64_image = encode_image("Path/to/image.jpeg")

response = client.chat.completions.create(
  model="google/gemini-2.0-flash",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is in this image?",
        },
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
)

print(response.choices[0])
```

## Generate an image

### Python

```python
from google.auth import default
import google.auth.transport.requests

import base64
from openai import OpenAI

# TODO(developer): Update and un-comment below lines
# project_id = "PROJECT_ID"
# location = "global"

# Programmatically get an access token
credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

# OpenAI Client
client = openai.OpenAI(
  base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
  api_key=credentials.token,
)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
base64_image = encode_image("/content/wayfairsofa.jpg")

response = client.chat.completions.create(
  model="google/gemini-2.0-flash",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is in this image?",
        },
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
)

print(response.choices[0])
```

## Audio understanding
Analyze audio input:

### Python

```python
from google.auth import default
import google.auth.transport.requests

import base64
from openai import OpenAI

# TODO(developer): Update and un-comment below lines
# project_id = "PROJECT_ID"
# location = "global"

# Programmatically get an access token
credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

# OpenAI Client
client = openai.OpenAI(
  base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
  api_key=credentials.token,
)

with open("/path/to/your/audio/file.wav", "rb") as audio_file:
base64_audio = base64.b64encode(audio_file.read()).decode('utf-8')

response = client.chat.completions.create(
  model="gemini-2.0-flash",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Transcribe this audio",
        },
        {
              "type": "input_audio",
              "input_audio": {
                "data": base64_audio,
                "format": "wav"
          }
        }
      ],
    }
  ],
)

print(response.choices[0].message.content)
```

## Structured output
Gemini models can output JSON objects in any structure you define.

### Python

```python
from google.auth import default
import google.auth.transport.requests

from pydantic import BaseModel
from openai import OpenAI

# TODO(developer): Update and un-comment below lines
# project_id = "PROJECT_ID"
# location = "global"

# Programmatically get an access token
credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

# OpenAI Client
client = openai.OpenAI(
  base_url=f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/openapi",
  api_key=credentials.token,
)

class CalendarEvent(BaseModel):
  name: str
  date: str
  participants: list[str]

completion = client.beta.chat.completions.parse(
  model="google/gemini-2.0-flash",
  messages=[
      {"role": "system", "content": "Extract the event information."},
      {"role": "user", "content": "John and Susan are going to an AI conference on Friday."},
  ],
  response_format=CalendarEvent,
)

print(completion.choices[0].message.parsed)
```

## Current limitations
*   Access tokens live for 1 hour by default. After expiration, they must be refreshed. See this code example for more information.
*   Support for the OpenAI libraries is still in preview while we extend feature support. For help any questions or issues, post in the Google Cloud Community.

## What's next
*   Unlock Gemini's potential using the Google Gen AI Libraries.
*   See more examples using the Chat Completions API with the OpenAI-compatible syntax.
*   See which Gemini models and parameters are supported in the Overview page.
