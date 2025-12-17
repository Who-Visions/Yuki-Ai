"""
🩵 Character Semantic Search Test
"""
from google.cloud import bigquery
from rich.console import Console

console = Console()

PROJECT_ID = "gifted-cooler-479623-r7"
DATASET_ID = "yuki_memory"


def search(query: str, top_k: int = 5):
    """Semantic search for characters"""
    client = bigquery.Client(PROJECT_ID)
    
    sql = f"""
    WITH query_emb AS (
        SELECT text_embedding AS qe
        FROM ML.GENERATE_TEXT_EMBEDDING(
            MODEL `{PROJECT_ID}.{DATASET_ID}.text_embedding_model`,
            (SELECT @query AS content)
        )
    )
    SELECT 
        c.full_name,
        c.category,
        (SELECT SUM(a*b)/(SQRT(SUM(a*a))*SQRT(SUM(b*b)))
         FROM UNNEST(c.embedding) a WITH OFFSET i
         JOIN UNNEST((SELECT qe FROM query_emb)) b WITH OFFSET j ON i=j) AS score
    FROM `{PROJECT_ID}.{DATASET_ID}.character_embeddings_v2` c
    ORDER BY score DESC
    LIMIT @top_k
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("query", "STRING", query),
            bigquery.ScalarQueryParameter("top_k", "INT64", top_k),
        ]
    )
    
    console.print(f"\n[bold]🔍 Searching: '{query}'[/bold]")
    console.print("-" * 40)
    
    for row in client.query(sql, job_config=job_config).result():
        console.print(f"  → {row.full_name} ({row.category}): {row.score:.4f}")


if __name__ == "__main__":
    search("dragon ball anime fighter")
    search("dark anime swordsman revenge")
    search("marvel superhero red cape")
    search("video game hero blonde sword")
    search("batman dark knight")
