from uuid import UUID

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


class RetrieverService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    async def retrieve(
        self,
        repository_id: UUID,
        question: str,
        limit: int = 5,
    ) -> list[dict]:

        query_embedding = await self.embedding_service.generate(
            text=question,
            input_type="query",
        )

        return await self.vector_service.search(
            repository_id=repository_id,
            query_embedding=query_embedding,
            top_k=limit,
        )
