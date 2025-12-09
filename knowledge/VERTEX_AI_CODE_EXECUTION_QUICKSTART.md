# Code Execution quickstart

> **Preview**
>
> This feature is subject to the "Pre-GA Offerings Terms" in the General Service Terms section of the Service Specific Terms. Pre-GA features are available "as is" and might have limited support. For more information, see the launch stage descriptions.

This page demonstrates how to make direct API calls to Vertex AI Agent Engine Code Execution to run untrusted code in an isolated sandbox environment.

## Create an Agent Engine instance

```python
import vertexai

client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

agent_engine = client.agent_engines.create()
agent_engine_name = agent_engine.api_resource.name
```

## Create a sandbox

```python
operation = client.agent_engines.sandboxes.create(
    spec={"code_execution_environment": {}},
    name=agent_engine_name,
    config=types.CreateAgentEngineSandboxConfig(display_name=SANDBOX_DISPLAY_NAME)
)

sandbox_name = operation.response.name
```

**Custom configuration:**

```python
operation = client.agent_engines.sandboxes.create(
   spec={
       "code_execution_environment": {
            "code_language": "LANGUAGE_JAVASCRIPT",
            "machine_config": "MACHINE_CONFIG_VCPU4_RAM4GIB"
        }
   },
   name='projects/PROJECT_ID/locations/LOCATION/reasoningEngines/AGENT_ENGINE_ID',
   config=types.CreateAgentEngineSandboxConfig(
       display_name=sandbox_display_name, ttl="3600s"),
)
```

## (Optional) List and get sandboxes

**List:**
```python
sandboxes = client.agent_engines.sandboxes.list(name=agent_engine_name)
```

**Get:**
```python
sandbox = client.agent_engines.sandboxes.get(name=sandbox_name)
```

## Execute code in a sandbox

```python
my_code = """
with open("input.txt", "r") as input:
   with open("output.txt", "w") as output:
       for line in input:
           print(line)
           output.write(line)
"""
input_data = {
   "code": my_code,
   "files": [{
       "name": "input.txt",
       "content": b"Hello, world!"
   }]
}


response = client.agent_engines.sandboxes.execute_code(
   name = sandbox_name,
   input_data = input_data
)
```

## Execute more code in a sandbox (State persistence)

```python
python_code = """
with open("output.txt", "w") as output:
    for line in lines:
        output.write(line + "World\n")
"""
input_data = {"code": python_code}

response = client.agent_engines.sandboxes.execute_code(
    name = sandbox_name,
    input_data = input_data
)
```

## Clean up

```python
client.agent_engines.sandboxes.delete(name=sandbox_name)
agent_engine.delete()
```
