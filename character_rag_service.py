"""
🩵 CYAN'S CHARACTER RAG SERVICE
Unified Dual Retrieval: Vertex AI RAG + BigQuery Embeddings
"""
import asyncio
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from rich.console import Console

console = Console()

# === CONFIGURATION ===
PROJECT_ID_RAG = "yuki-ai-914641083224"  # Vertex AI RAG project
PROJECT_ID_BQ = "gifted-cooler-479623-r7"  # BigQuery project
LOCATION = "us-central1"
RAG_CORPUS_NAME = "yuki-character-db"
BQ_DATASET = "yuki_memory"
BQ_TABLE = "character_embeddings"
EMBEDDING_MODEL = "text-embedding-005"


@dataclass
class CharacterResult:
    """Unified character search result"""
    id: str
    name: str
    full_name: str
    category: str
    score: float
    source: str  # "rag" or "bq" or "merged"
    content: Optional[str] = None
    
    def __hash__(self):
        return hash(self.id)


class CharacterRAGService:
    """
    Dual retrieval service for character database.
    Queries both Vertex AI RAG Engine and BigQuery Embeddings for redundancy.
    
    Usage:
        service = CharacterRAGService()
        results = await service.search("Goku", top_k=5)
    """
    
    def __init__(self):
        self._rag_corpus = None
        self._bq_client = None
        self._genai_client = None
    
    def _init_clients(self):
        """Lazy initialization of clients"""
        if self._bq_client is None:
            from google.cloud import bigquery
            self._bq_client = bigquery.Client(project=PROJECT_ID_BQ)
        
        if self._genai_client is None:
            from google import genai
            self._genai_client = genai.Client(
                vertexai=True, 
                project=PROJECT_ID_BQ, 
                location=LOCATION
            )
    
    def _get_rag_corpus_name(self) -> Optional[str]:
        """Get full RAG corpus resource name"""
        if self._rag_corpus:
            return self._rag_corpus
        
        try:
            import vertexai
            from vertexai import rag
            
            vertexai.init(project=PROJECT_ID_RAG, location=LOCATION)
            
            for corpus in rag.list_corpora():
                if corpus.display_name == RAG_CORPUS_NAME:
                    self._rag_corpus = corpus.name
                    return self._rag_corpus
        except Exception as e:
            console.print(f"[yellow]⚠️ RAG corpus lookup failed: {e}[/yellow]")
        
        return None
    
    async def _query_vertex_rag(self, query: str, top_k: int = 5) -> List[CharacterResult]:
        """Query Vertex AI RAG Engine"""
        results = []
        
        corpus_name = self._get_rag_corpus_name()
        if not corpus_name:
            console.print("[yellow]⚠️ RAG corpus not found, skipping...[/yellow]")
            return results
        
        try:
            from vertexai import rag
            
            response = rag.retrieval_query(
                text=query,
                rag_corpora=[corpus_name],
                similarity_top_k=top_k
            )
            
            if response.contexts.contexts:
                for i, ctx in enumerate(response.contexts.contexts):
                    # Parse the context text to extract character info
                    text = ctx.text
                    lines = text.split("\n")
                    name = lines[0] if lines else "Unknown"
                    
                    # Calculate a score based on position (RAG doesn't return scores directly)
                    score = 1.0 - (i * 0.1)
                    
                    results.append(CharacterResult(
                        id=f"rag_{i}",
                        name=name.split("(")[0].strip() if "(" in name else name,
                        full_name=name,
                        category=self._extract_category(text),
                        score=score,
                        source="rag",
                        content=text[:200]
                    ))
        except Exception as e:
            console.print(f"[red]❌ RAG query error: {e}[/red]")
        
        return results
    
    async def _query_bq_embeddings(self, query: str, top_k: int = 5) -> List[CharacterResult]:
        """Query BigQuery embeddings using vector similarity"""
        results = []
        self._init_clients()
        
        try:
            # Generate query embedding
            response = self._genai_client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=query
            )
            query_embedding = list(response.embeddings[0].values)
            
            # Cosine similarity search in BigQuery
            sql = f"""
            WITH query_vec AS (
                SELECT {query_embedding} AS qe
            )
            SELECT 
                c.character_id,
                c.name,
                c.full_name,
                c.category,
                c.content_text,
                (
                    SELECT 
                        SAFE_DIVIDE(
                            SUM(a * b),
                            SQRT(SUM(a * a)) * SQRT(SUM(b * b))
                        )
                    FROM UNNEST(c.embedding) a WITH OFFSET i
                    JOIN UNNEST((SELECT qe FROM query_vec)) b WITH OFFSET j
                    ON i = j
                ) AS similarity
            FROM `{PROJECT_ID_BQ}.{BQ_DATASET}.{BQ_TABLE}` c
            ORDER BY similarity DESC
            LIMIT {top_k}
            """
            
            query_results = self._bq_client.query(sql).result()
            
            for row in query_results:
                results.append(CharacterResult(
                    id=row.character_id,
                    name=row.name,
                    full_name=row.full_name,
                    category=row.category,
                    score=float(row.similarity) if row.similarity else 0.0,
                    source="bq",
                    content=row.content_text[:200] if row.content_text else None
                ))
                
        except Exception as e:
            console.print(f"[red]❌ BQ query error: {e}[/red]")
        
        return results
    
    def _extract_category(self, text: str) -> str:
        """Extract category from RAG response text"""
        if "Category:" in text:
            parts = text.split("Category:")
            if len(parts) > 1:
                return parts[1].split("\n")[0].strip()
        return "unknown"
    
    def _merge_results(
        self, 
        rag_results: List[CharacterResult], 
        bq_results: List[CharacterResult], 
        top_k: int
    ) -> List[CharacterResult]:
        """Merge and deduplicate results from both sources"""
        
        # Use a dict to dedupe by name (normalized)
        merged = {}
        
        # Add BQ results first (they have better IDs)
        for r in bq_results:
            key = r.name.lower().strip()
            if key not in merged:
                merged[key] = r
            else:
                # If already exists, boost score
                merged[key].score = max(merged[key].score, r.score) + 0.1
                merged[key].source = "merged"
        
        # Add RAG results
        for r in rag_results:
            key = r.name.lower().strip()
            if key not in merged:
                merged[key] = r
            else:
                # Boost score for appearing in both
                merged[key].score = max(merged[key].score, r.score) + 0.15
                merged[key].source = "merged"
        
        # Sort by score and return top_k
        sorted_results = sorted(merged.values(), key=lambda x: x.score, reverse=True)
        return sorted_results[:top_k]
    
    async def search(
        self, 
        query: str, 
        top_k: int = 5,
        use_rag: bool = True,
        use_bq: bool = True
    ) -> List[CharacterResult]:
        """
        Search for characters using dual RAG retrieval.
        
        Args:
            query: Search query (character name, description, franchise)
            top_k: Number of results to return
            use_rag: Whether to query Vertex AI RAG
            use_bq: Whether to query BigQuery embeddings
        
        Returns:
            List of CharacterResult sorted by relevance score
        """
        tasks = []
        
        if use_rag:
            tasks.append(self._query_vertex_rag(query, top_k))
        if use_bq:
            tasks.append(self._query_bq_embeddings(query, top_k))
        
        if not tasks:
            return []
        
        # Execute queries in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        rag_results = []
        bq_results = []
        
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                console.print(f"[red]Query {i} failed: {res}[/red]")
                continue
            if i == 0 and use_rag:
                rag_results = res
            elif (i == 0 and not use_rag) or (i == 1):
                bq_results = res
        
        # Merge results
        return self._merge_results(rag_results, bq_results, top_k)
    
    def search_sync(self, query: str, top_k: int = 5) -> List[CharacterResult]:
        """Synchronous wrapper for search"""
        return asyncio.run(self.search(query, top_k))


# === CLI Interface ===
def main():
    import sys
    
    console.print("\n[bold cyan]🩵 CYAN'S CHARACTER RAG SERVICE[/bold cyan]")
    console.print("[dim]Dual Retrieval: Vertex AI RAG + BigQuery Embeddings[/dim]\n")
    
    service = CharacterRAGService()
    
    # Test queries
    test_queries = [
        "Goku dragon ball",
        "dark knight batman",
        "anime swordsman black hair",
        "video game hero blonde sword",
        "marvel superhero red cape"
    ]
    
    query = sys.argv[1] if len(sys.argv) > 1 else test_queries[0]
    
    console.print(f"[bold]🔍 Query: '{query}'[/bold]\n")
    
    results = service.search_sync(query, top_k=5)
    
    if not results:
        console.print("[yellow]No results found[/yellow]")
    else:
        for i, r in enumerate(results, 1):
            source_badge = {
                "rag": "[blue]RAG[/blue]",
                "bq": "[green]BQ[/green]",
                "merged": "[magenta]MERGED[/magenta]"
            }.get(r.source, r.source)
            
            console.print(
                f"  {i}. [bold]{r.full_name}[/bold] "
                f"({r.category}) "
                f"- Score: {r.score:.3f} {source_badge}"
            )
    
    console.print()


if __name__ == "__main__":
    main()
