# Vertex AI Search Configuration

## Overview

This project uses **Vertex AI Search** for grounding agents on internal/technical documentation, specifically the **Google Cloud Documentation** website.

## App Details

- **App Name**: `Yuki-Search-App`
- **Resource ID**: `yuki-search-app_1766161961125`
- **Project ID**: `gifted-cooler-479623-r7` (Use this for Search App calls)
- **Data Store ID**: `yuki-docs-datastore_1766162068013`
- **Location**: `global`

## Integration

The `tools/web_fetch.py` script supports this app via the `datastore_id` parameter or default configuration.

```python
# Direct usage in Python
real_datastore_path = f"projects/gifted-cooler-479623-r7/locations/global/collections/default_collection/dataStores/yuki-docs-datastore_1766162068013"
grounding_tool = Tool(
    retrieval=Retrieval(
        vertex_ai_search={"datastore": real_datastore_path}
    )
)
```

## Setup Notes

- IAM Role `roles/discoveryengine.editor` was granted to `whoentertains@gmail.com`.
- Data Store indexes `cloud.google.com/docs`.
