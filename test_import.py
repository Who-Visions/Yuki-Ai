print("Start Import")
try:
    from google.genai.types import VertexAISearch
    print("Import Success")
except ImportError as e:
    print(f"Import Failed: {e}")
except Exception as e:
    print(f"Other Error: {e}")
print("End Script")
