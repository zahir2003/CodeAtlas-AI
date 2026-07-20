import asyncio

from app.clients.qdrant_client import QdrantService


async def main():

    service = QdrantService()

    await service.initialize()

    print("Qdrant Connected Successfully")


asyncio.run(main())
