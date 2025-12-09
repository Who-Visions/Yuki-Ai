# Yuki OpenAI Compatible Server

This server exposes Yuki's capabilities via an OpenAI-compatible API endpoint.
This allows other agents (like AutoGen, BabyAGI, or other OpenAI-client based tools) to talk to Yuki.

## Features
- **Endpoint**: `http://localhost:8000/v1/chat/completions`
- **Model**: Compatible with any model name (defaults to `gemini-2.5-pro` logic internally).
- **Tools**: All standard Yuki tools are enabled (Image Gen, Video Gen, Research, File System, etc.).

## How to Run

1. **Start the Server**:
   Double-click `start_yuki_server.bat` 
   OR run:
   ```bash
   python yuki_openai_server.py
   ```

2. **Connect from Python (OpenAI SDK)**:
   ```python
   from openai import OpenAI

   client = OpenAI(
       base_url="http://localhost:8000/v1",
       api_key="sk-dummy" # Not checked, but required by SDK
   )

   response = client.chat.completions.create(
       model="yuki",
       messages=[
           {"role": "user", "content": "Generate a cosplay image of a snow fox"}
       ]
   )

   print(response.choices[0].message.content)
   ```

3. **Connect from Other Agents**:
   - Set `OPENAI_API_BASE` or `base_url` to `http://localhost:8000/v1`.
   - Set `OPENAI_API_KEY` to any string.
