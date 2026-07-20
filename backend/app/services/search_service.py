from uuid import UUID

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


class SearchService:
    """
    Service responsible for semantic code search.

    Workflow:
        User Query
            ↓
        Generate Query Embedding
            ↓
        Search Qdrant
            ↓
        Return Matching Chunks
    """

    def __init__(self):
        self.embedding = EmbeddingService()
        self.vector = VectorService()

    async def search(
        self,
        repository_id: UUID,
        query: str,
        top_k: int = 5,
    ) -> dict:
        """
        Search a repository using semantic similarity.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        query_embedding = await self.embedding.generate(
            text=query,
            input_type="query",
        )

        matches = await self.vector.search(
            repository_id=repository_id,
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return {
            "repository_id": repository_id,
            "query": query,
            "total_matches": len(matches),
            "matches": matches,
        }
