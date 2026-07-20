import collections

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.core.config import settings
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PayloadSchemaType,
)

class QdrantService:

    def __init__(self):

        self.client = AsyncQdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )

    async def initialize(self):

        collections = await self.client.get_collections()

        existing = {collection.name for collection in collections.collections}

        if settings.QDRANT_COLLECTION not in existing:

            await self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=VectorParams(
                    size=4096,
                    distance=Distance.COSINE,
                ),
            )

        # Create payload index for repository_id
        try:
            await self.client.create_payload_index(
                collection_name=settings.QDRANT_COLLECTION,
                field_name="repository_id",
                field_schema=PayloadSchemaType.KEYWORD,
            )
        
        except Exception:
            # Ignore if the index already exists
            pass
