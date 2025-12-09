# Manage sessions using Google Cloud console or API calls

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

This section describes how to use Vertex AI Agent Engine Sessions to manage sessions using the Google Cloud console or direct API calls.

## Create a Vertex AI Agent Engine instance

```python
import vertexai

client = vertexai.Client(
  project="PROJECT_ID",
  location="LOCATION"
)
# If you don't have an Agent Engine instance already, create an instance.
agent_engine = client.agent_engines.create()
```

## List sessions

**REST:**

`GET https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ENGINE_ID/sessions`

```bash
curl -X GET \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     "https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ENGINE_ID/sessions"
```

## Create a session

**REST:**

`POST https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ENGINE_ID/sessions`

Request JSON body:
```json
{
  "userId": USER_ID
}
```

## Get a session

**REST:**

`GET https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ENGINE_ID/sessions/SESSION_ID`

## Delete a session

**REST:**

`DELETE https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ENGINE_ID/sessions/SESSION_ID`

## List events in a session

**REST:**

`GET https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ENGINE_ID/sessions/SESSION_ID/events`

## Append an event to a session

**REST:**

`POST https://LOCATION-aiplatform.googleapis.com/v1beta1/projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ENGINE_ID/sessions/SESSION_ID:appendEvent`

Request JSON body:
```json
{
  "author": AUTHOR,
  "invocationId": INVOCATION_ID,
  "timestamp": TIMESTAMP,
}
```

## Clean up

```python
agent_engine.delete(force=True)
```
