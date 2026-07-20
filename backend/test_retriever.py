import asyncio

from app.services.retriever_service import RetrieverService


async def main():

    retriever = RetrieverService()

    results = await retriever.retrieve("How does authentication work?")

    print(f"Retrieved {len(results)} chunks")

    for i, item in enumerate(results, start=1):

        print(f"\nResult {i}")
        print(f"Score: {item['score']:.4f}")
        print(item["payload"])


asyncio.run(main())
