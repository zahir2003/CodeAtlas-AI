from app.cache.embedding_cache import EmbeddingCache
from app.clients.nvidia_client import NVIDIAClient


class EmbeddingService:

    def __init__(self):
        self.client = NVIDIAClient()
        self.cache = EmbeddingCache()

    async def generate(
        self,
        text: str,
        input_type: str = "passage",
    ) -> list[float]:

        cached = self.cache.get(text)

        if cached is not None:
            return cached

        try:
            embedding = await self.client.create_embedding(
                text=text,
                input_type=input_type,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to generate embedding: {e}")

        if not embedding:
            raise ValueError("Embedding generation returned an empty vector.")

        self.cache.save(
            text,
            embedding,
        )

        return embedding
