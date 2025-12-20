import os
from google import genai
from google.genai.types import (
    GenerateContentConfig,
    GoogleSearch,
    Tool,
    ThinkingConfig,
    Retrieval,
)

def web_fetch(prompt, project_id=None, location="global", datastore_id="yuki-search-app_1766161961125"):
    """
    Uses Gemini with Grounding to fetch info. 
    Supports 'Public Google Search' or 'Vertex AI Search' (Custom Datastore).
    """
    print(f"--- Web Fetch: '{prompt}' ---")
    
    # Update to the active project with the Search App
    # Ensure this environment variable is correct or passed explicitly
    project_id = project_id or os.getenv("PROJECT_ID", "gifted-cooler-479623-r7")
    
    if not project_id:
        print("❌ Error: PROJECT_ID env var not set.")
        return

    client = genai.Client(vertexai=True, project=project_id, location=location)

    # Configure Grounding Tool
    if datastore_id:
        real_datastore_path = f"projects/{project_id}/locations/global/collections/default_collection/dataStores/yuki-docs-datastore_1766162068013"
        print(f"   Using Vertex AI Search Data Store: {real_datastore_path}")
        
        # Use dictionary configuration to avoid importing VertexAISearch class which caused hangs
        grounding_tool = Tool(
            retrieval=Retrieval(
                vertex_ai_search={"datastore": real_datastore_path}
            )
        )
    else:
        print("   Using Public Google Search")
        grounding_tool = Tool(
            google_search=GoogleSearch()
        )

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt,
            config=GenerateContentConfig(
                tools=[grounding_tool],
                response_modalities=["TEXT"],
                thinking_config=ThinkingConfig(thinking_level="LOW"),
            ),
        )
        
        print("\n✅ Grounded Response:")
        print(response.text)
        
        if response.candidates[0].grounding_metadata.web_search_queries:
            print("\n🔍 Search Queries Used:")
            for q in response.candidates[0].grounding_metadata.web_search_queries:
                print(f" - {q}")
                
    except Exception as e:
        print(f"❌ Web Fetch Error: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="Query or question to Fetch from web")
    parser.add_argument("--public", action="store_true", help="Force Public Google Search (ignore datastore)")
    args = parser.parse_args()
    
    # If public flag is set, pass None for datastore_id to trigger fallback
    ds_id = None if args.public else "yuki-search-app_1766161961125"
    
    web_fetch(args.prompt, datastore_id=ds_id)
