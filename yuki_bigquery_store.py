from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from rich.console import Console
import json
import time

console = Console()

class BigQueryVectorStore:
    def __init__(self, project_id: str, location: str = "US", dataset_id: str = "yuki_memory"):
        self.project_id = project_id
        self.location = location
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=project_id, location=location)
        self.table_id = f"{project_id}.{dataset_id}.cosplay_wisdom"

    def initialize_dataset(self):
        """Ensure dataset and table exist with correct schema."""
        # Check Dataset
        try:
            self.client.get_dataset(self.dataset_id)
        except NotFound:
            console.print(f"[yellow]Creating dataset {self.dataset_id}...[/]")
            dataset = bigquery.Dataset(f"{self.project_id}.{self.dataset_id}")
            dataset.location = self.location
            self.client.create_dataset(dataset, timeout=30)

        # Check Table
        schema = [
            bigquery.SchemaField("content", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("metadata", "JSON", mode="NULLABLE"),
            bigquery.SchemaField("embedding", "FLOAT", mode="REPEATED"), # Filled by ML trigger later
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED", default_value_expression="CURRENT_TIMESTAMP()"),
        ]
        
        try:
            self.client.get_table(self.table_id)
        except NotFound:
            console.print(f"[yellow]Creating table {self.table_id}...[/]")
            table = bigquery.Table(self.table_id, schema=schema)
            # Add clustering for performance if needed later
            self.client.create_table(table)
            time.sleep(1) # Propagate

    def add_memory(self, content: str, metadata: dict):
        """Insert a single memory chunk."""
        rows_to_insert = [
            {
                "content": content,
                "metadata": json.dumps(metadata) # JSON type in BQ expects dict or json string
            }
        ]
        
        errors = self.client.insert_rows_json(self.table_id, rows_to_insert)
        if errors:
            console.print(f"[red]BQ Insert Error: {errors}[/]")
        else:
            # Trigger embedding generation for this new row?
            # For efficiency in single-row inserts, often we use a view or scheduled query.
            # But the user wants it to work like Dav1d's batch ingestion likely does.
            # We'll add a trigger method or just note it.
            pass

    def generate_embeddings(self):
        """Trigger BQ ML to vectorize the content."""
        # This matches the pattern in setup_bq_ml_embeddings.py
        # We assume the model `bqml.text_embedding_005` exists.
        
        console.print("[cyan]Generating embeddings via BQ ML...[/cyan]")
        
        # We'll update the 'embedding' column for rows where it is null
        # Note: BQ UPDATE with ML.GENERATE is complex. 
        # Easier pattern: Insert into staging, then INSERT into vectors table with embedding.
        # But for this store, let's assume valid ML usage.
        
        # SQL to update null embeddings
        sql = f"""
        UPDATE `{self.table_id}` t
        SET embedding = ml_result.text_embedding
        FROM ML.GENERATE_TEXT_EMBEDDING(
            MODEL `{self.project_id}.bqml.text_embedding_005`,
            (SELECT content, metadata, created_at FROM `{self.table_id}` WHERE embedding IS NULL),
            STRUCT('content' AS content_column)
        ) ml_result
        WHERE t.content = ml_result.content
        """
        
        try:
            job = self.client.query(sql)
            job.result()
            console.print("[green]✅ Embeddings updated[/green]")
        except Exception as e:
            console.print(f"[red]Embedding Gen Error: {e}[/red]")
            console.print("[dim]Ensure `bqml.text_embedding_005` model exists (see setup_bq_ml_embeddings.py)[/dim]")
