import asyncio
import time

from app.services.embedding_service import EmbeddingService


async def main():

    service = EmbeddingService()

    start = time.time()

    embedding = await service.generate(
        "Hello NVIDIA"
    )

    end = time.time()

    print(f"Dimension: {len(embedding)}")

    print(f"Time: {end-start:.2f} sec")


asyncio.run(main())