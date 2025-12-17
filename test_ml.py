"""Quick test of BQ ML embedding output"""
from google.cloud import bigquery

client = bigquery.Client("gifted-cooler-479623-r7")

# Test the model
sql = """
SELECT * FROM ML.GENERATE_TEXT_EMBEDDING(
    MODEL `gifted-cooler-479623-r7.yuki_memory.text_embedding_model`,
    (SELECT 'test character for cosplay' AS content)
)
"""

result = client.query(sql).result()
for row in result:
    print("Row keys:", list(dict(row).keys()))
    for k, v in dict(row).items():
        val_str = str(v)[:200] if v else "None"
        print(f"  {k}: {val_str}")
