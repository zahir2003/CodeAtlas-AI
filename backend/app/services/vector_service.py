from uuid import UUID, uuid4

from qdrant_client.http.models import (
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
)

from app.clients.qdrant_client import QdrantService
from app.core.config import settings


class VectorService:
    """
    Handles all Qdrant vector operations.

    Responsibilities:
    - Store embeddings
    - Perform semantic search
    """

    BATCH_SIZE = 100

    def __init__(self):
        self.qdrant = QdrantService()

    async def insert_chunks(
        self,
        chunks: list[dict],
    ) -> int:
        """
        Insert repository chunks into Qdrant.
        """

        points: list[PointStruct] = []

        for chunk in chunks:
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=chunk["embedding"],
                    payload={
                        "repository_id": str(chunk["repository_id"]),
                        "file_path": chunk["file_path"],
                        "language": chunk["language"],
                        "extension": chunk.get("extension"),
                        "chunk_index": chunk["chunk_index"],
                        "start_char": chunk.get("start_char"),
                        "end_char": chunk.get("end_char"),
                        "code": chunk["content"],
                    },
                )
            )

        if not points:
            return 0

        try:
            for i in range(0, len(points), self.BATCH_SIZE):
                batch = points[i : i + self.BATCH_SIZE]

                await self.qdrant.client.upsert(
                    collection_name=settings.QDRANT_COLLECTION,
                    points=batch,
                )

        except Exception as e:
            raise RuntimeError("Failed to insert vectors into Qdrant.") from e

        return len(points)

    async def search(
        self,
        repository_id: UUID,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        """
        Search the repository using semantic similarity.
        """

        try:
            response = await self.qdrant.client.query_points(
                collection_name=settings.QDRANT_COLLECTION,
                query=query_embedding,
                query_filter=Filter(
                    must=[
                        FieldCondition(
                            key="repository_id",
                            match=MatchValue(
                                value=str(repository_id),
                            ),
                        )
                    ]
                ),
                limit=top_k,
                with_payload=True,
            )

        except Exception as e:
            raise RuntimeError("Failed to search vectors from Qdrant.") from e

        results: list[dict] = []

        for point in response.points:

            payload = point.payload or {}

            results.append(
                {
                    "score": round(float(point.score), 4),
                    "repository_id": payload.get("repository_id"),
                    "file_path": payload.get("file_path"),
                    "language": payload.get("language"),
                    "extension": payload.get("extension"),
                    "chunk_index": payload.get("chunk_index"),
                    "start_char": payload.get("start_char"),
                    "end_char": payload.get("end_char"),
                    "code": payload.get("code"),
                }
            )

        return results
